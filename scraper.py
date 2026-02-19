import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class AmazonAPI:
    def __init__(self, search_term, min_price, max_price):
        self.base_url = "https://www.amazon.de/"
        self.search_term = search_term
        self.min_price = min_price
        self.max_price = max_price

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=chrome_options)

        self.price_filter = f"&rh=p_36%3A{min_price}00-{max_price}00"

    def run(self):
        try:
            links = self.get_product_links()
            products = self.get_products_info(links)
            return products
        finally:
            self.driver.quit()

    def get_product_links(self):
        self.driver.get(self.base_url)

        search_box = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search_box.send_keys(self.search_term)
        search_box.send_keys(Keys.ENTER)

        time.sleep(3)

        self.driver.get(f"{self.driver.current_url}{self.price_filter}")
        time.sleep(3)

        results = self.driver.find_elements(By.XPATH, "//h2/a")

        links = [r.get_attribute("href") for r in results if r.get_attribute("href")]

        return links[:10]  # limit to 10 products for speed

    def get_products_info(self, links):
        products = []

        for link in links:
            try:
                self.driver.get(link)
                time.sleep(2)

                title = self.driver.find_element(By.ID, "productTitle").text
                price = self.get_price()
                seller = self.get_seller()

                products.append({
                    "title": title,
                    "price": price,
                    "seller": seller,
                    "url": link
                })

            except Exception:
                continue

        return products

    def get_price(self):
        try:
            price = self.driver.find_element(By.ID, "priceblock_ourprice").text
        except NoSuchElementException:
            try:
                price = self.driver.find_element(By.CLASS_NAME, "a-price-whole").text
            except:
                return None

        price = price.replace("€", "").replace(",", ".").strip()
        try:
            return float(price)
        except:
            return None

    def get_seller(self):
        try:
            return self.driver.find_element(By.ID, "bylineInfo").text
        except:
            return "Unknown"
