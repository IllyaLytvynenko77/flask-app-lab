from flask import Blueprint, redirect, session, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if "username" in session:
        return redirect(url_for("users.profile"))
    return redirect(url_for("users.login"))
