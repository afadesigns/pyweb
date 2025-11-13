import click
import json
from rust_scraper import scrape as rust_scrape

@click.group()
def cli():
    """A CLI for scraping websites."""
    pass

@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--selector', '-s', help='CSS selector to extract specific elements.')
@click.option('--output', '-o', type=click.Choice(['json', 'text']), default='text', help='Output format.')
def scrape(urls, selector, output):
    """Scrapes one or more websites and extracts data."""
    if not urls:
        click.echo("Please provide at least one URL to scrape.")
        return

    for url in urls:
        try:
            elements = rust_scrape(url, selector)
            result = {"url": url, "selector": selector, "elements": elements}

            if output == 'json':
                click.echo(json.dumps(result, indent=2))
            else:
                click.echo(click.style(f"\nResults for {result['url']}", fg='green', bold=True))
                for element in result['elements']:
                    click.echo(f"- {element}")
        except Exception as e:
            click.echo(click.style(f"Error scraping {url}: {e}", fg='red'), err=True)

if __name__ == '__main__':
    cli()
