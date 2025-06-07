import os 
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/render/project/.cache/playwright"

from playwright.sync_api import sync_playwright

def scrape_flipkart(query):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.flipkart.com/search?q={query}")
        try:
            page.wait_for_selector(".cPHDOP", timeout=15000) 
        except Exception as e:
            print(f"Failed to load search results page or find product items: {e}")
            browser.close()
            return []

        # print(f"cPHDOP loaded successfully")

        items = page.query_selector_all(".cPHDOP")

        for item in items[:5]:
            title = item.query_selector(".KzDlHZ")
            price = item.query_selector(".Nx9bqj._4b5DiR")
            link = item.query_selector("a.CGtC98")
            image = item.query_selector("img.DByuf4")

            title_text = title.inner_text() if title else None
            # print(f"title_text: {title_text}")

            price_text = price.inner_text() if price else None
            # print(f"price_text: {price_text}")

            # Get the full URL from the link element's href attribute
            link_url = link.get_attribute('href') if link else None

            # Ensure the link is relative and construct the full URL
            full_product_url = f"https://www.flipkart.com{link_url}" if link_url and link_url.startswith('/') else link_url
            # print(f"full_product_url: {full_product_url}")

            image_src = image.get_attribute("src") if image else ""
            # print(f"image_src: {image_src}")

            if title and price and link:
                products.append({
                    "title": title.inner_text() if title else "",
                    "price": price.inner_text() if price else "",
                    "site": "Flipkart",
                    "url": full_product_url,
                    "image": image_src,
                })

        browser.close()
    return products