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

    def test_registration_login_and_private_dashboard(self) -> None:
        self.register()
        self.assertIn(b"Your week, in motion", self.client.get("/").data)
        self.client.post("/logout", data={"csrf_token": self.token()}, follow_redirects=True)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_workout_create_edit_delete_and_progress(self) -> None:
        self.register()
        response = self.client.post(
            "/workouts/new",
            data=self.workout_data(self.token()),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Strength day", response.data)
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
            "/library?focus=abs&level=beginner&equipment=bodyweight"
        )
        self.assertEqual(library.status_code, 200)
        self.assertIn(b"Abs &amp; core", library.data)
        self.assertNotIn(b"<h3>Legs &amp; glutes</h3>", library.data)

        guide = self.client.get("/library/abs?level=beginner&equipment=bodyweight")
        self.assertEqual(guide.status_code, 200)
        self.assertIn(b"MOVEMENT SEQUENCE", guide.data)
        self.assertIn(b"exercise-demos/Dead_Bug/0.jpg", guide.data)
        self.assertIn(b"exercise-demos/Dead_Bug/1.jpg", guide.data)
        self.assertIn(b"Pause movement demo", guide.data)
        self.assertIn(b"Demo artwork credits", guide.data)
        self.assertIn(b"Start guided workout", guide.data)
        self.assertIn(b"Voice on", guide.data)
        self.assertIn(b"data-duration=\"30\"", guide.data)
        self.assertIn(b"NO EQUIPMENT", guide.data)
        self.assertNotIn(b"exercise-illustration", guide.data)
        self.assertNotIn(b"youtube", guide.data.lower())
        self.assertIn(b"Mark movement complete", guide.data)
        image = self.client.get("/static/exercise-demos/Dead_Bug/0.jpg")
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image.mimetype, "image/jpeg")
        image.close()

    def test_guided_workout_requires_a_completed_movement(self) -> None:
        self.register()
        response = self.client.post(
            "/library/abs/complete",
            data={
                "csrf_token": self.token(),
                "level": "beginner",
                "equipment": "bodyweight",
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
                "equipment": "bodyweight",
                "completed_exercise[]": ["0", "2"],
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Beginner Abs &amp; Core", response.data)
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

    def test_unknown_focus_or_movement_is_not_accepted(self) -> None:
        self.register()
        self.assertEqual(self.client.get("/library/not-real").status_code, 404)
        response = self.client.post(
            "/library/abs/complete",
            data={
                "csrf_token": self.token(),
                "level": "expert",
                "equipment": "bodyweight",
                "completed_exercise[]": ["0"],
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_every_focus_has_valid_equipment_free_routines(self) -> None:
        from exercise_library import FOCUSES, build_routine

        demo_root = Path(__file__).resolve().parents[1] / "static" / "exercise-demos"
        for focus in FOCUSES:
            for level in ("beginner", "intermediate"):
                for equipment in ("bodyweight", "gym"):
                    with self.subTest(focus=focus, level=level, equipment=equipment):
                        routine = build_routine(focus, level, equipment)
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
                        for item in routine["exercises"]:
                            if item["demo_id"].startswith("wger_"):
                                demo_files = [demo_root / f"{item['demo_id']}.png"]
                            else:
                                demo_files = [
                                    demo_root / item["demo_id"] / "0.jpg",
                                    demo_root / item["demo_id"] / "1.jpg",
                                ]
                            self.assertTrue(all(path.is_file() for path in demo_files))
                        self.assertTrue(all(item["sets"] in (2, 3) for item in routine["exercises"]))
        home_chest = build_routine("chest", "beginner", "bodyweight")
        gym_chest = build_routine("chest", "beginner", "gym")
        self.assertEqual(home_chest["exercises"][2]["name"], "Push-up")
        self.assertEqual(home_chest, gym_chest)


if __name__ == "__main__":
    unittest.main()
