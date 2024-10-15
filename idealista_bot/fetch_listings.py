from .config import API_URL, API_KEY, API_HOST, LOCATION_ID, LOCATION_NAME, MAX_ITEMS_PER_PAGE
import requests
import pandas as pd
import time



def get_total_listings(location_id = LOCATION_ID, location_name = LOCATION_NAME):

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
	    "x-rapidapi-host": API_HOST
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        total_listings = data.get('total', 0)
        print(f"Total listings found: {total_listings}")
        return total_listings
    else:
        print(f"Error: Unable to fetch total listings. Status code: {response.status_code}")
        return 0



def global_fetch(location_id = LOCATION_ID, location_name = LOCATION_NAME):
    
    total_listings = get_total_listings(location_id, location_name)
    
    if total_listings == 0:
        return []
    
    listings_per_page = MAX_ITEMS_PER_PAGE                      # Default number of listings returned per page
    total_pages = (total_listings // listings_per_page) + 1     # Calculate total pages
    
    all_listings = []
    page_number = 1

    while page_number <= total_pages:
        params = {
        "order": "relevance",
        "operation": "sale",
        "locationId": location_id,
        "locationName": location_name,
        "numPage": page_number,
        "maxItems": MAX_ITEMS_PER_PAGE,
        "location": "pt",
        "locale": "pt"
    }

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "idealista7.p.rapidapi.com"
        }

        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching page {page_number}: {response.status_code}")
            break

        data = response.json()
        listings = data.get('elementList', [])

        all_listings.extend(listings)
        print(f"Fetched {len(listings)} listings from page {page_number} out of {total_pages} pages")

        if len(listings) < listings_per_page:
            break # If the current page returned fewer than expected, we're also done

        page_number += 1
        time.sleep(3)

    print(f"Completed fetching all {total_listings} listings from the {total_pages} pages!")

    df = pd.DataFrame(all_listings)

    return df



def daily_fetch(location_id = LOCATION_ID, location_name = LOCATION_NAME):

    params = {
        "order": "mostrecent",
        "operation": "sale",
        "locationId": location_id,
        "locationName": location_name,
        "numPage": "1",
        "maxItems": "40",
        "location": "pt",
        "locale": "pt"
    }

    headers = {
	    "x-rapidapi-key": API_KEY,
	    "x-rapidapi-host": API_HOST
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        listings = data.get('elementList', [])
        df = pd.DataFrame(listings)
        return df
    else:
        print(f"Error: Unable to fetch most recent listings. Status code: {response.status_code}")
        return pd.DataFrame()