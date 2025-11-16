import asyncio, csv
from urllib.parse import urlencode, urljoin
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from urllib.parse import urlencode
SEARCH_BASE = "https://www.linkedin.com/jobs/search/"


def build_url(query="verkäufer", location="Zuerich", date_posted="r604800"):
    params = {
        "f_TPR": date_posted,
        "keywords": query,
        "location": location,
    }
    built_url = f"{SEARCH_BASE}?{urlencode(params)}"
    print(built_url)
    return built_url


build_url()
