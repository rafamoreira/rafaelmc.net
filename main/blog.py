import os
from datetime import datetime
from pathlib import Path
from typing import Any

import markdown
from feedgenerator import Rss201rev2Feed

from flask import Blueprint, Response, render_template

from main import SITE_URL

bp = Blueprint("blog", __name__, url_prefix="/blog")

POSTS_PATH = Path(__file__).resolve().parent.parent / "posts"


def get_all_posts_files() -> list[str]:
    files = sorted(
        filter(lambda x: x.endswith(".md"), os.listdir(POSTS_PATH)),
        reverse=True,
    )
    return files


def get_all_posts_meta() -> list[dict[str, Any]]:
    files = get_all_posts_files()
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


def get_post_content(filename: str) -> tuple[str, str, str]:
    with open(POSTS_PATH / filename, "r") as f:
        md = markdown.Markdown(
            extensions=["meta", "fenced_code", "codehilite"]
        )
        content = md.convert(f.read())
        return md.Meta["title"][0], md.Meta["date"][0], content


@bp.route("/")
def index():
    posts = get_all_posts_meta()

    return render_template("blog/index.html", posts=posts)


@bp.route("/post/<post_title>")
def post(post_title: str) -> str:
    with open(POSTS_PATH / (post_title + ".md")) as f:
        md = markdown.Markdown(
            extensions=["meta", "fenced_code", "codehilite"]
        )
        html = md.convert(f.read())

        post_rendered: dict[str, Any] = {
            "title": md.Meta["title"][0],
            "date": md.Meta["date"][0],
            "content": html,
        }

    return render_template("blog/post.html", post=post_rendered)


@bp.route("/feed")
def feed():
    feed = Rss201rev2Feed(
        title="rafaelmc.net",
        link=f"{SITE_URL}/blog",
        description="rafaelmc.net blog feed",
        language="en",
    )

    post_files = get_all_posts_files()

    for file in post_files:
        title, date, content = get_post_content(file)
        feed.add_item(
            title=title,
            link=f"{SITE_URL}/blog/post/{file[:-3]}",
            description=content,
            content=content,
            pubdate=datetime.strptime(
                date, "%Y-%m-%d"
            ),  # Adjust the date format if needed
        )

    return Response(feed.writeString("utf-8"), mimetype="application/rss+xml")
