import requests
from config import GNEWS_API_KEY
from logger import get_logger

logger = get_logger(__name__)

GNEWS_URL = "https://gnews.io/api/v4/top-headlines"

def fetch_gnews() -> list:
    """Fetch top headlines from GNews API."""
    try:
        # Make a GET request to GNEWS_URL with these params:
        #   token: GNEWS_API_KEY
        #   lang: "en"
        #   country: "us"
        #   max: 100
        # Set timeout=10
        response = requests.get(GNEWS_URL, params={
            "token": GNEWS_API_KEY, 
            "lang": "en", 
            "country": "us", 
            "max": 100, 
            }, timeout=10)
        
        # Call response.raise_for_status() to catch HTTP errors
        # Parse the JSON: data = response.json()
        # The articles are in data["articles"]
        response.raise_for_status()
        data = response.json()

        # For each item in data["articles"], build a dict with:
        #   title     → item["title"]
        #   url       → item["url"]
        #   summary   → item["description"]
        #   published → item["publishedAt"]
        #   source    → item["source"]["name"]  (default to "GNews" if missing)
        articles = []
        for item in data["articles"]:
            articles.append({
                'title': item["title"],
                'url': item["url"],
                'summary': item.get("description", ""),
                'published': item["publishedAt"],
                'source': item.get("source", {}).get("name", "GNews"),
                })
        logger.info(f"GNews: fetched {len(articles)} articles")
        return articles
            
            
            
        # Log how many articles were fetched
        # Return the list
        

    except Exception as e:
        logger.error(f"GNews fetch error: {e}")
        return []
