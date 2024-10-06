import os
from pathlib import Path

import markdown

from flask import Blueprint, render_template

bp = Blueprint("blog", __name__, url_prefix="/blog")

POSTS_PATH = Path(__file__).resolve().parent.parent / "posts"


def get_all_posts_meta():
    files = sorted(
        filter(lambda x: x.endswith(".md"), os.listdir(POSTS_PATH)), reverse=True
    )
    posts = []
    for file in files:
        with open(POSTS_PATH / file) as f:
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
    posts = get_all_posts_meta()

    return render_template("blog/index.html", posts=posts)


@bp.route("/post/<post>")
def post(post):
    with open(POSTS_PATH / (post + ".md")) as f:
        md = markdown.Markdown(extensions=["meta", "fenced_code", "codehilite"])
        html = md.convert(f.read())

        post = {
            "title": md.Meta["title"][0],
            "date": md.Meta["date"][0],
            "content": html,
        }

    return render_template("blog/post.html", post=post)
