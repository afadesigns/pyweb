from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from scraper import scraper

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ScrapeRequest(BaseModel):
    url: str
    selector: str | None = None

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/scrape", response_class=HTMLResponse)
async def scrape_post(request: Request, url: str = Form(...), selector: str = Form(None)):
    data = await scraper.scrape_website(url, selector)
    return templates.TemplateResponse(request, "results.html", {"results": data})

@app.get("/health")
async def health_check():
    return {"status": "ok"}
