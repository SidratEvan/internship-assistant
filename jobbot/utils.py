from datetime import datetime
import pandas as pd
from typing import List, Dict, Any
import yaml

TRACKER_COLUMNS = [
    "id","company","title","location","source","url","posted_at",
    "keywords","score","status","created_at","updated_at","notes"
]

def now_iso() -> str:
    """Return current time in ISO format."""
    return datetime.now().isoformat(timespec="seconds")

def init_tracker(path: str) -> pd.DataFrame:
    """Load the tracker CSV or create it if missing."""
    try:
        df = pd.read_csv(path)
        for c in TRACKER_COLUMNS:
            if c not in df.columns:
                df[c] = None
        return df[TRACKER_COLUMNS]
    except FileNotFoundError:
        df = pd.DataFrame(columns=TRACKER_COLUMNS)
        df.to_csv(path, index=False)
        return df

def upsert_tracker(path: str, rows: List[Dict[str, Any]]):
    """Insert new job rows into the tracker if not already present."""
    df = init_tracker(path)
    existing = set(df["id"].astype(str))
    new = [r for r in rows if str(r["id"]) not in existing]
    if new:
        df = pd.concat([df, pd.DataFrame(new)], ignore_index=True)
        df.to_csv(path, index=False)
    return df
    
def load_user_config(path="config.yaml"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}