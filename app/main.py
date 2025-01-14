from fastapi import FastAPI, Depends, HTTPException, Header
from app.services.scraper import ScraperService
from app.models import ScraperRequest, ScraperResponse
from app.config import settings

app = FastAPI()

class Request:
    def __init__(self, limit, proxy, url):
        self.limit = limit
        self.proxy = proxy
        self.url = url

def authenticate(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header is missing")
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer" or token != settings.API_TOKEN:
            raise HTTPException(status_code=403, detail="Unauthorized")
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")

@app.post("/scrape", response_model=ScraperResponse)
async def scrape_data(
    request: ScraperRequest,
    token: str = Depends(authenticate)):
    request = Request(limit=request.limit, proxy=request.proxy, url=request.url)
    scraper = ScraperService(request)
    result = await scraper.scrape()
    return result
