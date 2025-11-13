import aiohttp
from bs4 import BeautifulSoup
import logging
from cachetools import TTLCache
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scraper:
    def __init__(self, cache_size=100, cache_ttl=600):
        self.cache = TTLCache(maxsize=cache_size, ttl=cache_ttl)

    async def scrape_website(self, url: str, selector: str = None):
        cache_key = (url, selector)
        if cache_key in self.cache:
            logger.info(f"Cache hit for {url}")
            return self.cache[cache_key]

        logger.info(f"Cache miss for {url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")

                    if selector:
                        elements = [element.text.strip() for element in soup.select(selector)]
                        result = {"url": url, "selector": selector, "elements": elements}
                    else:
                        links = [a["href"] for a in soup.find_all("a", href=True)]
                        result = {"url": url, "links": links}
                    
                    self.cache[cache_key] = result
                    return result
        except aiohttp.ClientError as e:
            return {"error": f"An error occurred: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

scraper = Scraper()

def run_scrape(url: str, selector: str = None):
    return asyncio.run(scraper.scrape_website(url, selector))
