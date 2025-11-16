import random
import secrets
import json
import os
import hashlib
jobs_file = os.path.join(os.path.dirname(__file__), 'jobs', 'jobs.json')
class Job:
    def __init__(self, title, company, location, description, url, category=None):
        self.id = random.randint(10000000, 99999999)
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.url = url
        self.category = category if category else "General"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'url': self.url,
            'category': self.category
        }
    def save_job(self):
        # load existing jobs safely, append this job, write back and return the saved dict
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
        with open(os.path.join(os.path.dirname(__file__), 'jobs', 'jobs.json'), 'r') as f:
            jobs = json.load(f)
            for job in jobs:
                if job['id'] == int(job_id):
                    return job
        return None
    
