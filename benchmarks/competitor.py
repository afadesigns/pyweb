import asyncio
import httpx
from selectolax.parser import HTMLParser

async def fetch(client, url):
    response = await client.get(url)
    return response.text

async def scrape_httpx(urls, selector):
    limits = httpx.Limits(max_connections=1000, max_keepalive_connections=20)
    timeout = httpx.Timeout(30.0, connect=60.0)
    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        tasks = [fetch(client, url) for url in urls]
        pages = await asyncio.gather(*tasks)
        
        results = []
        for page in pages:
            tree = HTMLParser(page)
            elements = [node.text(strip=True) for node in tree.css(selector)]
            results.append(elements)
        return results

def run_httpx_benchmark(urls, selector):
    return asyncio.run(scrape_httpx(urls, selector))
