import os
from pathlib import Path
from typing import Any

import markdown

from flask import Blueprint, render_template

bp = Blueprint("blog", __name__, url_prefix="/blog")

POSTS_PATH = Path(__file__).resolve().parent.parent / "posts"


def get_all_posts_meta() -> list[dict[str, Any]]:
    files = sorted(
        filter(lambda x: x.endswith(".md"), os.listdir(POSTS_PATH)), reverse=True
    )
    posts: list[dict[str, Any]] = []
    for file in files:
        with open(POSTS_PATH / file) as f:
            md = markdown.Markdown(extensions=["meta"])
            _ = md.convert(f.read())
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


@bp.route("/post/<post_title>")
def post(post_title: str) -> str:
    with open(POSTS_PATH / (post_title + ".md")) as f:
        md = markdown.Markdown(extensions=["meta", "fenced_code", "codehilite"])
        html = md.convert(f.read())

        post_rendered: dict[str, Any] = {
            "title": md.Meta["title"][0],
            "date": md.Meta["date"][0],
            "content": html,
        }

    return render_template("blog/post.html", post=post_rendered)
