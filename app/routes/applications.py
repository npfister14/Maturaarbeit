from flask import Blueprint, render_template, request, redirect, send_file, flash
from app.models.application import Application
from app.models.job import Job
from app.utils.helpers import is_logged_in
from app.services.ai_service import generate_cover_letter_service
import os
bp = Blueprint('applications', __name__)

# dashboard vo allne applications
@bp.route("/applications", methods=["GET"])
def dashboard():
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    # alli applications vom user hole
    applications = Application.get_by_user(username)

    # nach status trennen
    drafts = [app for app in applications if app.status == "draft"]
    submitted = [app for app in applications if app.status == "submitted"]

    return render_template("applications/dashboard.html",
                         drafts=drafts,
                         submitted=submitted,
                         username=username)

# neue application erstelle
@bp.route("/applications/create", methods=["POST"])
def create():
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    job_id = request.form.get("job_id")
    language = request.form.get("language", "de")

    if not job_id:
        flash("Kein Job ausgewählt", "error")
        return redirect("/search_job")

    # luege ob user scho applied het
    if Application.user_has_applied(username, str(job_id)):
        # redirect zu existierende application
        apps = Application.get_by_user(username)
        #ich weiss es gitt en besser weg das zmache aber er fallt mir grad nd i
        for app in apps:
            if str(app.job_id) == str(job_id):
                flash("Du hast dich bereits auf diesen Job beworben", "error")
                return redirect(f"/applications/{app.id}")

    # neue application erstelle
    application = Application(
        user_id=username,
        job_id=str(job_id),
        language=language,
        status="draft"
    )
    application.save()
    flash("Bewerbungsentwurf erfolgreich erstellt", "success")

    return redirect(f"/applications/{application.id}")

# einzelni application azeige
@bp.route("/applications/<application_id>", methods=["GET"])
def view(application_id):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    application = Application.get_by_id(application_id)
    if not application:
        return "Application not found", 404

    # check ob das application vom user isch
    if application.user_id != username:
        return "Not authorized", 403

    # job details hole
    job = Job.get_job_by_id(application.job_id)

    return render_template("applications/view.html",
                         application=application,
                         job=job,
                         username=username)

# application als submitted markiere
@bp.route("/applications/<application_id>/submit", methods=["POST"])
def submit(application_id):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    application = Application.get_by_id(application_id)
    if not application or application.user_id != username:
        flash("Bewerbung nicht gefunden", "error")
        return redirect("/applications")

    application.mark_submitted()
    flash("Bewerbung als gesendet markiert", "success")

    return redirect(f"/applications/{application_id}")

# application lösche
@bp.route("/applications/<application_id>/delete", methods=["POST"])
def delete(application_id):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    application = Application.get_by_id(application_id)
    if not application or application.user_id != username:
        flash("Bewerbung nicht gefunden", "error")
        return redirect("/applications")

    application.delete()
    flash("Bewerbung erfolgreich gelöscht", "success")

    return redirect("/applications")


#motivationsschriibe generiere
@bp.route("/applications/<application_id>/generate_cover_letter", methods=["POST"])
def generate_cover_letter(application_id):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    application = Application.get_by_id(application_id)
    #cross user applications verhindere
    if not application or application.user_id != username:
        flash("Bewerbung nicht gefunden", "error")
        return redirect("/applications")
    job = Job.get_job_by_id(application.job_id)
    if not job:
        flash("Job nicht gefunden", "error")
        return redirect("/applications")

    # generiere motivationsschriibe
    cover_letter_path = application.generate_cover_letter(job)
    application.cover_letter_path = cover_letter_path
    application.save()

    flash("Anschreiben erfolgreich generiert", "success")

    return redirect(f"/applications/{application_id}")

# motivationsschriibe PDF azeige
@bp.route("/applications/<application_id>/cover-letter", methods=["GET"])
def view_cover_letter(application_id):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    application = Application.get_by_id(application_id)
    if not application or application.user_id != username:
        return "Not authorized", 403

    if not application.cover_letter_path or not os.path.exists(application.cover_letter_path):
        return "Cover letter not found", 404

    return send_file(application.cover_letter_path, mimetype='application/pdf')

# motivationsschriibe downloade
@bp.route("/applications/<application_id>/cover-letter/download", methods=["GET"])
def download_cover_letter(application_id):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    application = Application.get_by_id(application_id)
    if not application or application.user_id != username:
        return "Not authorized", 403

    if not application.cover_letter_path or not os.path.exists(application.cover_letter_path):
        return "Cover letter not found", 404

    return send_file(application.cover_letter_path, as_attachment=True, download_name=f"cover_letter_{application.id}.pdf")

# motivationsschriibe regeneriere
@bp.route("/applications/<application_id>/regenerate_cover_letter", methods=["POST"])
def regenerate_cover_letter(application_id):
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    username = user.username

    application = Application.get_by_id(application_id)
    if not application or application.user_id != username:
        flash("Bewerbung nicht gefunden", "error")
        return redirect("/applications")

    job = Job.get_job_by_id(application.job_id)
    if not job:
        flash("Job nicht gefunden", "error")
        return redirect("/applications")

    # alte cover letter lösche
    if application.cover_letter_path and os.path.exists(application.cover_letter_path):
        try:
            os.remove(application.cover_letter_path)
        except Exception:
            pass

    # neue generiere
    cover_letter_path = application.generate_cover_letter(job)
    application.cover_letter_path = cover_letter_path
    application.save()

    flash("Anschreiben erfolgreich neu generiert", "success")

    return redirect(f"/applications/{application_id}")