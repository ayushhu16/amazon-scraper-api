import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MediaSpaceAPI:

    def __init__(self, search, min_price, max_price):
        self.search = search
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def build_search_url(self):
        return f"https://mediaspace.mu/?s={self.search}"

    def scrape(self):
        url = self.build_search_url()

        try:
            response = requests.get(url, headers=self.headers, timeout=8)
        except:
            return {"error": "Request failed"}

        soup = BeautifulSoup(response.text, "lxml")

        return {
            "title": self.search,
            "date": datetime.utcnow().isoformat(),
            "products": []
        }
