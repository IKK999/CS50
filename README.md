# Mail — Single‑Page Webmail (Django + Vanilla JS)

A lightweight webmail client built with **Django** and a **single-page, fetch-driven UI**. The backend exposes a clean JSON API for mailbox operations, while the frontend renders mailboxes, message detail, and compose/reply flows without full page reloads.

This project was built to demonstrate practical full-stack fundamentals: **auth**, **REST-ish APIs**, **database modeling**, and **client-side state/UI**.

---

## Highlights

- **End-to-end feature delivery**: authentication → inbox/sent/archive → compose/reply → read/archive state.
- **Separation of concerns**: Django serves HTML shell + JSON endpoints; JS owns SPA-style rendering and interactions.
- **Realistic domain modeling**: per-user mailbox state (`read`, `archived`) stored server-side and updated through `PUT`.
- **Clean, inspectable API**: small set of endpoints with predictable request/response shapes.

---

## Features

- **Authentication**
  - Register, login, logout
  - Session-based auth with Django’s auth system (`AUTH_USER_MODEL = 'mail.User'`)
- **Mailboxes**
  - Inbox, Sent, Archived
  - Reverse-chronological ordering
- **Email workflows**
  - Compose and send to one or multiple recipients
  - Open message detail view
  - Reply (prefilled recipients, subject, and quoted body)
- **State updates**
  - Mark as read when opened
  - Archive/unarchive with a single click

---

## Tech stack

- **Backend**: Django (project generated with **Django 3.0.2**)
- **Database**: SQLite (`db.sqlite3`)
- **Frontend**: Vanilla JavaScript (Fetch API) + server-rendered templates
- **Styling**: Bootstrap 4 (CDN) + small custom CSS

---

## Project structure

```text
mail/                              # repo root
  manage.py
  db.sqlite3
  project3/                         # Django project (settings/urls/wsgi)
  mail/                             # Django app (models/views/urls)
    templates/mail/                 # layout + pages
    static/mail/                    # inbox.js + styles.css
    migrations/
```

---

## How it works (architecture overview)

After login, users land on a single template (`mail/templates/mail/inbox.html`) that contains three main UI regions:

- `#emails-view` (mailbox list)
- `#email-content` (opened message)
- `#compose-view` (compose/reply form)

Client-side code (`mail/static/mail/inbox.js`) toggles these views and talks to the backend JSON API using `fetch()` to:

- list mailbox contents
- fetch message detail
- send new messages
- update message state (`read`, `archived`)

---

## API (JSON endpoints)

Routes are defined in `mail/urls.py`.

### Compose / send

- **POST** `/emails`
- **Body**:

```json
{ "recipients": "a@b.com, c@d.com", "subject": "Hello", "body": "..." }
```

- **Response**: `201` with `{"message": "Email sent successfully."}`  

### List mailbox

- **GET** `/emails/<mailbox>`
- `<mailbox>` is one of: `inbox`, `sent`, `archive`
- **Response**: array of serialized emails

### Email detail

- **GET** `/emails/<id>`
- **Response**: serialized email object (see below)

### Update email state

- **PUT** `/emails/<id>`
- **Body** (either field can be provided):

```json
{ "read": true, "archived": false }
```

- **Response**: `204 No Content`

---

## Data model (core idea)

The main model is `Email` (`mail/models.py`). Each stored row is tied to a **specific user mailbox** via:

- `user` (the mailbox owner)
- `sender`
- `recipients` (many-to-many)
- `read`, `archived`, `timestamp`

Serialized email shape:

```json
{
  "id": 1,
  "sender": "sender@example.com",
  "recipients": ["a@example.com", "b@example.com"],
  "subject": "Subject",
  "body": "Body",
  "timestamp": "Apr 13 2026, 01:23 PM",
  "read": false,
  "archived": false
}
```

Implementation detail: when sending, the backend creates a mailbox copy for each recipient **and** the sender so that mailbox state (`read`/`archived`) can be tracked per user.

---

## Run locally

### Prerequisites

- Python 3.x
- Django installed in your environment

Because this repo doesn’t include a `requirements.txt`, install Django manually (example):

```bash
python -m pip install django
```

### Start the app

From the repo root:

```bash
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` and create an account.

---

## Quick code tour

- **Backend**
  - `mail/views.py`: JSON API + auth views
  - `mail/models.py`: `Email` model + `serialize()`
  - `mail/urls.py`: route definitions
- **Frontend**
  - `mail/static/mail/inbox.js`: SPA behavior + API calls
  - `mail/templates/mail/inbox.html`: page shell for JS-driven UI

