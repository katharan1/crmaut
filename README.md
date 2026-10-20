# Customer Insights

An Apify Actor that collects customer feedback about Česká spořitelna once a week and
delivers it as one anonymised dataset.

| Source | What is collected | Store Actor used |
|---|---|---|
| App Store | Reviews of George Česko (`1163368801`, CZ store) | `thewolves/appstore-reviews-scraper` |
| Google Play | Reviews of George (`cz.csas.georgego`) | `neatrat/google-play-store-reviews-scraper` |
| Reddit | Posts and comments found by search phrases | `clearpath/reddit-post-comments-bulk-scraper` |
| Facebook | Comments under posts of `facebook.com/ceskasporitelna` | `apify/facebook-posts-scraper` + `apify/facebook-comments-scraper` |
| Instagram | Comments under posts of `instagram.com/ceskasporitelna` | `apify/instagram-scraper` + `apify/instagram-comment-scraper` |
| LinkedIn | Comments under posts of `linkedin.com/company/10700` | `harvestapi/linkedin-company-posts` |

## Output

Every item has exactly these fields:

| Field | Example | Notes |
|---|---|---|
| `source` | `google_play` | `app_store`, `google_play`, `reddit`, `facebook`, `instagram`, `linkedin` |
| `id` | `google_play:4a789fbe-…` | Unique and stable, safe to use for de-duplication |
| `date` | `2026-10-13T08:12:00.000Z` | ISO 8601, UTC. App Store reviews only have a day |
| `text` | `…po aktualizaci nelze přihlásit…` | App Store: title and text merged |
| `rating` | `3` | 1–5 for app stores, `null` elsewhere |
| `context` | `r/czech: Česká spořitelna dotaz.` | Post or thread the comment replies to; app version for reviews |
| `url` | `https://www.reddit.com/r/czech/…` | Link to the item, never to its author |

No author names, usernames, profile links or pictures are kept.

## What each run does

1. Starts all six collectors in parallel. Each Store Actor run is capped at
   `maxCostPerSourceUsd` (default $2).
2. Looks at items from the last `lookbackDays` (default 8). For social sources it checks
   posts up to `threadMaxAgeDays` old (default 30), because new comments land on older posts too.
3. Cleans the data:
   - keeps only the 7 fields above
   - drops the bank's own replies on Facebook, Instagram and LinkedIn
   - drops emoji-only and empty comments
   - drops deleted Reddit comments and the same comment posted twice
   - Reddit: keeps a thread only if it is in a Czech subreddit (`redditCzechSubreddits`) or
     the post names the bank. This removes off-topic search hits.
4. Skips anything an earlier run already delivered, so the one-day overlap never
   produces duplicates.
5. Saves the new items to the run's dataset (the weekly batch) and appends them to the
   named dataset `customer-insights` (the full history).
6. Deletes the scrapers' raw datasets, which contain author data.
7. Writes a `SUMMARY` record to the run's key-value store: counts per source, what was
   dropped and why, and any source that failed. One failed source doesn't stop the others.

## Deploy

With the [Apify CLI](https://docs.apify.com/cli):

```bash
npm install -g apify-cli
apify login          # paste your API token from Apify Console → Settings → API & Integrations
apify push           # run from this folder; builds the Actor "customer-insights" in your account
```

Or in Apify Console: **Actors → Develop new → Link Git repository**, pointing at this repo.

## Schedule weekly

Apify Console → **Schedules → Create new**:

- Cron: `0 6 * * 1` (Mondays 06:00), timezone `Europe/Prague`
- Add the Actor `customer-insights` with the default input

## Getting the data into your app (later)

Either option works:

- **Pull:** after each run, fetch
  `GET https://api.apify.com/v2/acts/<username>~customer-insights/runs/last/dataset/items?status=SUCCEEDED&clean=true`
  with your API token.
- **Push:** add a webhook on the Actor for **Run succeeded**, pointing at your app. The
  payload includes `resource.defaultDatasetId`; fetch
  `GET https://api.apify.com/v2/datasets/<defaultDatasetId>/items`.

## Develop

```bash
npm install
npm test             # unit tests, no network needed
```

The source definitions are in `src/sources.js`, the field mapping and filters in
`src/normalize.js`, and the run logic in `src/main.js`.

## Known limits

- App Store's public feed only returns the newest ~500 reviews, which is enough for a weekly run
  but matters for a large backfill.
- Facebook, Instagram and LinkedIn only cover comments under the bank's own posts, not
  mentions elsewhere.
- LinkedIn sometimes hides some comments from logged-out visitors, so a post's comment count
  can be higher than what is collected.
- LinkedIn's terms forbid scraping; have legal/compliance confirm before relying on that source.
