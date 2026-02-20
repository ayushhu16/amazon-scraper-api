import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MediaSpaceAPI:

    def __init__(self, search, min_price, max_price):
        self.search = search
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        }

    def build_search_url(self):
        query = self.search.replace(" ", "+")
        return f"https://mediaspace.mu/?s={query}"

    def scrape(self):
        url = self.build_search_url()
        try:
            response = requests.get(url, headers=self.headers, timeout=8)
            response.raise_for_status()
        except Exception as e:
            return {"error": f"Request failed: {e}"}

        soup = BeautifulSoup(response.text, "lxml")
        products = []

        # MediaSpace product cards
        for card in soup.select(".product-item"):  # CSS selector for each product
            try:
                title_tag = card.select_one(".product-title a")
                price_tag = card.select_one(".price")
                link_tag = card.select_one(".product-title a")

                if not title_tag or not price_tag:
                    continue

                title = title_tag.text.strip()
                price_text = price_tag.text.strip().replace("Rs", "").replace(",", "").strip()
                price = float(price_text)
                link = link_tag['href']

                if self.min_price <= price <= self.max_price:
                    products.append({
                        "title": title,
                        "price": price,
                        "link": link
                    })
            except:
                continue

        best_item = None
        if products:
            best_item = min(products, key=lambda x: x["price"])

        return {
            "title": self.search,
            "date": datetime.utcnow().isoformat(),
            "products": products,
            "best_item": best_item
        }
