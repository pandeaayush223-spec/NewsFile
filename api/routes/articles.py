from fastapi import APIRouter
from storage.database import get_articles_by_topic, get_all_stats, get_article_by_id

router = APIRouter()

@router.get('/articles')
def get_articles(topic: str = None):
    if topic:
        return get_articles_by_topic(topic)
    else: 
        return get_all_stats()
    
@router.get('/articles/{article_id}')
def get_article(article_id: str):
    return get_article_by_id(article_id)
