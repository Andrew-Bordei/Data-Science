import pandas as pd
import sys 
import time 
import random

sys.path.append('./')
from extract.session import Session
from extract.extract import Extract
from load.load import Load
from transform.transform import Transform
from headers import HEADERS


class AmazonScrapper:
    def __init__(self, date: str) -> None:
        self.session = Session(HEADERS[0])
        self.extract = Extract(self.session.headers)
        self.date = date
    
    def scrape_asins(self) -> list[str]:
        """Hit the amazon api and get all the asins for 100 pages of listings"""
        all_asins = []
        unique_asins = set()

        # THIS CAN BE DONE ASYNC 
        for page in range(1, 25):
            time.sleep(random.uniform(2, 10))
            print(f"Getting asin's for page {page}")

            url = self.extract.build_page_url(page)
            products_page = self.extract.get_search_page(url)
            asin = self.extract.get_asin(products_page)
            if asin not in unique_asins:
                unique_asins.add(asin)
                all_asins.extend(asin)
        return all_asins
    
    def scrape_data(self, all_asins: list[str]) -> list[dict[str:any]]:
        """Extract the data from each asin's product page """
        all_product_data = []

        # THIS CAN BE DONE ASYNC
        for i in range(0, len(all_asins)):
            time.sleep(random.uniform(2, 10))

            if all_asins[i] != '':
                url = self.extract.build_asin_url(all_asins[i])
                soup = self.session.get_page(url, self.session.headers)
                product_data = self.extract.get_product_data(soup, all_asins[i])
                print(product_data)
                all_product_data.append(product_data)
        return all_product_data
    
    def main(self) -> str:
        transform = Transform(self.date)
        load = Load()

        asins = self.scrape_asins()
        data = self.scrape_data(asins)

        # SHOULD THIS BE MOVE SOMEWHERE ELSE??
        scraped_df = pd.DataFrame(data, 
            columns = [
                "title", "brand", "weight",'price','product_rating',
                'bought_last_month','num_reviews','product_description','product_upc',
                'honey_seller_rank', 'food_rank', 'asin'
            ]
        )
        scraped_df.to_csv(f'new_scrapper_data_{self.date}.csv')

        clean_df = transform.cleaning(scraped_df)

        load.insert_clean_data(clean_df, 'clean_data')

        return "Scraping process complete!"