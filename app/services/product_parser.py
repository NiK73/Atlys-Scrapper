class ProductParserService:
    """
    A service for parsing product data from an HTML soup based on a given configuration.

    This class is responsible for parsing product information from an HTML document
    (BeautifulSoup object) by dynamically extracting fields as per the provided configuration.
    """
    def __init__(self, config):
        self.config = config

    def parse(self, soup):
        """
        This method finds product cards in the HTML, extracts the specified fields (e.g., name, price, etc.),
        and returns a list of products with their corresponding details.
        """
        product_cards = soup.find_all(
            self.config["product_container"]["tag"], 
            class_=self.config["product_container"]["class"]
        )
        products = []

        for card in product_cards:
            product = {}
            # Extract fields dynamically based on the configuration
            for field, field_config in self.config["fields"].items():
                tag = field_config.get("tag")
                class_name = field_config.get("class")
                attribute = field_config.get("attribute", None)
                
                element = card.find(tag, class_=class_name)
                if attribute:
                    product[field] = element.get(attribute) if element else None
                else:
                    product[field] = element.text.strip() if element else None

            image_tag = card.find("img")
            if image_tag:
                # Check for lazy-loaded images (data-lazy-src or fallback to src)
                image_url = image_tag.get("data-lazy-src", image_tag.get("src"))
                product["image_url"] = image_url if image_url else None

            products.append(product)
        
        return products
