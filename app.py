from flask import Flask, jsonify, request
from scraper import AmazonAPI

app = Flask(__name__)

@app.route("/")
def home():
    return "Amazon Scraper API is running!"

@app.route("/scrape")
def scrape():
    search = request.args.get("search", "PS4")
    min_price = request.args.get("min", "275")
    max_price = request.args.get("max", "650")

    scraper = AmazonAPI(search, min_price, max_price)
    data = scraper.run()

    best_item = None
    if data:
        valid_prices = [p for p in data if p["price"]]
        if valid_prices:
            best_item = min(valid_prices, key=lambda x: x["price"])

    return jsonify({
        "search": search,
        "filters": {
            "min": min_price,
            "max": max_price
        },
        "best_item": best_item,
        "products": data
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
