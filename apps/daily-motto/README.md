# Daily Motivational Reminder App

## Goal
Send one short, calm, reflective, supportive daily reminder by email that alternates between work and fitness (70% mindset / 30% practical), helping me sustain steady growth.

## Success Metrics
1. Email delivery success: At least one email is sent and received each day.
2. Content quality check: Each email includes both mindset and practical elements (roughly 70/30).

## MVP Features
- Reminder generator (produces short messages based on the prompt)
- Scheduler (triggers send once per day)
- Email sender (SMTP or provider like SendGrid)
- Logging sent emails
- Basic user data: email address, timezone, preferred send time (default 8:00 AM, configurable)


[Scheduler (APScheduler)] 
        ↓ triggers daily
[Reminder Generator (litellm Groq model)]
        ↓ generates message
[Email Sender (smtplib)]
        ↓ sends email
[Storage/Database (SQLite)]
        ↑ logs sent email
