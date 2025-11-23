from dotenv import load_dotenv
import os

load_dotenv()

from idealista_bot.fetch_listings import global_fetch, daily_fetch
from idealista_bot.process_listings import global_process, daily_process
from idealista_bot.notify import send_email
from idealista_bot.config import LOCATION_NAME
from datetime import datetime
import pandas as pd
import schedule
import time

def daily_task():
    
    new_df = daily_fetch()
    
    updated_df = daily_process(new_df)

    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    if not updated_df.empty:
        send_email(updated_df, formatted_time)

    print(f"[{formatted_time}] Fetch, processing and notification completed!")
    print(updated_df)



def initial_run(location_name = LOCATION_NAME):
    
    filename = os.path.join('data', location_name.lower() + '_listings.csv')

    if not os.path.exists(filename):
        all_data = global_fetch()
        global_process(all_data, location_name)
        print("Initial global fetch complete and data saved.")
    else:
        print("Data already exists. Skipping global fetch.")



if __name__ == "__main__":
    # Initial run to fetch all listings
    initial_run()

    # Schedule the fetches for daily updates
    daily_task()