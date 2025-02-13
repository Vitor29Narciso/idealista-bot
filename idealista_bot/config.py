from dotenv import load_dotenv
import os

load_dotenv()

API_URL = "https://idealista7.p.rapidapi.com/listhomes"
API_KEY = os.getenv('API_KEY')
API_HOST = "idealista7.p.rapidapi.com"

LOCATION_ID = "0-EU-PT-31" # Madeira Island ID | 0-EU-PT-31-03 Funchal, Madeira ID
LOCATION_NAME = "Madeira"
MAX_ITEMS_PER_PAGE = 40

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_APP_PASSWORD = os.getenv('SENDER_APP_PASSWORD')

RECIPIENT_EMAIL_ONE = os.getenv('RECIPIENT_EMAIL_ONE')
RECIPIENT_EMAIL_TWO = os.getenv('RECIPIENT_EMAIL_TWO')
RECIPIENT_EMAIL_THREE = os.getenv('RECIPIENT_EMAIL_THREE')