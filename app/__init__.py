from flask import Flask
from markupsafe import Markup
import markdown
import os

def format_job_description(text):
    if not text:
        return ''
    return Markup(markdown.markdown(text))

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    app.jinja_env.filters['format_description'] = format_job_description

    # blueprints registriere
    from app.routes import main, auth, jobs, favorites, profile, cv, applications

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(favorites.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(cv.bp)
    app.register_blueprint(applications.bp)
    return app
