import click
import json
from rust_scraper import scrape_urls_concurrent
from concurrent.futures import ThreadPoolExecutor, as_completed

@click.group()
def cli():
    """A CLI for scraping websites."""
    pass

def scrape_single_url_wrapper(url, selector):
    """Wrapper to call the Rust scraper for a single URL."""
    return url, scrape_urls_concurrent([url], selector)[0]

@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--selector', '-s', help='CSS selector to extract specific elements.')
@click.option('--output', '-o', type=click.Choice(['json', 'text']), default='text', help='Output format.')
@click.option('--workers', '-w', default=10, help='Number of concurrent workers.')
def scrape(urls, selector, output, workers):
    """Scrapes one or more websites and extracts data concurrently."""
    if not urls:
        click.echo("Please provide at least one URL to scrape.")
        return

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_url = {executor.submit(scrape_single_url_wrapper, url, selector): url for url in urls}
        for future in as_completed(future_to_url):
            url, elements = future.result()
            if not elements:
                click.echo(click.style(f"Error or no elements found for {url}", fg='red'), err=True)
                continue

            result_data = {"url": url, "selector": selector, "elements": elements}

            if output == 'json':
                click.echo(json.dumps(result_data, indent=2))
            else:
                click.echo(click.style(f"\nResults for {url}", fg='green', bold=True))
                for element in elements:
                    click.echo(f"- {element}")

if __name__ == '__main__':
    cli()
