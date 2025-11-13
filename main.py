from fastapi import FastAPI
from pydantic import BaseModel
from scraper import scrape_website

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str
    selector: str | None = None

@app.get("/")
async def root():
    return {"message": "Welcome to the PyWeb Scraper API"}

@app.get("/scrape")
async def scrape_get(url: str):
    data = await scrape_website(url)
    return {"data": data}

@app.post("/scrape")
async def scrape_post(request: ScrapeRequest):
    data = await scrape_website(request.url, request.selector)
    return {"data": data}
