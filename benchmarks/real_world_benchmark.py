import timeit
import click
import sys
import os
import asyncio
import numpy as np
import subprocess
import time

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust_scraper import scrape_urls_concurrent
from competitor import scrape_httpx

# --- Benchmark Configuration ---
LOCAL_SERVER_PORT = 8000
BASE_URL = f"http://127.0.0.1:{LOCAL_SERVER_PORT}"
TEST_URL = f"{BASE_URL}/test_page.html"
RUNS = 100  # 100 pages
SELECTOR = "h3 > a"
LATENCY_THRESHOLD_MS = 50

async def run_benchmark(pyweb_concurrency, httpx_concurrency):
    """Main async function to run the real-world benchmarks."""
    urls = [TEST_URL] * RUNS
    
    # --- pyweb Benchmark ---
    start_time = timeit.default_timer()
    _results, pyweb_latencies_ms = await scrape_urls_concurrent(urls, SELECTOR, pyweb_concurrency)
    pyweb_total_time = timeit.default_timer() - start_time

    pyweb_avg_latency = np.mean(pyweb_latencies_ms)
    pyweb_jitter = np.std(pyweb_latencies_ms)
    pyweb_exceeding_threshold = np.sum(np.array(pyweb_latencies_ms) > LATENCY_THRESHOLD_MS)
    pyweb_exceeding_percentage = (pyweb_exceeding_threshold / RUNS) * 100
    
    # --- httpx Benchmark ---
    start_time = timeit.default_timer()
    _httpx_results, httpx_latencies_ms = await scrape_httpx(urls, SELECTOR, httpx_concurrency)
    httpx_total_time = timeit.default_timer() - start_time

    httpx_avg_latency = np.mean(httpx_latencies_ms)
    httpx_jitter = np.std(httpx_latencies_ms)
    httpx_exceeding_threshold = np.sum(np.array(httpx_latencies_ms) > LATENCY_THRESHOLD_MS)
    httpx_exceeding_percentage = (httpx_exceeding_threshold / RUNS) * 100

    print("\n--- Real-World Benchmark Results ---")
    print(f"Scraping {RUNS} pages from local aiohttp server")
    print(f"Latency Threshold: {LATENCY_THRESHOLD_MS}ms")
    print("\n--- pyweb (tuned async Rust) ---")
    print(f"Total Time: {pyweb_total_time:.4f} seconds")
    print(f"Average Latency: {pyweb_avg_latency:.2f} ms")
    print(f"Jitter (Std Dev): {pyweb_jitter:.2f} ms")
    print(f"Requests > {LATENCY_THRESHOLD_MS}ms: {pyweb_exceeding_threshold} ({pyweb_exceeding_percentage:.2f}%) ")

    print("\n--- httpx+selectolax ---")
    print(f"Total Time: {httpx_total_time:.4f} seconds")
    print(f"Average Latency: {httpx_avg_latency:.2f} ms")
    print(f"Jitter (Std Dev): {httpx_jitter:.2f} ms")
    print(f"Requests > {LATENCY_THRESHOLD_MS}ms: {httpx_exceeding_threshold} ({httpx_exceeding_percentage:.2f}%) ")

@click.command()
@click.option('--pyweb-concurrency', '-c', default=50, help='Number of concurrent requests for pyweb.')
@click.option('--httpx-concurrency', '-hc', default=200, help='Number of concurrent requests for httpx.')
def main(pyweb_concurrency, httpx_concurrency):
    """Sync wrapper to run the async benchmark."""
    server_process = None
    try:
        server_path = os.path.join(os.path.dirname(__file__), 'http_server.py')
        server_process = subprocess.Popen([sys.executable, server_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2) # Give the server time to start
        asyncio.run(run_benchmark(pyweb_concurrency, httpx_concurrency))
    finally:
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()
