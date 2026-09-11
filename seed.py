"""
Seed the BlogSpace database with demo users and posts.

Usage:
    python seed.py            # seeds only if the database has no posts yet
    python seed.py --fresh    # deletes ALL users and posts first, then seeds

Run from the project root. The demo content lives in flaskblog/seed_data.py.
Every demo user's password is 'demo1234'; the admin keeps 'khushal143'.
"""
import argparse

from flaskblog import create_app, db
from flaskblog.models import Post, User
from flaskblog.seed_data import populate_demo_data


def main(fresh: bool):
    app = create_app()
    with app.app_context():
        if fresh:
            deleted_posts = Post.query.delete()
            deleted_users = User.query.delete()
            db.session.commit()
            print(f'Removed {deleted_posts} posts and {deleted_users} users')

        if populate_demo_data():
            print('Database seeded successfully!')
        else:
            print('Database already contains posts -- nothing to do. '
                  'Use --fresh to reset and reseed.')

        users = User.query.count()
        posts = Post.query.count()
        print(f'Totals: {users} users, {posts} posts')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed BlogSpace with demo data')
    parser.add_argument('--fresh', action='store_true',
                        help='delete all existing users and posts before seeding')
    main(parser.parse_args().fresh)
