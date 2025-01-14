import redis

class CacheService:
    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, db=0)

    def is_updated(self, product):
        key = product["product_title"]
        cached_price = self.client.get(key)
        return cached_price and cached_price == product["product_price"]

    def update(self, product):
        key = product["product_title"]
        self.client.set(key, product["product_price"])
