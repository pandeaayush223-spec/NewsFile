from apscheduler.schedulers.background import BackgroundScheduler
from pipeline.pipeline import run_pipeline
from config import REFRESH_INTERVAL_MINS

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_pipeline, 'interval', minutes=REFRESH_INTERVAL_MINS)
    scheduler.start()
