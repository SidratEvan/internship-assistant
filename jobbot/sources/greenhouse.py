import requests
from bs4 import BeautifulSoup
import json

def fetch_greenhouse(company_slug: str):
    url = f"https://boards.greenhouse.io/{company_slug}"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    jobs = []

    for script in scripts:
        try:
            if not script.string:
                continue
            data = json.loads(script.string)
            postings = data if isinstance(data, list) else [data]
            for jd in postings:
                if jd.get("@type") == "JobPosting":
                    jobs.append({
                        "id": f"gh-{jd.get('identifier', {}).get('value')}",
                        "company": company_slug,
                        "title": jd.get("title"),
                        "location": (
                            jd.get("jobLocation", [{}])[0]
                              .get("address", {})
                              .get("addressLocality")
                        ),
                        "source": "greenhouse",
                        "url": jd.get("hiringOrganization", {}).get("sameAs") or url,
                        "posted_at": jd.get("datePosted"),
                    })
        except Exception:
            continue

    return jobs

