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
3. Create a virtual environment:
   ```bash
   uv venv
   ```
4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
5. Install the dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

### Basic Scraping (get all links)
```bash
python cli.py scrape https://example.com
```

### Scraping with a CSS Selector
```bash
python cli.py scrape https://example.com --selector "h1"
```

### Changing Output Format
```bash
python cli.py scrape https://example.com -s "h1" -o json
```
