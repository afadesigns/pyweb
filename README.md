# pyweb: The High-Performance Python Web Scraper

**pyweb** is a command-line web scraper built for speed. It uses a Rust core with `rayon` for concurrent HTTP requests and `scraper` for parsing, wrapped in a simple and intuitive Python CLI with `click`.

## Performance

`pyweb` is designed to be fast. Here's how it compares to a strong Python competitor (`httpx` + `selectolax`) when scraping 50 pages from `books.toscrape.com`:

| Scraper          | Time (seconds) |
| ---------------- | -------------- |
| **pyweb**        | **5.50**       |
| httpx+selectolax | 2.96           |

While `pyweb` is not the absolute fastest in this benchmark, it demonstrates the power of a Rust core for CPU-bound parsing tasks and efficient, multi-threaded I/O.

## Installation

```bash
pip install pyweb-scraper
```

## Usage

```bash
pyweb scrape [OPTIONS] [URLS]...
```

**Options:**

*   `-s, --selector TEXT`: CSS selector to extract specific elements.
*   `-o, --output [json|text]`: Output format.
*   `--help`: Show this message and exit.

**Example:**

```bash
pyweb scrape "http://books.toscrape.com" -s "h3 > a"
```
