"""
fetch_feeds.py
Fetches recent tweets from configured accounts via Twitter API v2
and saves results to feed-x.json in the repo root.
"""

import os
import json
import tweepy
from datetime import datetime, timezone, timedelta

# ── Config ─────────────────────────────────────────────────────────────────

BEARER_TOKEN = os.environ["TWITTER_BEARER_TOKEN"]
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "accounts.json")
OUTPUT_PATH = os.path.join(ROOT_DIR, "feed-x.json")

# ── Setup ──────────────────────────────────────────────────────────────────

client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

accounts = config["vc_partners"] + config["founders_leaders"]
tweets_per_account = config["fetch_settings"]["tweets_per_account"]
hours_lookback = config["fetch_settings"]["hours_lookback"]
start_time = datetime.now(timezone.utc) - timedelta(hours=hours_lookback)

# ── Fetch ──────────────────────────────────────────────────────────────────

results = []

for account in accounts:
    username = account["username"]
    print(f"Fetching @{username}...")

    try:
        # Resolve username to user ID
        user_resp = client.get_user(username=username, user_fields=["id", "name"])
        if not user_resp.data:
            print(f"  ⚠ User not found: @{username}")
            continue

        user_id = user_resp.data.id

        # Fetch recent tweets
        tweets_resp = client.get_users_tweets(
            id=user_id,
            max_results=tweets_per_account,
            start_time=start_time,
            tweet_fields=["created_at", "text", "note_tweet"],
            exclude=["retweets", "replies"],
        )

        if not tweets_resp.data:
            print(f"  — No tweets in last {hours_lookback}h")
            continue

        for tweet in tweets_resp.data:
            # Use note_tweet for full untruncated text if available
            text = tweet.text
            if hasattr(tweet, "note_tweet") and tweet.note_tweet:
                text = tweet.note_tweet.get("text", tweet.text)

            results.append({
                "account": f"@{username}",
                "name": account["name"],
                "org": account["org"],
                "text": text,
                "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                "url": f"https://x.com/{username}/status/{tweet.id}",
            })

        print(f"  ✓ {len(tweets_resp.data)} tweets fetched")

    except tweepy.errors.TweepyException as e:
        print(f"  ✗ Error fetching @{username}: {e}")
        continue

# ── Save ───────────────────────────────────────────────────────────────────

output = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "period_hours": hours_lookback,
    "tweet_count": len(results),
    "tweets": results,
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✅ Done. {len(results)} tweets saved to feed-x.json")
