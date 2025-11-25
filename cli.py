"""
The main command-line interface for pyru.

This module provides a CLI for scraping websites using a hyper-optimized Rust core.
It uses the `click` library to define commands and options.
"""

import click
import json
import asyncio
import toml
from pathlib import Path
import sys
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
@click.option('--selector', '-s', help='CSS selector to extract specific elements.')
@click.option('--output', '-o', type=click.Choice(['json', 'text']), default='text', help='Output format.')
@click.option('--concurrency', '-c', type=int, default=50, help='Number of concurrent requests.')
@click.option('--config', '-C', type=click.Path(exists=True, dir_okay=False, path_type=Path), help='Path to a TOML configuration file.')
@click.option('--input-file', '-i', type=click.Path(exists=True, dir_okay=False, path_type=Path), help='Path to a file containing URLs to scrape, one per line.')
def scrape(urls, selector, output, concurrency, config, input_file):
    """
    Scrapes one or more websites and extracts data concurrently.

    URLS: One or more URLs to scrape.
    """
    config_options = {}
    if config:
        try:
            config_options = toml.load(config)
        except toml.TomlDecodeError as e:
            click.echo(click.style(f"Error decoding TOML config file {config}: {e}", fg='red'), err=True)
            sys.exit(1)

    # Apply config options, allowing CLI arguments to override
    selector = selector if selector is not None else config_options.get("scrape", {}).get("selector")
    output = output if output != 'text' else config_options.get("scrape", {}).get("output", 'text') # 'text' is default in click
    concurrency = concurrency if concurrency != 50 else config_options.get("scrape", {}).get("concurrency", 50)
    config_urls = config_options.get("scrape", {}).get("urls", [])

    file_urls = []
    if input_file:
        try:
            with open(input_file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip()]
        except IOError as e:
            click.echo(click.style(f"Error reading input file {input_file}: {e}", fg='red'), err=True)
            sys.exit(1)

    # Determine final list of URLs: CLI args > Input file > Config file
    final_urls = []
    if urls:
        final_urls = list(urls)
    elif file_urls:
        final_urls = file_urls
    elif config_urls:
        final_urls = config_urls

    if selector is None:
        click.echo(click.style("Error: Missing option '--selector' / '-s'.", fg='red'), err=True)
        sys.exit(1)

    if not final_urls:
        click.echo("Please provide at least one URL to scrape, either via arguments, a config file, or an input file.", err=True)
        sys.exit(1)
    asyncio.run(scrape_async(tuple(final_urls), selector, output, concurrency))

if __name__ == '__main__':
    cli()