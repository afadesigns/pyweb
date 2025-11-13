import aiohttp
from selectolax.parser import HTMLParser
import logging
from cachetools import TTLCache
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Configure logging
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.INFO)

async def scrape(session, url, selector, cache, use_cache, logger):
    if use_cache:
        cache_key = (url, selector)
        if cache_key in cache:
            logger.info(f"Cache hit for {url}")
            return cache[cache_key]

    logger.info(f"Cache miss for {url}")
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()

            tree = HTMLParser(content)
            if selector:
                elements = [node.text(strip=True) for node in tree.css(selector)]
            else:
                links = [node.attributes['href'] for node in tree.css('a[href]')]

            if selector:
                result = {"url": url, "selector": selector, "elements": elements}
            else:
                result = {"url": url, "links": links}
            
            if use_cache:
                cache[cache_key] = result
            return result
    except aiohttp.ClientError as e:
        return {"url": url, "error": f"An error occurred: {e}"}
    except Exception as e:
        return {"url": url, "error": f"An unexpected error occurred: {str(e)}"}

async def scrape_urls_concurrently(urls: list[str], selector: str = None, use_cache=True, logger=default_logger):
    cache = TTLCache(maxsize=100, ttl=600)
    async with aiohttp.ClientSession() as session:
        tasks = [scrape(session, url, selector, cache, use_cache, logger) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

def run_scrape(urls: list[str], selector: str = None, use_cache=True):
    return asyncio.run(scrape_urls_concurrently(urls, selector, use_cache))
