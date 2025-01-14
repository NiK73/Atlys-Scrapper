from pydantic import BaseModel, Field

class ScraperRequest(BaseModel):
    limit: int = Field(default=None, description="Number of pages to scrape")
    proxy: str = Field(default=None, description="Proxy string to use for scraping")
    url: str = Field(default=None, description="URL to scrape")

class ScraperResponse(BaseModel):
    total_scraped: int
    updated_products: int
    message: str
