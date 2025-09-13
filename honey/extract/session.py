import json
import requests
from amazon.headers import HEADERS
import random

class Session:
    def __init__(self, headers) -> None:
        # self.payload = payload
        self.user_agent = random.randint(0,10)
        self.headers = headers
        self.headers['User-Agent'] = HEADERS[self.user_agent].get('User-Agent')
        self.session = requests.Session()

    def return_data_safely(self, resp: requests.Session) -> dict:
        if resp.status_code == 200:
            return resp.text
        return None 
    
    def kroger_get_gtins_endpoint(self, url: str, headers: dict[str, str]) -> dict:
        response = self.session.get(url, headers=headers)

        return self.return_data_safely(response) 
    
    def kroger_get_products(self, gtins_list: list[str], headers: dict[str, str]) -> dict[str, any]:
        all_data = []

        for i in range(0, len(gtins_list), 10):
            url = "https://www.kroger.com/atlas/v1/product/v2/products?" \
            f"filter.gtin13s={gtins_list[i]}&filter.gtin13s={gtins_list[i+1]}&filter.gtin13s={gtins_list[i+2]}&" \
            f"filter.gtin13s={gtins_list[i+3]}&filter.gtin13s={gtins_list[i+4]}&filter.gtin13s={gtins_list[i+5]}&" \
            f"filter.gtin13s={gtins_list[i+6]}&filter.gtin13s={gtins_list[i+7]}&filter.gtin13s={gtins_list[i+8]}&" \
            f"&filter.gtin13s={gtins_list[i+9]}&filter.verified=true"

            resp = self.session.get(url, headers=headers)

            if resp.status_code == 200: 
                data = json.loads(resp.text)
                all_data.append(data)
        return all_data
    