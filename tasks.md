# NEWSFILE — Remaining Todos

## 🐛 Bugs

### Bug 1 — Miscategorized articles
Articles are being classified into wrong topics (e.g. tech articles showing under Health).
- File: `classifier/keyword_classifier.py` and `config.py`
- The keyword matching is too broad. Tighten keywords in `TOPIC_KEYWORDS` in `config.py` to use multi-word phrases instead of single common words.
- Example: change `"stock"` to `"stock market"`, change `"app"` to `"app development"`

---

## 🔌 Feed Overhaul

Replace RSS feeds with proper news APIs for better article quality and coverage.

### Task 1 — GNews API fetcher
- Create `scraper/gnews_fetcher.py`
- Sign up at https://gnews.io and add `GNEWS_API_KEY` to `.env.development`
- Fetch top headlines across all topics
- Return list of dicts with: `title`, `url`, `summary`, `published`, `source`
- Handle API errors gracefully with logger

### Task 2 — Guardian API fetcher
- Create `scraper/guardian_fetcher.py`
- Sign up at https://bonobo.capi.gutools.co.uk/register/developer and add `GUARDIAN_API_KEY` to `.env.development`
- Fetch latest articles, request `body` field for full text
- Return list of dicts with: `title`, `url`, `summary`, `full_text`, `published`, `source`

### Task 3 — Mediastack API fetcher
- Create `scraper/mediastack_fetcher.py`
- Sign up at https://mediastack.com and add `MEDIASTACK_API_KEY` to `.env.development`
- Fetch latest news as supplementary source
- Return list of dicts with: `title`, `url`, `summary`, `published`, `source`

### Task 4 — Update pipeline to use new fetchers
- In `pipeline/pipeline.py`, import and call all three new fetchers
- Combine results from all three into one list
- Keep existing deduplication logic (`article_exists(url)`)
- Remove or comment out the old RSS scraper call (`fetch_all_feeds`)

### Task 5 — Update config.py
- Remove `RSS_FEEDS` dict
- Add API key env var reads: `GNEWS_API_KEY`, `GUARDIAN_API_KEY`, `MEDIASTACK_API_KEY`
- Keep everything else the same

---

## ✨ Features

### Feature 1 — Groq stats improvements
- File: `classifier/groq_stats.py` and frontend `app/page.tsx`
- The stats prompt needs to be improved to extract more meaningful numerical data
- Chart should only show when there are 2+ comparable data points (already fixed in frontend)
- Key Metrics labels are sometimes duplicated — deduplicate them in the Groq response parsing

### Feature 2 — Stats-focused search mode
- Add a new API endpoint: `GET /search/stats?q=query`
- This endpoint searches articles AND filters for ones that contain numbers, percentages, or dollar figures using a regex like `\d+%|\$\d+|\d+ (million|billion|thousand)`
- Run Groq over each result to extract the key stat
- Return articles sorted by stat relevance
- Add a "Stats Search" toggle button in the frontend search bar

### Feature 3 — Evidence block generator
- Add new endpoint: `POST /articles/{id}/evidence`
- Use Groq to generate a formatted debate evidence block from the article
- Output format:
  ```
  [TAG LINE — one sentence argument this card supports]
  Author Last Name, Title/Credentials, Publication, Full Date
  "[Quotable excerpt — the most citable sentence or two from the article]"
  WARRANT: [Why this evidence supports the tag]
  IMPACT: [What happens if this is true — consequence for the debate]
  ```
- Add "Evidence Block" button in the article modal in `app/page.tsx`, next to "View Stats"
- Display the evidence block in a monospace/card-style panel below the article header

---

## 🔖 Later

- Bookmarking/saving articles to a personal file
- User login with Supabase Auth
- Debater profile flag — unlocks evidence block and stats search
- Paid tier — larger article database