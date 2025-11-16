"""
The definitive performance benchmark for pyru.

This script runs a controlled, local benchmark to compare the performance of `pyru`
against a best-in-class pure-Python competitor (`httpx` + `selectolax`).

It starts a local `aiohttp` server to eliminate network latency and variability,
then makes a series of concurrent requests to it, measuring both total execution
time and per-request latency.
"""

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

from rust_scraper import scrape_urls_concurrent_h3
from competitor import scrape_httpx

# --- Benchmark Configuration ---
LOCAL_SERVER_PORT = 8000
BASE_URL = f"https://127.0.0.1:{LOCAL_SERVER_PORT}"
TEST_URL = f"{BASE_URL}/test_page.html"
RUNS = 100  # Number of pages to scrape
SELECTOR = "h3 > a"
LATENCY_THRESHOLD_MS = 50

async def run_benchmark(pyru_concurrency, httpx_concurrency):
    """
    Main async function to run and compare the real-world benchmarks.

    Args:
        pyru_concurrency (int): The concurrency level for the pyru benchmark.
        httpx_concurrency (int): The concurrency level for the httpx benchmark.
    """
    urls = [TEST_URL] * RUNS
    
    # --- pyru Benchmark ---
    start_time = timeit.default_timer()
    _results, pyru_latencies_ms = await scrape_urls_concurrent_h3(urls, SELECTOR, pyru_concurrency)
    pyru_total_time = timeit.default_timer() - start_time

    pyru_avg_latency = np.mean(pyru_latencies_ms)
    pyru_jitter = np.std(pyru_latencies_ms)
    pyru_exceeding_threshold = np.sum(np.array(pyru_latencies_ms) > LATENCY_THRESHOLD_MS)
    pyru_exceeding_percentage = (pyru_exceeding_threshold / RUNS) * 100
    
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
    print("\n--- pyru (tuned async Rust) ---")
    print(f"Total Time: {pyru_total_time:.4f} seconds")
    print(f"Average Latency: {pyru_avg_latency:.2f} ms")
    print(f"Jitter (Std Dev): {pyru_jitter:.2f} ms")
    print(f"Requests > {LATENCY_THRESHOLD_MS}ms: {pyru_exceeding_threshold} ({pyru_exceeding_percentage:.2f}%)")

    print("\n--- httpx+selectolax ---")
    print(f"Total Time: {httpx_total_time:.4f} seconds")
    print(f"Average Latency: {httpx_avg_latency:.2f} ms")
    print(f"Jitter (Std Dev): {httpx_jitter:.2f} ms")
    print(f"Requests > {LATENCY_THRESHOLD_MS}ms: {httpx_exceeding_threshold} ({httpx_exceeding_percentage:.2f}%)")

@click.command()
@click.option('--pyru-concurrency', '-c', default=175, help='Number of concurrent requests for pyru.')
@click.option('--httpx-concurrency', '-hc', default=175, help='Number of concurrent requests for httpx.')
def main(pyru_concurrency, httpx_concurrency):
    """
    Sync wrapper to start the local server and run the async benchmark.
    """
    server_process = None
    try:
        server_path = os.path.join(os.path.dirname(__file__), 'http_server.py')
        server_process = subprocess.Popen([sys.executable, server_path, "--http3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5) # Give the server time to start
        asyncio.run(run_benchmark(pyru_concurrency, httpx_concurrency))
    finally:
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()