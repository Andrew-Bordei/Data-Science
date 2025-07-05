import sys 
import pandas as pd 
import json

sys.path.append('./')

from scraper_helpers import *
from data_processing.database_operations import *
from data_processing.cleaning_pipeline import *

def main(total_pages_scrape: int, date: str) -> str:
    # Scrape the data 
    scraped_data = scrape(total_pages_scrape)
    
    # Data sanity check 
    print(scraped_data)

    # Length sanity check 
    print("Length of scrapped data: ",len(scraped_data))

    # Determine if data should be cleaned & stored in db 
    answer = input("Would you like to clean & insert the data into the database? Y/n")

    if answer == "Y":
        # Convert to a dataframe 
        scraped_df = pd.DataFrame(
            scraped_data,
            columns = [
                "title", "brand", "weight",'price','price_per_ounce','product_rating',
                'bought_last_month','num_reviews','product_description','product_upc', 
                "date_acquired"
            ]
        )

        # Clean the data & add a date column 
        df = cleaning_pipeline(scraped_df)
        df['date_acquired'] = f"{date}"
        print(df.head())

        # Insert data in db 
        print(insert_clean_data(df, 'clean_data'))

    else: 
        # Save the scrapped data as JSON if it doesn't pass sanity checks 
        with open(f'scraped_data_{date}', 'w') as file_out:
            json.dump(scraped_data, file_out)
    
    return "Scraping process complete!"

if __name__ == '__main__': 
    # Run scraper 
    main(100, "2025-07-05")
