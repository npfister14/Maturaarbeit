from flask import Blueprint, render_template, request, redirect
from app.models.user import User
from app.utils.helpers import is_logged_in

bp = Blueprint('profile', __name__)

@bp.route("/user")
def redirect_user():
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    if user.username:
        return redirect(f"/user/{user.username}")
    return redirect("/login")

@bp.route("/user/<username>")
def user_profile(username):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    return render_template("user.html", user=user, username=user.username if user else None)

@bp.route("/user/<username>/settings")
def settings(username):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    return render_template("settings.html", user=user, username=user.username if user else None)

#test funktion
@bp.route("/whoami")
def whoami():
    user = is_logged_in(request)
    if user:
        return f"You are logged in as {user.username}"
    return "You are not logged in"
