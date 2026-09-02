from functools import wraps

from flask import render_template, abort
from flask_login import login_required, current_user

from flaskblog.admin import admin
from flaskblog.models import User, Post


def admin_required(view_func):
    """Decorator that allows access only to logged-in administrators.

    Non-logged-in visitors are redirected to the login page;
    logged-in non-admins get a 403 error page.
    """
    @wraps(view_func)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view_func(*args, **kwargs)
    return wrapper


@admin.route('/admin')
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.count(),
        'total_admins': User.query.filter_by(is_admin=True).count(),
    }
    users = User.query.order_by(User.id).all()

    return render_template('admin/dashboard.html', title='Admin Dashboard',
                           stats=stats, users=users)
