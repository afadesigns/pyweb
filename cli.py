import click
import json
from scraper import run_scrape

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

    results = run_scrape(list(urls), selector)

    for result in results:
        if 'error' in result:
            click.echo(click.style(f"Error scraping {result.get('url', '')}: {result['error']}", fg='red'), err=True)
            continue

        if output == 'json':
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(click.style(f"\nResults for {result['url']}", fg='green', bold=True))
            if 'elements' in result:
                for element in result['elements']:
                    click.echo(f"- {element}")
            elif 'links' in result:
                for link in result['links']:
                    click.echo(f"- {link}")

if __name__ == '__main__':
    cli()
