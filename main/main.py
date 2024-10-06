import os
from pathlib import Path

from flask import Blueprint, render_template


bp = Blueprint("main", __name__)

ARTICLES_PATH = Path(__file__).resolve().parent.parent / "articles"


@bp.route("/")
def index():
    markdown_files = [f for f in os.listdir(ARTICLES_PATH) if f.endswith(".md")]
    files = sorted(markdown_files, reverse=True)[:5]
    Markdown
    return render_template("main/index.html", articles=articles)


@bp.route("/up")
def up():
    return "healthy"
