import os
from pathlib import Path

import markdown

from flask import Blueprint, render_template

bp = Blueprint("blog", __name__, url_prefix="/blog")


def get_all_posts_meta():
    posts_path = Path(__file__).resolve().parent.parent / "posts"
    files = sorted(
        filter(lambda x: x.endswith(".md"), os.listdir(posts_path)), reverse=True
    )
    posts = []
    for file in files:
        with open(posts_path / file) as f:
            md = markdown.Markdown(extensions=["meta"])
            md.convert(f.read())
            posts.append(
                {
                    "title": md.Meta["title"][0],
                    "date": md.Meta["date"][0],
                    "url": "/blog/post/" + file[:-3],
                }
            )
    return posts


@bp.route("/")
def index():
    articles = [{"id": 1, "title": "a"}, {"id": 1, "title": "a"}]

    return render_template("blog/index.html", articles=articles)
