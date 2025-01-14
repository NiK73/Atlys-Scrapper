import redis

class CacheService:
    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, db=0)

    def is_updated(self, product):
        print("product - ", product)
        key = product["title"]
        cached_price = self.client.get(key)
        if cached_price:
            cached_price = cached_price.decode('utf-8')  # Decoding the byte string to a regular string
    
        print("cached_price - ", cached_price, product["price"])
        return cached_price and cached_price == product["price"]

    def update(self, product):
        key = product["title"]
        self.client.set(key, product["price"])
