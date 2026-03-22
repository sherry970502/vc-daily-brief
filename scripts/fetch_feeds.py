"""
fetch_feeds.py
Fetches recent tweets from configured accounts via Twitter API v2.
Requires TWITTER_BEARER_TOKEN environment variable.
"""

import json
import os
import time
from datetime import datetime, timezone, timedelta

import requests

# ── Config ─────────────────────────────────────────────────────────────────

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "accounts.json")
OUTPUT_PATH = os.path.join(ROOT_DIR, "feed-x.json")

BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "DailyBriefBot/1.0",
}

API_BASE = "https://api.twitter.com/2"

# ── Helpers ─────────────────────────────────────────────────────────────────

def get_user_id(username: str):
    """Resolve @username to numeric user ID."""
    url = f"{API_BASE}/users/by/username/{username}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        print(f"  ✗ @{username}: user lookup failed ({resp.status_code})")
        return None
    data = resp.json()
    return data.get("data", {}).get("id")


def fetch_tweets(username: str, user_id: str, hours_lookback: int, max_results: int = 5) -> list[dict]:
    """Fetch recent tweets for a user via API v2."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_lookback)
    start_time = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = f"{API_BASE}/users/{user_id}/tweets"
    params = {
        "max_results": min(max_results * 3, 100),  # fetch extra to filter RTs
        "start_time": start_time,
        "tweet.fields": "created_at,text",
        "exclude": "retweets,replies",
    }

    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if resp.status_code != 200:
        print(f"  ✗ @{username}: tweets fetch failed ({resp.status_code}) — {resp.text[:200]}")
        return []

    data = resp.json()
    tweets_raw = data.get("data", [])
    if not tweets_raw:
        print(f"  ✓ @{username}: 0 tweets in last {hours_lookback}h")
        return []

    tweets = []
    for t in tweets_raw[:max_results]:
        created_at = t.get("created_at")
        tweets.append({
            "created_at": created_at,
            "text": t.get("text", "").strip(),
            "url": f"https://x.com/{username}/status/{t['id']}",
        })

    print(f"  ✓ @{username}: {len(tweets)} tweets")
    return tweets


# ── Main ────────────────────────────────────────────────────────────────────

if not BEARER_TOKEN:
    print("✗ TWITTER_BEARER_TOKEN not set. Skipping X feed.")
    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "period_hours": 48,
        "tweet_count": 0,
        "tweets": [],
        "error": "TWITTER_BEARER_TOKEN not set",
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    exit(0)

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

accounts = config["vc_partners"] + config["founders_leaders"]
hours_lookback = config["fetch_settings"]["hours_lookback"]
tweets_per_account = config["fetch_settings"]["tweets_per_account"]

results = []

for account in accounts:
    username = account["username"]
    print(f"Fetching @{username}...")

    user_id = get_user_id(username)
    if not user_id:
        time.sleep(1)
        continue

    tweets = fetch_tweets(username, user_id, hours_lookback, tweets_per_account)
    for tweet in tweets:
        results.append({
            "account": f"@{username}",
            "name": account["name"],
            "org": account["org"],
            **tweet,
        })

    time.sleep(1)  # avoid rate limiting

output = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "period_hours": hours_lookback,
    "tweet_count": len(results),
    "tweets": results,
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✅ Done. {len(results)} tweets saved to feed-x.json")
