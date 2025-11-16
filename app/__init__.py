from flask import Flask
import os

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Register blueprints
    from app.routes import main, auth, jobs, favorites, profile, cv, applications

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(favorites.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(cv.bp)
    app.register_blueprint(applications.bp)
    return app
