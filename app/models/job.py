import random
import secrets
import json
import os
import hashlib
from datetime import datetime
import uuid

jobs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'jobs', 'jobs.json')

class Job:
    def __init__(self, title, company, location, description, url, category=None,
                 company_url=None, emails=None, job_type=None, is_remote=None,
                 date_posted=None, compensation=None, saved_at=None, search_term=None):
        self.id = str(uuid.uuid4()) #das isch ja mal so viel intelligenter als random ints
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.url = url
        self.category = category if category else "General"
        self.company_url = company_url
        self.emails = emails or []
        self.job_type = job_type
        self.is_remote = is_remote
        self.date_posted = date_posted
        self.compensation = compensation
        self.saved_at = saved_at if saved_at else datetime.now().isoformat()
        self.search_term = search_term

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'name': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'url': self.url,
            'category': self.category,
            'company_url': self.company_url,
            'emails': self.emails,
            'job_type': self.job_type,
            'is_remote': self.is_remote,
            'date_posted': self.date_posted,
            'compensation': self.compensation,
            'saved_at': self.saved_at,
            'search_term': self.search_term
        }

    @staticmethod
    def cleanup_old_jobs():
        #eifach eifach alti jobs lösche als luege ob sie no gitt
        try:
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
        except Exception:
            return

        now = datetime.now()
        valid_jobs = []

        for job in jobs:
            saved_at_str = job.get('saved_at')
            if not saved_at_str:
                continue

            try:
                saved_at = datetime.fromisoformat(saved_at_str)
                age_hours = (now - saved_at).total_seconds() / 3600
                if age_hours < 24:
                    valid_jobs.append(job)
            except:
                continue

        try:
            with open(jobs_file, 'w') as f:
                json.dump(valid_jobs, f, indent=2)
        except Exception as e:
            print("Failed to cleanup jobs:", e)
    def save_job(self):
        # neue Job i d """"""Datebank""""""" speichere
        try:
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
        except Exception:
            jobs = []

        job_dict = self.to_dict()
        print("Saving job:", job_dict)
        jobs.append(job_dict)
        try:
            with open(jobs_file, 'w') as f:
                json.dump(jobs, f, indent=2)
        except Exception as e:
            print("Failed to write jobs file:", e)

        return job_dict

    @staticmethod
    def get_job_by_id(job_id):
        with open(os.path.join(os.path.dirname(__file__), '..', '..', 'jobs', 'jobs.json'), 'r') as f:
            jobs = json.load(f)
            for job_dict in jobs:
                if str(job_dict['id']) == str(job_id):
                    job = Job(
                        title=job_dict['title'],
                        company=job_dict['company'],
                        location=job_dict['location'],
                        description=job_dict['description'],
                        url=job_dict['url'],
                        category=job_dict.get('category'),
                        company_url=job_dict.get('company_url'),
                        emails=job_dict.get('emails'),
                        job_type=job_dict.get('job_type'),
                        is_remote=job_dict.get('is_remote'),
                        date_posted=job_dict.get('date_posted'),
                        compensation=job_dict.get('compensation'),
                        saved_at=job_dict.get('saved_at')
                    )
                    job.id = job_dict['id']  # preserve original id
                    return job
        return None
