"""
fetch_news.py
Fetches recent articles from news RSS feeds and Reddit hot posts.
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
NEWS_OUTPUT  = os.path.join(ROOT_DIR, "feed-news.json")
REDDIT_OUTPUT = os.path.join(ROOT_DIR, "feed-reddit.json")

HOURS_LOOKBACK = 24

HEADERS = {
    "User-Agent": "DailyBriefBot/1.0 (personal news aggregator; contact via GitHub)"
}

# ── News RSS Sources ────────────────────────────────────────────────────────

NEWS_FEEDS = [
    # English
    { "name": "TechCrunch",       "url": "https://techcrunch.com/feed/",                        "lang": "en" },
    { "name": "Crunchbase News",  "url": "https://news.crunchbase.com/feed/",                   "lang": "en" },
    { "name": "Fortune",          "url": "https://fortune.com/feed/",                            "lang": "en" },
    { "name": "StrictlyVC",       "url": "https://strictlyvc.com/feed/",                         "lang": "en" },
    { "name": "VentureBeat",      "url": "https://feeds.feedburner.com/venturebeat/SZYF",        "lang": "en" },
    { "name": "MIT Tech Review",  "url": "https://www.technologyreview.com/feed/",               "lang": "en" },
    # Chinese
    { "name": "36氪",              "url": "https://36kr.com/feed",                               "lang": "zh" },
    { "name": "虎嗅",              "url": "https://www.huxiu.com/rss/0.xml",                     "lang": "zh" },
]

# ── Reddit Sources ──────────────────────────────────────────────────────────

REDDIT_SUBS = [
    "venturecapital",
    "startups",
    "ycombinator",
    "artificial",
    "SaaS",
    "techstartups",
]

# ── Helpers ─────────────────────────────────────────────────────────────────

def parse_date(entry) -> datetime | None:
    for field in ["published", "updated"]:
        val = entry.get(field)
        if val:
            try:
                dt = parsedate_to_datetime(val)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except Exception:
                pass
    return None

def fetch_rss_feed(source: dict, cutoff: datetime) -> list[dict]:
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  ✗ {source['name']}: HTTP {resp.status_code}")
            return []

        feed = feedparser.parse(resp.content)
        articles = []
        for entry in feed.entries:
            pub = parse_date(entry)
            if pub and pub < cutoff:
                continue
            articles.append({
                "source": source["name"],
                "lang": source["lang"],
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "published_at": pub.isoformat() if pub else None,
                "summary": entry.get("summary", "")[:300].strip(),
            })

        print(f"  ✓ {source['name']}: {len(articles)} articles")
        return articles[:8]

    except Exception as e:
        print(f"  ✗ {source['name']}: {e}")
        return []

def fetch_reddit(subreddit: str, limit: int = 8) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/hot.rss?limit={limit}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  ✗ r/{subreddit}: HTTP {resp.status_code}")
            return []

        feed = feedparser.parse(resp.content)
        if not feed.entries:
            print(f"  ✗ r/{subreddit}: empty feed")
            return []

        posts = []
        for entry in feed.entries[:limit]:
            pub = parse_date(entry)
            posts.append({
                "subreddit": f"r/{subreddit}",
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "created_at": pub.isoformat() if pub else None,
            })

        print(f"  ✓ r/{subreddit}: {len(posts)} posts")
        return posts

    except Exception as e:
        print(f"  ✗ r/{subreddit}: {e}")
        return []

# ── Main ────────────────────────────────────────────────────────────────────

cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_LOOKBACK)

# Fetch news
print("=== Fetching News RSS ===")
news_results = []
for source in NEWS_FEEDS:
    articles = fetch_rss_feed(source, cutoff)
    news_results.extend(articles)
    time.sleep(1)

news_output = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "period_hours": HOURS_LOOKBACK,
    "article_count": len(news_results),
    "articles": news_results,
}
with open(NEWS_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(news_output, f, ensure_ascii=False, indent=2)
print(f"\n✅ News: {len(news_results)} articles saved to feed-news.json\n")

# Fetch Reddit
print("=== Fetching Reddit ===")
reddit_results = []
for sub in REDDIT_SUBS:
    posts = fetch_reddit(sub)
    reddit_results.extend(posts)
    time.sleep(1)

reddit_output = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "post_count": len(reddit_results),
    "posts": reddit_results,
}
with open(REDDIT_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(reddit_output, f, ensure_ascii=False, indent=2)
print(f"\n✅ Reddit: {len(reddit_results)} posts saved to feed-reddit.json")
