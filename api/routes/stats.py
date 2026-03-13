from fastapi import APIRouter
from storage.database import get_all_stats

router = APIRouter()


@router.get("/stats")
def stats():
    return get_all_stats()