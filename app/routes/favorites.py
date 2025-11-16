from flask import Blueprint, render_template, request, redirect, flash
import json
import os
from app.models.user import User
from app.utils.helpers import is_logged_in

bp = Blueprint('favorites', __name__)

jobs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'jobs', 'jobs.json')

@bp.route("/jobs/favorites", methods=["GET","POST"])
def favorites():
    user = is_logged_in(request)
    if not user:
        return redirect("/login")

    if request.method == "POST":
        job_id = request.form.get("job_id")
        try:
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
            job = next((j for j in jobs if str(j['id']) == str(job_id)), None)
        except Exception:
            job = None
        if job:
            user.favorite(job["id"])
            flash("Job added to favorites", "success")
            return redirect("/jobs/favorites")
        else:
            flash("Job not found", "error")
            return redirect("/jobs/favorites")

    # favorite azzeige
    try:
        with open(jobs_file, 'r') as f:
            all_jobs = json.load(f)
    except Exception:
        all_jobs = []

    # nume die wo au favorited sind, !WIP! jobs wos n¨me git us em user file lésche
    favorites = [job for job in all_jobs if job.get('id') in (user.favorites or [])]

    return render_template("favorites.html", favorites=favorites, username=user.username)

@bp.route("/jobs/favorites/remove", methods=["POST"])
def remove_favorite():
    user = is_logged_in(request)
    if not user:
        return redirect("/login")

    job_id = request.form.get("job_id")
    if job_id:
        try:
            user.unfavorite(str(job_id))
            flash("Job removed from favorites", "success")
        except Exception as e:
            print(f"Error removing favorite: {e}")
            flash("Error removing job from favorites", "error")

    return redirect("/jobs/favorites")
