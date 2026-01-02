from flask import Blueprint, render_template, request, flash
import json
import os
import math
from app.models.job import Job
from jobspy import scrape_jobs
from app.utils.helpers import is_logged_in
bp = Blueprint('jobs', __name__)

# datei pfäd
jobs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'jobs', 'jobs.json')
default_job_sites = ["indeed", "linkedin", "google"]

def clean_value(value):
    #bereinige will jobspy öppis komisches zruckgitt
    if value is None:
        return None
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
    if isinstance(value, str) and value.lower() in ['nan', 'none', 'null']:
        return None
    # datetime objects au iso format string konvertiere fürs json
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    return value

#ein spezifische job
@bp.route("/job/<job_id>", methods=["GET"])
def job_detail(job_id):
    print("job called with id" + str(job_id))
    try:
        with open(jobs_file, 'r') as f:
            jobs = json.load(f)
            print(jobs)
        job = next((j for j in jobs if str(j['id']) == str(job_id)), None)
    except Exception:
        job = None
    print(job)

    # luege ob user iigloggt isch und ob er scho applied het
    from app.models.application import Application
    user = is_logged_in(request)
    username = user.username if user else None
    has_applied = False
    existing_app_id = None

    if username and job:
        has_applied = Application.user_has_applied(username, str(job_id))
        if has_applied:
            apps = Application.get_by_user(username)
            for app in apps:
                if str(app.job_id) == str(job_id):
                    existing_app_id = app.id
                    break

    return render_template("job_detail.html",
                         job_id=job['id'],
                         job=job,
                         username=username,
                         has_applied=has_applied,
                         existing_app_id=existing_app_id)

#search siite
@bp.route("/search_job", methods=["GET","POST"])
def search():
    user = is_logged_in(request)
    username = user.username if user else None

    if request.method == "GET":
        return render_template("search.html", username=username)
    else:
        #job scrape logik
        search_term = request.form.get("search_term")
        location = request.form.get("location") or "Zurich, Switzerland"

        # liechtestei ersetze wills konflit mit linkedin git
        if 'liechtenstein' in location.lower():
            location = "Zurich, Switzerland"
            print("Replaced Liechtenstein with Zurich, Switzerland (LinkedIn doesn't support Liechtenstein)")

        site_names = default_job_sites

        print(f"DEBUG: Scraping with location='{location}', sites={site_names}")
        try:
            jobs = scrape_jobs(search_term=search_term, location=location, site_name=site_names, results_wanted=10, hours_old=72, linkedin_fetch_description=True)
        except Exception as e:
            print(f"DEBUG: Scraping failed with error: {type(e).__name__}: {e}")
            if 'liechtenstein' in str(e).lower():
                print(f"LinkedIn Liechtenstein error detected, retrying without LinkedIn")
                site_names = ["indeed", "google"]
                jobs = scrape_jobs(search_term=search_term, location=location, site_name=site_names, results_wanted=10, hours_old=72)
            else:
                raise
        # weird ass dateformat, so funktionierts aber meistens
        try:
            jobs_list = jobs.to_dict(orient='records')
        except Exception:
            jobs_list = jobs if isinstance(jobs, list) else []

        for i in jobs_list:
            try:

                location = clean_value(i.get('location')) or clean_value(i.get('place')) or clean_value(i.get('zip')) or 'No Location'

                print("Scraped entry:", i)

                emails = i.get('emails') or []
                if isinstance(emails, list):
                    emails = [clean_value(e) for e in emails if clean_value(e)]
                else:
                    emails = []
                
                #wemmers so umständlich macht gitts (fast) nie en error
                job = Job(
                    title=clean_value(i.get('title')) or clean_value(i.get('name')) or clean_value(i.get('job_title')) or 'No Title',
                    company=clean_value(i.get('company')) or clean_value(i.get('employer')) or 'No Company',
                    location=location,
                    description=clean_value(i.get('description')) or clean_value(i.get('summary')) or '',
                    url=clean_value(i.get('job_url')) or clean_value(i.get('url')) or clean_value(i.get('link')) or '',
                    category=clean_value(i.get('job_function')) or clean_value(i.get('category')) or 'General',
                    company_url=clean_value(i.get('company_url')),
                    emails=emails,
                    job_type=clean_value(i.get('job_type')),
                    is_remote=clean_value(i.get('is_remote')),
                    date_posted=clean_value(i.get('date_posted')),
                    compensation=clean_value(i.get('compensation')),
                    search_term=search_term
                )
                job.save_job()
                #leider nur fast
            except Exception as e:
                print(f"Error saving job: {e}, skipping this entry")
                continue

        Job.cleanup_old_jobs()

        try:
            with open(jobs_file, 'r') as f:
                all_jobs = json.load(f)
        except Exception:
            all_jobs = []

        # nur jobs vo dem search term zeige
        filtered_jobs = [j for j in all_jobs if j.get('search_term') == search_term]

        if filtered_jobs:
            flash(f"{len(filtered_jobs)} Jobs für '{search_term}' gefunden", "success")
        else:
            flash(f"Keine Jobs für '{search_term}' gefunden. Versuche einen anderen Suchbegriff.", "error")

        return render_template("jobs.html", jobs=filtered_jobs, username=username)
