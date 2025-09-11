import requests
from dateutil import parser

def fetch_greenhouse(company_slug: str):
    """
    Fetch job postings from Greenhouse using their public JSON endpoint.
    Example: https://boards.greenhouse.io/<company>.json
    """
    url = f"https://boards.greenhouse.io/{company_slug}.json"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()

    jobs = []
    for jd in data.get("jobs", []):
        jobs.append({
            "id": f"gh-{jd.get('id')}",
            "company": (jd.get("company") or {}).get("name") or company_slug,
            "title": jd.get("title"),
            "location": (jd.get("location") or {}).get("name"),
            "source": "greenhouse",
            "url": jd.get("absolute_url"),
            "posted_at": parser.parse(jd.get("updated_at")).isoformat() if jd.get("updated_at") else None,
        })
    return jobs
