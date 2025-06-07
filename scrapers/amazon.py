import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def scrape_amazon(query):
    url = f"https://www.amazon.in/s?k={requests.utils.quote(query)}"
    r = requests.get(url, headers={ os.getenv("HEADERS"): os.getenv("HEADERS_USER_AGENT")}, timeout=5)
    soup = BeautifulSoup(r.text, "html.parser")
    items = []

    product_divs = soup.select("div.s-result-item[data-asin]")

    if not product_divs:
        print(f"No product divs found for query: {query}")
        return []
    

    for div in product_divs[:6]:
        title = div.select_one("a.a-link-normal h2 span")
        price = div.select_one("span.a-price-whole")
        link = div.select_one("a.a-link-normal")
        image = div.select_one("img.s-image")

        product_data = {
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
            "site": "Amazon",
            "url": "https://www.amazon.in" + link["href"] if link and link.has_attr("href") else None,
            "image": image["src"] if image and image.has_attr("src") else None
        }

        if title and price and link:
            items.append(product_data)
        
        # Debugging prints - keep for now to verify
        # print(f"--- Product ---")
        # print(f"Title: {product_data['title']}")
        # print(f"Price: {product_data['price']}")
        # print(f"URL: {product_data['url']}")
        # print(f"Image: {product_data['image']}")
        # print("-" * 20)
        
    return items