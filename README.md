# Vinland

Vinland is a responsive workout coach and fitness-training journal built with Flask, SQLite, and plain JavaScript. Members can choose a workout focus, follow a guided routine, watch movement demonstrations, and save completed sessions to a private training log.

## Features

- Private accounts with salted password hashing and signed sessions.
- CSRF protection on every form submission.
- Create, edit, and delete workouts with multiple exercises, duration, dates, and notes.
- Search training history by workout title, notes, or exercise, and filter sessions to the last 30 or 90 days.
- Guided, equipment-free beginner and intermediate routines for abs/core, chest, back, arms, legs/glutes, and full body.
- A preview-first workout guide that shows every movement and form demo before the guided player.
- A timed workout player where users hear an exercise introduction and form cue before choosing to start the timer, with repeating set countdowns, rest timers, pause/skip controls, and automatic progression through the full session.
- Gradual, per-focus progression: work intervals increase by five seconds with each completed guided session, up to a 20-second increase; sets increase every three sessions and are capped.
- Guided bodyweight routines rotate one movement at a time toward harder variations after each completed session, with progression tracked independently for each focus.
- Earn 100 XP for every saved workout, level up every 300 XP, and progress through warrior ranks from Ironbound to True Warrior; XP and ranks are derived from saved workout history.
- Open the rank indicator to see current and upcoming ranks, XP needed for each unlock, and the rank-specific mascot and badge.
- For each focus, the five-movement workout window advances after every guided session, introducing one harder bodyweight variation at a time until the final stage.
- Bundled two-position human exercise demos with smooth cross-fades, plus manual step-through controls.
- Mark completed movements and save the guided session directly to your training log; the saved time is adjusted to the movements completed.
- Personal dashboard with weekly sessions, lifting volume, workout streak, and recent sessions.
- A dashboard movement banner with bundled upper- and lower-body exercise illustrations.
- 30-day training progress chart and private profile/weight goals.
- Responsive layout, accessible form labels, and local SQLite storage.

## Run locally

Python 3.10 or newer is recommended.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>. The SQLite database is created in `instance\vinland.sqlite3` on first run. Set `FLASK_DEBUG=true` only for local development.

If port 5000 is already in use, run `$env:PORT = '5057'; python app.py` in PowerShell and open <http://127.0.0.1:5057>.

## Deploy on Render

1. Push this project to a GitHub repository.
2. In Render, choose **New → Blueprint** and connect that repository.
3. Render reads `render.yaml`, installs dependencies, generates a `SECRET_KEY`, and provisions a persistent disk for SQLite.
4. Once the service is live, open its URL and create your account.

The app refuses to start with `ENVIRONMENT=production` unless `SECRET_KEY` is configured. Keep `DATABASE_PATH` on persistent storage in production; ephemeral filesystems can lose SQLite data on redeploy.

The workout catalog and exercise demonstrations are bundled with the app. Movements use locally stored, two-position human exercise photos from the public-domain [Free Exercise DB](https://github.com/yuhonas/free-exercise-db); previews blend between the two poses. Bird Dog uses a CC BY 2.0 photo by PTPioneer, mirrored to show the opposite-side reach. See [`static/exercise-demos/ATTRIBUTIONS.md`](static/exercise-demos/ATTRIBUTIONS.md) for creators, sources, and license details. Guided demonstrations work without an external video service, video-site account, or AI API. They are visual movement references, not camera-based coaching or personalized medical advice.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Data and privacy

Workout and profile data is scoped to the signed-in account. Passwords are stored as one-way password hashes. Do not put `instance\vinland.sqlite3` or `.env` into source control. Configure a long, random `SECRET_KEY` for any deployment outside the included Render Blueprint.

Vinland’s training volume is calculated as sets × reps × entered weight in kilograms. Bodyweight or cardio-only work can be recorded with a weight of `0`; it contributes to session and exercise counts, not weighted volume.
