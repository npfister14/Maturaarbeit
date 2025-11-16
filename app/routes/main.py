from flask import Blueprint, render_template, request, redirect
import json
import os
from app.utils.helpers import is_logged_in
from app.models.application import Application

bp = Blueprint('main', __name__)

jobs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'jobs', 'jobs.json')

@bp.route("/")
@bp.route("/index", methods=["GET"])
def index():
    user = is_logged_in(request)
    username = user.username if user else None

    # Get application stats for logged-in users
    application_stats = None
    if user:
        try:
            applications = Application.get_by_user(username)
            drafts = [app for app in applications if app.status == "draft"]
            submitted = [app for app in applications if app.status == "submitted"]

            # Get favorites count
            favorites_count = len(user.favorites) if user.favorites else 0

            application_stats = {
                'total': len(applications),
                'drafts': len(drafts),
                'submitted': len(submitted),
                'favorites': favorites_count
            }
        except Exception as e:
            print(f"Error getting application stats: {e}")

    return render_template("index.html",
                         username=username,
                         application_stats=application_stats)
