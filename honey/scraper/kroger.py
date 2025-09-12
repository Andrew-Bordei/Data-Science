from Data_Science.honey.extract.extract import Extract
from Data_Science.honey.extract.session import Session

gtin_headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'X-Kroger-Channel': 'WEB',
  'x-laf-object': '[{"modality":{"type":"PICKUP","handoffLocation":{"storeId":"03400375","facilityId":"14258"},"handoffAddress":{"address":{"addressLines":["11565 S Highway 6"],"cityTown":"Sugar Land","name":"West Airport","postalCode":"77498","stateProvince":"TX","residential":false,"countryCode":"US"},"location":{"lat":29.6479694,"lng":-95.6494359}}},"sources":[{"storeId":"03400375","facilityId":"14258"}],"assortmentKeys":["03400375"],"listingKeys":["03400375"]}]',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-GPC': '1',
  'TE': 'trailers'
}

product_headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'x-laf-object': '[{"modality":{"type":"PICKUP","handoffLocation":{"storeId":"03400375","facilityId":"14258"},"handoffAddress":{"address":{"addressLines":["11565 S Highway 6"],"cityTown":"Sugar Land","name":"West Airport","postalCode":"77498","stateProvince":"TX","residential":false,"countryCode":"US"},"location":{"lat":29.6479694,"lng":-95.6494359}}},"sources":[{"storeId":"03400375","facilityId":"14258"}],"assortmentKeys":["03400375"],"listingKeys":["03400375"]}]',
  'User-Time-Zone': 'America/Chicago',
  'X-Kroger-Channel': 'WEB',
  'x-call-origin': '{"component":"internal search","page":"internal search"}',
  'x-modality': '{"type":"PICKUP","locationId":"03400375"}',
  'x-modality-type': 'PICKUP',
  'X-Facility-Id': '03400375',
  'Connection': 'keep-alive',
  'Referer': 'https://www.kroger.com/search?query=honey&searchType=previous_searches',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-GPC': '1',
  'TE': 'trailers'
}

gtin_url = "https://www.kroger.com/atlas/v1/search/v1/products-search?filter.query=honey&filter.fulfillmentMethods=IN_STORE&filter.fulfillmentMethods=PICKUP&filter.fulfillmentMethods=DELIVERY&page.offset=0&page.size=24"



sess = Session()
ext = Extract()

gtin_page = sess.kroger_get_gtins_endpoint(gtin_url, gtin_headers)
list_gtins = ext.kroger_extract_gtins(gtin_page)

product_page = sess.kroger_get_products(list_gtins, product_headers)



