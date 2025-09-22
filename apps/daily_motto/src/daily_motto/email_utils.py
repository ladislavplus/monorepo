import os
from dotenv import load_dotenv
from sib_api_v3_sdk import ApiClient, Configuration, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException

# Load environment
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")

# Setup Brevo API client
configuration = Configuration()
configuration.api_key['api-key'] = BREVO_API_KEY
api_instance = TransactionalEmailsApi(ApiClient(configuration))

def send_email(to_email: str, subject: str, body: str):
    send_smtp_email = SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": EMAIL_FROM},
        subject=subject,
        html_content=body  # Can also use "text_content=body" for plain text
    )
    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print(f"✅ Email sent to {to_email}, Message ID: {response.message_id}")
    except ApiException as e:
        print(f"❌ Error sending email: {e}")

def send_email_dummy(to_email: str, subject: str, body: str):
# Dummy function for testing
    print(f"✅ Email dummy sent to {to_email}, subject: {subject}, body: {body}")

