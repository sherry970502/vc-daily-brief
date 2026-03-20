# Daily Brief · VC & Tech Intelligence

A Claude Code skill that generates a daily briefing on VC, startup, and AI news by combining real-time Twitter/X data with news and Reddit discussions.

## How It Works

1. **GitHub Actions** runs every day at 06:00 UTC
2. **`scripts/fetch_feeds.py`** pulls recent tweets from 18 curated VC/founder accounts via Twitter API v2
3. Results are saved to **`feed-x.json`**
4. When invoked, **`SKILL.md`** reads the pre-fetched data and supplements it with live web searches for news and Reddit

## Setup

### 1. Fork this repository

### 2. Add your Twitter Bearer Token

Go to **Settings → Secrets and variables → Actions → New repository secret**

- Name: `TWITTER_BEARER_TOKEN`
- Value: your Bearer Token from [developer.twitter.com](https://developer.twitter.com)

### 3. Enable GitHub Actions

Actions will run automatically at 06:00 UTC daily. You can also trigger manually from the **Actions** tab.

### 4. Install the skill in Claude Code

```bash
# Add to your Claude Code skills
```

## Customizing Accounts

Edit `config/accounts.json` to add or remove Twitter accounts.

## Usage

```
/daily-brief
```

The skill will ask for your language and style preference, then generate a structured briefing from the latest data.

## Sources

- **Twitter/X**: 18 curated VC partners and founders (see `config/accounts.json`)
- **News**: TechCrunch, Fortune, Axios, Crunchbase, 36Kr, LatePost, and more
- **Reddit**: r/venturecapital, r/startups, r/artificial, r/YCombinator, and more
