import timeit
import click
import sys
import os
import asyncio

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust_scraper import scrape_urls_concurrent
from competitor import run_httpx_benchmark

# --- Benchmark Configuration ---
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
RUNS = 50  # 50 pages
SELECTOR = "h3 > a"

async def run_benchmark(concurrency):
    """Main async function to run the real-world benchmarks."""
    urls = [BASE_URL.format(i) for i in range(1, RUNS + 1)]
    
    # --- pyweb Benchmark ---
    start_time = timeit.default_timer()
    await scrape_urls_concurrent(urls, SELECTOR, concurrency)
    pyweb_time = timeit.default_timer() - start_time
    
    # --- httpx Benchmark ---
    start_time = timeit.default_timer()
    await asyncio.to_thread(run_httpx_benchmark, urls, SELECTOR)
    httpx_time = timeit.default_timer() - start_time

    print("\n--- Real-World Benchmark Results ---")
    print(f"Scraping {RUNS} pages from books.toscrape.com")
    print(f"pyweb (concurrency={concurrency}): {pyweb_time:.4f} seconds")
    print(f"httpx+selectolax: {httpx_time:.4f} seconds")

@click.command()
@click.option('--concurrency', '-c', default=100, help='Number of concurrent requests for pyweb.')
def main(concurrency):
    """Sync wrapper to run the async benchmark."""
    asyncio.run(run_benchmark(concurrency))

if __name__ == "__main__":
    main()
