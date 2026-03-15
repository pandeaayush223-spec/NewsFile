from fastapi import APIRouter
from pipeline.pipeline import run_pipeline

router = APIRouter()

@router.post("/scheduler/run-now")
def run_now():
    run_pipeline()
    return {"status": "ok"}