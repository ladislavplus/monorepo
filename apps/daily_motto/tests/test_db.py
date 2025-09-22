
from datetime import time
from src.daily_motto.models import User, get_db

# Quick test: insert one user
def test_add_user():
    # get_db() is a generator, so we use next() to get the session
    db = next(get_db())
    try:
        email = "test@example.com"
        # check if user already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"⚠️ User already exists: {existing.id} {existing.email}")
            return

        new_user = User(
            email=email,
            timezone="Europe/Prague",
            preferred_send_time=time(9, 0, 0)  # 09:00:00 as time object
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("✅ User added:", new_user.id, new_user.email)
    finally:
        db.close()


def test_list_users():
    db = next(get_db())
    try:
        users = db.query(User).all()
        print("📋 Users in DB:")
        for u in users:
            print(f"- {u.id}: {u.email}, {u.timezone}, {u.preferred_send_time}")
    finally:
        db.close()


if __name__ == "__main__":
    test_add_user()
    test_list_users()
