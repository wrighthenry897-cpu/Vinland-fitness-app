from __future__ import annotations

import hmac
import math
import os
import re
import secrets
import sqlite3
from datetime import date, datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar

from flask import (
    Flask,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from exercise_library import FOCUSES, build_routine

F = TypeVar("F", bound=Callable[..., Any])

XP_PER_WORKOUT = 100
XP_PER_LEVEL = 300
PLAYER_RANKS = (
    "Ironbound",
    "Battle-Hardened",
    "Stormforged",
    "Legend of Vinland",
    "True Warrior",
)
PLAYER_RANK_BADGES = (
    ("🐺", "Iron Wolf", "⚒"),
    ("🐻", "War Bear", "⚔"),
    ("🦅", "Storm Raven", "ϟ"),
    ("🐉", "Vinland Dragon", "♜"),
    ("🦁", "True Warrior Crest", "♛"),
)


def calculate_player_progress(session_count: int) -> dict[str, int | str]:
    sessions = max(0, session_count)
    xp = sessions * XP_PER_WORKOUT
    level = xp // XP_PER_LEVEL + 1
    xp_in_level = xp % XP_PER_LEVEL
    return {
        "sessions": sessions,
        "xp": xp,
        "level": level,
        "rank": PLAYER_RANKS[min(level - 1, len(PLAYER_RANKS) - 1)],
        "xp_in_level": xp_in_level,
        "xp_to_next": XP_PER_LEVEL - xp_in_level,
        "progress_percent": xp_in_level * 100 // XP_PER_LEVEL,
        "xp_per_workout": XP_PER_WORKOUT,
        "xp_per_level": XP_PER_LEVEL,
    }


def build_rank_progression(xp: int) -> list[dict[str, int | str]]:
    current_rank_index = min(max(0, xp) // XP_PER_LEVEL, len(PLAYER_RANKS) - 1)
    ranks = []
    for index, (rank, (mascot, badge, badge_symbol)) in enumerate(
        zip(PLAYER_RANKS, PLAYER_RANK_BADGES)
    ):
        required_xp = index * XP_PER_LEVEL
        ranks.append(
            {
                "name": rank,
                "mascot": mascot,
                "badge": badge,
                "badge_symbol": badge_symbol,
                "level": index + 1,
                "required_xp": required_xp,
                "xp_remaining": max(0, required_xp - xp),
                "status": (
                    "current"
                    if index == current_rank_index
                    else "unlocked"
                    if index < current_rank_index
                    else "locked"
                ),
            }
        )
    return ranks


def flash_player_level_up(previous_sessions: int, current_sessions: int) -> None:
    previous_level = calculate_player_progress(previous_sessions)["level"]
    current_progress = calculate_player_progress(current_sessions)
    if current_progress["level"] > previous_level:
        flash(
            f"Level up! You reached Level {current_progress['level']} "
            f"and earned the {current_progress['rank']} rank.",
            "success",
        )


def guided_session_count(db: sqlite3.Connection, user_id: int, focus: str) -> int:
    category_name = FOCUSES[focus]["name"].lower()
    return int(
        db.execute(
            """
            SELECT COUNT(*) FROM workouts
            WHERE user_id = ?
              AND (
                  notes LIKE ?
                  OR (
                      notes LIKE 'Guided Vinland session%'
                      AND LOWER(title) LIKE ?
                  )
              )
            """,
            (
                user_id,
                f"Guided Vinland session · focus={focus} ·%",
                f"%{category_name}%",
            ),
        ).fetchone()[0]
    )


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    production = os.environ.get("ENVIRONMENT", "").lower() == "production"
    secret_key = os.environ.get("SECRET_KEY")
    if production and not secret_key:
        raise RuntimeError("Set SECRET_KEY to a long, random value before deployment.")

    app.config.from_mapping(
        SECRET_KEY=secret_key or "vinland-local-development-key-change-before-deploy",
        DATABASE_PATH=os.environ.get(
            "DATABASE_PATH", str(Path(app.instance_path) / "vinland.sqlite3")
        ),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=production,
        MAX_CONTENT_LENGTH=1 * 1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    initialize_database(app)

    @app.before_request
    def load_request_state() -> None:
        g.user = None
        user_id = session.get("user_id")
        if user_id is not None:
            g.user = get_db().execute(
                "SELECT id, name, email, current_weight, target_weight FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
            if g.user is None:
                session.clear()

        if request.method == "POST":
            token = session.get("csrf_token", "")
            submitted = request.form.get("csrf_token", "")
            if not token or not hmac.compare_digest(token, submitted):
                abort(400, description="Your session expired. Refresh the page and try again.")

    @app.teardown_appcontext
    def close_database(_error: BaseException | None = None) -> None:
        connection = g.pop("db", None)
        if connection is not None:
            connection.close()

    @app.context_processor
    def inject_template_state() -> dict[str, Any]:
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        player = getattr(g, "player_progress", None)
        if g.user is not None and player is None:
            session_count = get_db().execute(
                "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
            ).fetchone()[0]
            player = calculate_player_progress(session_count)
            g.player_progress = player
        return {
            "csrf_token": session["csrf_token"],
            "today": date.today().isoformat(),
            "player": player,
        }

    @app.template_filter("datetimeformat")
    def format_date(value: str, date_format: str = "%b %d, %Y") -> str:
        return date.fromisoformat(value).strftime(date_format)

    def login_required(view: F) -> F:
        @wraps(view)
        def wrapped_view(*args: Any, **kwargs: Any) -> Any:
            if g.user is None:
                flash("Sign in to continue.", "info")
                return redirect(url_for("login"))
            return view(*args, **kwargs)

        return wrapped_view  # type: ignore[return-value]

    def owned_workout(workout_id: int) -> sqlite3.Row:
        workout = get_db().execute(
            "SELECT * FROM workouts WHERE id = ? AND user_id = ?",
            (workout_id, g.user["id"]),
        ).fetchone()
        if workout is None:
            abort(404)
        return workout

    @app.get("/")
    @login_required
    def dashboard() -> str:
        db = get_db()
        today = date.today()
        week_start = today - timedelta(days=6)
        weekly_rows = db.execute(
            """
            SELECT workout_date, COUNT(*) AS sessions,
                   COALESCE(SUM((
                       SELECT COALESCE(SUM(e.sets * e.reps * e.weight), 0)
                       FROM exercises e WHERE e.workout_id = workouts.id
                   )), 0) AS volume
            FROM workouts
            WHERE user_id = ? AND workout_date BETWEEN ? AND ?
            GROUP BY workout_date
            """,
            (g.user["id"], week_start.isoformat(), today.isoformat()),
        ).fetchall()
        by_day = {row["workout_date"]: row for row in weekly_rows}
        chart_days = []
        for offset in range(6, -1, -1):
            day = today - timedelta(days=offset)
            row = by_day.get(day.isoformat())
            chart_days.append(
                {
                    "label": day.strftime("%a"),
                    "date": day.strftime("%b %d"),
                    "volume": round(row["volume"]) if row else 0,
                    "sessions": row["sessions"] if row else 0,
                }
            )

        stats = db.execute(
            """
            SELECT COUNT(*) AS sessions,
                   COALESCE(SUM((
                       SELECT COALESCE(SUM(e.sets * e.reps * e.weight), 0)
                       FROM exercises e WHERE e.workout_id = workouts.id
                   )), 0) AS volume
            FROM workouts
            WHERE user_id = ? AND workout_date BETWEEN ? AND ?
            """,
            (g.user["id"], week_start.isoformat(), today.isoformat()),
        ).fetchone()
        recent = db.execute(
            "SELECT id, title, workout_date, duration FROM workouts "
            "WHERE user_id = ? ORDER BY workout_date DESC, id DESC LIMIT 4",
            (g.user["id"],),
        ).fetchall()
        streak = calculate_streak(
            db.execute(
                "SELECT DISTINCT workout_date FROM workouts WHERE user_id = ? "
                "AND workout_date <= ? ORDER BY workout_date DESC",
                (g.user["id"], today.isoformat()),
            ).fetchall(),
            today,
        )
        total_workouts = db.execute(
            "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
        ).fetchone()[0]
        player = calculate_player_progress(total_workouts)
        g.player_progress = player
        return render_template(
            "dashboard.html",
            stats=stats,
            chart_days=chart_days,
            recent=recent,
            streak=streak,
            total_workouts=total_workouts,
            player=player,
        )

    @app.route("/register", methods=["GET", "POST"])
    def register() -> str:
        if g.user is not None:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            error = validate_registration(name, email, password)
            if error:
                flash(error, "error")
            else:
                try:
                    cursor = get_db().execute(
                        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                        (name, email, generate_password_hash(password)),
                    )
                    get_db().commit()
                except sqlite3.IntegrityError:
                    flash("An account with that email already exists.", "error")
                else:
                    session.clear()
                    session["user_id"] = cursor.lastrowid
                    flash("Your Vinland account is ready. Let’s get moving.", "success")
                    return redirect(url_for("dashboard"))
        return render_template("auth.html", mode="register")

    @app.route("/login", methods=["GET", "POST"])
    def login() -> str:
        if g.user is not None:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            user = get_db().execute(
                "SELECT id, password_hash FROM users WHERE email = ?", (email,)
            ).fetchone()
            if user is None:
                current_app.logger.warning(
                    "Sign-in rejected because no account matched the submitted email."
                )
                flash("That email and password combination didn’t match.", "error")
            elif not check_password_hash(user["password_hash"], password):
                current_app.logger.warning(
                    "Sign-in rejected because the password hash did not match."
                )
                flash("That email and password combination didn’t match.", "error")
            else:
                session.clear()
                session["user_id"] = user["id"]
                flash("Welcome back.", "success")
                return redirect(url_for("dashboard"))
        return render_template("auth.html", mode="login")

    @app.post("/logout")
    @login_required
    def logout() -> Any:
        session.clear()
        flash("You’ve been signed out.", "info")
        return redirect(url_for("login"))

    @app.get("/library")
    @login_required
    def workout_library() -> str:
        focus = request.args.get("focus", "all")
        level = request.args.get("level", "beginner")
        if focus not in {"all", *FOCUSES}:
            focus = "all"
        if level not in {"beginner", "intermediate"}:
            level = "beginner"
        db = get_db()
        day_number = db.execute(
            "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
        ).fetchone()[0] + 1
        routine_durations = {}
        routine_progress = {}
        for slug in FOCUSES:
            completed_sessions = guided_session_count(db, g.user["id"], slug)
            routine = build_routine(
                slug,
                level,
                completed_sessions,
            )
            routine_durations[slug] = routine["duration"]
            routine_progress[slug] = {
                "stage": routine["progression_stage"],
                "stages": routine["progression_stages"],
                "sessions": completed_sessions,
                "next_stage_unlocked": routine["next_stage_unlocked"],
            }
        return render_template(
            "library.html",
            focuses=FOCUSES,
            selected_focus=focus,
            selected_level=level,
            day_number=day_number,
            routine_durations=routine_durations,
            routine_progress=routine_progress,
        )

    @app.get("/library/<focus>")
    @login_required
    def workout_guide(focus: str) -> str:
        if focus not in FOCUSES:
            abort(404)
        level = request.args.get("level", "beginner")
        try:
            preview_offset = int(request.args.get("preview", "0"))
        except ValueError:
            abort(400, description="Choose a valid workout day to preview.")
        completed_sessions = guided_session_count(
            get_db(), g.user["id"], focus
        )
        current_routine = build_routine(focus, level, completed_sessions)
        if current_routine is None:
            abort(404)
        if not 0 <= preview_offset < current_routine["progression_stages"]:
            abort(400, description="That workout day is outside this focus rotation.")
        routine = build_routine(focus, level, completed_sessions + preview_offset)
        if routine is None:
            abort(404)
        day_number = get_db().execute(
            "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
        ).fetchone()[0] + 1
        preview_days = [
            {
                "offset": offset,
                "day": day_number + offset,
                "stage": (
                    (completed_sessions + offset)
                    % current_routine["progression_stages"]
                )
                + 1,
            }
            for offset in range(current_routine["progression_stages"])
        ]
        return render_template(
            "workout_guide.html",
            routine=routine,
            day_number=day_number + preview_offset,
            preview_offset=preview_offset,
            preview_days=preview_days,
        )

    @app.post("/library/<focus>/complete")
    @login_required
    def complete_guided_workout(focus: str) -> Any:
        level = request.form.get("level", "beginner")
        completed_sessions = guided_session_count(
            get_db(), g.user["id"], focus
        )
        routine = build_routine(
            focus, level, completed_sessions
        )
        if routine is None:
            abort(404)
        raw_indexes = request.form.getlist("completed_exercise[]")
        try:
            indexes = sorted({int(value) for value in raw_indexes})
        except ValueError:
            abort(400, description="The selected exercises were invalid.")
        exercises = routine["exercises"]
        if not indexes or any(index < 0 or index >= len(exercises) for index in indexes):
            flash("Mark at least one movement complete to save your workout.", "error")
            return redirect(url_for("workout_guide", focus=focus, level=level))

        db = get_db()
        previous_sessions = db.execute(
            "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
        ).fetchone()[0]
        duration = max(1, round(routine["duration"] * len(indexes) / len(exercises)))
        cursor = db.execute(
            "INSERT INTO workouts (user_id, title, workout_date, duration, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                g.user["id"],
                routine["title"].title(),
                date.today().isoformat(),
                duration,
                f"Guided Vinland session · focus={focus} · {level} · bodyweight · "
                f"{len(indexes)} of {len(exercises)} movements completed.",
            ),
        )
        logged_exercises = []
        for index in indexes:
            exercise = exercises[index]
            target = exercise["target"]
            match = re.search(r"\d+", target)
            reps = 1 if "sec" in target else int(match.group()) if match else 1
            logged_exercises.append(
                (cursor.lastrowid, exercise["name"], exercise["sets"], reps, 0)
            )
        db.executemany(
            "INSERT INTO exercises (workout_id, name, sets, reps, weight) VALUES (?, ?, ?, ?, ?)",
            logged_exercises,
        )
        db.commit()
        flash(
            f"Session complete — {XP_PER_WORKOUT} XP earned! "
            "Your workout was added to your training log.",
            "success",
        )
        flash_player_level_up(previous_sessions, previous_sessions + 1)
        return redirect(url_for("workout_list"))

    @app.route("/workouts/new", methods=["GET", "POST"])
    @login_required
    def new_workout() -> str | Any:
        if request.method == "POST":
            data, exercises, error = parse_workout_form()
            if error:
                flash(error, "error")
                return render_template("workout_form.html", mode="new", workout=data, exercises=exercises)
            db = get_db()
            previous_sessions = db.execute(
                "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
            ).fetchone()[0]
            cursor = db.execute(
                "INSERT INTO workouts (user_id, title, workout_date, duration, notes) "
                "VALUES (?, ?, ?, ?, ?)",
                (g.user["id"], data["title"], data["workout_date"], data["duration"], data["notes"]),
            )
            insert_exercises(db, cursor.lastrowid, exercises)
            db.commit()
            flash(
                f"Workout saved — {XP_PER_WORKOUT} XP earned. Nice work showing up.",
                "success",
            )
            flash_player_level_up(previous_sessions, previous_sessions + 1)
            return redirect(url_for("workout_list"))
        return render_template("workout_form.html", mode="new", workout={}, exercises=[{}])

    @app.get("/workouts")
    @login_required
    def workout_list() -> str:
        search_query = request.args.get("q", "").strip()[:100]
        period = request.args.get("period", "all")
        if period not in {"all", "30", "90"}:
            period = "all"

        conditions = ["w.user_id = ?"]
        parameters: list[Any] = [g.user["id"]]
        if search_query:
            escaped_query = search_query.replace("!", "!!").replace("%", "!%").replace("_", "!_")
            pattern = f"%{escaped_query}%"
            conditions.append(
                """
                (
                    w.title LIKE ? ESCAPE '!'
                    OR w.notes LIKE ? ESCAPE '!'
                    OR EXISTS (
                        SELECT 1 FROM exercises e
                        WHERE e.workout_id = w.id AND e.name LIKE ? ESCAPE '!'
                    )
                )
                """
            )
            parameters.extend([pattern, pattern, pattern])
        if period != "all":
            start_date = date.today() - timedelta(days=int(period) - 1)
            conditions.append("w.workout_date >= ?")
            parameters.append(start_date.isoformat())
        where_clause = " AND ".join(conditions)
        workouts = get_db().execute(
            f"""
            SELECT w.id, w.title, w.workout_date, w.duration, w.notes,
                   COUNT(e.id) AS exercise_count,
                   COALESCE(SUM(e.sets * e.reps * e.weight), 0) AS volume
            FROM workouts w LEFT JOIN exercises e ON e.workout_id = w.id
            WHERE {where_clause}
            GROUP BY w.id
            ORDER BY w.workout_date DESC, w.id DESC
            """,
            parameters,
        ).fetchall()
        total_workouts = get_db().execute(
            "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
        ).fetchone()[0]
        return render_template(
            "workouts.html",
            workouts=workouts,
            search_query=search_query,
            period=period,
            total_workouts=total_workouts,
        )

    @app.route("/workouts/<int:workout_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_workout(workout_id: int) -> str | Any:
        workout = owned_workout(workout_id)
        db = get_db()
        if request.method == "POST":
            data, exercises, error = parse_workout_form()
            if error:
                flash(error, "error")
                return render_template(
                    "workout_form.html",
                    mode="edit",
                    workout=data,
                    exercises=exercises,
                    workout_id=workout_id,
                )
            db.execute(
                "UPDATE workouts SET title = ?, workout_date = ?, duration = ?, notes = ? "
                "WHERE id = ? AND user_id = ?",
                (data["title"], data["workout_date"], data["duration"], data["notes"], workout_id, g.user["id"]),
            )
            db.execute("DELETE FROM exercises WHERE workout_id = ?", (workout_id,))
            insert_exercises(db, workout_id, exercises)
            db.commit()
            flash("Workout updated.", "success")
            return redirect(url_for("workout_list"))
        exercises = db.execute(
            "SELECT name, sets, reps, weight FROM exercises WHERE workout_id = ? ORDER BY id",
            (workout_id,),
        ).fetchall()
        return render_template(
            "workout_form.html",
            mode="edit",
            workout=workout,
            exercises=exercises or [{}],
            workout_id=workout_id,
        )

    @app.post("/workouts/<int:workout_id>/delete")
    @login_required
    def delete_workout(workout_id: int) -> Any:
        owned_workout(workout_id)
        db = get_db()
        db.execute(
            "DELETE FROM workouts WHERE id = ? AND user_id = ?",
            (workout_id, g.user["id"]),
        )
        db.commit()
        flash("Workout deleted.", "info")
        return redirect(url_for("workout_list"))

    @app.get("/progress")
    @login_required
    def progress() -> str:
        db = get_db()
        today = date.today()
        start = today - timedelta(days=29)
        rows = db.execute(
            """
            SELECT workout_date, COUNT(*) AS sessions,
                   COALESCE(SUM((
                       SELECT COALESCE(SUM(e.sets * e.reps * e.weight), 0)
                       FROM exercises e WHERE e.workout_id = workouts.id
                   )), 0) AS volume
            FROM workouts
            WHERE user_id = ? AND workout_date BETWEEN ? AND ?
            GROUP BY workout_date ORDER BY workout_date
            """,
            (g.user["id"], start.isoformat(), today.isoformat()),
        ).fetchall()
        days = [
            {
                "label": (start + timedelta(days=i)).strftime("%d"),
                "date": (start + timedelta(days=i)).strftime("%b %d"),
                "volume": round(next((row["volume"] for row in rows if row["workout_date"] == (start + timedelta(days=i)).isoformat()), 0)),
                "sessions": next((row["sessions"] for row in rows if row["workout_date"] == (start + timedelta(days=i)).isoformat()), 0),
            }
            for i in range(30)
        ]
        totals = db.execute(
            """
            SELECT COUNT(DISTINCT w.id) AS sessions,
                   COUNT(e.id) AS exercises,
                   COALESCE(SUM(e.sets * e.reps * e.weight), 0) AS volume
            FROM workouts w LEFT JOIN exercises e ON e.workout_id = w.id
            WHERE w.user_id = ? AND w.workout_date BETWEEN ? AND ?
            """,
            (g.user["id"], start.isoformat(), today.isoformat()),
        ).fetchone()
        return render_template("progress.html", days=days, totals=totals)

    @app.get("/ranks")
    @login_required
    def rank_progression() -> str:
        player = calculate_player_progress(
            get_db().execute(
                "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
            ).fetchone()[0]
        )
        g.player_progress = player
        return render_template(
            "rank_progression.html",
            ranks=build_rank_progression(player["xp"]),
            player=player,
        )

    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile() -> str | Any:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name or len(name) > 60:
                flash("Your name must be between 1 and 60 characters.", "error")
                return render_template("profile.html")
            try:
                current = parse_optional_weight(request.form.get("current_weight", ""))
                target = parse_optional_weight(request.form.get("target_weight", ""))
            except ValueError as error:
                flash(str(error), "error")
                return render_template("profile.html")
            db = get_db()
            db.execute(
                "UPDATE users SET name = ?, current_weight = ?, target_weight = ? WHERE id = ?",
                (name, current, target, g.user["id"]),
            )
            db.commit()
            flash("Your profile has been updated.", "success")
            return redirect(url_for("profile"))
        return render_template("profile.html")

    @app.errorhandler(400)
    def bad_request(error: Any) -> tuple[str, int]:
        return render_template("error.html", code=400, message=getattr(error, "description", "Bad request.")), 400

    @app.errorhandler(404)
    def not_found(_error: Any) -> tuple[str, int]:
        return render_template("error.html", code=404, message="We couldn’t find that page or workout."), 404

    return app


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        connection = sqlite3.connect(current_app_config_path())
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


def current_app_config_path() -> str:
    from flask import current_app

    return current_app.config["DATABASE_PATH"]


def initialize_database(app: Flask) -> None:
    path = Path(app.config["DATABASE_PATH"])
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                current_weight REAL,
                target_weight REAL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                workout_date TEXT NOT NULL,
                duration INTEGER NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS workouts_user_date
                ON workouts(user_id, workout_date DESC);
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id INTEGER NOT NULL REFERENCES workouts(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                sets INTEGER NOT NULL,
                reps INTEGER NOT NULL,
                weight REAL NOT NULL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS exercises_workout ON exercises(workout_id);
            """
        )
    finally:
        db.close()


def validate_registration(name: str, email: str, password: str) -> str | None:
    name = name.strip()
    email = email.strip().lower()
    if not name or len(name) > 60:
        return "Please enter a name between 1 and 60 characters."
    if len(email) > 254 or "@" not in email or email.startswith("@") or email.endswith("@"):
        return "Enter a valid email address."
    if len(password) < 8 or len(password) > 128:
        return "Your password must be between 8 and 128 characters."
    return None


def parse_workout_form() -> tuple[dict[str, Any], list[dict[str, Any]], str | None]:
    data: dict[str, Any] = {
        "title": request.form.get("title", "").strip(),
        "workout_date": request.form.get("workout_date", ""),
        "duration": request.form.get("duration", ""),
        "notes": request.form.get("notes", "").strip(),
    }
    submitted_fields = [
        request.form.getlist(field)
        for field in ("exercise_name[]", "exercise_sets[]", "exercise_reps[]", "exercise_weight[]")
    ]
    row_count = max(map(len, submitted_fields), default=0)
    raw_exercises = [
        {
            key: values[index] if index < len(values) else ""
            for key, values in zip(("name", "sets", "reps", "weight"), submitted_fields)
        }
        for index in range(row_count)
    ]
    if not data["title"] or len(data["title"]) > 80:
        return data, raw_exercises, "Give your workout a title (up to 80 characters)."
    try:
        workout_date = datetime.strptime(data["workout_date"], "%Y-%m-%d").date()
        if workout_date > date.today():
            raise ValueError
        duration = int(data["duration"])
        if not 1 <= duration <= 600:
            raise ValueError
    except ValueError:
        return data, raw_exercises, "Choose a valid date and a duration between 1 and 600 minutes."
    if len(data["notes"]) > 1000:
        return data, raw_exercises, "Keep workout notes under 1,000 characters."
    data["duration"] = duration
    data["workout_date"] = workout_date.isoformat()

    if len(set(map(len, submitted_fields))) != 1:
        return data, raw_exercises, "One or more exercise details are missing. Review each row and try again."
    names, sets_values, reps_values, weights = submitted_fields
    exercises = []
    for name, sets_value, reps_value, weight_value in zip(names, sets_values, reps_values, weights):
        name = name.strip()
        if not name and not sets_value and not reps_value and not weight_value:
            continue
        try:
            sets = int(sets_value)
            reps = int(reps_value)
            weight = float(weight_value or 0)
            if not name or len(name) > 80 or not 1 <= sets <= 100 or not 1 <= reps <= 1000:
                raise ValueError
            if not math.isfinite(weight) or not 0 <= weight <= 2000:
                raise ValueError
        except ValueError:
            return data, raw_exercises, "Check each exercise: add a name, valid sets and reps, and a weight from 0 to 2,000 kg."
        exercises.append({"name": name, "sets": sets, "reps": reps, "weight": weight})
    if not exercises:
        return data, raw_exercises, "Add at least one exercise to your workout."
    if len(exercises) > 30:
        return data, raw_exercises, "A workout can contain up to 30 exercises."
    return data, exercises, None


def insert_exercises(db: sqlite3.Connection, workout_id: int, exercises: list[dict[str, Any]]) -> None:
    db.executemany(
        "INSERT INTO exercises (workout_id, name, sets, reps, weight) VALUES (?, ?, ?, ?, ?)",
        [
            (workout_id, exercise["name"], exercise["sets"], exercise["reps"], exercise["weight"])
            for exercise in exercises
        ],
    )


def parse_optional_weight(value: str) -> float | None:
    if not value.strip():
        return None
    try:
        weight = float(value)
    except ValueError as error:
        raise ValueError("Enter a valid weight in kilograms.") from error
    if not math.isfinite(weight) or not 0 <= weight <= 500:
        raise ValueError("Weight must be between 0 and 500 kg.")
    return weight


def calculate_streak(rows: list[sqlite3.Row], today: date) -> int:
    workout_days = {date.fromisoformat(row["workout_date"]) for row in rows}
    cursor = today if today in workout_days else today - timedelta(days=1)
    streak = 0
    while cursor in workout_days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG", "").lower() == "true",
        port=int(os.environ.get("PORT", "5000")),
    )
