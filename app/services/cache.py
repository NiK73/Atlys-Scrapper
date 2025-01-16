import redis
from app.config import settings

class CacheService:
    """
    This class provides methods to check if a product's price is up-to-date in the cache 
    and to update the cache with the latest price for a given product.
    """
    def __init__(self):
        self.client = redis.Redis.from_url(settings.REDIS_URL)
    def is_updated(self, product):
        """
        This method retrieves the cached price of the product from Redis and compares it
        with the current price of the product. If they match, it indicates that the product's 
        price is up-to-date in the cache.
        """
        key = product["title"]
        cached_price = self.client.get(key)
        if cached_price:
            cached_price = cached_price.decode('utf-8')  # Decoding the byte string to a regular string
    
        return cached_price and cached_price == product["price"]

    def update(self, product):
        """
        This method stores the product's title as the cache key and its price as the cache value 
        in Redis. This is used to keep the cache up-to-date with the latest price for the product.
        """
        key = product["title"]
        self.client.set(key, product["price"])
