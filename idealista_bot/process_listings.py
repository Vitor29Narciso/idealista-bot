from .config import LOCATION_NAME
import pandas as pd
import os



def global_process(df, location_name = LOCATION_NAME):
    
    # Get the directory where this script is located, then go up one level to project root
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(script_dir, 'data')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    filename = os.path.join(data_dir, f"{location_name.lower()}_listings.csv")
    df.to_csv(filename, index=False, encoding='utf-8-sig')

    print("Saved " + str(df.shape[0]) + f" listings to {filename}")



def daily_process(new_df, location_name = LOCATION_NAME):

    # Check if new_df is empty
    if new_df.empty:
        print("No new listings to process.")
        return pd.DataFrame()
    
    # Validate required columns
    required_columns = ['propertyCode', 'price']
    missing_columns = [col for col in required_columns if col not in new_df.columns]
    if missing_columns:
        print(f"Error: Missing required columns in new data: {missing_columns}")
        return pd.DataFrame()

    # Get the directory where this script is located, then go up one level to project root
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(script_dir, 'data')
    filename = os.path.join(data_dir, f"{location_name.lower()}_listings.csv")

    if os.path.exists(filename):
        try:
            current_df = pd.read_csv(filename)
            print(f"Loaded {len(current_df)} existing listings from {filename}")
            print(current_df.head())
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return pd.DataFrame()
    else:
        print("CSV file does not exist.")
        return pd.DataFrame()

    # Ensure consistent data types
    new_df['propertyCode'] = new_df['propertyCode'].astype(str).str.strip()
    new_df['price'] = new_df['price'].astype(float)

    current_df['propertyCode'] = current_df['propertyCode'].astype(str).str.strip()
    current_df['price'] = current_df['price'].astype(float)
    
    # Handle parish_name field if it doesn't exist in current_df (for backward compatibility)
    if 'parish_name' not in current_df.columns and 'parish_name' in new_df.columns:
        print("Adding parish_name field to existing data...")
        current_df['parish_name'] = 'Unknown'  # Default value for existing data

    new_listings = []

    current_listing_dict = dict(zip(current_df['propertyCode'], current_df['price']))

    for _, new_row in new_df.iterrows():
        id = new_row['propertyCode']
        new_price = new_row['price']

        if id not in current_listing_dict:
            new_row['flag'] = 'new'
            new_listings.append(new_row)
        else:
            existing_price = current_listing_dict[id]

            if new_price != existing_price:
                # Price has changed, mark as updated
                new_row['flag'] = 'updated'
                new_row['old_price'] = existing_price
                new_listings.append(new_row)

                # Remove the old entry from current_df
                current_df = current_df[current_df['propertyCode'] != id]
            else:
                # Price is the same, treat as a duplicate, ignore it
                continue

    updated_df = pd.DataFrame(new_listings)
    updated_df_no_old_price = updated_df.copy()

    for col in ['flag', 'old_price']:
        if col in updated_df_no_old_price.columns:
            updated_df_no_old_price = updated_df_no_old_price.drop(columns=[col])
        else:
            print(f"Column '{col}' does not exist in the DataFrame.")

    # Concatenate the new and updated listings with the current listings
    final_df = pd.concat([updated_df_no_old_price, current_df], ignore_index=True)

    # Save the updated DataFrame back to CSV
    global_process(final_df, location_name)

    return updated_df