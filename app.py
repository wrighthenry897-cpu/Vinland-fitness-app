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
        return {"csrf_token": session["csrf_token"], "today": date.today().isoformat()}

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
        return render_template(
            "dashboard.html",
            stats=stats,
            chart_days=chart_days,
            recent=recent,
            streak=streak,
            total_workouts=db.execute(
                "SELECT COUNT(*) FROM workouts WHERE user_id = ?", (g.user["id"],)
            ).fetchone()[0],
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
            if user is None or not check_password_hash(user["password_hash"], password):
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
        equipment = "bodyweight"
        if focus not in {"all", *FOCUSES}:
            focus = "all"
        if level not in {"beginner", "intermediate"}:
            level = "beginner"
        routine_durations = {
            slug: build_routine(slug, level, "bodyweight")["duration"]
            for slug in FOCUSES
        }
        return render_template(
            "library.html",
            focuses=FOCUSES,
            selected_focus=focus,
            selected_level=level,
            selected_equipment=equipment,
            routine_durations=routine_durations,
        )

    @app.get("/library/<focus>")
    @login_required
    def workout_guide(focus: str) -> str:
        level = request.args.get("level", "beginner")
        equipment = "bodyweight"
        routine = build_routine(focus, level, equipment)
        if routine is None:
            abort(404)
        return render_template("workout_guide.html", routine=routine)

    @app.post("/library/<focus>/complete")
    @login_required
    def complete_guided_workout(focus: str) -> Any:
        level = request.form.get("level", "beginner")
        equipment = request.form.get("equipment", "bodyweight")
        routine = build_routine(focus, level, equipment)
        if routine is None:
            abort(404)
        equipment = routine["equipment"]
        raw_indexes = request.form.getlist("completed_exercise[]")
        try:
            indexes = sorted({int(value) for value in raw_indexes})
        except ValueError:
            abort(400, description="The selected exercises were invalid.")
        exercises = routine["exercises"]
        if not indexes or any(index < 0 or index >= len(exercises) for index in indexes):
            flash("Mark at least one movement complete to save your workout.", "error")
            return redirect(url_for("workout_guide", focus=focus, level=level, equipment=equipment))

        db = get_db()
        duration = max(1, round(routine["duration"] * len(indexes) / len(exercises)))
        cursor = db.execute(
            "INSERT INTO workouts (user_id, title, workout_date, duration, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                g.user["id"],
                routine["title"].title(),
                date.today().isoformat(),
                duration,
                f"Guided Vinland session · {level} · {equipment} · "
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
        flash("Session complete — your workout was added to your training log.", "success")
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
            cursor = db.execute(
                "INSERT INTO workouts (user_id, title, workout_date, duration, notes) "
                "VALUES (?, ?, ?, ?, ?)",
                (g.user["id"], data["title"], data["workout_date"], data["duration"], data["notes"]),
            )
            insert_exercises(db, cursor.lastrowid, exercises)
            db.commit()
            flash("Workout saved. Nice work showing up.", "success")
            return redirect(url_for("workout_list"))
        return render_template("workout_form.html", mode="new", workout={}, exercises=[{}])

    @app.get("/workouts")
    @login_required
    def workout_list() -> str:
        workouts = get_db().execute(
            """
            SELECT w.id, w.title, w.workout_date, w.duration, w.notes,
                   COUNT(e.id) AS exercise_count,
                   COALESCE(SUM(e.sets * e.reps * e.weight), 0) AS volume
            FROM workouts w LEFT JOIN exercises e ON e.workout_id = w.id
            WHERE w.user_id = ?
            GROUP BY w.id
            ORDER BY w.workout_date DESC, w.id DESC
            """,
            (g.user["id"],),
        ).fetchall()
        return render_template("workouts.html", workouts=workouts)

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
