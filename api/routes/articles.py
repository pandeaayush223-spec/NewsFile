from fastapi import APIRouter
from storage.database import get_articles_by_topic, get_all_stats, get_article_by_id
from classifier.groq_stats import extract_stats
import json

router = APIRouter()

@router.get('/articles')
def get_articles(topic: str = None, days: int = None):
    if topic:
        return get_articles_by_topic(topic)
    else: 
        return get_all_stats()
    
@router.get('/articles/{article_id}')
def get_article(article_id: str):
    return get_article_by_id(article_id)

@router.post('/articles/{article_id}/stats')
def get_article_stats(article_id: str):
    article = get_article_by_id(article_id)
    if not article:
        return {"error": "Article not found"}
    raw = extract_stats(article["title"], article["full_text"] or article["summary"])
    try:
        return json.loads(raw)
    except:
        return {"error": "Could not parse stats", "raw": raw}