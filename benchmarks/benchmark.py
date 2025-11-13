import timeit
import subprocess
import os
import sys
import click
import time

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust_scraper import scrape_urls_concurrent
from competitor import run_httpx_benchmark

# --- Benchmark Configuration ---
PORT = 8000
BASE_URL = f"http://127.0.0.1:{PORT}"
TEST_URL = f"{BASE_URL}/test_page.html"
RUNS = 1000
SELECTOR = "p.item"

def run_pyweb_benchmark(urls, selector):
    """Runs the benchmark for the pyweb scraper."""
    scrape_urls_concurrent(urls, selector)

def run_scrapy_benchmark(urls, selector):
    """Runs the benchmark for the Scrapy spider."""
    with open('urls.txt', 'w') as f:
        for url in urls:
            f.write(f"{url}\n")
            
    spider_path = os.path.join(os.path.dirname(__file__), 'scrapy_spider.py')
    command = [
        'scrapy', 'runspider', spider_path,
        '-a', f'selector={selector}',
        '--nolog'
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove('urls.txt')

@click.command()
def main():
    """Main function to run the benchmarks."""
    server_process = None
    try:
        server_path = os.path.join(os.path.dirname(__file__), 'http_server.py')
        server_process = subprocess.Popen(['python', server_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)

        urls = [TEST_URL] * RUNS
        
        pyweb_time = timeit.timeit(lambda: run_pyweb_benchmark(urls, SELECTOR), number=1)
        scrapy_time = timeit.timeit(lambda: run_scrapy_benchmark(urls, SELECTOR), number=1)
        httpx_time = timeit.timeit(lambda: run_httpx_benchmark(urls, SELECTOR), number=1)

        print("\n--- Benchmark Results ---")
        print(f"pyweb ({RUNS} runs): {pyweb_time:.4f} seconds")
        print(f"httpx+selectolax ({RUNS} runs): {httpx_time:.4f} seconds")
        print(f"Scrapy ({RUNS} runs): {scrapy_time:.4f} seconds")

    finally:
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()
