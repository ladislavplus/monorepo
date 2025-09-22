from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def job():
    print(f"Reminder happened, at {datetime.now()}")

scheduler = BlockingScheduler()
# Run job every day at 8:00 AM
# scheduler.add_job(job, 'cron', hour=8, minute=0)
scheduler.add_job(job, 'cron', minute='*/2')

print("Scheduler started. Press Ctrl+C to exit.")
scheduler.start()
