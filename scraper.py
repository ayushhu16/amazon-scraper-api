import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MediaSpaceAPI:
    def __init__(self, search, min_price=0, max_price=999999):
        self.search = search.lower()
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.base_url = "https://mediaspace.mu/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def build_search_url(self):
        # Mediaspace doesn’t have a search query param like Amazon.
        # So we go to the main shop and filter manually.
        return self.base_url + "shop/"

    def parse_price(self, text):
        try:
            # remove currency and formatting
            price = text.replace("₨", "").replace(",", "").strip()
            return float(price)
        except:
            return None

    def scrape(self):
        url = self.build_search_url()
        response = requests.get(url, headers=self.headers, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")

        products = []

        # find product blocks (these usually have price and title)
        for item in soup.select("li.product"):
            title_el = item.select_one("h2.woocommerce-loop-product__title")
            price_el = item.select_one("span.woocommerce-Price-amount")
            link_el = item.select_one("a.woocommerce-LoopProduct-link")

            if not title_el or not price_el or not link_el:
                continue

            title = title_el.text.strip()

            # only include products matching search term
            if self.search not in title.lower():
                continue

            price = self.parse_price(price_el.text)
            link = link_el["href"]

            # price filter check
            if price is None or not (self.min_price <= price <= self.max_price):
                continue

            products.append({
                "title": title,
                "price": price,
                "link": link
            })

        # Determine best (lowest price)
        best_item = None
        if products:
            products = sorted(products, key=lambda x: x["price"])
            best_item = products[0]

        return {
            "title": self.search,
            "date": datetime.utcnow().isoformat(),
            "filters": {
                "min": self.min_price,
                "max": self.max_price
            },
            "base_link": url,
            "best_item": best_item,
            "products": products
        }
