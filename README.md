# Wiki — Django + Markdown Knowledge Base

A lightweight Wikipedia-style web app where content is authored in **Markdown** and served as **HTML** using **Django**. Users can browse all entries, view any page, search by title (exact + partial matches), create new pages, edit existing ones, and jump to a random entry.

This project showcases practical full‑stack fundamentals: routing, templates, form handling, server-side rendering, persistent file-backed content, and clean UI composition with Bootstrap.

## Highlights

- **Markdown → HTML rendering**: content is stored as `.md` files and rendered dynamically for display.
- **Create & Edit flows**: server-side forms with validation, duplicate-title protection, and persistence.
- **Search UX**:
  - exact match redirects to the entry
  - partial matches list relevant pages
- **Random page**: one click to explore the knowledge base.
- **Django templates + Bootstrap layout**: consistent nav + responsive structure.

## Tech Stack

- **Backend**: Python, Django
- **Rendering**: Django Templates (server-side rendered pages)
- **Markdown**: `markdown` library (converts `.md` to HTML)
- **Storage**: file-backed entries (`/entries/*.md`) via Django’s `default_storage`
- **Styling**: Bootstrap 4 + custom CSS (`encyclopedia/static/encyclopedia/styles.css`)
- **DB**: SQLite present (`db.sqlite3`) (not required for core wiki entry storage)

## Key User Flows

- **Browse all pages**: view the index of all entries.
- **View an entry**: `/wiki/<title>` renders the Markdown entry as HTML.
- **Search**: `/search/?q=<query>`
  - exact title → entry page
  - otherwise → list of partial matches
- **Create**: `/create/` creates a new Markdown entry (rejects duplicates).
- **Edit**: `/edit/<title>` updates an existing entry’s Markdown content.
- **Random**: `/random/` navigates to a randomly selected entry.

## Project Structure

```
.
├── encyclopedia/                 # Django app
│   ├── templates/encyclopedia/   # HTML templates
│   ├── static/encyclopedia/      # CSS
│   ├── util.py                   # entry list/save/get helpers (file-backed storage)
│   ├── views.py                  # request handlers (browse/view/search/create/edit/random)
│   └── urls.py                   # app routes
├── entries/                      # Markdown source-of-truth for wiki pages
├── wiki/                         # Django project config
│   ├── settings.py
│   └── urls.py
├── db.sqlite3
└── manage.py
```

## Architecture Notes (Implementation Details)

- **Entry storage**: The canonical content lives in `entries/<Title>.md`. The helper functions in `encyclopedia/util.py` list, read, and write entries.
- **Rendering**: `encyclopedia/views.py` uses the `markdown` package to convert Markdown to HTML for page display.
- **Templates**: Base layout is `encyclopedia/templates/encyclopedia/layout.html`, providing the sidebar navigation and search form.

## Local Setup

### Prerequisites

- Python 3.x
- pip

### Run locally

```bash
# from the project root (where manage.py lives)
python3 -m venv .venv
source .venv/bin/activate

pip install django markdown
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

## Routes (Quick Reference)

- `/` — list all pages
- `/wiki/<title>` — view entry
- `/search/?q=<query>` — search (exact/partial)
- `/create/` — create new page
- `/edit/<title>` — edit an existing page
- `/random/` — random entry

## What This Demonstrates

- **Django fundamentals**: URL routing, views, templates, static files, forms, redirects, error states.
- **Data modeling choices**: file-backed content store (Markdown as source of truth) with helper utilities.
- **Product thinking**: create/edit/search flows + “random page” for discovery.
- **Readable structure**: clear separation of concerns (routing vs view logic vs storage helpers vs templates).
