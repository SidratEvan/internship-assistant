import re

def _tokens(s: str):
    return re.findall(r"[A-Za-z0-9#+\-\.]{2,}", s.lower()) if s else []

def score_job(job, keywords, locations=None):
    score = 0
    toks = _tokens((job.get("title") or "") + " " + (job.get("location") or ""))
    for k in [k.strip().lower() for k in keywords if k.strip()]:
        if k in toks:
            score += 5
    if locations:
        for l in [l.strip().lower() for l in locations if l.strip()]:
            if job.get("location") and l in job["location"].lower():
                score += 3
    return score
