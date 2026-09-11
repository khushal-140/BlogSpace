
from flask import render_template, request, Blueprint
from sqlalchemy import func
from flaskblog import db
from flaskblog.models import Post, User

main= Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page=request.args.get('page',1,type=int) # retrieves the "page" parameter from the query string (defaults to 1) for pagination
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=6, error_out=True) # newest posts first, 6 per page

    # Sections that make the home page feel alive (rendered on the first page only)
    featured=Post.query.filter_by(is_featured=True).order_by(Post.date_posted.desc()).limit(3).all()
    popular_authors=(
        db.session.query(User, func.count(Post.id).label('post_count'))
        .join(Post)
        .group_by(User.id)
        .order_by(func.count(Post.id).desc(), func.max(Post.date_posted).desc())
        .limit(4)
        .all()
    ) # authors with the most published posts, newest activity first
    total_posts=Post.query.count()
    total_users=User.query.count()
    total_categories=db.session.query(func.count(func.distinct(Post.category))).scalar()

    return render_template('home.html',posts=posts,featured=featured,
                           popular_authors=popular_authors,
                           total_posts=total_posts,total_users=total_users,
                           total_categories=total_categories)

@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/contact')
def contact():
    return "<h1> contact us</h1>"
