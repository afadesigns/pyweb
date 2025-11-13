import click
import json
from scraper import run_scrape

@click.group()
def cli():
    """A CLI for scraping websites."""
    pass

@cli.command()
@click.argument('url')
@click.option('--selector', '-s', help='CSS selector to extract specific elements.')
@click.option('--output', '-o', type=click.Choice(['json', 'text']), default='text', help='Output format.')
def scrape(url, selector, output):
    """Scrapes a website and extracts data."""
    result = run_scrape(url, selector)

    if 'error' in result:
        click.echo(click.style(f"Error: {result['error']}", fg='red'), err=True)
        return

    if output == 'json':
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo(click.style(f"Results for {result['url']}", fg='green', bold=True))
        if 'elements' in result:
            for element in result['elements']:
                click.echo(f"- {element}")
        elif 'links' in result:
            for link in result['links']:
                click.echo(f"- {link}")

if __name__ == '__main__':
    cli()
