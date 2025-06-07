import os 
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/temp/playwright"


from flask import Flask, request, jsonify
from scrapers.amazon import scrape_amazon
from scrapers.flipkart import scrape_flipkart

app = Flask(__name__)

@app.route("/scrape", methods=["GET"])
def scrape():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400
    
    results = []
    results.extend(scrape_amazon(query))
    results.extend(scrape_flipkart(query))

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)