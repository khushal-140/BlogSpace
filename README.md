# BlogSpace

A full-stack blogging web application built with Python Flask.

## Features

- User registration and login (session-based auth with Flask-Login)
- Create, update, and delete blog posts (paginated)
- User profiles with picture upload (Pillow)
- Secure password hashing (Flask-Bcrypt)
- Password reset via email tokens (Flask-Mail)
- Custom 403/404/500 error pages

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python Flask 3 |
| Database | SQLite via Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Forms | Flask-WTF (CSRF protected) |
| Auth | Flask-Login + Flask-Bcrypt |
| Email | Flask-Mail |
| Deployment | Render |

## Project Structure

```
BlogSpace/
├── run.py                  # Entry point
├── requirements.txt
└── flaskblog/              # Application package
    ├── __init__.py         # App factory + extensions
    ├── config.py           # Configuration (env vars)
    ├── models.py           # User & Post models
    ├── main/               # Home & about pages
    ├── posts/              # Blog post CRUD
    ├── users/              # Register / login / account
    └── errors/             # Error handlers
```

## Environment Variables

All configuration is read from environment variables (see `flaskblog/config.py`). Local development works with defaults; in production always set these.

| Variable | Purpose | Default |
|----------|---------|---------|
| `SECRET_KEY` | Session/CSRF signing key | dev fallback (**set in production!**) |
| `DATABASE_URL` | Database connection | `sqlite:///site.db` |
| `FLASK_DEBUG` | `1` = debugger + auto-reload (development only) | `0` |
| `ADMIN_USERNAME` | First admin account, auto-created on startup | — |
| `ADMIN_EMAIL` | Email of the first admin | — |
| `ADMIN_PASSWORD` | Password of the first admin | — |
| `MAIL_SERVER` / `MAIL_PORT` / `MAIL_USERNAME` / `MAIL_PASSWORD` | SMTP settings for password-reset emails | Gmail defaults |

The admin account is created automatically on startup when all three `ADMIN_*` variables are set and no user with that username/email exists. You can also create admins manually with `python create_admin.py`.

## Deploy on Render

1. Push the repository to GitHub (Render watches the repo).
2. Create a **Python Web Service** connected to this repo:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn run:app`
3. Add the environment variables: `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` (and optionally the `MAIL_*` ones).
4. Deploy. On startup the app creates its database and the first admin account automatically.

> Note: on the free plan Render's disk is temporary — the SQLite database resets on every deploy/restart. The admin account is re-created from the env vars on each start, so you can always log in.

## Run Locally

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) enable the debugger / auto-reload
set FLASK_DEBUG=1            # Windows
export FLASK_DEBUG=1         # Linux / Mac

# 4. Start the app -- the database is created automatically
python run.py
```

Open http://127.0.0.1:5000 in your browser.
