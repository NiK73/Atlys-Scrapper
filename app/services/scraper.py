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
    """
    A service that scrapes product data from a specified URL and performs
    various operations such as cleaning product prices, saving data to storage, 
    and updating cache.
    """
    # BASE_URL = "https://dentalstall.com/shop/page/"

    def __init__(self, request):
        self.limit = request.limit
        self.BASE_URL = request.url
        self.proxy = request.proxy
        self.storage = StorageService()
        self.cache = CacheService()

    @retry(3, delay=5)  # Retry mechanism
    async def scrape_page(self, page_number):
        """
        Scrapes a single page of product data.

        This method makes an HTTP request to the specified URL for the page number, 
        follows redirects if necessary, and returns the HTML content of the page.
        """
        url = f"{self.BASE_URL}{page_number}/"
        async with httpx.AsyncClient(proxy=self.proxy, timeout=10, verify=False) as client:
            response = await client.get(url)
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
        """
        This method scrapes the pages for products, parses the product information, 
        cleans the product price, and saves the products to the storage. It also 
        updates the cache and sends notifications about the total number of products 
        scraped and updated.
        """
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

