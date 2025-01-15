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

