import timeit
import subprocess
import os
import sys
import logging

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import run_scrape

# --- Benchmark Configuration ---
PORT = 8000
BASE_URL = f"http://127.0.0.1:{PORT}"
TEST_URL = f"{BASE_URL}/test_page.html"
RUNS = 100
SELECTOR = "p.item"

def run_pyweb_benchmark(urls, selector):
    """Runs the benchmark for the pyweb scraper."""
    run_scrape(urls, selector, use_cache=False)

def main():
    """Main function to run the benchmarks."""
    server_process = None
    try:
        # Start the local HTTP server
        server_path = os.path.join(os.path.dirname(__file__), 'http_server.py')
        server_process = subprocess.Popen(['python', server_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Give the server a moment to start
        import time
        time.sleep(1)

        # --- Run benchmark ---
        urls = [TEST_URL] * RUNS
        time = timeit.timeit(lambda: run_pyweb_benchmark(urls, SELECTOR), number=1)
        
        print("\n--- Benchmark Results ---")
        print(f"pyweb (selectolax, {RUNS} runs): {time:.4f} seconds")

    finally:
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()
