from dotenv import load_dotenv
import os

load_dotenv()

API_URL = "https://idealista7.p.rapidapi.com/listhomes"
API_KEY = os.getenv('API_KEY')
API_HOST = "idealista7.p.rapidapi.com"

LOCATION_ID = ["0-EU-PT-31-02-001-01", "0-EU-PT-31-02-003-03", "0-EU-PT-31-03-007-07"]
LOCATION_NAME = "Madeira"
MAX_ITEMS_PER_PAGE = 40

# Parish ID to Name Mapping
PARISH_MAPPING = {
    "0-EU-PT-31-02-001-01": "Câmara de Lobos",
    "0-EU-PT-31-02-003-03": "Estreito de Câmara de Lobos", 
    "0-EU-PT-31-03-007-07": "São Martinho"
}

# API Search Parameters
API_PARAMS = {
    "operation": "sale",
    "location": "pt",
    "locale": "pt",
    "minPrice": "100000",
    "maxPrice": "400000",
    "flat": True,
    "bedrooms0": False,
    "bedrooms1": True,
    "bedrooms2": True,
    "bedrooms3": True,
    "garage": True
}

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_APP_PASSWORD = os.getenv('SENDER_APP_PASSWORD')

RECIPIENT_EMAIL_ONE = os.getenv('RECIPIENT_EMAIL_ONE')
RECIPIENT_EMAIL_TWO = os.getenv('RECIPIENT_EMAIL_TWO')
RECIPIENT_EMAIL_THREE = os.getenv('RECIPIENT_EMAIL_THREE')