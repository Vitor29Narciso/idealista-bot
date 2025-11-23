from .config import API_URL, API_KEY, API_HOST, LOCATION_ID, LOCATION_NAME, MAX_ITEMS_PER_PAGE, API_PARAMS, PARISH_MAPPING
import requests
import pandas as pd
import time



def get_total_listings(location_id, location_name):
    """
    Get total listings for a single parish.
    
    Args:
        location_id: Single location ID for a parish
        location_name: Name of the overall location (e.g., "Madeira")
    
    Returns:
        Total number of listings for the parish
    """
    
    params = {
        "order": "relevance",
        "locationId": location_id,
        "locationName": location_name,
        "numPage": "1",
        "maxItems": "0",
        **API_PARAMS
    }

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        total_listings = data.get('total', 0)
        parish_name = PARISH_MAPPING.get(location_id, location_id)
        print(f"Parish {parish_name}: {total_listings} listings")
        return total_listings
    else:
        parish_name = PARISH_MAPPING.get(location_id, location_id)
        print(f"Error fetching listings for parish {parish_name}. Status code: {response.status_code}")
        return 0



def global_fetch(location_ids = LOCATION_ID, location_name = LOCATION_NAME):
    """
    Fetch all listings from multiple parishes.
    
    Args:
        location_ids: List of location IDs for different parishes
        location_name: Name of the overall location (e.g., "Madeira")
    
    Returns:
        DataFrame containing all listings from all parishes
    """
    
    # Ensure location_ids is a list
    if isinstance(location_ids, str):
        location_ids = [location_ids]
    
    all_listings = []
    
    for location_id in location_ids:
        parish_name = PARISH_MAPPING.get(location_id, location_id)
        print(f"\nFetching listings for parish: {parish_name}")
        
        # Get total listings for this parish
        parish_total = get_total_listings(location_id, location_name)
        
        if parish_total == 0:
            print(f"No listings found for parish {parish_name}")
            continue
        
        listings_per_page = MAX_ITEMS_PER_PAGE
        total_pages = (parish_total // listings_per_page) + 1
        page_number = 1

        while page_number <= total_pages:
            params = {
                "order": "relevance",
                "locationId": location_id,
                "locationName": location_name,
                "numPage": page_number,
                "maxItems": MAX_ITEMS_PER_PAGE,
                **API_PARAMS
            }

            headers = {
                "x-rapidapi-key": API_KEY,
                "x-rapidapi-host": API_HOST
            }

            response = requests.get(API_URL, headers=headers, params=params)

            if response.status_code != 200:
                print(f"Error fetching page {page_number} for parish {parish_name}: {response.status_code}")
                break

            data = response.json()
            listings = data.get('elementList', [])

            # Add parish identifier to each listing for tracking
            for listing in listings:
                listing['parish_name'] = parish_name

            all_listings.extend(listings)
            print(f"Fetched {len(listings)} listings from page {page_number}/{total_pages} for parish {parish_name}")

            if len(listings) < listings_per_page:
                break # If the current page returned fewer than expected, we're done with this parish

            page_number += 1
            time.sleep(3)

        print(f"Completed fetching {parish_total} listings for parish {parish_name}")
    
    total_fetched = len(all_listings)
    print(f"\nCompleted fetching all {total_fetched} listings from {len(location_ids)} parishes!")

    df = pd.DataFrame(all_listings)
    return df



def daily_fetch(location_ids = LOCATION_ID, location_name = LOCATION_NAME):
    """
    Fetch the most recent listings from multiple parishes.
    
    Args:
        location_ids: List of location IDs for different parishes
        location_name: Name of the overall location (e.g., "Madeira")
    
    Returns:
        DataFrame containing the most recent listings from all parishes
    """
    
    # Ensure location_ids is a list
    if isinstance(location_ids, str):
        location_ids = [location_ids]
    
    all_listings = []
    
    for location_id in location_ids:
        parish_name = PARISH_MAPPING.get(location_id, location_id)
        print(f"Fetching most recent listings for parish: {parish_name}")
        
        params = {
            "order": "mostrecent",
            "locationId": location_id,
            "locationName": location_name,
            "numPage": "1",
            "maxItems": MAX_ITEMS_PER_PAGE,
            **API_PARAMS
        }

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": API_HOST
        }

        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            listings = data.get('elementList', [])
            
            # Add parish identifier to each listing for tracking
            for listing in listings:
                listing['parish_name'] = parish_name
            
            all_listings.extend(listings)
            print(f"Fetched {len(listings)} recent listings from parish {parish_name}")
        else:
            print(f"Error fetching recent listings for parish {parish_name}. Status code: {response.status_code}")
        
        # Add a small delay between requests to be respectful to the API
        time.sleep(1)
    
    total_fetched = len(all_listings)
    print(f"Total recent listings fetched from all parishes: {total_fetched}")
    
    df = pd.DataFrame(all_listings)
    return df