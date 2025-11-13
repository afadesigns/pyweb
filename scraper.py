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
        self.session = None

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close_session(self):
        if self.session:
            await self.session.close()

    async def scrape_website(self, url: str, selector: str = None):
        cache_key = (url, selector)
        if cache_key in self.cache:
            logger.info(f"Cache hit for {url}")
            return self.cache[cache_key]

        logger.info(f"Cache miss for {url}")
        try:
            session = await self._get_session()
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
            return {"url": url, "error": f"An error occurred: {e}"}
        except Exception as e:
            return {"url": url, "error": f"An unexpected error occurred: {str(e)}"}

    async def scrape_urls_concurrently(self, urls: list[str], selector: str = None):
        tasks = [self.scrape_website(url, selector) for url in urls]
        results = await asyncio.gather(*tasks)
        await self.close_session()
        return results

scraper = Scraper()

def run_scrape(urls: list[str], selector: str = None):
    if len(urls) == 1:
        return [asyncio.run(scraper.scrape_website(urls[0], selector))]
    return asyncio.run(scraper.scrape_urls_concurrently(urls, selector))
