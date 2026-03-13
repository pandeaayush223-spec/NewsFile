from fastapi import APIRouter
from storage.database import search_articles

router = APIRouter()


@router.get("/search")
def search(q: str):
    return search_articles(q)