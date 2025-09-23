
from daily_motto.models import get_db, ReminderTemplate

template_text = (
    "Generate a short daily motivational reminder for work and fitness, "
    "70% mindset-focused, 30% practical, calm and reflective tone."
)

session = next(get_db())  # Using next() to get the session from
# Check if template already exists
existing = session.query(ReminderTemplate).filter_by(role="mixed").first()
if existing:
        print(f"⚠️ Template already exists: ID {existing.id}")
else:
        template = ReminderTemplate(
            role="mixed",
            prompt_text=template_text,
            weight_mindset=0.7,
            weight_practical=0.3
        )
        session.add(template)
        session.commit()
        print(f"✅ Template added with ID {template.id}")
session.close()
