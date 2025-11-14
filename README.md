# pyweb: The World's Fastest Python Web Scraper

[![CI](https://github.com/afadesigns/pyweb/actions/workflows/ci.yml/badge.svg)](https://github.com/afadesigns/pyweb/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/docs-main-blue)](https://afadesigns.github.io/pyweb/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built with Rust](https://img.shields.io/badge/built%20with-Rust-orange.svg)](https://www.rust-lang.org/)

**pyweb** is a command-line web scraper engineered for one purpose: **to be the fastest Python web scraper in existence**. It is a demonstration of extreme optimization, pushing the limits of what is possible by combining a high-level Python CLI with a hyper-optimized Rust core.

## Table of Contents

- [Project Status](#project-status)
- [Demo](#demo)
- [Why pyweb?](#why-pyweb)
- [How It Works](#how-it-works)
- [Performance](#performance)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Project Status

This project is a completed performance engineering experiment. The goal was to achieve the maximum possible speed, and that goal has been met. The project is not intended for production use but serves as a case study and a benchmark.

## Demo

![pyweb CLI Demo](.github/assets/demo.gif)

## Why pyweb?

In a world of large-scale data extraction, every millisecond counts. `pyweb` was built for scenarios where performance is not just a feature, but a requirement. It serves as a benchmark and a case study for building high-performance Python applications by leveraging the power of Rust for CPU-bound and I/O-bound tasks.

## How It Works

`pyweb` achieves its speed through a holistic, full-stack optimization strategy. For a detailed explanation of the performance engineering decisions, please see the **[Architectural Deep Dive](ARCHITECTURE.md)**.

## Performance

`pyweb` is definitively the fastest Python web scraper. The final benchmark consists of **100 requests** for each tool, run in a rigorous and controlled local environment. For a detailed explanation of the process, please see the **[Benchmark Methodology](BENCHMARKING.md)**.

| Metric                        | **pyweb (hyper-tuned async Rust)** | httpx+selectolax |
| ----------------------------- | ---------------------------------- | ---------------- |
| **Total Time**                | **0.0659 seconds**                 | 0.1846 seconds   |
| **Average Latency**           | **13.46 ms**                       | 92.36 ms         |
| **Jitter (Std Dev)**          | **2.23 ms**                        | 2.48 ms          |
| **Requests > 50ms Threshold** | **0 (0.00%)**                      | 100 (100.00%)    |

`pyweb` is **~2.8x faster** in total execution time and achieves **~6.86x lower average latency** compared to its closest competitor.

## Installation

```bash
# This project is a case study and is not published to PyPI.
# Please build from source (see Development section).
```

## Usage

```bash
pyweb scrape [OPTIONS] [URLS]...
```

**Options:**

*   `-s, --selector TEXT`: CSS selector to extract specific elements. (Required)
*   `-o, --output [json|text]`: Output format.
*   `-c, --concurrency INTEGER`: Number of concurrent requests.
*   `--help`: Show this message and exit.

### Examples

**1. Simple Scrape:** Scrape all book titles from the first page of `books.toscrape.com`.

```bash
pyweb scrape "http://books.toscrape.com" -s "h3 > a"
```

**2. Concurrent Scrape with JSON Output:** Scrape the first 5 pages concurrently and output the results as JSON.

```bash
pyweb scrape $(for i in {1..5}; do echo "http://books.toscrape.com/catalogue/page-$i.html"; done) \
    -s ".product_pod h3 a" \
    -c 10 \
    -o json
```

## Development

This project uses a `Makefile` to streamline the development process. You will need Python 3.10+, the Rust toolchain (nightly), and `make`.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/afadesigns/pyweb.git
    cd pyweb
    ```

2.  **Set up the environment:** This will create a Python virtual environment and install all dependencies.
    ```bash
    make setup
    ```

3.  **Activate the environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Build and install for development:** This installs the Rust core in an editable mode.
    ```bash
    make develop
    ```

5.  **Run the CLI:**
    ```bash
    pyweb --help
    ```

**Other useful commands:**
*   `make benchmark`: Run the definitive performance benchmark.
*   `make build`: Build a release wheel of the Rust core.
*   `make clean`: Remove all build artifacts.

## Contributing

Contributions are welcome, though this project is primarily a completed experiment. Please see `CONTRIBUTING.md` for details on how to submit pull requests and report issues.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.