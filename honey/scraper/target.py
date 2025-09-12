import pandas as pd 
import json 
import sys
from datetime import datetime


from target.extract import Extract
from target.session import Session

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
  'Accept': 'application/json',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Referer': 'https://www.target.com/s?searchTerm=honey',
  'Origin': 'https://www.target.com',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'Sec-GPC': '1',
  'Priority': 'u=4',
  'TE': 'trailers',
}

if __name__ == '__main__': 
    date = datetime.today().strftime('%Y-%m-%d')

    ext = Extract()
    session = Session(headers)

    all_data = []

    for offset in range(0, 265, 24):
        url = "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&include_sponsored=false" \
        f"&keyword=honey&new_search=true&offset={offset}&page=%2Fs%2Fhoney&pricing_store_id=1457&useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A140.0%29+" \
        "Gecko%2F20100101+Firefox%2F140.0&visitor_id=01982362E05F0201B59980DC5DA58A50"

        data = session.get_page(url, session.headers)
        json_data = json.loads(data)

        target_data = ext.extract_data(json_data)
        all_data.extend(target_data)

    scraped_df = pd.DataFrame(all_data, 
        columns = [
            "title", "brand",'price','price_per_oz', 'rating',
            'num_reviews','product_type','tcin'
        ]
    )
    scraped_df.to_csv(f'target_data_{date}.csv') 
