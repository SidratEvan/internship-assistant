import requests

def fetch_ashby(org_name: str):
    url = "https://jobs.ashbyhq.com/api/non-user-graphql"
    query = """
    query JobBoardWithTeams($name: String!) {
      jobBoardWithTeams(organizationHostedJobsPageName: $name) {
        jobPostings {
          id
          title
          locationName
          employmentType
          compensationTierSummary
        }
      }
    }
    """
    payload = {"query": query, "variables": {"name": org_name}}

    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return []   # fail gracefully

    postings = []
    if data and "data" in data:
        postings = (
            data.get("data", {})
            .get("jobBoardWithTeams", {})
            .get("jobPostings", [])
            or []
        )

    jobs = []
    for jd in postings:
        jobs.append({
            "id": f"ab-{jd.get('id')}",
            "company": org_name,
            "title": jd.get("title"),
            "location": jd.get("locationName"),
            "source": "ashby",
            "url": f"https://jobs.ashbyhq.com/{org_name}/job/{jd.get('id')}",
            "employmentType": jd.get("employmentType"),
            "compensation": jd.get("compensationTierSummary"),
        })
    return jobs
