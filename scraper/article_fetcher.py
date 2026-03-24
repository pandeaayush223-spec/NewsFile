import requests

from logger import get_logger

logger = get_logger(__name__)

#- Fetches article HTML and returns as string
#- rate limiting (10 seconds)

_JS_WALL_SIGNALS = [
    "enable javascript", "please enable js",
    "disable your ad blocker", "you need to enable javascript",
]

def fetch_article_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 NewsfileBot/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        if any(signal in html.lower() for signal in _JS_WALL_SIGNALS):
            logger.warning(f"JS-gated page, skipping full text: {url}")
            return ""
        return html
    except Exception as e:
        logger.error(f'Error fetching {url}: {e}')
        return ''
    
