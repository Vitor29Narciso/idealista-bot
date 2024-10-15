from config import LOCATION_NAME
import pandas as pd
import os



def global_process(df, location_name = LOCATION_NAME):
    
    filename = '../data/' + location_name.lower() + '_listings.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')

    print("Saved " + str(df.shape[0]) + f" listings to {filename}")



def daily_process(new_df, location_name = LOCATION_NAME):

    filename = '../data/' + location_name.lower() + '_listings.csv'

    if os.path.exists(filename):
        current_df = pd.read_csv(filename)
    else:
        print("CSV file does not exist.")
        return pd.DataFrame()

    new_listings = []

    for _, new_row in new_df.iterrows():
        id = new_row['propertyCode']
        new_price = new_row['price']

        existing_row = current_df[current_df['propertyCode'] == id]

        if existing_row.empty:
            new_row['flag'] = 'new'
            new_listings.append(new_row)
        else:
            existing_price = existing_row['price'].values[0]

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

    updated_df_no_old_price = updated_df_no_old_price.drop(columns=['status', 'old_price'])

    # Concatenate the new and updated listings with the current listings
    final_df = pd.concat([updated_df_no_old_price, current_df], ignore_index=True)

    # Save the updated DataFrame back to CSV
    global_process(final_df, location_name)

    return updated_df