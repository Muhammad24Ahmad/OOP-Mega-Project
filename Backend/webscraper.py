import requests


class WebScraper:
    """A class to handle web scraping."""

    def scrape(self, url):
        """Scrapes the web page provided by the URL."""
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to retrieve data from {url} with status code {response.status_code}")


