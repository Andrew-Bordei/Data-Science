import json
import requests
from bs4 import BeautifulSoup

class Extract:
    # def __init__(self, headers, payload):
    #     self.headers = headers 
    #     self.payload = payload
    def __init__(self):
        pass

    def kroger_extract_gtins(self, json_data: dict[str:any]) -> list[str]:
        gtins_list = []

        num_items = len(json_data['data']['productsSearch'])

        for i in range(0,num_items):
            gtin = json_data['data']['productsSearch'][i]['upc']
            gtins_list.append(gtin)
        return gtins_list
    
    def kroger_extract_data(self, json_data: list[str:any]) -> list[dict[str:any]]:
        all_data = []
        num_prods = len(json_data["data"]['products'])
        base_path = json_data['data']['products']

        for i in range(0, num_prods):
            title = self.safely_traverse_dict(base_path[i], 'item', 'description')
            brand = self.safely_traverse_dict(base_path[i], 'item', 'brand', 'name')
            price = self.safely_traverse_dict(base_path[i], 'price', 'storePrices', 'regular', 'unitPrice')
            price_per_oz = self.safely_traverse_dict(base_path[i], 'price', 'storePrices', 'regular', 'equivalizedUnitPriceString')
            size = self.safely_traverse_dict(base_path[i], 'item', 'customerFacingSize')
            avg_rating = self.safely_traverse_dict(base_path[i], 'item', 'ratingsAndReviewsAggregate', 'averageRating')
            num_reviews = self.safely_traverse_dict(base_path[i], 'item', 'ratingsAndReviewsAggregate', 'numberOfReviews')
            num_inventory = self.safely_traverse_dict(base_path[i], 'inventory', 'locations', 0, 'available')
            inventory_status = self.safely_traverse_dict(base_path[i], 'inventory', 'locations', 0, 'stockLevel')
            sub_commodity = self.safely_traverse_dict(base_path[i], 'item', 'familyTree', 'subCommodity', 'name')
            country_origin = self.safely_traverse_dict(base_path[i], 'item', 'countriesOfOrigin')
            upc = self.safely_traverse_dict(base_path[i], 'item', 'upc')

            product_data = {
                "title": title, 
                "brand": brand, 
                "price": price,  
                "price_per_oz": price_per_oz,  
                "size": size, 
                "avg_rating": avg_rating, 
                "num_reviews": num_reviews, 
                "num_inventory": num_inventory, 
                "inventory_status": inventory_status, 
                "country_origin": country_origin, 
                "sub_commodity": sub_commodity, 
                "upc": upc
            }
            all_data.append(product_data)
        return all_data

    """Amazon functions"""
    def build_page_url(self, page: int) -> str: 
        return f"https://www.amazon.com/s/query?k=honey&page={page}"
    
    def build_asin_url(self, asin: str) -> str: 
        return f"https://www.amazon.com/dp/{asin}"
    
    def get_search_page(self, url):
        response = requests.request("POST", url, headers=self.headers, data=self.payload)

        return response.text
    
    def parse_page(self, data):
        # Split by '&&&' and strip whitespace
        split_data = [s.strip() for s in data.split('&&&') if s.strip()]
        
        parsed_data = []
        for string in split_data:
            try:
                parsed_item = json.loads(string)
                parsed_data.append(parsed_item)
            except:
                print(f"Error parsing JSON: {string}")
        return parsed_data
    
    def get_asin(self, data):
        asin_list = []
        parsed_data = self.parse_page(data)

        for i in range(2,len(parsed_data)):
            try:
                asin = parsed_data[i][2]['asin']
                asin_list.append(asin)
            except:
                continue
        return asin_list 

    def get_product_column(self, soup: BeautifulSoup) -> BeautifulSoup:
        # Scrape product details column 
        product_col = soup.find(id="detailBullets_feature_div")

        if product_col: 
            return product_col
        return None 

    def get_brand(self, soup: BeautifulSoup) -> str: 
        if soup:
            brand = soup.find(class_="a-spacing-small po-brand")

            if brand: 
                brand = brand.find(class_='a-size-base po-break-word')
                if brand: 
                    return brand.text 
        return None 

    def get_prices(self, soup: BeautifulSoup) -> float:
        if soup:
            whole_price = soup.find(class_="a-price-whole")
            decimal_price = soup.find(class_="a-price-fraction")
        
            if whole_price and decimal_price:
                price = whole_price.text + decimal_price.text
                return price 
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
    
    def get_food_sellers_rank(self, soup: BeautifulSoup):
        if soup: 
            rank = soup.find_all(class_="a-list-item")
            food_rank = [item for item in rank if "Grocery & Gourmet Food (See" in item.get_text()]
            
            if food_rank: 
                return food_rank[0].text
        return None
    
    def get_data(soup: BeautifulSoup, *args, **kwargs: any):
        if soup: 
            data = soup.find(kwargs=kwargs)
            if data:
                return data['title'] if args == 'rating' else data.text
        return None
 
    def get_product_data(self, soup: BeautifulSoup, asin: str) -> dict[str:any]:
        """Get the product details from a listing """
        title = self.get_data(soup, id="productTitle")
        brand = self.get_brand(soup)
        price = self.get_prices(soup)
        num_reviews = self.get_data(soup, id="acrCustomerReviewText")
        product_rating = self.get_data(soup, 'rating', id="acrPopover")
        bought_last_month = self.get_data(soup, id="social-proofing-faceout-title-tk_bought")
        description = self.get_data(soup, id="productDescription")

        product_col = self.get_product_column(soup)
        product_upc = self.get_product_upc(product_col)
        weight = self.get_weight(product_col)

        honey_seller_rank = self.get_data(soup, class_="a-unordered-list a-nostyle a-vertical zg_hrsr")
        food_rank = self.get_food_sellers_rank(soup)
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
            "honey_seller_rank":honey_seller_rank,
            "food_rank": food_rank,
            "asin": asin,
        }
        return product_data
