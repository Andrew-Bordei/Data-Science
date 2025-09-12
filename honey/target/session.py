import requests
from headers import HEADERS
import random

class Session:
    def __init__(self, headers) -> None:
        self.user_agent = random.randint(0,10)
        self.headers = headers
        self.headers['User-Agent'] = HEADERS[self.user_agent].get('User-Agent')
        self.session = requests.Session()

    def return_page_safely(self, resp: requests.Session) -> dict:
        """Return the text from page if request is successful"""
        if resp.status_code == 200:
            return resp.text
        return None 
    
    def get_page(self, url: str, headers: dict[str, str]) -> dict[str, any]:
        """Send a request to Target.com for specific url page"""
        response = self.session.get(url, headers=headers)

        return self.return_page_safely(response)