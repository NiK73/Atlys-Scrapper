import httpx
import json
from bs4 import BeautifulSoup
from app.services.storage import StorageService
from app.services.product_parser import ProductParserService
from app.services.product_cleaner import ProductCleaner
from app.services.cache import CacheService
from app.services.notifications import NotificationsService
from app.utils import retry
from app.config import settings

class ScraperService:
    # BASE_URL = "https://dentalstall.com/shop/page/"

    def __init__(self, request):
        self.limit = request.limit
        self.BASE_URL = request.url
        self.proxy = request.proxy
        self.storage = StorageService()
        self.cache = CacheService()

    @retry(3, delay=5)  # Retry mechanism
    async def scrape_page(self, page_number):
        url = f"{self.BASE_URL}{page_number}/"
        

        async with httpx.AsyncClient(proxies=self.proxy) as client:
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
        parser_config = settings.site_configs[self.BASE_URL]

        parser = ProductParserService(parser_config)
        updated_products = 0

        for page in range(1, self.limit + 1):
            html = await self.scrape_page(page)
            soup = BeautifulSoup(html, "html.parser")
            products = parser.parse(soup)
            for product in products:
                # self.storage.save(product)
                cleaned_product = ProductCleaner.clean_price(product)
                if not self.cache.is_updated(cleaned_product):
                    self.storage.save(cleaned_product)  # Save the product to storage
                    self.cache.update(cleaned_product)  # Update the cache
                    updated_products += 1
                scraped_products.append(cleaned_product)
        total_scraped_products = len(scraped_products)

        NotificationsService.send_notification(total_scraped_products, updated_products)

        return {"total_scraped": total_scraped_products, "updated_products": updated_products, "message": "Scraping completed."}

    # async def scrape(self):
    #     scraped_products = []
    #     for page in range(1, self.limit + 1):
    #         html = await self.scrape_page(page)
    #         # print("html - ", html)
    #         soup = BeautifulSoup(html, "html.parser")
    #         # print("soup - ", soup)
    #         products = self.parse_products(soup)
    #         for product in products:
    #             product_json = json.dumps(product)
    #             self.storage.save(product_json)
    #             # Check if product has been updated in the cache
    #             # if not self.cache.is_updated(product):
    #             #     self.storage.save(product)  # Save the product to storage
    #             #     self.cache.update(product)  # Update the cache
    #             scraped_products.append(product_json)

    #     # Return a summary of the scraping process
    #     return {"total_scraped": len(scraped_products), "message": "Scraping completed."}

    # def parse_products(self, soup):
    #     product_cards = soup.find_all("li", class_="product")  # Adjusted to target <li> elements with class "product"
    #     products = []

    #     for card in product_cards:
    #         title_tag = card.find("h2", class_="woo-loop-product__title")
    #         title = title_tag.text.strip() if title_tag else None

    #         # Extract product price (including discounted price if available)
    #         price_tag = card.find("span", class_="price")
    #         price = None
    #         if price_tag:
    #             price_value = price_tag.find("ins")
    #             if price_value:
    #                 price = price_value.text.strip()
    #             else:
    #                 price = price_tag.text.strip()

    #         # Extract product image URL (check for lazy-loaded images)
    #         image_tag = card.find("img")
    #         image_url = None
    #         if image_tag:
    #             # Check if the image has a lazy-loaded URL
    #             image_url = image_tag.get("data-lazy-src", image_tag.get("src"))

    #         # Extract product URL (link to the product page)
    #         product_url_tag = card.find("a", href=True)
    #         product_url = product_url_tag["href"] if product_url_tag else None

    #         # Append product data to the list
    #         products.append({
    #             "title": title,
    #             "price": price,
    #             "image_url": image_url,
    #             "product_url": product_url
    #         })
        
    #     return products




