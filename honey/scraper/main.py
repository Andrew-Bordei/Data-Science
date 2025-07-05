import pandas as pd
from session import Session
from extract import Extract

class AmazonScrapper:
    def __init__(self) -> None:
        self.session = Session()
        self.extract = Extract(self.session.headers, self.session.payload)
        self.amazon_session = self.session.get_amazon_session()
        
    def main(self):
        all_product_data = []
        all_asins = []

        for i in range(1):
            url = f"https://www.amazon.com/s/query?k=honey&page={i}"
            products_page = self.extract.get_search_page(url)
            asin = self.extract.get_asin(products_page)
            all_asins.append(asin)

            # print(products_page)
            # search_pages.append(products_page)

        # asin = self.extract.get_asin(search_pages)

        print(all_asins)

        for i in range(0, len(all_asins)):
            print("Geting product data of asin list: ", i)
            for k in range(0, len(all_asins[i])):
                print("Geting product data of asin: ", all_asins[i][k])
                if all_asins[i][k] != '':
                    url = f"https://www.amazon.com/dp/{all_asins[i][k]}"
                    soup = self.session.get_session(url, self.session.headers, self.amazon_session)
                    # product_data = self.extract.get_product_data(soup)
                    # print(product_data)
                    # all_product_data.append(product_data)
                    center = self.extract.get_center_column(soup)
                    title = self.extract.get_title(center, soup)
                    print(title)

        # print(all_product_data)

        # scraped_df = pd.DataFrame(
        #     all_product_data,
        #     columns = [
        #         "title", "brand", "weight",'price','product_rating',
        #         'bought_last_month','num_reviews','product_description','product_upc'
        #     ]
        # )

        # scraped_df.to_csv('new_scrapper_data.csv')

        return scraped_df
    
if __name__ == '__main__': 
    amazon_scrapper = AmazonScrapper()
    amazon_scrapper.main()