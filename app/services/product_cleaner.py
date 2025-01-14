import re

class ProductCleaner:
    @staticmethod
    def clean_price(product: str) -> str:
        """
        This function removes the rupee sign and any extra characters,
        leaving only the numeric value (with decimals if applicable).
        """
        # Remove rupee sign and any non-numeric characters
        cleaned_price = re.sub(r"[^\d.]", "", product['price'])
        product['price'] = cleaned_price
        return product