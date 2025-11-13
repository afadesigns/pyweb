import timeit
import subprocess
import os
import sys
import click
import time
import http.client

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust_scraper import scrape as rust_scrape

# --- Benchmark Configuration ---
PORT = 8000
BASE_URL = f"127.0.0.1:{PORT}"
TEST_URL = f"/test_page.html"
RUNS = 1000
SELECTOR = "p.item"

def run_pyweb_benchmark(urls, selector):
    """Runs the benchmark for the pyweb scraper."""
    conn = http.client.HTTPConnection(BASE_URL)
    for _ in urls:
        conn.request("GET", TEST_URL)
        response = conn.getresponse()
        data = response.read()
        # The rust_scrape function expects a URL, so we'll just pass the test URL
        rust_scrape(f"http://{BASE_URL}{TEST_URL}", selector)
    conn.close()

def run_scrapy_benchmark(urls, selector):
    """Runs the benchmark for the Scrapy spider."""
    with open('urls.txt', 'w') as f:
        for url in urls:
            f.write(f"http://{BASE_URL}{TEST_URL}\n")
            
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
        time.sleep(3)

        urls = [TEST_URL] * RUNS
        
        pyweb_time = timeit.timeit(lambda: run_pyweb_benchmark(urls, SELECTOR), number=1)
        scrapy_time = timeit.timeit(lambda: run_scrapy_benchmark(urls, SELECTOR), number=1)

        print("\n--- Benchmark Results ---")
        print(f"pyweb (Rust, {RUNS} runs): {pyweb_time:.4f} seconds")
        print(f"Scrapy ({RUNS} runs): {scrapy_time:.4f} seconds")

    finally:
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()
