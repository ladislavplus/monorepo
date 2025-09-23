import datetime
from daily_motto.email_utils import send_email

if __name__ == "__main__":
    # Test sending an email
    send_email("testemail@example.com", "Sending Email Test", "Hello from Daily-Motto. "+datetime.datetime.now().isoformat())
