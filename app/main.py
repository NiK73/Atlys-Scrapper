from fastapi import FastAPI, Depends, HTTPException
from app.services.scraper import ScraperService
from app.models import ScraperRequest, ScraperResponse
from app.config import settings

app = FastAPI()

class Request:
    def __init__(self, limit, proxy):
        self.limit = limit
        self.proxy = proxy

def authenticate(token: str):
    if token != settings.API_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")

@app.post("/scrape", response_model=ScraperResponse)
async def scrape_data(request: ScraperRequest, token: str = Depends(authenticate)):
    request = Request(limit=5, proxy="http://your-proxy-url:port")
    scraper = ScraperService(request)
    result = await scraper.scrape()
    return result
