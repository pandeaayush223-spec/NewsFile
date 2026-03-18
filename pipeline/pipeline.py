from scraper.rss_scraper import fetch_all_feeds
from scraper.article_fetcher import fetch_article_html
from scraper.text_cleaner import clean_html
from classifier.keyword_classifier import classify_article
from storage.database import insert_article, article_exists, prune_topic
from storage.file_manager import save_article_json
import hashlib
from datetime import datetime
import time

def run_pipeline() -> None:
    articles = fetch_all_feeds()
    print(f"Found {len(articles)} articles from feeds")
    
    for article in articles:
        if article_exists(article['url']):
            print(f'the article {article} already exists in the database')
            continue
        html = fetch_article_html(article['url'])
        time.sleep(1.5)
        full_text = clean_html(html)
        topic = classify_article(article['title'], article['summary'])
        article_id = hashlib.sha256(article["url"].encode()).hexdigest()[:16]
        
        complete_article = {"id": article_id, "title": article["title"], "url": article["url"], "source": article["source"], "topic": topic, "summary": article["summary"], 
            "full_text": full_text, "published_date": article["published"], "scraped_at": datetime.utcnow().isoformat(),  "word_count": len(full_text.split())
}

        insert_article(complete_article)
        save_article_json(complete_article)
        prune_topic(topic)

        