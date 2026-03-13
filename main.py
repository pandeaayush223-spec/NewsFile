import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scheduler.job_scheduler import start_scheduler
from contextlib import asynccontextmanager
from api.routes import articles, topics, search, stats, scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)
app.include_router(topics.router)
app.include_router(search.router)
app.include_router(stats.router)
app.include_router(scheduler.router)

@app.get("/health")
def health():
    return {"status": "ok"}

