from config import API_KEY
import requests # type: ignore

def get_total_listings(location_id: str = "0-EU-PT-31", location_name: str = "Madeira") -> int:

    url = "https://idealista7.p.rapidapi.com/listhomes"

    params = {
        "order": "relevance",
        "operation": "sale",
        "locationId": location_id,
        "locationName": location_name,
        "numPage": "1",
        "maxItems": "0",
        "location": "pt",
        "locale": "pt"
    }

    headers = {
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": "idealista7.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)

    print(response.json())

    if response.status_code == 200:
        data = response.json()
        total_listings = data.get('total', 0)
        print(f"Total listings found: {total_listings}")
        return total_listings
    else:
        print(f"Error: Unable to fetch total listings. Status code: {response.status_code}")
        return 0
    
get_total_listings()