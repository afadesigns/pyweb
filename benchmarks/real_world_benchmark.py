import timeit
import click
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust_scraper import scrape_urls_concurrent
from competitor import run_httpx_benchmark

# --- Benchmark Configuration ---
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
RUNS = 50  # 50 pages
SELECTOR = "h3 > a"

@click.command()
def main():
    """Main function to run the real-world benchmarks."""
    urls = [BASE_URL.format(i) for i in range(1, RUNS + 1)]
    
    # --- pyweb Benchmark ---
    pyweb_time = timeit.timeit(lambda: scrape_urls_concurrent(urls, SELECTOR), number=1)
    
    # --- httpx Benchmark ---
    httpx_time = timeit.timeit(lambda: run_httpx_benchmark(urls, SELECTOR), number=1)

    print("\n--- Real-World Benchmark Results ---")
    print(f"Scraping {RUNS} pages from books.toscrape.com")
    print(f"pyweb: {pyweb_time:.4f} seconds")
    print(f"httpx+selectolax: {httpx_time:.4f} seconds")

if __name__ == "__main__":
    main()
