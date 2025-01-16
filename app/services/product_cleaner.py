import re

class ProductCleaner:
    @staticmethod
    def clean_price(product: str) -> str:
        """
        Cleans the price of a product by removing any non-numeric characters 
        (except for the decimal point) and returns the cleaned price.
        Args:
            product (str): A dictionary containing product information, with a 
                           'price' field that is a string representation of the price.

        Returns:
            str: The product dictionary with the 'price' field cleaned to only 
                 contain numeric characters and a decimal point.
        """
        # Remove rupee sign and any non-numeric characters
        cleaned_price = re.sub(r"[^\d.]", "", product['price'])
        product['price'] = cleaned_price
        return product