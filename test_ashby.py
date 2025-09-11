from jobbot.sources.ashby import fetch_ashby
from jobbot.utils import upsert_tracker, now_iso
from jobbot.filters import score_job

TRACKER_PATH = "data/applications.csv"

companies = ["ramp"]
keywords = ["intern", "developer", "software"]
locations = ["remote", "canada"]

for name in companies:
    print(f"\nFetching jobs for {name}...")
    try:
        jobs = fetch_ashby(name)
        print(f"Found {len(jobs)} jobs at {name}")

        rows = []
        for j in jobs:
            score = score_job(j, keywords, locations)
            rows.append({
                "id": j["id"],
                "company": j["company"],
                "title": j["title"],
                "location": j["location"],
                "source": j["source"],
                "url": j["url"],
                "posted_at": j.get("posted_at"),
                "keywords": ",".join(keywords),
                "score": score,
                "status": "new",
                "created_at": now_iso(),
                "updated_at": now_iso(),
                "notes": "",
            })

        upsert_tracker(TRACKER_PATH, rows)
        print(f"Saved {len(rows)} jobs with scores to {TRACKER_PATH}")

    except Exception as e:
        print(f"Error fetching {name}: {e}")
