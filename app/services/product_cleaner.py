import re

class ProductCleaner:
    @staticmethod
    def clean_price(product: str) -> str:
        # Remove rupee sign and any non-numeric characters
        cleaned_price = re.sub(r"[^\d.]", "", product['price'])
        product['price'] = cleaned_price
        return product