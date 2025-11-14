import asyncio
import httpx
from selectolax.parser import HTMLParser
import time

async def fetch(client, url):
    start_time = time.perf_counter()
    response = await client.get(url)
    end_time = time.perf_counter()
    return response.text, (end_time - start_time) * 1000 # return latency in ms

async def scrape_httpx(urls, selector, concurrency):
    limits = httpx.Limits(max_connections=concurrency, max_keepalive_connections=20)
    timeout = httpx.Timeout(30.0, connect=60.0)
    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        tasks = [fetch(client, url) for url in urls]
        pages_and_latencies = await asyncio.gather(*tasks)
        
        results = []
        latencies = []
        for page, latency in pages_and_latencies:
            tree = HTMLParser(page)
            elements = [node.text(strip=True) for node in tree.css(selector)]
            results.append(elements)
            latencies.append(latency)
        return results, latencies

def run_httpx_benchmark(urls, selector, concurrency):
    return asyncio.run(scrape_httpx(urls, selector, concurrency))
