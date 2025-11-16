"""
The main command-line interface for pyru.

This module provides a CLI for scraping websites using a hyper-optimized Rust core.
It uses the `click` library to define commands and options.
"""

import click
import json
import asyncio
from rust_scraper import scrape_urls_concurrent

@click.group()
def cli():
    """A high-performance, concurrent web scraper built with Rust."""
    pass

async def scrape_async(urls, selector, output, concurrency):
    """
    Asynchronous scraping logic.

    This function orchestrates the call to the Rust core and formats the output.

    Args:
        urls (tuple): A tuple of URLs to scrape.
        selector (str): The CSS selector for extracting elements.
        output (str): The desired output format ('json' or 'text').
        concurrency (int): The number of concurrent requests to make.
    """
    results, _latencies = await scrape_urls_concurrent(list(urls), selector, concurrency)

    for i, url in enumerate(urls):
        elements = results[i]
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

@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--selector', '-s', required=True, help='CSS selector to extract specific elements.')
@click.option('--output', '-o', type=click.Choice(['json', 'text']), default='text', help='Output format.')
@click.option('--concurrency', '-c', default=50, help='Number of concurrent requests.')
def scrape(urls, selector, output, concurrency):
    """
    Scrapes one or more websites and extracts data concurrently.

    URLS: One or more URLs to scrape.
    """
    if not urls:
        click.echo("Please provide at least one URL to scrape.")
        return
    asyncio.run(scrape_async(urls, selector, output, concurrency))

if __name__ == '__main__':
    cli()