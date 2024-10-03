from flask import Blueprint


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return "main index"


@bp.route("/up")
def up():
    return "healthy"
