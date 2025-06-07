from flask import Flask, request, jsonify
from scrapers.amazon import scrape_amazon
from scrapers.flipkart import scrape_flipkart
from scrapers.ebay import scrape_ebay

app = Flask(__name__)

@app.route("/scrape", methods=["GET"])
def scrape():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing 'q' query"}), 400
    

    try:
        results = scrape_amazon(query) + scrape_ebay(query) + scrape_flipkart(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)