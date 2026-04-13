# JpChars — Japanese Letters Learning (Django + Vanilla JS)

JpChars is a full‑stack web app for learning **Hiragana** and **Katakana** through short, interactive exercises. It’s built as a **Django** application that serves an authenticated HTML “shell”, then uses **vanilla JavaScript** to deliver **SPA-like** interactions backed by lightweight JSON endpoints.

## Why this project is interesting (engineering highlights)

- **Hybrid architecture (SSR + dynamic frontend)**: Django templates provide the page structure and auth flow, while `static/jpchars/index.js` drives client-side navigation and exercise flows with `fetch()` calls to JSON routes.
- **Custom user model + progression tracking**: A custom `User(AbstractUser)` stores independent progress for Hiragana/Katakana; progression is enforced server-side.
- **Backend-driven content + deterministic serialization**: Exercises and tasks live in the database and serialize to JSON via explicit `serialize()` methods.
- **Multiple learning modes in one flow**:
  - Multiple-choice (JP → romaji)
  - Multiple-choice (romaji → JP)
  - Free input (JP → romaji)
  - Free input (romaji → JP)
  - A **matching mini-game** to finish each level
- **Responsive UI**: CSS uses media queries to scale the quiz UI across desktop/tablet/mobile, plus animated UI affordances (greeting + result notifier).

## Tech stack

- **Backend**: Python, **Django 5.1.6**
- **Auth**: Django session auth (register/login/logout)
- **Database**: SQLite (default, local)
- **Frontend**: Vanilla JavaScript + Django templates
- **Styling**: Bootstrap 4 (CDN) + custom CSS

## App walkthrough (what users can do)

- Create an account, log in, and choose a track: **Hiragana** or **Katakana**
- Browse exercises grouped by level (level “parents” expand/collapse their children)
- Complete a level via a mixed quiz set and a final matching round
- Track progress in **Profile** with completion bars for each track

## Project structure

```text
capstone/
├─ manage.py
├─ db.sqlite3
├─ capstone/                  # Django project
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ asgi.py
└─ jpchars/                   # Main app
   ├─ models.py               # User, Exercise, Task
   ├─ views.py                # Auth + JSON API + progression logic
   ├─ urls.py                 # App routes
   ├─ templates/jpchars/      # layout/index/login/register
   └─ static/jpchars/         # index.js + styles.css
```

## Data model

- **`User`**: extends `AbstractUser`
  - `hiragana_level` (int)
  - `katakana_level` (int)
- **`Exercise`**: (track, level, representation, hint)
- **`Task`**: (track, min_level, japanese, romaji, priority)

Exercises/Tasks are administered via Django admin and returned to the frontend as JSON for interactive rendering.

## JSON API (used by the frontend)

All routes are under the main site root (see `jpchars/urls.py`).

- **`GET /get_levels`** → `[hiragana_level, katakana_level]`
- **`GET /get_exercises`** → list of exercises
- **`GET /get_tasks/<type>/<level>`** → task list for a given track + level
- **`PUT /update_level`** → updates stored progress for a track

## Local setup

### Prerequisites

- **Python 3.10+** recommended

### Run the app

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install "Django==5.1.6"

python manage.py migrate
python manage.py runserver
```

Then open:

- **App**: `http://127.0.0.1:8000/`
- **Admin** (optional): `http://127.0.0.1:8000/admin/`

### Seed exercises/tasks (if your DB is empty)

This repo includes `db.sqlite3`, but if you migrate into a fresh DB you can add content via the admin UI:

```bash
python manage.py createsuperuser
```

Then log into `/admin/` and create `Exercise` + `Task` entries.
