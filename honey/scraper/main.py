from amazon_scraper import AmazonScrapper
import time 

if __name__ == '__main__': 
    # To scrape 100 pages 5.5 hrs, 333 min
    start = time.time()
    amazon_scrapper = AmazonScrapper("2025-09-08")
    amazon_scrapper.main()
    end = time.time()
    print(f"Program executed in: {end-start} seconds")
    