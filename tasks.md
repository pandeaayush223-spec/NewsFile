# NEWSFILE — Remaining Todos

## 🧹 HTML Parsing Improvements ✅

- Expand tag removal: `figure`, `figcaption`, `aside`, `picture` and CSS class selectors for captions/share/social/byline/credit
- Filter paragraphs shorter than 8 words (catches "Share:", "Imago", timestamps)
- Filter boilerplate strings: "copyright", "please enable js", "ad blocker", etc.
- Deduplicate paragraphs before joining
- Detect JS-gated pages in `article_fetcher.py` and return `""` so pipeline falls back to summary

---

## 🎯 Topic Scope Narrowing

- Restrict accepted topics to: Politics, Economics, Geopolitics, Climate, Health, AI policy
- Articles classified as Sports, Entertainment, Arts, or other off-topic categories should be rejected (not inserted into the database)
- Update `pipeline/pipeline.py` to skip articles where `topic` is not in the approved set
- Update `config.py` TOPICS dict to reflect the narrowed scope

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

### Feature 3 — Better stats visualizations
- Improve charts in the stats panel (`app/page.tsx`)
- Consider multiple chart types (bar, line, pie) depending on the data shape
- Show trend lines where applicable
- Improve empty/loading states

### Feature 4 — Evidence block generator
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

## 🚩 User Reporting System

- Add `POST /articles/{id}/report` endpoint — user flags an article as misclassified
- Store reports in a Supabase `reports` table with `article_id`, `reported_topic`, `suggested_topic`, `timestamp`
- Add a small "Wrong topic?" button in the article card or modal in the frontend
- (Later) Use report data to retrain or adjust keyword thresholds

---

## 🏷️ Subtopic Classification (Backend + Frontend)

- Backend: expose subtopic filtering via the API (e.g. `GET /articles?topic=Technology&subtopic=AI`)
- Frontend: add subtopic UI — when a topic is selected, show its subtopics as a secondary filter row
- Groq should handle subtopic assignment for articles that fall through keyword classification (already partially done via `classify()` in `classifier/classifier.py` — verify Groq is actually returning valid subtopics, not just `null`)
- Confirm subtopics are being stored correctly in Supabase and returned in API responses

---

## 🔖 Later

- Bookmarking/saving articles to a personal file
- User login with Supabase Auth
- Debater profile flag — unlocks evidence block and stats search
- Paid tier — larger article database