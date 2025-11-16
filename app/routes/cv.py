from flask import Blueprint, render_template, request, redirect, send_file, flash
import os
from werkzeug.utils import secure_filename
from app.models.user import User
from app.utils.helpers import is_logged_in

bp = Blueprint('cv', __name__)

# confjgi
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', 'cvs')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1 giga?


def allowed_file(filename):
    # döff mer so
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/cv", methods=["GET", "POST"])
def cv_upload():
    # cv ufelade
    user = is_logged_in(request)
    if not user:
        return redirect("/login")

    if request.method == "POST":
        # luegt obs au es file het, isch chli buggy
        if 'cv_file' not in request.files:
            flash("No file selected", "error")
            return redirect("/cv")

        file = request.files['cv_file']

        # same eif wege leere files
        if file.filename == '':
            flash("No file selected", "error")
            return redirect("/cv")

        # file selber und name prüefe
        if file and allowed_file(file.filename):
            #filename putze
            filename = secure_filename(file.filename)

            # mer sött ja eig au nur ei datei pro user ha
            file_extension = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{user.username}_cv.{file_extension}"

            # Save file
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

            try:
                file.save(filepath)
                user.upload_cv(filepath)
                print(f"CV saved for {user.username} at {filepath}")
                flash("CV uploaded successfully!", "success")
                return redirect("/cv/view")
            except Exception as e:
                print(f"Error saving file: {e}")
                flash("Error uploading file. Please try again.", "error")
                return redirect("/cv")
        else:
            flash("Invalid file type. Please upload PDF, DOC, or DOCX.", "error")
            return redirect("/cv")

    return render_template("cv.html", user=user, username=user.username if user else None)

@bp.route("/cv/view")
def cv_view():
    # cv azeige
    user = is_logged_in(request)
    if not user:
        return redirect("/login")
    return render_template("cv_view.html", user=user, username=user.username if user else None)

@bp.route("/cv/download")
def cv_download():
    # cv herunterlade
    user = is_logged_in(request)
    if not user:
        return redirect("/login")

    # zruggschicke
    for ext in ALLOWED_EXTENSIONS:
        filename = f"{user.username}_cv.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=f"{user.username}_CV.{ext}")

    flash("CV not found", "error")
    return redirect("/cv")

@bp.route("/cv/delete")
def cv_delete():
    # cv löschen
    user = is_logged_in(request)
    if not user:
        return redirect("/login")

    # nahluege und lösche
    deleted = False
    for ext in ALLOWED_EXTENSIONS:
        filename = f"{user.username}_cv.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                user.cv = None
                deleted = True
                break
            except Exception as e:
                print(f"Error deleting file: {e}")
                flash("Error deleting CV. Please try again.", "error")
                return redirect("/cv")

    if deleted:
        user.cv = None
        user.save_user()
        flash("CV deleted successfully", "success")
        return redirect("/cv")
    else:
        flash("No CV found to delete", "error")
        return redirect("/cv")
