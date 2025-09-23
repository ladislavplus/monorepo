import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from daily_motto.env_utils import load_env
load_env()

# Send email using SMTP (Gmail example)
def send_email(to_email: str, subject: str, body: str):
    # Gmail credentials
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PSW')  # App password, not your real Gmail password
    
    # Compose message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email via Gmail's SMTP server
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)


def send_email_dummy(to_email: str, subject: str, body: str):
# Dummy function for testing
    print(f"✅ Email dummy sent to {to_email}, subject: {subject}, body: {body}")

