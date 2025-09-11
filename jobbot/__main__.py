import argparse
from pathlib import Path
from jobbot.sources.ashby import fetch_ashby
from jobbot.filters import score_job
from jobbot.utils import upsert_tracker, now_iso
from jobbot.templating import render_cover_letter, load_user_config
import pandas as pd
from pathlib import Path
from jobbot.sources.greenhouse import fetch_greenhouse


ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "data" / "applications.csv"

def search_cmd(args):
    config = load_user_config()
    companies = config.get("companies", ["ramp"])  # fallback if not defined

    rows = []

    for slug in companies:
        print(f"\nFetching jobs for {slug}...")

        jobs = []
        # Try Ashby first
        try:
            jobs = fetch_ashby(slug)
        except Exception:
            pass

        # If Ashby failed or returned none, try Greenhouse
        if not jobs:
            try:
                jobs = fetch_greenhouse(slug)
            except Exception:
                pass

        for j in jobs:
            score = score_job(j, args.keywords.split(","), args.locations.split(",") if args.locations else None)
            if score > 0:
                rows.append({
                    "id": j["id"],
                    "company": j["company"],
                    "title": j["title"],
                    "location": j["location"],
                    "source": j["source"],
                    "url": j["url"],
                    "posted_at": j.get("posted_at"),
                    "keywords": args.keywords,
                    "score": score,
                    "status": "new",
                    "created_at": now_iso(),
                    "updated_at": now_iso(),
                    "notes": "",
                })

    rows.sort(key=lambda r: r["score"], reverse=True)
    for r in rows[:20]:
        print(f"[{r['score']}] {r['company']} — {r['title']} ({r['location']}) :: {r['url']}")

    if args.save:
        upsert_tracker(str(TRACKER), rows)
        print(f"\nSaved {len(rows)} jobs to {TRACKER}")

def generate_cmd(args):
    df = pd.read_csv("data/applications.csv")
    job = df[df["id"] == args.job_id].iloc[0].to_dict()
    user = load_user_config()["user"]

    context = {
        "company": job["company"],
        "title": job["title"],
        "location": job["location"],
        "user": user,
    }

    # Render the letter
    letter = render_cover_letter("templates/cover_letter.jinja", context)

    # Print in terminal
    print("\n" + "="*40 + "\n")
    print(letter)
    print("\n" + "="*40 + "\n")

    # Save as Markdown
    outdir = Path("docs/letters")
    outdir.mkdir(parents=True, exist_ok=True)
    outfile_md = outdir / f"{job['id']}.md"
    with open(outfile_md, "w", encoding="utf-8") as f:
        f.write(letter)
    print(f"Cover letter saved to {outfile_md}")

    # Optional PDF export
    if args.pdf:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        pdf_path = outdir / f"{job['id']}.pdf"
        doc = SimpleDocTemplate(str(pdf_path), pagesize=LETTER)
        styles = getSampleStyleSheet()
        story = []

        for line in letter.split("\n"):
            if line.strip():
                story.append(Paragraph(line, styles["Normal"]))
                story.append(Spacer(1, 12))
        doc.build(story)
        print(f"Cover letter also exported as {pdf_path}")



def build_parser():
    import argparse
    p = argparse.ArgumentParser(prog="jobbot", description="Internship Assistant CLI")
    s = p.add_subparsers(dest="cmd", required=True)

    ss = s.add_parser("search")
    ss.add_argument("--keywords", default="intern,software")
    ss.add_argument("--locations", default="remote,canada")
    ss.add_argument("--save", action="store_true")
    ss.set_defaults(func=search_cmd)

    gs = s.add_parser("generate")
    gs.add_argument("--job-id", required=True)
    gs.add_argument("--pdf", action="store_true", help="Also export as PDF")
    gs.set_defaults(func=generate_cmd)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
