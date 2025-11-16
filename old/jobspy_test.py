import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "google"], # "glassdoor", "bayt", "naukri", "bdjobs"
    search_term="software engineer",
    results_wanted=10,
    hours_old=24,
    location="Zurich, Switzerland",
    country_indeed='Switzerland',

)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
