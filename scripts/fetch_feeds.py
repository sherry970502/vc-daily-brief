"""
fetch_feeds.py
Fetches recent tweets from configured accounts via Nitter RSS feeds.
Tries multiple Nitter instances as fallbacks.
No API key required.
"""

import json
import os
import time
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

import feedparser
import requests

# ── Config ─────────────────────────────────────────────────────────────────

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "accounts.json")
OUTPUT_PATH = os.path.join(ROOT_DIR, "feed-x.json")

# Nitter instances to try in order (fallback chain)
NITTER_INSTANCES = [
    "nitter.privacydev.net",
    "nitter.poast.org",
    "nitter.1d4.us",
    "nitter.cz",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DailyBriefBot/1.0; RSS reader)"
}

# ── Helpers ─────────────────────────────────────────────────────────────────

def fetch_rss(username: str, hours_lookback: int) -> list[dict]:
    """Try each Nitter instance until one returns a valid feed."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_lookback)

    for instance in NITTER_INSTANCES:
        url = f"https://{instance}/{username}/rss"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                continue

            feed = feedparser.parse(resp.content)
            if not feed.entries:
                continue

            tweets = []
            for entry in feed.entries:
                # Parse publication date
                pub_date = None
                if hasattr(entry, "published"):
                    try:
                        pub_date = parsedate_to_datetime(entry.published)
                        if pub_date.tzinfo is None:
                            pub_date = pub_date.replace(tzinfo=timezone.utc)
                    except Exception:
                        pass

                # Skip if older than lookback window
                if pub_date and pub_date < cutoff:
                    continue

                # Skip retweets
                title = entry.get("title", "")
                if title.startswith("RT by "):
                    continue

                # Clean up content
                text = entry.get("title", "")
                if text.startswith(f"{username}:"):
                    text = text[len(username) + 1:].strip()

                tweets.append({
                    "created_at": pub_date.isoformat() if pub_date else None,
                    "text": text,
                    "url": entry.get("link", ""),
                })

            print(f"  ✓ {len(tweets)} tweets via {instance}")
            return tweets[:5]  # Max 5 per account

        except Exception as e:
            print(f"  — {instance} failed: {e}")
            continue

    print(f"  ✗ All Nitter instances failed for @{username}")
    return []

# ── Main ────────────────────────────────────────────────────────────────────

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

accounts = config["vc_partners"] + config["founders_leaders"]
hours_lookback = config["fetch_settings"]["hours_lookback"]

results = []

for account in accounts:
    username = account["username"]
    print(f"Fetching @{username}...")

    tweets = fetch_rss(username, hours_lookback)
    for tweet in tweets:
        results.append({
            "account": f"@{username}",
            "name": account["name"],
            "org": account["org"],
            **tweet,
        })

    time.sleep(1)  # Be polite to Nitter instances

output = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "period_hours": hours_lookback,
    "tweet_count": len(results),
    "tweets": results,
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✅ Done. {len(results)} tweets saved to feed-x.json")
