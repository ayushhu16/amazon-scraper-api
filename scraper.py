import requests
from bs4 import BeautifulSoup
from datetime import datetime


class AmazonAPI:
    def __init__(self, search, min_price=0, max_price=999999):
        self.search = search
        self.min_price = float(min_price)
        self.max_price = float(max_price)

        self.base_url = "https://www.amazon.de/s"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def build_url(self):
        return f"{self.base_url}?k={self.search.replace(' ', '+')}"

    def scrape(self):
        url = self.build_url()

        response = requests.get(url, headers=self.headers, timeout=15)
        soup = BeautifulSoup(response.text, "lxml")

        products = []

        items = soup.select("div.s-result-item")

        for item in items:
            title = item.select_one("h2 span")
            price_whole = item.select_one(".a-price-whole")
            price_fraction = item.select_one(".a-price-fraction")
            link = item.select_one("h2 a")

            if not title or not price_whole:
                continue

            price_text = price_whole.text.replace(".", "")
            if price_fraction:
                price_text += "." + price_fraction.text

            try:
                price = float(price_text)
            except:
                continue

            if not (self.min_price <= price <= self.max_price):
                continue

            product = {
                "title": title.text.strip(),
                "price": price,
                "link": "https://www.amazon.de" + link["href"] if link else None
            }

            products.append(product)

        best_item = min(products, key=lambda x: x["price"]) if products else None

        return {
            "title": self.search,
            "date": datetime.utcnow().isoformat(),
            "filters": {
                "min": self.min_price,
                "max": self.max_price
            },
            "base_link": self.base_url,
            "best_item": best_item,
            "products": products
        }
