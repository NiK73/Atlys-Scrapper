import httpx
import json
from bs4 import BeautifulSoup
from app.services.storage import StorageService
from app.services.cache import CacheService
from app.utils import retry

class ScraperService:
    BASE_URL = "https://dentalstall.com/shop/page/"

    def __init__(self, request):
        self.limit = request.limit
        self.proxy = request.proxy
        self.storage = StorageService()
        self.cache = CacheService()

    @retry(3, delay=5)  # Retry mechanism
    async def scrape_page(self, page_number):
        url = f"{self.BASE_URL}{page_number}/"
        # If a proxy is provided, use httpx.Proxy

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            print("response - ", response)
            if response.status_code == 301:
                # Extract the new URL from the 'Location' header
                redirect_url = response.headers.get('Location')
                print(f"Redirected to: {redirect_url}")
                # Follow the redirect manually
                response = await client.get(redirect_url)
                # print("response 2 - ", response.text)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.text

    async def scrape(self):
        scraped_products = []
        for page in range(1, self.limit + 1):
            html = await self.scrape_page(page)
            # print("html - ", html)
            soup = BeautifulSoup(html, "html.parser")
            # print("soup - ", soup)
            products = self.parse_products(soup)
            for product in products:
                product_json = json.dumps(product)
                self.storage.save(product_json)
                # Check if product has been updated in the cache
                # if not self.cache.is_updated(product):
                #     self.storage.save(product)  # Save the product to storage
                #     self.cache.update(product)  # Update the cache
                scraped_products.append(product_json)

        # Return a summary of the scraping process
        return {"total_scraped": len(scraped_products), "message": "Scraping completed."}

    def parse_products(self, soup):
        product_cards = soup.find_all("li", class_="product")  # Adjusted to target <li> elements with class "product"
        products = []

        for card in product_cards:
            # Extract product title
            title_tag = card.find("h2", class_="woo-loop-product__title")
            title = title_tag.text.strip() if title_tag else None

            # Extract product price (including discounted price if available)
            price_tag = card.find("span", class_="price")
            price = None
            if price_tag:
                price_value = price_tag.find("ins")
                if price_value:
                    price = price_value.text.strip()
                else:
                    price = price_tag.text.strip()

            # Extract product image URL (check for lazy-loaded images)
            image_tag = card.find("img")
            image_url = None
            if image_tag:
                # Check if the image has a lazy-loaded URL
                image_url = image_tag.get("data-lazy-src", image_tag.get("src"))

            # Extract product URL (link to the product page)
            product_url_tag = card.find("a", href=True)
            product_url = product_url_tag["href"] if product_url_tag else None

            # Append product data to the list
            products.append({
                "title": title,
                "price": price,
                "image_url": image_url,
                "product_url": product_url
            })
        
        return products
