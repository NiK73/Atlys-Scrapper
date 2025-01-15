import redis
from app.config import settings

class CacheService:
    def __init__(self):
        self.client = redis.Redis.from_url(settings.REDIS_URL)
    def is_updated(self, product):
        key = product["title"]
        cached_price = self.client.get(key)
        if cached_price:
            cached_price = cached_price.decode('utf-8')  # Decoding the byte string to a regular string
    
        return cached_price and cached_price == product["price"]

    def update(self, product):
        key = product["title"]
        self.client.set(key, product["price"])
