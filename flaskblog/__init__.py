import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail  import Mail
from flaskblog.config import Config
from flask_migrate import Migrate




db=SQLAlchemy() # This initializes the SQLAlchemy object with the Flask application, allowing us to interact with the database using SQLAlchemy's ORM (Object-Relational Mapping) features.
bcrypt = Bcrypt()
login_manager = LoginManager() # This initializes the LoginManager object with the Flask application, which is used to manage user authentication and session management in the application.
login_manager.login_view = 'users.login' # This sets the login view for the LoginManager. It specifies that if a user tries to access a protected route without being authenticated, they will be redirected to the 'login' view (which is defined in the routes.py file).
login_manager.login_message_category = 'info' # This sets the category for the flash message that
migrate = Migrate()

mail=Mail()

#from flaskblog import routes # This imports the routes module from the flaskblog package, which contains the route definitions for the application. This is done at the end to avoid circular imports, as the routes module will need to import the app object defined in this __init__.py file.




def _create_initial_admin():
    """Create the first admin account from environment variables.

    Used on deployment (e.g. Render): set ADMIN_USERNAME, ADMIN_EMAIL and
    ADMIN_PASSWORD in the environment and the account is created automatically
    on startup if it doesn't exist yet. If any variable is missing, this
    silently does nothing.
    """
    from flaskblog.models import User

    username = os.environ.get('ADMIN_USERNAME')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASSWORD')

    if not (username and email and password):
        return

    existing = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing:
        return

    admin = User(username=username, email=email,
                 password=bcrypt.generate_password_hash(password).decode('utf-8'),
                 is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print(f'[BlogSpace] Created initial admin account: {username} <{email}>')


def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    from flaskblog.admin import admin

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all() # creates the database tables automatically if they don't exist yet (fresh/empty database)
        _create_initial_admin()
        # Auto-seed demo content on an empty database, so a fresh deployment
        # (e.g. Render) immediately shows a lively blog. Set SEED_DEMO_DATA=0
        # to disable this behaviour.
        if os.environ.get('SEED_DEMO_DATA', '1') == '1':
            from flaskblog.seed_data import populate_demo_data
            populate_demo_data()

    return app