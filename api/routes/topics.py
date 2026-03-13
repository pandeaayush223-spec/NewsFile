from fastapi import APIRouter
from storage.database import get_topics

router = APIRouter()

@router.get("/topics")
def get_topic():
    return get_topics()