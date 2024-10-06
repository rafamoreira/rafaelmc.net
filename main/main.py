import os
from pathlib import Path

import markdown

from flask import Blueprint, render_template


bp = Blueprint("main", __name__)

ARTICLES_PATH = Path(__file__).resolve().parent.parent / "articles"


@bp.route("/")
def index():
    files = sorted(
        filter(lambda x: x.endswith(".md"), os.listdir(ARTICLES_PATH)), reverse=True
    )
    meta = []
    for file in files:
        with open(ARTICLES_PATH / file) as f:
            md = markdown.Markdown(extensions=["meta"])
            md.convert(f.read())
            meta.append(
                {
                    "title": md.Meta["title"][0],
                    "date": md.Meta["date"][0],
                    "url": "/blog/post/" + file,
                }
            )

    return render_template("main/index.html", posts=meta)


@bp.route("/up")
def up():
    return "healthy"
