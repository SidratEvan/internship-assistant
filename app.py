import streamlit as st
import pandas as pd
from jobbot.sources.ashby import fetch_ashby
from jobbot.sources.greenhouse import fetch_greenhouse
from jobbot.filters import score_job
from jobbot.utils import upsert_tracker, now_iso, load_user_config
from jobbot.templating import render_cover_letter, load_user_config
from pathlib import Path

TRACKER_PATH = "data/applications.csv"

st.set_page_config(page_title="Internship Assistant", layout="wide")

st.title("🚀 Internship Assistant Webapp")

# Sidebar
st.sidebar.header("Settings")
keywords = st.sidebar.text_input("Keywords", "intern,software")
locations = st.sidebar.text_input("Locations", "remote,canada")
config = load_user_config()
companies = config.get("companies", ["ramp", "stripe", "discord"])

if st.sidebar.button("Search Jobs"):
    all_rows = []
    for company in companies:
        st.write(f"🔎 Searching {company}...")
        jobs = []
        try:
            jobs = fetch_ashby(company)
            if jobs:
                st.success(f"Found {len(jobs)} jobs at {company} (Ashby) ✅")
            else:
                jobs = fetch_greenhouse(company)
                if jobs:
                    st.success(f"Found {len(jobs)} jobs at {company} (Greenhouse) ✅")
                else:
                    st.info(f"No jobs found at {company}")
        except Exception:
            st.warning(f"⚠️ Skipping {company} (fetch failed)")


        for j in jobs:
            score = score_job(j, keywords.split(","), locations.split(","))
            all_rows.append({
                "id": j["id"],
                "company": j["company"],
                "title": j["title"],
                "location": j["location"],
                "url": j["url"],
                "score": score,
                "source": j["source"],
                "posted_at": j.get("posted_at"),
            })

    df = pd.DataFrame(all_rows)
    if not df.empty:
        st.success(f"Found {len(df)} jobs across {len(companies)} companies ✅")
        st.dataframe(df[["id","company","title","location","score","url"]])
        if st.button("Save to Tracker"):
            upsert_tracker(TRACKER_PATH, all_rows)
            st.success("Jobs saved to tracker ✅")
    else:
        st.warning("No jobs found at any company.")


st.sidebar.markdown("---")
st.sidebar.header("Cover Letter")

job_id = st.sidebar.text_input("Job ID from tracker")
if st.sidebar.button("Generate Cover Letter"):
    if not job_id:
        st.warning("Please enter a Job ID")
    else:
        df = pd.read_csv(TRACKER_PATH)
        if job_id not in df["id"].values:
            st.error("Job ID not found in tracker.")
        else:
            job = df[df["id"] == job_id].iloc[0].to_dict()
            user = load_user_config()["user"]
            context = {
                "company": job["company"],
                "title": job["title"],
                "location": job["location"],
                "user": user,
            }
            letter = render_cover_letter("templates/cover_letter.jinja", context)
            st.subheader("📄 Generated Cover Letter")
            st.text_area("Preview", letter, height=400)

            # Save as Markdown file
            outdir = Path("docs/letters")
            outdir.mkdir(parents=True, exist_ok=True)
            outfile = outdir / f"{job_id}.md"
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(letter)

            st.success(f"Cover letter saved as {outfile}")
