from flask import Blueprint, render_template

from main.blog import get_all_posts_meta


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    posts = get_all_posts_meta()

    return render_template("main/index.html", posts=posts)


@bp.route("/up")
def up():
    return "healthy"
