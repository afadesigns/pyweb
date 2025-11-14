# `pyweb` Benchmark Methodology

The performance claims made in this project are backed by a rigorous and transparent benchmarking methodology. This document explains how the benchmarks are conducted to ensure the results are accurate, reproducible, and fair.

## The Problem with Real-World Benchmarks

Initial benchmarks were run against a public website (`books.toscrape.com`). However, this approach proved to be unreliable for measuring the true performance of the scraper. The results were heavily influenced by factors outside of our control:

-   **Network Latency:** Internet latency is variable and unpredictable.
-   **Server Performance:** The target server's load and performance can fluctuate.
-   **Rate Limiting:** External servers may rate limit or block high-frequency requests.

These factors introduce significant noise into the measurements, making it impossible to isolate the performance of the client application itself.

## The Solution: A Controlled Local Environment

To eliminate external variables, we created a controlled, high-performance local benchmarking environment.

### 1. High-Performance Local Server

The benchmark is run against a local `aiohttp` server (`benchmarks/http_server.py`). This server is:
-   **Asynchronous:** Capable of handling a high number of concurrent requests without becoming a bottleneck.
-   **Local:** Runs on `127.0.0.1`, eliminating all network latency.
-   **Consistent:** Serves a static HTML file (`benchmarks/test_page.html`), ensuring every request is identical.

### 2. Fine-Grained Measurement

We measure two key metrics:

-   **Total Execution Time:** The wall-clock time to complete all 100 requests. This is measured in Python using `timeit.default_timer()`.
-   **Per-Request Latency:** The time taken for each individual request, from initiation to the completion of parsing. This is measured *inside* the Rust core using `std::time::Instant` for maximum precision.

### 3. Statistical Analysis

The per-request latencies are collected and analyzed using `numpy` to calculate:

-   **Average Latency:** The mean of all request latencies.
-   **Jitter (Standard Deviation):** A measure of the consistency of the latencies.
-   **Latency Threshold Violations:** The number of requests that exceeded a predefined threshold (50ms).

### 4. Competitor Fairness

The competitor (`httpx` + `selectolax`) is run in the exact same environment, against the same local server, with the same concurrency settings, to ensure a fair, apples-to-apples comparison.

This rigorous methodology ensures that our benchmark results accurately reflect the performance of the `pyweb` scraper itself, free from the noise and variability of the public internet.
