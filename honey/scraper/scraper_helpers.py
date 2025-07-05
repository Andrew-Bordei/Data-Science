from bs4 import BeautifulSoup
import requests 
from urllib.parse import urlparse, parse_qs
import sys 
from scraper_helpers import *

sys.path.append('../')

COOKIE = "" \
    "session-id=137-9572815-1085150; session-id-time=2082787201l; i18n-prefs=USD; lc-main=en_US; " \
    "ubid-main=130-7709812-5953729; session-token=udgNEPRoDVj7UoZc8yKe9XGrabqlfTvcmvb5gCWaYZ0SqWeFj5K5fCPBLZikUzqqiAy4Vt+S606217iHDVl/ZxBb6ikml2PRjb5AMJZ81HfESPxffSKbC/eLFipObdZFruAejM/uNZB9RdtC81FZ7K1GX1f8hdlpQIdQBsfWYmHTavUQv6Z2+oCz9kpBk5oPUYeZDl7fA8FhJl9/qEWvaaOhW9EgNSc1UReajtafqIJPNEToPL0z6rkgmQhFRSZX1ffGFo/N1xyZn25BozP7RB28Oyoh6JpSpm5PPPpwtjtsL6cUgA8Otici2+T3IIqwyvMu/ypJjtF7MDCMiTiynVlFfKCBjB8Y; " \
    "skin=noskin; csm-hit=tb:s-QP5GGN147SM2MMVFYGVR|1751647071320&t:1751647071415&adb:adblk_no; rxc=AAci5pMnxA8YrBeuhG0"

# Likely need to cycle through several different headers to change where requests are coming from
HEADERS = {
    "Accept" : "*/*", 
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Referer": "https://www.amazon.com/",
    "Connection": "keep-alive",
    # "Cookie": f"{COOKIE}",
}

# Get site cookies 
SESSION = requests.Session()
SESSION.get("https://www.amazon.com")

BASE_URL = "https://www.amazon.com"

seen_urls = set()

def get_session(url: str, headers: dict[str:str], session: requests) -> BeautifulSoup:
    # Get the page html return as soup object
    response = session.get(url, headers = headers)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup 

def get_center_column(soup: BeautifulSoup) -> BeautifulSoup:
    # Get column where data to scrape is 
    center_col = soup.find(id="centerCol")

    if center_col:
        return center_col
    
    return None

def get_product_column(soup: BeautifulSoup) -> BeautifulSoup:
    # Scrape product details column 
    product_col = soup.find(id="detailBullets_feature_div")

    if product_col: 
        return product_col
    
    return None 

def get_data_safely(soup, **identifier):
    if soup is None:
        return None
    
    data = soup.find(**identifier)

    if data is None:
        return None 
    return data.text

def get_title(center_col: BeautifulSoup) -> str: 
    # Scrape title 
    title = get_data_safely(center_col, id="productTitle")

    return title 

def get_brand(center_col: BeautifulSoup) -> str: 
    if center_col:
        brand = center_col.find(class_="a-spacing-small po-brand")
        if brand: 
            brand = brand.find(class_='a-size-base po-break-word').text
            return brand 
    return None 

def get_prices(center_col: BeautifulSoup) -> float:
    whole_price = get_data_safely(center_col, class_="a-price-whole")
    decimal_price = get_data_safely(center_col, class_="a-price-fraction")
    
    if whole_price and decimal_price:
        price = whole_price + decimal_price
        return price 
    return None 

def get_reviews(center_col: BeautifulSoup) -> str:
    if center_col:
        num_reviews = center_col.find(id="acrCustomerReviewText")
        
        if num_reviews and num_reviews.has_attr('aria-label'):
            return num_reviews['aria-label']
    return None 

def get_rating(center_col: BeautifulSoup) -> str:
    if center_col:
        product_rating = center_col.find(id="acrPopover")

        if product_rating and product_rating.has_attr('title'):
            return product_rating['title']
    return None 

def get_product_upc(product_col: BeautifulSoup) -> str:
    if product_col:
        product_upc = product_col.find(class_="a-text-bold", string=lambda text: 'UPC' in text)

        if product_upc:
            return product_upc.find_next_sibling('span').text
    return None 

def get_weight(product_col: BeautifulSoup) -> str: 
    if product_col:
        weight = product_col.find(class_="a-text-bold", string=lambda text: 'Unit' in text)
    
        if weight:
            return weight.find_next_sibling('span').text  
    return None 

def get_seller_rank(product_col: BeautifulSoup) -> str: 
    if product_col:
        seller_rank = product_col.find(class_="a-text-bold", string=lambda text: 'Sellers' in text)

        if seller_rank: 
            return seller_rank
    return None 

def get_product_link(query: str, page) -> list[str]:
    """
    Get the product links for each listing on a webpage
    """
    product_urls = []
    
    # Specify the product page we're scraping  
    amazon_query = f"https://www.amazon.com/s?k={query}&page={page}"
    
    # Get the page html 
    soup = get_session(amazon_query, HEADERS, SESSION)

    for link in soup.find_all(class_='a-link-normal s-line-clamp-3 s-link-style a-text-normal', href=True):
    # Product link is sponsored, it's tracked closely by Amazon for advertising data 
    # It should bypass the redirect and go directly to the product
    # This is a weak area in the code, that I'm not sure is the best route, should be improved later 
        if "/sspa/" in link['href']:
            params = parse_qs(urlparse(link['href']).query)
            full_url = "https://www.amazon.com" + params.get('url', [''])[0]  
        
        if "https" in link['href']:
            full_url = link['href']
        else:
            full_url = BASE_URL + link['href']
        
        if full_url not in seen_urls:
            product_urls.append(full_url)

    return product_urls

"""This can be threaded"""
def get_product_data(url: str) -> dict[str:str]:
    """
    Get the product details from a listing 
    """
    # Get the page html 
    soup = get_session(url, HEADERS, SESSION)

    """async proces 1 start"""
   # Get column where data to scrape is 
    center_col = get_center_column(soup)
    
    # Scrape info from the center column 
    title = get_title(center_col)
    brand = get_brand(center_col)
    price = get_prices(center_col)
    num_reviews = get_reviews(center_col) 
    product_rating = get_rating(center_col)
    bought_last_month = get_data_safely(center_col, id="social-proofing-faceout-title-tk_bought")
    description = get_data_safely(center_col, class_="a-unordered-list a-vertical a-spacing-mini")
    """ async proces 1 end """

    """async proces 2 start"""
    # Scrape product details 
    product_col = get_product_column(soup)
    product_upc = get_product_upc(product_col)
    weight = get_weight(product_col)
    """async proces 2 end"""

    product_data = {
        "title": title,
        "brand": brand,
        "weight": weight,
        "price":  price, 
        "product_rating": product_rating,
        "bought_last_month": bought_last_month, 
        "num_reviews": num_reviews, 
        # "seller_rank": seller_rank,
        "description": description,
        "product_upc": product_upc,
    }

    return product_data

def scrape(total_pages_scrape: int) -> list[dict[str:any]]:
    page = 1 
    scraped_data = []

    while True: 
        # Can this be threaded? 
        product_links = get_product_link(f"honey", page)
        if page > total_pages_scrape:
            break 

        for link in product_links: 
            print(f"Page {page}: ", link)
            if link not in seen_urls:
                seen_urls.add(link)
                product_data = get_product_data(link)
                scraped_data.append(product_data)
        page += 1 
    return scraped_data
    