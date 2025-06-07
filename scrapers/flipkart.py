import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def scrape_flipkart(query):
    url = f"https://www.flipkart.com/search?q={requests.utils.quote(query)}"
    r = requests.get(url, headers={ os.getenv("HEADERS"): os.getenv("HEADERS_USER_AGENT")}, timeout=100)
    soup = BeautifulSoup(r.text, "html.parser")
    items = []

    product_divs = soup.select("div.cPHDOP")

    if not product_divs:
        print(f"No product divs found on Flipkart for query: {query}. Check for CAPTCHA or HTML changes.")
        return []

    for div in product_divs[:6]:
        main_product = div.select_one("a.CGtC98")
        if main_product:
            title = main_product.select_one("div.KzDlHZ")
            price = main_product.select_one("div.Nx9bqj._4b5DiR")
            link = main_product.get("href")
            image = main_product.select_one("img.DByuf4").get("src")
        
            # Debugging prints
            # print(f"--- Product ---")
            # print(f"Title: {title}")
            # print(f"Price: {price}")
            # print(f"URL: {link}")
            # print(f"Image: {image}")
            # print("-" * 20)

            if title and price and link:
                items.append({
                    "title": title.get_text(strip=True),
                    "price": price.get_text(strip=True),
                    "site": "Flipkart",
                    "url": "https://www.flipkart.com" + link if link.startswith('/') else link,
                    "image": image if image else ""
                })
    return items