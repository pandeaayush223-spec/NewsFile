from logger import get_logger
from scraper.rss_scraper import fetch_all_feeds
from scraper.article_fetcher import fetch_article_html
from scraper.text_cleaner import clean_html, clean_summary  
from classifier.keyword_classifier import classify_article
from storage.database import insert_article, article_exists, prune_topic
from storage.file_manager import save_article_json
import hashlib
from datetime import datetime, timezone
import time

logger = get_logger(__name__)

def run_pipeline() -> None:
    articles = fetch_all_feeds()
    logger.info(f"Found {len(articles)} articles from feeds")

    for article in articles:
        if article_exists(article['url']):
            logger.debug(f"Skipping duplicate: {article['url']}")
            continue
        html = fetch_article_html(article['url'])
        time.sleep(0.5)
        full_text = clean_html(html)
        topic, subtopic = classify_article(article['title'], article['summary'])
        article_id = hashlib.sha256(article["url"].encode()).hexdigest()[:16]

        complete_article = {"id": article_id, "title": article["title"], "url": article["url"], "source": article["source"], "topic": topic, "subtopic": subtopic, "summary": clean_summary(article["summary"]),
            "full_text": full_text, "published_date": article["published"], "scraped_at": datetime.now(timezone.utc).isoformat(),  "word_count": len(full_text.split())
}

        insert_article(complete_article)
        save_article_json(complete_article)
        prune_topic(topic)

        