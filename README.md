# Network — Django Social Network

A Twitter-style social network built with Django. Users can register/login, create posts, follow/unfollow other users, like posts, and browse feeds with pagination. The UI is server-rendered with a thin JavaScript layer that fetches JSON from Django endpoints to deliver an app-like experience (inline editing, live like toggles, and page navigation without full reloads).

## Why this project is employer-relevant

- **Full-stack fundamentals**: database modeling, authentication, server-rendered templates, and REST-like JSON endpoints.
- **Interactive UI without a frontend framework**: a clean demonstration of using `fetch()` + Django to build dynamic behavior.
- **Practical product features**: profiles, follow graph, personalized feed (“Following”), likes, and editing with permission checks.

## Features

- **Authentication**: register, login, logout (Django auth).
- **Create posts**: authenticated users can publish new posts.
- **Feeds**:
  - **All Posts** feed
  - **Following** feed (only posts from followed users)
  - **Profile** page (posts by a specific user)
- **Follow system**: follow/unfollow users, follower/following counts.
- **Likes**: like/unlike posts with immediate UI feedback.
- **Inline editing**: authors can edit their own posts (HTTP `PUT`).
- **Pagination**: 10 posts per page using Django’s `Paginator`.

## Tech stack

- **Backend**: Python, Django
- **Database**: SQLite (default, via Django ORM)
- **Frontend**: Django templates + Bootstrap 4 + vanilla JavaScript
- **API style**: lightweight JSON endpoints (no separate SPA build)

## Architecture (code tour)

- **Project config**: `project4/settings.py`, `project4/urls.py`
- **App**: `network/`
  - **Models**: `network/models.py`
    - `Post` (content, timestamp, author)
    - `Follow` (follower → followed)
    - `Like` (liker → post)
    - Custom `User` model (`AUTH_USER_MODEL = "network.User"`)
  - **Routes**: `network/urls.py`
  - **Views + JSON endpoints**: `network/views.py`
  - **Templates**: `network/templates/network/`
    - `index.html` contains the main feed UI and `fetch()` logic
    - `layout.html` defines navigation + Bootstrap base
  - **Styling**: `network/static/network/styles.css`

## JSON endpoints (used by the frontend)

These routes are called from the JavaScript embedded in `network/templates/network/index.html`:

- **Fetch posts**: `GET /posts/<section>/<page>/<name>`
  - `section`: `All Posts` | `Following` | `Profile`
  - `page`: 1-indexed page number
  - `name`: username for Profile; otherwise `none`
- **Pagination availability**: `GET /pages_present/<section>/<page>/<name>`
  - returns `[has_previous, has_next]`
- **Profile follow data**:
  - `GET /follow_count/<author>` → `{ followers, following }`
  - `GET /follow_status/<author>` → `true|false`
  - `GET /flip_status/<author>` → toggles follow/unfollow
- **Post editing**: `PUT /edit_post/<section>/<page>/<name>/<i>`
  - updates the \(i\)-th post on the requested page (author-only)
- **Likes**:
  - `GET /switch_status/<section>/<page>/<name>/<i>` → toggles like, returns `true|false`
  - `GET /is_liked/<section>/<page>/<name>/<i>` → returns `true|false`

## Data model (high level)

- **`User`** can have many **`Post`**s.
- **`Follow`** implements a directed follower graph:
  - `follower` → the user doing the following
  - `followed` → the user being followed
- **`Like`** is a join table between `User` and `Post`.

## Local setup

### Prerequisites

- Python 3
- (Recommended) a virtual environment tool (`venv`)

### Run the project

From the project root (the folder containing `manage.py`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install django
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

### Create an admin user (optional)

```bash
python manage.py createsuperuser
```

Admin panel: `http://127.0.0.1:8000/admin/`.

## Notes on implementation

- **Authorization**: editing is restricted to the post’s author (checked server-side in `edit_post`).
- **Pagination**: performed on the server via `Paginator(..., 10)`; the UI queries whether next/previous pages exist.
- **UI behavior**: the feed is rendered client-side from JSON (fast refreshes, no template duplication for each feed).

## What I’d improve next (roadmap)

- **Stable post identifiers in routes**: edit/like endpoints currently address posts by “index on a page”; using `post_id` would be more robust.
- **CSRF protection for `PUT`**: add CSRF token header handling for non-GET requests in `fetch()`.
- **Stronger API semantics**: use `POST/DELETE` for follow/like toggles, and return updated counts in responses.
- **Test coverage**: add unit tests for follow/like/edit permissions and pagination edge cases.
- **Production readiness**: move `SECRET_KEY` to environment variables and configure `ALLOWED_HOSTS`.

## Screenshots / demo

Add screenshots or a short demo video/gif here to showcase:

- All Posts feed + pagination
- Profile page with follow button and follower counts
- Inline post editing
- Like/unlike interactions

