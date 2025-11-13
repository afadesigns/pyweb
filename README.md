# PyWeb Scraper

A hyper modern Python web scraper CLI.

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
