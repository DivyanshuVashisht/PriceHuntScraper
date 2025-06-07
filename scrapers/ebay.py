import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def scrape_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={requests.utils.quote(query)}"
    headers = {
        os.getenv("HEADERS"): os.getenv("HEADERS_USER_AGENT"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        items = []

        product_divs = soup.select("ul.srp-results li.s-item") 

        if not product_divs:
            print(f"No product items found for query: {query} on eBay. Check selectors or page structure. Status Code: {r.status_code}")
            return []

        # Iterate over the first 6 product items found
        for div in product_divs[:6]: 
            
           title = div.select_one("div.s-item__title")
           unwanted_prefix = "New Listing"
           if title.get_text(strip=True).startswith(unwanted_prefix):
               cleaned_title = title.get_text(strip=True)[len(unwanted_prefix):].strip()
           else:
               cleaned_title = title.get_text(strip=True) # If "New Listing" is not there, use the full text

           price = div.select_one("span.s-item__price").get_text(strip=True)
           link = div.select_one("div.s-item__info a.s-item__link")["href"]
           image = div.select_one("div.s-item__image-wrapper img")["src"]
           
           # Debugging prints - keep for now to verify
           print(f"--- Product ---")            
           print(f"Title: {cleaned_title}")
           print(f"Price: {price}")
           print(f"URL: {link}")
           print(f"Image: {image}")
           print("-" * 20)
           
           # Create the product data dictionary
           product_data = {
              "title": cleaned_title,
              "price": price,
              "site": "eBay", 
              "url": link if link else None,
              "image": image
           }

           # Only append if essential data is found
           if product_data["title"] and product_data["price"] and product_data["url"]:
                items.append(product_data)
        return items

    except Exception as e:
        print(f"Error scraping Ebay: {e}")
        return []
