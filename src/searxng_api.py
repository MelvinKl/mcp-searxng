"""SearXNG API client."""

import requests


class SearxngAPI:
    """Client for interacting with SearXNG API."""

    def __init__(self, base_url: str):
        """Initialize the SearXNG API client."""
        self._base_url = base_url

    def search(self, searchterm: str):
        """Search the internet for the given searchterm.

        Parameters
        ----------
        searchterm : str
            The term to search for.
        """
        response = requests.get(
            url=f"{self._base_url}/search",
            params={
                "q": searchterm,
                "format": "json",
            },
            timeout=100,
        )
        return response.json()
