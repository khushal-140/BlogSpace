"""
Standalone script to create an admin account for BlogSpace.

The password is hashed with bcrypt before saving -- the plain text
password is never stored in the database.

Usage:
    python create_admin.py --username admin --email you@example.com --password yourpassword
"""
import argparse

from flaskblog import create_app, db, bcrypt
from flaskblog.models import User


def create_admin(username, email, password):
    app = create_app()
    with app.app_context():
        # Make sure no user with the same username or email already exists
        existing = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing:
            print('A user with that username or email already exists!')
            return

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = User(username=username, email=email,
                     password=hashed_password, is_admin=True)
        db.session.add(admin)
        db.session.commit()

        print('Admin account created successfully!')
        print(f'  username: {username}')
        print(f'  email:    {email}')
        print(f'  is_admin: {admin.is_admin}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create an admin account for BlogSpace')
    parser.add_argument('--username', required=True, help='Admin username')
    parser.add_argument('--email', required=True, help='Admin email address')
    parser.add_argument('--password', required=True, help='Password (will be hashed before saving)')
    args = parser.parse_args()

    create_admin(args.username, args.email, args.password)
