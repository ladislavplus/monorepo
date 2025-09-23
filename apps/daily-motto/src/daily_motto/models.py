
from datetime import datetime
import os
from urllib.parse import urlparse
from daily_motto.env_utils import load_env

from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Text, Time, Float, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()

class User(Base):
    """User of the daily motto app."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    timezone = Column(String, nullable=False)
    preferred_send_time = Column(Time, nullable=False)
    status = Column(String, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_emails = relationship("SentHistory", back_populates="user")

class SentHistory(Base):
    """History of sent emails."""
    __tablename__ = 'sent_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    sent_at = Column(DateTime, default=datetime.utcnow)
    subject = Column(String)
    body = Column(Text)
    user = relationship("User", back_populates="sent_emails")

class ReminderTemplate(Base):
    """Template for reminders."""
    __tablename__ = 'reminder_templates'
    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)  # e.g., "work", "fitness", "mixed"
    prompt_text = Column(Text, nullable=False)
    weight_mindset = Column(Float, default=0.7)
    weight_practical = Column(Float, default=0.3)
    created_at = Column(DateTime, default=datetime.utcnow)


# --- DB session helper ---
load_env()
db_url = os.getenv("DATABASE_URL")
if not db_url or not db_url.strip():
    raise ValueError("DATABASE_URL environment variable is not set or empty.")

print("Using DATABASE_URL:", db_url)
# Parse the path
parsed = urlparse(db_url)
db_path = parsed.path

if os.name == "nt" and db_url.startswith("sqlite:///"):
    if db_path.startswith("//"):
        db_path = db_path.lstrip("/")  # removes one or two leading slashes

# if os.path.exists(db_path):
#    print("✅ SQLite database found.")
#else:
#    print("❌ SQLite database does not exist on disk:", db_path)
   # exit(1)
engine = create_engine(db_url, echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(engine)
    print("Database and tables created!")

if __name__ == "__main__":
    print("model.py run directly")
