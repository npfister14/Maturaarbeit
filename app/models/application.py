import uuid
import json
import os
from datetime import datetime
from app.models.user import User
from app.services.ai_service import generate_cover_letter_service


applications_file = os.path.join(os.path.dirname(__file__), '..', '..', 'applications', 'applications.json')


class Application:
    def __init__(self, user_id, job_id, language="de", status="draft",
                 created_date=None, submitted_date=None, cover_letter_path=None,
                 email_draft=None, notes="", application_id=None):
        self.id = application_id if application_id else str(uuid.uuid4())
        self.user_id = user_id
        self.job_id = job_id
        self.status = status  # "draft" oder "submitted"
        self.created_date = created_date if created_date else datetime.now().isoformat()
        self.submitted_date = submitted_date
        self.language = language
        self.cover_letter_path = cover_letter_path
        self.email_draft = email_draft
        self.notes = notes

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'status': self.status,
            'created_date': self.created_date,
            'submitted_date': self.submitted_date,
            'language': self.language,
            'cover_letter_path': self.cover_letter_path,
            'email_draft': self.email_draft,
            'notes': self.notes
        }

    def save(self):
        # application i applications.json speichere
        try:
            with open(applications_file, 'r') as f:
                applications = json.load(f)
        except:
            applications = []

        # luege ob application scho existiert und update oder hinzuefüege
        app_dict = self.to_dict()
        found = False
        for i, app in enumerate(applications):
            if app['id'] == self.id:
                applications[i] = app_dict
                found = True
                break

        if not found:
            applications.append(app_dict)

        try:
            with open(applications_file, 'w') as f:
                json.dump(applications, f, indent=2)
        except Exception as e:
            print(f"Failed to save application: {e}")

        return app_dict

    def delete(self):
        # application lösche
        try:
            with open(applications_file, 'r') as f:
                applications = json.load(f)
        except Exception:
            return False

        applications = [app for app in applications if app['id'] != self.id]

        try:
            with open(applications_file, 'w') as f:
                json.dump(applications, f, indent=2)
        except Exception:
            return False

        # cover letter file lösche wenn existiert
        if self.cover_letter_path and os.path.exists(self.cover_letter_path):
            try:
                os.remove(self.cover_letter_path)
            except Exception:
                pass

        return True

    def mark_submitted(self):
        self.status = "submitted"
        self.submitted_date = datetime.now().isoformat()
        self.save()

    def generate_cover_letter(self, job):
        # motivationsschriibe generiere
        user = User(self.user_id)
        if not user.cv:
            print("No CV found for user")
            return None

        cover_letter_path = generate_cover_letter_service(user.cv, job)
        return cover_letter_path

    @staticmethod
    def get_by_id(application_id):
        try:
            with open(applications_file, 'r') as f:
                applications = json.load(f)
                for app in applications:
                    if app['id'] == application_id:
                        return Application(
                            application_id=app['id'],
                            user_id=app['user_id'],
                            job_id=app['job_id'],
                            status=app.get('status', 'draft'),
                            created_date=app.get('created_date'),
                            submitted_date=app.get('submitted_date'),
                            language=app.get('language', 'de'),
                            cover_letter_path=app.get('cover_letter_path'),
                            email_draft=app.get('email_draft'),
                            notes=app.get('notes', '')
                        )
        except Exception:
            return None
        return None

    @staticmethod
    def get_by_user(username):
        # alli applications vo eim user hole
        try:
            with open(applications_file, 'r') as f:
                applications = json.load(f)
                user_apps = []
                for app in applications:
                    if app['user_id'] == username:
                        user_apps.append(Application(
                            application_id=app['id'],
                            user_id=app['user_id'],
                            job_id=app['job_id'],
                            status=app.get('status', 'draft'),
                            created_date=app.get('created_date'),
                            submitted_date=app.get('submitted_date'),
                            language=app.get('language', 'de'),
                            cover_letter_path=app.get('cover_letter_path'),
                            email_draft=app.get('email_draft'),
                            notes=app.get('notes', '')
                        ))
                return user_apps
        except Exception:
            return []

    @staticmethod
    def user_has_applied(username, job_id):
        # luege ob user scho applied het
        try:
            with open(applications_file, 'r') as f:
                applications = json.load(f)
                for app in applications:
                    if app['user_id'] == username and app['job_id'] == job_id:
                        return True
        except Exception:
            return False
        return False
