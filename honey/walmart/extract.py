import requests 
import json
import time 
import random
from headers import create_headers

class Extract: 
    def __init__(self, start_page, end_page, query):
        self.start_page = start_page
        self.end_page = end_page
        self.query = query

    def build_url(self, page: int, query: str) -> str:
        url = f'https://www.walmart.com/orchestra/snb/graphql/Search/5744c0906433ffdb63324b75ef27012a487e5a424d630b497392b60423e66105/search?variables=%7B%22id%22%3A%22%22%2C%22affinityOverride%22%3A%22store_led%22%2C%22pap%22%3A%22%7B%5C%22polaris%5C%22%3A%7B%5C%22ms_max_page_within_rerank%5C%22%3A11%2C%5C%22ms_slp%5C%22%3A14%2C%5C%22ms_triggered%5C%22%3Atrue%7D%7D%22%2C%22dealsId%22%3A%22%22%2C%22query%22%3A%22{query}%22%2C%22nudgeContext%22%3A%22%22%2C%22page%22%3A{page}%2C%22prg%22%3A%22desktop%22%2C%22catId%22%3A%22%22%2C%22facet%22%3A%22%22%2C%22sort%22%3A%22best_match%22%2C%22rawFacet%22%3A%22%22%2C%22seoPath%22%3A%22%22%2C%22ps%22%3A40%2C%22limit%22%3A40%2C%22ptss%22%3A%22%22%2C%22trsp%22%3A%22%22%2C%22beShelfId%22%3A%22%22%2C%22recall_set%22%3A%22%22%2C%22module_search%22%3A%22%22%2C%22min_price%22%3A%22%22%2C%22max_price%22%3A%22%22%2C%22storeSlotBooked%22%3A%22%22%2C%22additionalQueryParams%22%3A%7B%22hidden_facet%22%3Anull%2C%22translation%22%3Anull%2C%22isMoreOptionsTileEnabled%22%3Atrue%2C%22isGenAiEnabled%22%3Atrue%2C%22rootDimension%22%3A%22%22%2C%22altQuery%22%3A%22%22%2C%22selectedFilter%22%3A%22%22%2C%22isModuleArrayReq%22%3Afalse%7D%2C%22searchArgs%22%3A%7B%22query%22%3A%22{query}%22%2C%22cat_id%22%3A%22%22%2C%22prg%22%3A%22desktop%22%2C%22facet%22%3A%22%22%7D%2C%22ffAwareSearchOptOut%22%3Afalse%2C%22fitmentFieldParams%22%3A%7B%22powerSportEnabled%22%3Atrue%2C%22dynamicFitmentEnabled%22%3Atrue%2C%22extendedAttributesEnabled%22%3Atrue%2C%22fuelTypeEnabled%22%3Afalse%7D%2C%22fitmentSearchParams%22%3A%7B%22id%22%3A%22%22%2C%22affinityOverride%22%3A%22store_led%22%2C%22pap%22%3A%22%7B%5C%22polaris%5C%22%3A%7B%5C%22ms_max_page_within_rerank%5C%22%3A11%2C%5C%22ms_slp%5C%22%3A14%2C%5C%22ms_triggered%5C%22%3Atrue%7D%7D%22%2C%22dealsId%22%3A%22%22%2C%22query%22%3A%22{query}%22%2C%22nudgeContext%22%3A%22%22%2C%22page%22%3A{page}%2C%22prg%22%3A%22desktop%22%2C%22catId%22%3A%22%22%2C%22facet%22%3A%22%22%2C%22sort%22%3A%22best_match%22%2C%22rawFacet%22%3A%22%22%2C%22seoPath%22%3A%22%22%2C%22ps%22%3A40%2C%22limit%22%3A40%2C%22ptss%22%3A%22%22%2C%22trsp%22%3A%22%22%2C%22beShelfId%22%3A%22%22%2C%22recall_set%22%3A%22%22%2C%22module_search%22%3A%22%22%2C%22min_price%22%3A%22%22%2C%22max_price%22%3A%22%22%2C%22storeSlotBooked%22%3A%22%22%2C%22additionalQueryParams%22%3A%7B%22hidden_facet%22%3Anull%2C%22translation%22%3Anull%2C%22isMoreOptionsTileEnabled%22%3Atrue%2C%22isGenAiEnabled%22%3Atrue%2C%22rootDimension%22%3A%22%22%2C%22altQuery%22%3A%22%22%2C%22selectedFilter%22%3A%22%22%2C%22isModuleArrayReq%22%3Afalse%7D%2C%22searchArgs%22%3A%7B%22query%22%3A%22{query}%22%2C%22cat_id%22%3A%22%22%2C%22prg%22%3A%22desktop%22%2C%22facet%22%3A%22%22%7D%2C%22ffAwareSearchOptOut%22%3Afalse%2C%22cat_id%22%3A%22%22%2C%22_be_shelf_id%22%3A%22%22%7D%2C%22enableFashionTopNav%22%3Afalse%2C%22enableRelatedSearches%22%3Atrue%2C%22enablePortableFacets%22%3Atrue%2C%22enableFacetCount%22%3Atrue%2C%22fetchMarquee%22%3Atrue%2C%22fetchSkyline%22%3Atrue%2C%22fetchGallery%22%3Afalse%2C%22fetchSbaTop%22%3Atrue%2C%22fetchSBAV1%22%3Afalse%2C%22enableAdsPromoData%22%3Afalse%2C%22fetchDac%22%3Afalse%2C%22tenant%22%3A%22WM_GLASS%22%2C%22enableMultiSave%22%3Afalse%2C%22enableInStoreShelfMessage%22%3Afalse%2C%22enableSellerType%22%3Afalse%2C%22enableItemRank%22%3Afalse%2C%22enableAdditionalSearchDepartmentAnalytics%22%3Atrue%2C%22enableFulfillmentTagsEnhacements%22%3Afalse%2C%22enableRxDrugScheduleModal%22%3Afalse%2C%22enablePromoData%22%3Atrue%2C%22enableSignInToSeePrice%22%3Afalse%2C%22enablePromotionMessages%22%3Afalse%2C%22enableItemLimits%22%3Afalse%2C%22enableCanAddToList%22%3Afalse%2C%22enableIsFreeWarranty%22%3Afalse%2C%22enableShopSimilarBottomSheet%22%3Afalse%2C%22pageType%22%3A%22SearchPage%22%7D'
        return url 
    
    def request_api(self, url: str, headers: dict[str, str]) -> dict[str, any]:
        response = requests.request('GET', url, headers=headers)

        data = json.loads(response.text)
        return data 
    
    def safely_traverse_dict(self, data: dict[str, any], *keys) -> any:
        for key in keys:
            try:
                value = data[key]
            except (KeyError, TypeError):
                return None
        return value
    
    def get_num_products(self, data: dict[str,any]) -> int:
        try: 
            num_products = len(data['data']['search']['searchResult']['itemStacks'][0]['itemsV2'])
        except:
            num_products = 0
        return num_products
    
    def extract_data(self, data: dict[str,any], num_products: int) -> dict[str,any]: 
        extracted_data = []

        for j in range(0, num_products):
            dict_path = data['data']['search']['searchResult']['itemStacks'][0]['itemsV2'][j]
            name = self.safely_traverse_dict(dict_path, 'name')
            item_id = self.safely_traverse_dict(dict_path, 'usItemId')
            brand = self.safely_traverse_dict(dict_path, 'brand')
            rating = self.safely_traverse_dict(dict_path, 'averageRating')
            num_reviews = self.safely_traverse_dict(dict_path, 'numberOfReviews')
            price = self.safely_traverse_dict(dict_path, 'priceInfo', 'currentPrice', 'price')
            price_per_ounce = self.safely_traverse_dict(dict_path, 'priceInfo', 'unitPrice', 'price')

            product_data = {
                "name":name, 
                "item_id":item_id, 
                "brand":brand, 
                "rating":rating, 
                "num_reviews":num_reviews, 
                "price":price, 
                "price_per_ounce":price_per_ounce
            }
            extracted_data.append(product_data)
        return extracted_data

    def extraction_process(self) -> dict[str,any]:
        all_data = []

        for page in range(self.start_page, self.end_page):
            print(f"Getting data on page: {page}")
            url = self.build_url(page, self.query)

            headers = create_headers(self.query, page)

            page_data = self.request_api(url, headers)

            num_products = self.get_num_products(page_data)

            product_data = self.extract_data(page_data, num_products)

            all_data.append(product_data)
            time.sleep(random.uniform(0.25, 5))
        return all_data
