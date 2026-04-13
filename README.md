# Commerce (Django Auctions)

An eBay-style commerce web app built with **Django**: users can register/login, create auction listings, place bids, leave comments, maintain a watchlist, browse by category, and close auctions with an automatic winner state.

This project is a strong “full-stack fundamentals” portfolio piece: **relational modeling**, **server-rendered UI**, **authentication**, **CRUD + business rules**, and a clean Django app structure.

## Highlights (what an employer cares about)

- **End-to-end product flow**: listings → bidding → closing auctions → winner messaging.
- **Relational data modeling**: custom `User` model + `Listing`, `Bid`, `Comment` with many-to-many relationships.
- **Business rule enforcement**:
  - bids must be **strictly greater** than the current highest bid
  - listing owners can **close** their own auctions
  - authenticated-only actions (bid, comment, watchlist, create listing)
- **Server-rendered UI**: Django templates + Bootstrap for quick, consistent layout.
- **Admin support**: all models registered in Django Admin.

## Feature tour

- **Authentication**
  - Register, log in, log out
- **Listings**
  - View **Active Listings**
  - Create a listing (title, description, starting bid, optional image URL, optional category)
  - View a listing detail page (image, description, current price, bid count, category, owner)
- **Bidding**
  - Submit bids with validation against the current highest bid
  - Display bid leader (including “you are the current bidder”)
- **Watchlist**
  - Add/remove any listing to a personal watchlist
  - Watchlist count displayed in the navbar
- **Comments**
  - Comment on listings (minimum length validation)
  - Display comment thread under each listing
- **Categories**
  - Browse distinct categories
  - Filter listings by category
- **Closing auctions**
  - Listing owners can close an auction
  - Listing page shows win/lose messaging after closure

## Tech stack

- **Backend**: Python + Django (project structure generated from Django startproject)
- **Frontend**: Django Templates, Bootstrap 4, minimal custom CSS
- **Database**: SQLite (local development)

## Architecture overview

### Project structure

```
.
├── manage.py
├── db.sqlite3
├── commerce/                 # Django project config
│   ├── settings.py
│   └── urls.py
└── auctions/                 # Main app
    ├── models.py             # User, Listing, Bid, Comment
    ├── views.py              # Page + action views (bids, comments, watchlist, close)
    ├── urls.py               # App routes
    ├── templates/auctions/   # layout + pages
    └── static/auctions/      # CSS
```

### Data model (high level)

- **`User`** (custom auth model)
  - `owned`: listings the user created
  - `watchlisted`: listings the user is watching
  - `bidden`: bids the user has placed
  - `commented`: comments the user has made
- **`Listing`**
  - title, description, starting bid, optional image URL, optional category
  - `bids` and `comments` (many-to-many)
  - `is_active` boolean to represent open/closed auctions
  - helper methods: highest bid, bid count, bid leader, owner, comment list
- **`Bid`**: decimal amount
- **`Comment`**: text content

## Routes (app)

The `auctions` app exposes the following endpoints:

- `/` active listings
- `/register`, `/login`, `/logout`
- `/create` create listing
- `/listing/<id>` listing detail
- `/submit_bid/<id>` place bid (POST)
- `/submit_comment/<id>` add comment (POST)
- `/change_watchlist/<id>` toggle watchlist
- `/close_auction/<id>` close listing
- `/watchlist` watchlisted items
- `/categories`, `/category/<name>` category browsing

## Getting started (local)

### Prerequisites

- Python 3.x
- pip

### Setup

Create and activate a virtual environment, then install Django:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install django
```

### Run migrations

If you want a fresh database:

```bash
python manage.py migrate
```

This repo also includes a `db.sqlite3` file. If you keep it, you can try running the server immediately. (If it’s out of sync with your Django version, prefer the fresh-migration path above.)

### Start the dev server

```bash
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

### (Optional) Create an admin user

```bash
python manage.py createsuperuser
```

Admin lives at `/admin/`.
