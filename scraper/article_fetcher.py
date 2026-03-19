import requests

from logger import get_logger

logger = get_logger(__name__)

#- Fetches article HTML and returns as string
#- rate limiting (10 seconds)

def fetch_article_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 NewsfileBot/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.text
    except Exception as e:
        logger.error(f'Error fetching {url}: {e}')
        return ''
    
