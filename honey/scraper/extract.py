import json
import requests
from bs4 import BeautifulSoup
from queue import Queue

class Extract:
    def __init__(self, headers, payload):
        self.headers = headers 
        self.payload = payload
    
    def get_search_page(self, url):
        response = requests.request("POST", url, headers=self.headers, data=self.payload)

        return response.text
    
    def parse_page(self, data):
        # Split by '&&&' and strip whitespace
        split_data = [s.strip() for s in data.split('&&&') if s.strip()]
        
        # Parse each JSON string
        parsed_data = []
        for string in split_data:
            try:
                parsed_item = json.loads(string)
                parsed_data.append(parsed_item)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                print(f"Problematic string: {str[:100]}...")
        
        return parsed_data
    
    def get_asin(self, data):
        parsed_data = self.parse_page(data)

        queue = []

        for i in range(2,len(parsed_data)):
            try:
                asin = parsed_data[i][2]['asin']
                queue.append(asin)
            except:
                continue
        
        return queue 
    
    def get_center_column(self, soup: BeautifulSoup) -> BeautifulSoup:
        # Get column where data to scrape is 
        center_col = soup.find(id="centerCol")

        if center_col:
            return center_col
        
        return None

    def get_product_column(self, soup: BeautifulSoup) -> BeautifulSoup:
        # Scrape product details column 
        product_col = soup.find(id="detailBullets_feature_div")

        if product_col: 
            return product_col
        
        return None 

    def get_title(self, center_col: BeautifulSoup, soup: BeautifulSoup) -> str: 
        if soup is None:
            return None

        # Scrape title 
        title = soup.find(center_col, id="productTitle")

        if title is None:
            return None

        return title 

    def get_brand(self, center_col: BeautifulSoup) -> str: 
        if center_col:
            brand = center_col.find(class_="a-spacing-small po-brand")
            if brand: 
                brand = brand.find(class_='a-size-base po-break-word').text
                return brand 
        return None 

    def get_prices(self, center_col: BeautifulSoup, soup: BeautifulSoup) -> float:
        if soup is None:
            return None
        
        whole_price = soup.find(center_col, class_="a-price-whole")
        decimal_price = soup.find(center_col, class_="a-price-fraction")
        
        if whole_price and decimal_price:
            price = whole_price + decimal_price
            return price 
            
        return None 

    def get_reviews(self, center_col: BeautifulSoup) -> str:
        if center_col:
            num_reviews = center_col.find(id="acrCustomerReviewText")
            
            if num_reviews and num_reviews.has_attr('aria-label'):
                return num_reviews['aria-label']
        return None 

    def get_rating(self, center_col: BeautifulSoup) -> str:
        if center_col:
            product_rating = center_col.find(id="acrPopover")

            if product_rating and product_rating.has_attr('title'):
                return product_rating['title']
        return None 

    def get_product_upc(self, product_col: BeautifulSoup) -> str:
        if product_col:
            product_upc = product_col.find(class_="a-text-bold", string=lambda text: 'UPC' in text)

            if product_upc:
                return product_upc.find_next_sibling('span').text
        return None 

    def get_weight(self, product_col: BeautifulSoup) -> str: 
        if product_col:
            weight = product_col.find(class_="a-text-bold", string=lambda text: 'Unit' in text)
        
            if weight:
                return weight.find_next_sibling('span').text  
        return None 
    
    def get_bought_monthly(self, center_column: BeautifulSoup, id: str) -> str:
        if center_column is None:
            return None
        
        monthly_sales = center_column.find(id)

        if monthly_sales is None:
            return None
        
        return monthly_sales
    
    def get_description(self, center_column: BeautifulSoup, class_: str):
        if center_column is None:
            return None
        
        description = center_column.find(class_)

        if description is None:
            return None
        
        return description

    
    def get_product_data(self, soup: BeautifulSoup) -> dict[str:any]:
        """
        Get the product details from a listing 
        """
        """async proces 1 start"""

        # Get column where data to scrape is 
        center_col = self.get_center_column(soup)
        
        # Scrape info from the center column 
        title = self.get_title(center_col, soup)
        brand = self.get_brand(center_col)
        price = self.get_prices(center_col, soup)
        num_reviews = self.get_reviews(center_col) 
        product_rating = self.get_rating(center_col)
        bought_last_month = self.get_bought_monthly(center_col, id="social-proofing-faceout-title-tk_bought")
        description = self.get_description(center_col, class_="a-unordered-list a-vertical a-spacing-mini")
        """ async proces 1 end """

        """async proces 2 start"""
        # Scrape product details 
        product_col = self.get_product_column(soup)
        product_upc = self.get_product_upc(product_col)
        weight = self.get_weight(product_col)
        """async proces 2 end"""

        product_data = {
            "title": title,
            "brand": brand,
            "weight": weight,
            "price":  price, 
            "product_rating": product_rating,
            "bought_last_month": bought_last_month, 
            "num_reviews": num_reviews, 
            "description": description,
            "product_upc": product_upc,
        }

        return product_data

    

