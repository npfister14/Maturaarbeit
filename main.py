from flask import Flask, render_template, request, redirect, make_response, request as flask_request
import secrets
import json
import os
from user import User
import hashlib
app = Flask(__name__)
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users', 'users.json')
jobs_file = os.path.join(os.path.dirname(__file__), 'jobs', 'jobs.json')
#def save_user_token(username, token):
#    try:
#        with open(USERS_FILE, 'r') as f:
#            users = json.load(f)
#    except (FileNotFoundError, json.JSONDecodeError):
#        users = []
#    users = [u for u in users if u.get('username') != username]
#    users.append({'username': username.split('@')[0], 'token': token, 'email': username})
#    with open(USERS_FILE, 'w') as f:
#        json.dump(users, f)

def get_username_by_token(token):
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    except Exception:
        return None
    for user in users:
        if user.get('token') == token:
            return user.get('username')
    return None

@app.route("/index", methods=["GET", "POST"])
def index():
    token = flask_request.cookies.get("user_token")
    username = get_username_by_token(token)
    if username is None:
        return redirect("/login")
    jobs_file = os.path.join(os.path.dirname(__file__), 'jobs', 'jobs.json')
    if request.method == "POST":
        selected_category = request.form.get("category")
        #jobs vo json lade
        try:
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
            filtered_jobs = [job for job in jobs if job['category'] == selected_category]
            print("fetched jobs:", filtered_jobs)
            #seperates jobs html, TO_DO! CSS! JAVASCRIPT ZUM SELECTE!
            return render_template("jobs.html", jobs=filtered_jobs)
        except Exception:
            filtered_jobs = []
        return "error"

    if request.method == "GET":
        try:
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
            categories = sorted(set(job['category'] for job in jobs))
        except Exception:
            categories = []
        return render_template("index.html", username=username, categories=categories)

#ein spezifische job
@app.route("/job/<job_id>", methods=["GET"])
def job_detail(job_id):
    print("job called with id" + str(job_id))
    jobs_file = os.path.join(os.path.dirname(__file__), 'jobs', 'jobs.json')
    try:
        with open(jobs_file, 'r') as f:
            jobs = json.load(f)
            print(jobs)
        job = next((j for j in jobs if j['id'] == int(job_id)), None)
    except Exception:
        job = None
    print(job)
    return render_template("job_detail.html", job_id=job['id'], job=job)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #user objekt nach username, autofetcht passwort und token
        user = User(username)
        print(user.password, password)
        print(hashlib.sha256(password.encode("utf-8")).hexdigest())
        if user and user.password == hashlib.sha256(password.encode("utf-8")).hexdigest():
            token = user.token
            resp = make_response(redirect("/index"))
            resp.set_cookie("user_token", token)
            return resp
        else:
            return "Invalid username or password"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username, password=password)
        #token generiere und speichere, chönt au usem json gholt werde
        token = secrets.token_urlsafe(16)
        user.save_user()
        resp = make_response(redirect("/index"))
        resp.set_cookie("user_token", token)
        return resp
    return render_template("register.html")

@app.route("/logout")
def logout():
    #falls keis login, login page
    resp = make_response(redirect("/login"))
    resp.delete_cookie("user_token")
    return resp

#test funktion
@app.route("/whoami")
def whoami():
    token = flask_request.cookies.get("user_token")
    username = get_username_by_token(token)
    if username:
        return f"You are logged in as {username}"
    return "You are not logged in"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999, debug=True)

