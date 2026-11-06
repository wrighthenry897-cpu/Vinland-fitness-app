import tempfile
import unittest
from pathlib import Path

from app import create_app


class VinlandAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-key",
                "DATABASE_PATH": str(Path(self.temp_dir.name) / "test.sqlite3"),
            }
        )
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def token(self) -> str:
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as session:
            return session["csrf_token"]

    def register(self, email: str = "alex@example.com") -> None:
        csrf_token = self.token()
        response = self.client.post(
            "/register",
            data={
                "csrf_token": csrf_token,
                "name": "Alex Morgan",
                "email": email,
                "password": "a-strong-password",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def workout_data(self, csrf_token: str, title: str = "Strength day") -> dict[str, str]:
        from datetime import date

        return {
            "csrf_token": csrf_token,
            "title": title,
            "workout_date": date.today().isoformat(),
            "duration": "45",
            "notes": "Felt strong",
            "exercise_name[]": ["Squat", "Row"],
            "exercise_sets[]": ["3", "4"],
            "exercise_reps[]": ["8", "10"],
            "exercise_weight[]": ["60", "30"],
        }

    def test_each_workout_focus_has_its_own_card_color(self) -> None:
        from exercise_library import FOCUSES

        colors = [focus["color"] for focus in FOCUSES.values()]
        self.assertEqual(len(colors), len(set(colors)))
        self.register()
        library = self.client.get("/library?focus=all&level=beginner")
        for slug, focus in FOCUSES.items():
            self.assertIn(
                f"focus-{focus['color']} has-photo-art focus-{slug}".encode(),
                library.data,
            )

    def test_registration_login_and_private_dashboard(self) -> None:
        self.register()
        self.assertIn(b"Your week, in motion", self.client.get("/").data)
        self.client.post("/logout", data={"csrf_token": self.token()}, follow_redirects=True)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

        restarted_app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-key",
                "DATABASE_PATH": self.app.config["DATABASE_PATH"],
            }
        )
        restarted_client = restarted_app.test_client()
        login_page = restarted_client.get("/login")
        self.assertEqual(login_page.status_code, 200)
        with restarted_client.session_transaction() as session:
            csrf_token = session["csrf_token"]
        response = restarted_client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "email": "ALEX@example.com",
                "password": "a-strong-password",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/", response.location)
        self.assertIn(b"Your week, in motion", restarted_client.get("/").data)

    def test_login_failure_logs_reason_without_credentials(self) -> None:
        self.register()
        self.client.post("/logout", data={"csrf_token": self.token()})
        login_page = self.client.get("/login")
        self.assertEqual(login_page.status_code, 200)
        with self.client.session_transaction() as session:
            csrf_token = session["csrf_token"]

        with self.assertLogs("app", level="WARNING") as captured:
            response = self.client.post(
                "/login",
                data={
                    "csrf_token": csrf_token,
                    "email": "alex@example.com",
                    "password": "incorrect-password",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"didn\xe2\x80\x99t match", response.data)
        self.assertIn("password hash did not match", captured.output[0])
        self.assertNotIn("alex@example.com", captured.output[0])
        self.assertNotIn("incorrect-password", captured.output[0])

    def test_workout_create_edit_delete_and_progress(self) -> None:
        self.register()
        response = self.client.post(
            "/workouts/new",
            data=self.workout_data(self.token()),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Strength day", response.data)
        self.assertIn(b"WORKOUT COMPLETE!", response.data)
        self.assertIn(b"+100 XP", response.data)
        self.assertIn(b"100 XP earned", response.data)
        self.assertIn(b'class="completion-celebration is-visible"', response.data)
        self.assertIn(b"2,640", self.client.get("/").data)
        self.assertIn(b"Volume over the last 30 days", self.client.get("/progress").data)

        with self.app.app_context():
            from app import get_db

            workout_id = get_db().execute("SELECT id FROM workouts").fetchone()["id"]
        response = self.client.post(
            f"/workouts/{workout_id}/edit",
            data=self.workout_data(self.token(), "Updated strength"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated strength", response.data)

        response = self.client.post(
            f"/workouts/{workout_id}/delete",
            data={"csrf_token": self.token()},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No workouts yet", response.data)

    def test_workout_log_search_and_date_filters(self) -> None:
        from datetime import date, timedelta

        self.register()
        today = date.today()
        recent = self.workout_data(self.token(), "Upper strength")
        recent["notes"] = "Felt great"
        self.client.post("/workouts/new", data=recent)
        old = self.workout_data(self.token(), "Old training day")
        old["workout_date"] = (today - timedelta(days=100)).isoformat()
        old["exercise_name[]"] = ["Dead bug", "Bridge"]
        old["notes"] = "Core focus"
        self.client.post("/workouts/new", data=old)

        response = self.client.get("/workouts?q=dead+bug")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Old training day", response.data)
        self.assertNotIn(b"Upper strength", response.data)

        response = self.client.get("/workouts?q=core")
        self.assertIn(b"Old training day", response.data)
        self.assertNotIn(b"Upper strength", response.data)

        response = self.client.get("/workouts?q=%25")
        self.assertIn(b"No sessions match those filters.", response.data)

        response = self.client.get("/workouts?period=30")
        self.assertIn(b"Upper strength", response.data)
        self.assertNotIn(b"Old training day", response.data)

        response = self.client.get("/workouts?q=missing&period=90")
        self.assertIn(b"No sessions match those filters.", response.data)
        self.assertIn(b"Clear filters", response.data)

    def test_csrf_and_account_isolation(self) -> None:
        self.register()
        response = self.client.post("/workouts/new", data=self.workout_data("invalid"))
        self.assertEqual(response.status_code, 400)
        with self.app.app_context():
            from app import get_db

            get_db().execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("Taylor", "taylor@example.com", "not-a-login-hash"),
            )
            get_db().commit()
            second_id = get_db().execute(
                "SELECT id FROM users WHERE email = ?", ("taylor@example.com",)
            ).fetchone()["id"]
            cursor = get_db().execute(
                "INSERT INTO workouts (user_id, title, workout_date, duration) VALUES (?, ?, ?, ?)",
                (second_id, "Private session", "2026-01-01", 30),
            )
            get_db().commit()
            other_workout_id = cursor.lastrowid
        self.assertEqual(self.client.get("/workouts").status_code, 200)
        self.assertEqual(self.client.get(f"/workouts/{other_workout_id}/edit").status_code, 404)

    def test_registration_validation_and_duplicate_email(self) -> None:
        token = self.token()
        invalid = self.client.post(
            "/register",
            data={"csrf_token": token, "name": "Alex", "email": "bad", "password": "tiny"},
        )
        self.assertEqual(invalid.status_code, 200)
        self.register()
        self.client.post("/logout", data={"csrf_token": self.token()})
        duplicate = self.client.post(
            "/register",
            data={
                "csrf_token": self.token(),
                "name": "Another Alex",
                "email": "alex@example.com",
                "password": "a-strong-password",
            },
        )
        self.assertEqual(duplicate.status_code, 200)
        self.assertIn(b"already exists", duplicate.data)

    def test_profile_updates_private_weight_goals(self) -> None:
        self.register()
        response = self.client.post(
            "/profile",
            data={
                "csrf_token": self.token(),
                "name": "Alex M",
                "current_weight": "82.5",
                "target_weight": "77",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"82.5", self.client.get("/").data)

    def test_profile_allows_zero_weight_for_lightweight_tracking(self) -> None:
        self.register()
        response = self.client.post(
            "/profile",
            data={
                "csrf_token": self.token(),
                "name": "Alex M",
                "current_weight": "0",
                "target_weight": "0",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Your profile has been updated.", response.data)
        dashboard = self.client.get("/")
        self.assertIn(b"0.0", dashboard.data)
        self.assertIn(b"0.0 kg", dashboard.data)
        profile = self.client.get("/profile")
        self.assertIn(b'min="0"', profile.data)
        self.assertIn(b'value="0.0"', profile.data)

    def test_dashboard_and_progress_charts_include_accessible_daily_data(self) -> None:
        self.register()
        dashboard = self.client.get("/")
        self.assertIn(b'aria-controls="sidebar"', dashboard.data)
        self.assertIn(b'role="img" aria-label="Bar chart', dashboard.data)
        self.assertIn(b"View daily data", dashboard.data)
        self.assertIn(b"<th scope=\"col\">Volume</th>", dashboard.data)

        progress = self.client.get("/progress")
        self.assertIn(b'role="img" aria-label="Line chart', progress.data)
        self.assertIn(b"View daily data", progress.data)
        self.assertIn(b"<th scope=\"col\">Sessions</th>", progress.data)

    def test_invalid_exercise_is_preserved_for_correction(self) -> None:
        self.register()
        data = self.workout_data(self.token())
        data["exercise_sets[]"] = ["not-a-set", "4"]
        response = self.client.post("/workouts/new", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"not-a-set", response.data)
        self.assertIn(b"Check each exercise", response.data)

    def test_workout_library_shows_bundled_human_movement_demos(self) -> None:
        self.register()
        library = self.client.get(
            "/library?focus=abs&level=beginner"
        )
        self.assertEqual(library.status_code, 200)
        self.assertIn(b"Abs &amp; core", library.data)
        self.assertIn(b"No equipment", library.data)
        self.assertIn(b"STAGE 1 / 30", library.data)
        self.assertIn(b'<a class="focus-card focus-mint has-photo-art focus-abs"', library.data)
        self.assertIn(b"aria-label=\"Day 1: view Abs &amp; core workout\"", library.data)
        self.assertNotIn(b"<h3>Legs &amp; glutes</h3>", library.data)

        all_focuses = self.client.get("/library?focus=all&level=beginner")
        for focus in ("abs", "chest", "back", "arms", "legs", "full-body"):
            self.assertIn(f'has-photo-art focus-{focus}'.encode(), all_focuses.data)
            self.assertIn(b'class="focus-photo-art"', all_focuses.data)
            self.assertIn(f'images/workout-focus/{focus}.jpg'.encode(), all_focuses.data)
            image = self.client.get(f"/static/images/workout-focus/{focus}.jpg")
            self.assertEqual(image.status_code, 200)
            image.close()

        guide = self.client.get("/library/abs?level=beginner")
        self.assertEqual(guide.status_code, 200)
        self.assertIn(b"MOVEMENT SEQUENCE", guide.data)
        self.assertIn(b"Voice &amp; delivery settings", guide.data)
        self.assertIn(b'id="coach-voice-select"', guide.data)
        self.assertIn(b'id="coach-style-select"', guide.data)
        self.assertIn(b'id="coach-speed-select"', guide.data)
        self.assertIn(
            b'data-demo-start="/static/exercise-demos/Dead_Bug/0.jpg"',
            guide.data,
        )
        self.assertIn(b"STAGE 1 / 30", guide.data)
        self.assertIn(b"DAY&nbsp;1", guide.data)
        self.assertIn(b"Pick a day to preview", guide.data)
        self.assertIn(b"DAY&nbsp;1", guide.data)
        self.assertIn(b'aria-current="page"', guide.data)
        future_guide = self.client.get("/library/abs?level=beginner&preview=1")
        self.assertEqual(future_guide.status_code, 200)
        self.assertIn(b"DAY&nbsp;2", future_guide.data)
        self.assertIn(b"UPCOMING WORKOUT PREVIEW", future_guide.data)
        self.assertIn(b'aria-current="page"', future_guide.data)
        self.assertIn(b"Forearm plank", future_guide.data)
        self.assertIn(b"UPCOMING DAY PREVIEW", future_guide.data)
        self.assertNotIn(b"Mark movement complete", future_guide.data)
        self.assertNotIn(b'id="guided-player"', future_guide.data)
        later_guide = self.client.get("/library/abs?level=beginner&preview=20")
        self.assertIn(b"DAY&nbsp;21", later_guide.data)
        self.assertIn(b"STAGE 21 / 30", later_guide.data)
        self.assertIn(b'aria-current="page"', later_guide.data)
        self.assertEqual(self.client.get("/library/abs?preview=30").status_code, 400)
        self.assertEqual(self.client.get("/library/abs?preview=invalid").status_code, 400)
        self.assertIn(b"exercise-demos/Dead_Bug/0.jpg", guide.data)
        self.assertIn(b"exercise-demos/Dead_Bug/1.jpg", guide.data)
        self.assertIn(b'class="demo-frame-number">01</span>', guide.data)
        self.assertIn(b'class="demo-frame-label">START</span>', guide.data)
        self.assertIn(b'data-first-label="SIDE 1"', guide.data)
        self.assertIn(b"exercise-demos/Bird_Dog/0.jpg", guide.data)
        self.assertIn(b"exercise-demos/Bird_Dog/1.jpg", guide.data)
        self.assertIn(b"Alternate opposite-side reaches", guide.data)
        self.assertIn(b'data-first-position="first-side reach"', guide.data)
        self.assertIn(b'data-second-position="opposite-side reach"', guide.data)
        self.assertIn(b"Pause movement demo", guide.data)
        self.assertIn(b"Demo artwork credits", guide.data)
        self.assertIn(b"Tell me about this exercise", guide.data)
        self.assertIn(b"Your exercise timer will wait until you choose to begin", guide.data)
        self.assertIn(b"Voice on", guide.data)
        self.assertIn(b"data-duration=\"30\"", guide.data)
        self.assertIn(b"NO EQUIPMENT", guide.data)
        self.assertNotIn(b"gym", guide.data.lower())
        self.assertNotIn(b"exercise-illustration", guide.data)
        self.assertNotIn(b"youtube", guide.data.lower())
        self.assertIn(b"Mark movement complete", guide.data)
        image = self.client.get("/static/exercise-demos/Dead_Bug/0.jpg")
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image.mimetype, "image/jpeg")
        image.close()
        bird_dog_image = self.client.get("/static/exercise-demos/Bird_Dog/0.jpg")
        self.assertEqual(bird_dog_image.status_code, 200)
        self.assertEqual(bird_dog_image.mimetype, "image/jpeg")
        bird_dog_image.close()
        opposite_side_image = self.client.get("/static/exercise-demos/Bird_Dog/1.jpg")
        self.assertEqual(opposite_side_image.status_code, 200)
        self.assertEqual(opposite_side_image.mimetype, "image/jpeg")
        opposite_side_image.close()

    def test_guided_workout_requires_a_completed_movement(self) -> None:
        self.register()
        response = self.client.post(
            "/library/abs/complete",
            data={
                "csrf_token": self.token(),
                "level": "beginner",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mark at least one movement complete", response.data)
        with self.app.app_context():
            from app import get_db

            self.assertEqual(get_db().execute("SELECT COUNT(*) FROM workouts").fetchone()[0], 0)

    def test_guided_workout_saves_only_completed_movements(self) -> None:
        self.register()
        response = self.client.post(
            "/library/abs/complete",
            data={
                "csrf_token": self.token(),
                "level": "beginner",
                "completed_exercise[]": ["0", "2"],
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"+100 XP", response.data)
        self.assertIn(b"100 XP earned", response.data)
        self.assertIn(b"Beginner Abs &amp; Core", response.data)
        self.assertIn(b"WORKOUT COMPLETE!", response.data)
        self.assertIn(b'id="completion-celebration"', response.data)
        self.assertIn(b'class="clash-dagger clash-dagger-left"', response.data)
        self.assertIn(b'class="clash-dagger clash-dagger-right"', response.data)
        with self.app.app_context():
            from app import get_db

            workout = get_db().execute("SELECT * FROM workouts").fetchone()
            exercises = get_db().execute(
                "SELECT name, sets, reps FROM exercises WHERE workout_id = ? ORDER BY id",
                (workout["id"],),
            ).fetchall()
            self.assertEqual(workout["title"], "Beginner Abs & Core")
            self.assertEqual(len(exercises), 2)
            self.assertEqual([exercise["name"] for exercise in exercises], ["Dead bug", "Glute bridge"])
            self.assertTrue(all(exercise["sets"] == 2 for exercise in exercises))

    def test_guided_workout_progresses_after_each_completed_session(self) -> None:
        self.register()
        first_day = self.client.get("/library/abs?level=beginner")
        self.assertIn(b"DAY&nbsp;1", first_day.data)
        library = self.client.get("/library")
        self.assertIn(b"DAY 1", library.data)
        response = self.client.post(
            "/library/abs/complete",
            data={
                "csrf_token": self.token(),
                "level": "beginner",
                "completed_exercise[]": ["0"],
            },
        )
        self.assertEqual(response.status_code, 302)
        guide = self.client.get("/library/abs?level=beginner")
        self.assertEqual(guide.status_code, 200)
        self.assertIn(b"DAY&nbsp;2", guide.data)
        library = self.client.get("/library")
        self.assertIn(b"DAY 2", library.data)
        self.assertIn(b"STAGE 2 / 30", guide.data)
        self.assertIn(b"Bird dog", guide.data)
        self.assertIn(b'data-duration="35"', guide.data)

        from exercise_library import build_routine

        fourth_session = build_routine("abs", "beginner", completed_sessions=3)
        self.assertEqual(fourth_session["sets"], 3)
        self.assertEqual(fourth_session["work_seconds"], 45)
        capped = build_routine("abs", "beginner", completed_sessions=20)
        self.assertEqual(capped["sets"], 4)
        self.assertEqual(capped["work_seconds"], 50)

    def test_workouts_award_xp_and_level_up_across_save_methods(self) -> None:
        from app import build_rank_progression, calculate_player_progress

        self.register()
        self.assertEqual(calculate_player_progress(0)["level"], 1)
        self.assertEqual(calculate_player_progress(2)["xp_to_next"], 100)
        self.assertEqual(
            [calculate_player_progress(sessions)["rank"] for sessions in (0, 3, 6, 9, 12)],
            ["Ironbound", "Battle-Hardened", "Stormforged", "Legend of Vinland", "True Warrior"],
        )
        self.assertEqual(calculate_player_progress(12)["rank"], "True Warrior")
        self.assertEqual(calculate_player_progress(100)["rank"], "True Warrior")
        rank_path = build_rank_progression(200)
        self.assertEqual(rank_path[0]["status"], "current")
        self.assertEqual(rank_path[1]["xp_remaining"], 100)
        self.assertEqual(rank_path[-1]["xp_remaining"], 1000)
        self.assertEqual(
            len({rank["badge_symbol"] for rank in rank_path}),
            len(rank_path),
        )

        for title in ("First workout", "Second workout"):
            self.client.post(
                "/workouts/new",
                data=self.workout_data(self.token(), title),
                follow_redirects=True,
            )

        response = self.client.post(
            "/library/abs/complete",
            data={
                "csrf_token": self.token(),
                "level": "beginner",
                "completed_exercise[]": ["0"],
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Level up! You reached Level 2", response.data)
        self.assertIn(b"Battle-Hardened rank", response.data)

        dashboard = self.client.get("/")
        self.assertIn(b"300 XP earned", dashboard.data)
        self.assertIn(b"Level 3", dashboard.data)
        self.assertIn(b"LV 2", dashboard.data)
        self.assertIn(b"/ranks", dashboard.data)

    def test_rank_progression_page_shows_mascots_badges_and_unlock_xp(self) -> None:
        self.register()
        for title in ("First workout", "Second workout"):
            self.client.post(
                "/workouts/new",
                data=self.workout_data(self.token(), title),
                follow_redirects=True,
            )

        response = self.client.get("/ranks")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Rank path", response.data)
        self.assertIn(b"Iron Wolf badge", response.data)
        self.assertIn(b"War Bear badge", response.data)
        self.assertIn(b"True Warrior Crest badge", response.data)
        self.assertIn(b"100 XP", response.data)
        self.assertIn(b"aria-label=\"All ranks\"", response.data)

    def test_unknown_focus_or_movement_is_not_accepted(self) -> None:
        self.register()
        self.assertEqual(self.client.get("/library/not-real").status_code, 404)
        response = self.client.post(
            "/library/abs/complete",
            data={
                "csrf_token": self.token(),
                "level": "expert",
                "completed_exercise[]": ["0"],
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_every_focus_has_valid_equipment_free_routines(self) -> None:
        from exercise_library import FOCUSES, build_routine

        demo_root = Path(__file__).resolve().parents[1] / "static" / "exercise-demos"
        for focus in FOCUSES:
            for level in ("beginner", "intermediate"):
                with self.subTest(focus=focus, level=level):
                    routine = build_routine(focus, level)
                    self.assertIsNotNone(routine)
                    self.assertEqual(routine["equipment"], "bodyweight")
                    self.assertEqual(len(routine["exercises"]), 5)
                    self.assertEqual(
                        len({item["name"] for item in routine["exercises"]}), 5
                    )
                    self.assertTrue(all(item["animation"] for item in routine["exercises"]))
                    self.assertTrue(all(item["duration_seconds"] in (30, 40) for item in routine["exercises"]))
                    total_seconds = (
                        len(routine["exercises"])
                        * routine["sets"]
                        * routine["exercises"][0]["duration_seconds"]
                        + (len(routine["exercises"]) * routine["sets"] - 1)
                        * routine["rest"]
                    )
                    self.assertEqual(routine["duration"], (total_seconds + 59) // 60)
                    self.assertTrue(
                        all(
                            item["bodyweight"] == "No equipment"
                            or "opposite hand" in item["bodyweight"]
                            for item in routine["exercises"]
                        )
                    )
                    self.assertTrue(
                        all("gym" not in item and "gym_cue" not in item for item in routine["exercises"])
                    )
                    for item in routine["exercises"]:
                        self.assertFalse(item["demo_id"].startswith("wger_"))
                        demo_files = [
                            demo_root / item["demo_id"] / "0.jpg",
                            demo_root / item["demo_id"] / "1.jpg",
                        ]
                        self.assertTrue(all(path.suffix == ".jpg" for path in demo_files))
                        self.assertTrue(all(path.is_file() for path in demo_files))
                    self.assertTrue(all(item["sets"] in (2, 3) for item in routine["exercises"]))
        home_chest = build_routine("chest", "beginner")
        self.assertEqual(home_chest["exercises"][2]["name"], "Push-up")
        self.assertNotIn("gym", str(home_chest).lower())

    def test_each_focus_rotates_through_progressively_harder_bodyweight_moves(self) -> None:
        from exercise_library import FOCUSES, MOVEMENTS, build_routine

        demo_root = Path(__file__).resolve().parents[1] / "static" / "exercise-demos"
        for focus, movement_pool in MOVEMENTS.items():
            with self.subTest(focus=focus):
                self.assertEqual(len(movement_pool), 30)
                self.assertEqual(len({item["name"] for item in movement_pool}), 30)
                stage_count = len(movement_pool)
                routines = [
                    build_routine(focus, "beginner", completed_sessions=session)
                    for session in range(stage_count)
                ]
                self.assertEqual(routines[0]["progression_stage"], 1)
                self.assertEqual(routines[0]["progression_stages"], 30)
                self.assertEqual(
                    routines[-1]["progression_stage"],
                    routines[-1]["progression_stages"],
                )
                for current, following in zip(routines, routines[1:]):
                    current_names = [item["name"] for item in current["exercises"]]
                    next_names = [item["name"] for item in following["exercises"]]
                    self.assertNotEqual(current_names, next_names)
                    self.assertEqual(len(set(current_names) & set(next_names)), 4)
                    self.assertTrue(
                        all(item["bodyweight"] == "No equipment" for item in following["exercises"])
                    )
                for routine in routines:
                    for item in routine["exercises"]:
                        self.assertFalse(item["demo_id"].startswith("wger_"))
                        demo_files = [
                            demo_root / item["demo_id"] / "0.jpg",
                            demo_root / item["demo_id"] / "1.jpg",
                        ]
                        self.assertTrue(all(path.suffix == ".jpg" for path in demo_files))
                        self.assertTrue(all(path.is_file() for path in demo_files))
                rotated_names = {
                    item["name"]
                    for routine in routines
                    for item in routine["exercises"]
                }
                self.assertEqual(rotated_names, {item["name"] for item in movement_pool})
                next_rotation = build_routine(
                    focus, "beginner", completed_sessions=stage_count
                )
                self.assertEqual(next_rotation["progression_stage"], 1)
                self.assertEqual(
                    [item["name"] for item in next_rotation["exercises"]],
                    [item["name"] for item in routines[0]["exercises"]],
                )
        self.assertEqual(set(MOVEMENTS), set(FOCUSES))


if __name__ == "__main__":
    unittest.main()
