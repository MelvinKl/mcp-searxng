import requests


class SearxngAPI:
    def __init__(self, base_url: str):
        self._base_url = base_url

    def search(
        self,
        searchterm:str 
    ):
        """
        Searches on the internet for the given searchterm and return the 

        Parameters
        ----------
        searchterm: str
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
