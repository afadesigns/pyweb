import click
import json
from rust_scraper import scrape_urls_concurrent

@click.group()
def cli():
    """A CLI for scraping websites."""
    pass

@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--selector', '-s', help='CSS selector to extract specific elements.')
@click.option('--output', '-o', type=click.Choice(['json', 'text']), default='text', help='Output format.')
def scrape(urls, selector, output):
    """Scrapes one or more websites and extracts data concurrently."""
    if not urls:
        click.echo("Please provide at least one URL to scrape.")
        return

    results = scrape_urls_concurrent(list(urls), selector)

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

if __name__ == '__main__':
    cli()
