from jobbot.sources.greenhouse import fetch_greenhouse

companies = ["stripe", "discord"]

for slug in companies:
    print(f"\nFetching jobs for {slug}...")
    try:
        jobs = fetch_greenhouse(slug)
        print(f"Found {len(jobs)} jobs at {slug}")
        for j in jobs[:5]:
            print(f"- {j['title']} ({j['location']}) :: {j['url']}")
    except Exception as e:
        print(f"Error fetching {slug}: {e}")
