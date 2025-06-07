from playwright.sync_api import sync_playwright

def scrape_amazon(query):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.amazon.in/s?k={query}")

        try:
            page.wait_for_selector("div.s-result-item[data-asin]", timeout=15000)
        except Exception as e:
            print(f"Failed to load search results page or find product items: {e}")
            browser.close()
            return []

        # print("div.s-result-item loaded successfully")
        
        items = page.query_selector_all("div.s-result-item[data-asin]")
        
        for item in items[:5]:
            title = item.query_selector("h2 span")
            price = item.query_selector(".a-price-whole")
            link = item.query_selector("a.a-link-normal.s-line-clamp-2")
            image = item.query_selector("img.s-image")

            title_text = title.inner_text() if title else None
            # print(f"title_text: {title_text}")
            price_text = price.inner_text() if price else None
            # print(f"price_test: {price_text}")

            # Get the full URL from the link element's href attribute
            link_url = link.get_attribute('href') if link else None

            # Ensure the link is relative and construct the full URL
            full_product_url = f"https://www.amazon.in{link_url}" if link_url and link_url.startswith('/') else link_url
            # print(f"full_product_url: {full_product_url}")

            image_src = image.get_attribute("src") if image else ""
            # print(f"image_src: {image_src}")

            if title and price and link:
                products.append({
                    "title": title_text,
                    "price": f"₹{price_text}",
                    "site": "Amazon",
                    "url": full_product_url,
                    "image": image_src,
                })

        browser.close()
    return products