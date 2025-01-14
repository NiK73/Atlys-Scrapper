from pydantic import BaseModel, Field

class ScraperRequest(BaseModel):
    limit: int = Field(default=None, description="Number of pages to scrape")
    proxy: str = Field(default=None, description="Proxy string to use for scraping")

class ScraperResponse(BaseModel):
    total_scraped: int
    message: str
