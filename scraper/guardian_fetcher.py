import requests
from config import GUARDIAN_API_KEY
from logger import get_logger

logger = get_logger(__name__)

GUARDIAN_URL = "https://content.guardianapis.com/search"

def fetch_guardian() -> list:
    """Fetch latest articles from The Guardian API."""
    try:
        response = requests.get(GUARDIAN_URL, params={
            "api-key": GUARDIAN_API_KEY,
            "show-fields": "bodyText,trailText",
            "order-by": "newest",
            "page-size": 50,
        }, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for item in data["response"]["results"]:
            fields = item.get("fields", {})
            articles.append({
                "title": item["webTitle"],
                "url": item["webUrl"],
                "summary": fields.get("trailText", ""),
                "full_text": fields.get("bodyText", ""),
                "published": item["webPublicationDate"],
                "source": "The Guardian",
            })
        logger.info(f"Guardian: fetched {len(articles)} articles")
        return articles

    except Exception as e:
        logger.error(f"Guardian fetch error: {e}")
        return []
