import json
from session import Session
from constants import START_OFFSET, END_OFFSET, STEP

class Extract:
    def safely_traverse_dict(self, data: dict[str: any], *keys) -> any:
        for key in keys:
            try:
                data = data[key]
            except KeyError:
                return None
        return data
    
    def extract_data(self, json_data: dict[str:any]) -> list[dict[str:any]]:
        data = []
        base_path = json_data['data']['search']['products']

        for i in range(0, len(base_path)):
            title = self.safely_traverse_dict(base_path[i], 'item', 'product_description', 'title')
            brand = self.safely_traverse_dict(base_path[i], 'item', 'primary_brand', 'name')
            price = self.safely_traverse_dict(base_path[i], 'price', 'current_retail')
            price_per_oz = self.safely_traverse_dict(base_path[i], 'price', 'formatted_unit_price')
            rating = self.safely_traverse_dict(base_path[i], 'ratings_and_reviews', 'statistics', 'rating', 'average')
            num_reviews = self.safely_traverse_dict(base_path[i], 'ratings_and_reviews', 'statistics', 'rating', 'count')
            product_type = self.safely_traverse_dict(base_path[i], 'item', 'product_classification', 'item_type', 'name')
            tcin = self.safely_traverse_dict(base_path[i], 'tcin')

            product_data = {
                "title": title,
                "brand": brand,
                "price": price,
                "price_per_oz": price_per_oz, 
                "rating": rating, 
                "num_reviews": num_reviews,
                "product_type": product_type,
                "tcin": tcin
            }
            data.append(product_data)
        return data
    
    def build_url(self, offset: int, query: str) -> str: 
        url = f"https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&include_sponsored=false" \
        f"&keyword={query}&new_search=true&offset={offset}&page=%2Fs%2F{query}&pricing_store_id=1457&useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A140.0%29+" \
        "Gecko%2F20100101+Firefox%2F140.0&visitor_id=01982362E05F0201B59980DC5DA58A50"

        return url
    
    def traverse_all_pages(self, session: Session, query: str) -> list[any]:
        """Get all the pages with product data from the website"""
        all_data = []
    
        for offset in range(START_OFFSET, END_OFFSET, STEP): 
            url = self.build_url(offset, query)
            page = session.get_page(url, session.headers)
            
            # load website page 
            json_data = json.loads(page)

            data = self.extract_data(json_data)
            all_data.extend(data)
        return all_data
    