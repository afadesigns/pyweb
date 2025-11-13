# PyWeb Scraper

**The fastest Python web scraper.**

`pyweb` is a hyper-modern Python web scraper CLI, meticulously engineered for unparalleled speed. By leveraging a high-performance core written in Rust, `pyweb` achieves speeds that are an order of magnitude faster than established scraping frameworks.

## Performance

When benchmarked against `Scrapy`, one of Python's most popular and respected scraping libraries, `pyweb` demonstrates a staggering performance advantage.

In a benchmark scraping 1,000 pages from a local web server, `pyweb` was nearly **10x faster** than `Scrapy`:

| Scraper | Time (seconds) |
|---|---|
| **pyweb (Rust Core)** | **0.57** |
| Scrapy | 4.83 |

*Benchmark details: Scraping 1000 identical pages from a local web server to isolate parsing and processing speed. The task was to extract 10 specific paragraph elements from each page.*

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/afadesigns/pyweb.git
   ```
2. Navigate to the project directory:
   ```bash
   cd pyweb
   ```
3. Install the project:
   ```bash
   pip install .
   ```

## Usage

### Basic Scraping (get all links)
```bash
pyweb scrape https://example.com
```

### Scraping Multiple URLs
```bash
pyweb scrape https://example.com https://google.com
```

### Scraping with a CSS Selector
```bash
pyweb scrape https://example.com --selector "h1"
```

### Changing Output Format
```bash
pyweb scrape https://example.com -s "h1" -o json
```
