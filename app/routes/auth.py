from flask import Blueprint, render_template, request, redirect, make_response, flash
import secrets
import hashlib
from app.models.user import User

bp = Blueprint('auth', __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #user objekt nach username, autofetcht passwort und token
        user = User(username)
        if user and user.password == hashlib.sha256(password.encode("utf-8")).hexdigest():
            token = user.token
            resp = make_response(redirect("/index"))
            resp.set_cookie("user_token", token)
            flash(f"Willkommen zurück, {username}!", "success")
            return resp
        else:
            flash("Ungültiger Benutzername oder Passwort", "error")
            return redirect("/login")
    return render_template("login.html", username=None)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username, password=password)
        user.create_user()
        resp = make_response(redirect("/index"))
        resp.set_cookie("user_token", user.token)
        flash(f"Konto erfolgreich erstellt! Willkommen, {username}!", "success")
        return resp
    return render_template("register.html", username=None)

@bp.route("/logout")
def logout():
    #falls keis login, login page
    resp = make_response(redirect("/login"))
    resp.delete_cookie("user_token")
    flash("Du wurdest erfolgreich abgemeldet", "success")
    return resp
