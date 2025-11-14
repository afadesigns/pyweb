# pyweb: The World's Fastest Python Web Scraper

[![CI](https://github.com/afadesigns/pyweb/actions/workflows/ci.yml/badge.svg)](https://github.com/afadesigns/pyweb/actions/workflows/ci.yml)

**pyweb** is a command-line web scraper engineered for one purpose: **to be the fastest Python web scraper in existence**. It is a demonstration of extreme optimization, pushing the limits of what is possible by combining a high-level Python CLI with a hyper-optimized Rust core.

## Why pyweb?

In a world of large-scale data extraction, every millisecond counts. `pyweb` was built for scenarios where performance is not just a feature, but a requirement. It serves as a benchmark and a case study for building high-performance Python applications by leveraging the power of Rust for CPU-bound and I/O-bound tasks.

## How It Works

`pyweb` achieves its speed through a holistic optimization strategy spanning every layer of the stack:

*   **Hybrid Architecture:** A user-friendly Python CLI (`click`) acts as a wrapper around a high-performance, multi-threaded scraping core written in Rust.
*   **Asynchronous I/O:** The Rust core is built on `tokio`, a state-of-the-art asynchronous runtime, and uses the kernel's `io_uring` interface on Linux for the most efficient I/O operations possible.
*   **Optimized HTTP and TLS:** The `reqwest` client is fine-tuned to use a pure Rust TLS implementation (`rustls`) and is forced to use HTTP/1.1 to minimize connection latency for rapid, independent requests.
*   **Advanced Compiler Optimizations:** The Rust core is compiled with Profile-Guided Optimization (PGO), Link-Time Optimization (LTO), and native CPU-specific instruction sets to generate the most efficient machine code possible.
*   **High-Performance Memory Management:** The system's default memory allocator is replaced with `mimalloc`, which is designed for highly concurrent applications.
*   **Code Micro-Optimizations:** The Rust code is carefully written to eliminate unnecessary allocations and redundant work in the hot path, such as parsing CSS selectors only once.

## Performance

`pyweb` is definitively the fastest Python web scraper. The final benchmark, scraping 100 pages from a local `aiohttp` server, was conducted after applying advanced OS-level network tuning (`tcp_tw_reuse`, `tcp_fin_timeout`). The results below compare `pyweb` against the best-in-class pure-Python async solution (`httpx` + `selectolax`).

| Metric                        | **pyweb (hyper-tuned async Rust)** | httpx+selectolax |
| ----------------------------- | ---------------------------------- | ---------------- |
| **Total Time**                | **0.0659 seconds**                 | 0.1846 seconds   |
| **Average Latency**           | **13.46 ms**                       | 92.36 ms         |
| **Jitter (Std Dev)**          | **2.23 ms**                        | 2.48 ms          |
| **Requests > 50ms Threshold** | **0 (0.00%)**                      | 100 (100.00%)    |

`pyweb` is **~2.8x faster** in total execution time and achieves **~6.86x lower average latency** compared to its closest competitor.

## Installation

```bash
# Coming soon to PyPI!
# For now, please build from source (see Development section).
```

## Usage

```bash
pyweb scrape [OPTIONS] [URLS]...
```

**Options:**

*   `-s, --selector TEXT`: CSS selector to extract specific elements.
*   `-o, --output [json|text]`: Output format.
*   `-c, --concurrency INTEGER`: Number of concurrent requests.
*   `--help`: Show this message and exit.

**Example:**

```bash
# Scrape all book titles from the first page of books.toscrape.com
pyweb scrape "http://books.toscrape.com" -s "h3 > a" -c 200
```

## Development

To build and run `pyweb` from source, you will need Python 3.10+ and the Rust toolchain (nightly).

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/afadesigns/pyweb.git
    cd pyweb
    ```

2.  **Set up the Python environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Build the Rust core:**
    ```bash
    cd rust_scraper
    maturin develop
    ```

4.  **Run the CLI:**
    ```bash
    cd ..
    pyweb --help
    ```

## Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` for details on how to submit pull requests, report issues, and run benchmarks.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.