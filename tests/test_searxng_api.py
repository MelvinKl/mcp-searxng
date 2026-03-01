import pytest
import requests
from unittest.mock import Mock, patch
from searxng_api import SearxngAPI


class TestSearxngAPI:
    def test_init(self):
        api = SearxngAPI("https://example.com")
        assert api._base_url == "https://example.com"

    @patch("searxng_api.requests.get")
    def test_search_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        api = SearxngAPI("https://example.com")
        result = api.search("test query")

        mock_get.assert_called_once_with(
            url="https://example.com/search",
            params={
                "q": "test query",
                "format": "json",
            },
            timeout=100,
        )
        assert result == {"results": []}

    @patch("searxng_api.requests.get")
    def test_search_with_results(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{"title": "Test", "url": "https://test.com"}]
        }
        mock_get.return_value = mock_response

        api = SearxngAPI("https://example.com")
        result = api.search("test")

        assert len(result["results"]) == 1
        assert result["results"][0]["title"] == "Test"

    @patch("searxng_api.requests.get")
    def test_search_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")

        api = SearxngAPI("https://example.com")

        with pytest.raises(requests.RequestException):
            api.search("test")
