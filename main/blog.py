from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/")
def index():
    articles = [{"id": 1, "title": "a"}, {"id": 1, "title": "a"}]
    return render_template("blog/index.html", articles=articles)
