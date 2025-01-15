from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    API_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str


    site_configs: Dict[str, Dict] = {
        "https://dentalstall.com/shop/page/": {
            "product_container": {"tag": "li", "class": "product"},
            "fields": {
                "title": {"tag": "h2", "class": "woo-loop-product__title"},
                "price": {"tag": "span", "class": "price"},
                "image_url": {"tag": "img", "attribute": "src"},
                "product_url": {"tag": "a", "attribute": "href"}
            }
        },
        "site2": {
            "product_container": {"tag": "div", "class": "product-item"},
            "fields": {
                "title": {"tag": "p", "class": "product-title"},
                "price": {"tag": "span", "class": "product-price"},
                "image_url": {"tag": "img", "attribute": "data-src"},
                "product_url": {"tag": "a", "attribute": "data-link"}
            }
        }
    }

    class Config:
        env_file = ".env"

settings = Settings()
