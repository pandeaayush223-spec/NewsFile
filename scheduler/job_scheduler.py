from apscheduler.schedulers.background import BackgroundScheduler
from pipeline.pipeline import run_pipeline
from config import REFRESH_INTERVAL_MINS
from logger import get_logger

logger = get_logger(__name__)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_pipeline, 'interval', minutes=REFRESH_INTERVAL_MINS)
    scheduler.add_job(run_backup, 'interval', hours=24)  # runs once a day
    
    logger.info(f"Scheduler started — pipeline every {REFRESH_INTERVAL_MINS} mins, backup every 24hrs")
    scheduler.start()
