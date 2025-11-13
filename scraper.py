import requests
from bs4 import BeautifulSoup
import logging
from cachetools import TTLCache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory cache with a TTL of 10 minutes
cache = TTLCache(maxsize=100, ttl=600)

async def scrape_website(url: str, selector: str = None):
    cache_key = (url, selector)
    if cache_key in cache:
        logger.info(f"Cache hit for {url}")
        return cache[cache_key]

    logger.info(f"Cache miss for {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")

        if selector:
            elements = [element.text for element in soup.select(selector)]
            result = {"url": url, "selector": selector, "elements": elements}
        else:
            # If no selector is provided, return all links as before
            links = [a["href"] for a in soup.find_all("a", href=True)]
            result = {"url": url, "links": links}
        
        cache[cache_key] = result
        return result
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error occurred: {e}"}
    except requests.exceptions.ConnectionError as e:
        return {"error": f"Error connecting to the server: {e}"}
    except requests.exceptions.Timeout as e:
        return {"error": f"The request timed out: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
