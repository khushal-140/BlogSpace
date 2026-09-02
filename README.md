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

## Run Locally

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) set environment variables
set SECRET_KEY=your-random-secret     # Windows
export SECRET_KEY=your-random-secret  # Linux / Mac

# 4. Start the app -- the database is created automatically
python run.py
```

Open http://127.0.0.1:5000 in your browser.
