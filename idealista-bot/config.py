from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')

RECIPIENT_EMAIL_ONE = os.getenv('RECIPIENT_EMAIL_ONE')
RECIPIENT_EMAIL_TWO = os.getenv('RECIPIENT_EMAIL_TWO')
RECIPIENT_EMAIL_THREE = os.getenv('RECIPIENT_EMAIL_THREE')