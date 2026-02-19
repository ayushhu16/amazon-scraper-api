from flask import Flask, request, jsonify
from scraper import AmazonAPI

app = Flask(__name__)

@app.route("/")
def home():
    return "Amazon Scraper API Running"

@app.route("/scrape")
def scrape():
    search = request.args.get("search", "PS5")
    min_price = request.args.get("min", 0)
    max_price = request.args.get("max", 999999)

    scraper = AmazonAPI(search, min_price, max_price)
    data = scraper.scrape()

    return jsonify(data)
