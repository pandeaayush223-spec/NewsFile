import requests
from config import MEDIASTACK_API_KEY
from logger import get_logger

logger = get_logger(__name__)

MEDIASTACK_URL = "http://api.mediastack.com/v1/news"

def fetch_mediastack() -> list:
    """Fetch latest news from Mediastack API."""
    try:
        response = requests.get(MEDIASTACK_URL, params={
            "access_key": MEDIASTACK_API_KEY,
            "languages": "en",
            "countries": "us",
            "limit": 100,
        }, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for item in data["data"]:
            articles.append({
                "title": item["title"],
                "url": item["url"],
                "summary": item.get("description", ""),
                "published": item["published_at"],
                "source": item.get("source", "Mediastack"),
            })
        logger.info(f"Mediastack: fetched {len(articles)} articles")
        return articles

    except Exception as e:
        logger.error(f"Mediastack fetch error: {e}")
        return []
