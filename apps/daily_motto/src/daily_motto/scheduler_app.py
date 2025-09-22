

import os
import sys
import random
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

from env_utils import load_env
load_env()

import litellm
from models import get_db, User, SentHistory, ReminderTemplate
from email_utils import send_email_dummy  # Use send_email in production

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# --- API Key check ---
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    logging.error("GROQ_API_KEY not found in environment. Exiting.")
    sys.exit(1)

# --- Reminder generation ---
def generate_reminder(prompt_text: str) -> str:
    """Generate reminder text using LiteLLM/Groq."""
    try:
        response = litellm.completion(
            model="groq/llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"LLM error: {e}")
        return ""

# --- Main reminder sending logic ---
def send_reminders():
    session = next(get_db())
    try:
        users = session.query(User).filter_by(status="active").all()
        templates = session.query(ReminderTemplate).all()
        if not templates:
            logging.warning("No reminder templates found.")
            return

        for user in users:
            template = random.choice(templates)
            prompt = template.prompt_text
            reminder_text = generate_reminder(prompt)
            if not reminder_text:
                logging.warning(f"No reminder generated for {user.email}.")
                continue

            try:
                send_email_dummy(user.email, "Your Daily Motivation", reminder_text)
                logging.info(f"Email sent to {user.email}")
            except Exception as e:
                logging.error(f"Failed to send email to {user.email}: {e}")
                continue

            sent_email = SentHistory(
                user_id=user.id,
                subject="Daily Motivation",
                body=reminder_text
            )
            session.add(sent_email)
            session.commit()
            logging.info(f"Reminder recorded for {user.email}")
    finally:
        session.close()

# --- Scheduler setup ---
def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(send_reminders, 'cron', minute='*/1')
    logging.info("Scheduler started. Press Ctrl+C to exit.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")

if __name__ == "__main__":
    main()
