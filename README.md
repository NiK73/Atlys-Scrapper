Web Scraper Project
This project is a web scraper designed to extract product data from various e-commerce websites and store the data in a storage system. 
It supports proxy usage for better anonymity and bypassing restrictions. 
The project is built using FastAPI, httpx, and BeautifulSoup for web scraping.

Prerequisites
Before you begin, ensure you have the following installed on your machine:

Python 3.8 or later
Redis (for caching)
Required Python libraries (listed below)

Setup Instructions

1. Clone the Repository
First, clone the repository to your local machine:

2. Install Dependencies - 
pip install -r requirements.txt

3. Configure Redis - 
redis-server

4. Running the Project - 
uvicorn main:app --reload

5. Scraping Data API -
curl  -X POST \
  'http://127.0.0.1:8000/scrape' \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "limit": 1,
    "proxy": "http://proxy-server:port",
    "url": "https://dentalstall.com/shop/page/"
}' 
