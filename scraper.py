import requests
from bs4 import BeautifulSoup

async def scrape_website(url: str, selector: str = None):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        if selector:
            elements = [element.text for element in soup.select(selector)]
            return {"url": url, "selector": selector, "elements": elements}
        else:
            # If no selector is provided, return all links as before
            links = [a["href"] for a in soup.find_all("a", href=True)]
            return {"url": url, "links": links}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
