from flask import Blueprint, render_template

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/")
def index():
    articles = [{"id": 1, "title": "a"}, {"id": 1, "title": "a"}]

    return render_template("blog/index.html", articles=articles)
