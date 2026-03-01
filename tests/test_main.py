import os
import sys
from unittest.mock import MagicMock, Mock, patch
import pytest


def test_search_success():
    """Test successful search."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from searxng_api import SearxngAPI

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        api = SearxngAPI("http://example.com")
        result = api.search("test query")

        assert result == {"results": []}
        mock_get.assert_called_once_with(
            url="http://example.com/search",
            params={"q": "test query", "format": "json"},
            timeout=100,
        )


def test_initialization():
    """Test server initialization."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from main import SearXngMcpServer

    with patch("main.SearxngAPI"):
        with patch("main.FastMCP"):
            server = SearXngMcpServer(
                searxng_url="http://localhost:8080",
                port=8080,
                host="0.0.0.0",
                transport="streamable-http",
            )

            assert server._port == 8080
            assert server._host == "0.0.0.0"
            assert server._transport == "streamable-http"
            assert isinstance(server._client, Mock)


def test_initialization_with_sse():
    """Test server initialization with SSE transport."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from main import SearXngMcpServer

    with patch("main.SearxngAPI"):
        with patch("main.FastMCP"):
            server = SearXngMcpServer(searxng_url="http://localhost:8080", transport="sse")

            assert server._transport == "sse"


def test_start():
    """Test server start method."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from main import SearXngMcpServer

    with patch("main.SearxngAPI") as mock_api_class:
        mock_api_instance = MagicMock()
        mock_api_class.return_value = mock_api_instance

        with patch("main.FastMCP") as mock_mcp_class:
            mock_server = MagicMock()
            mock_mcp_class.return_value = mock_server

            with patch.object(mock_server, "run"), patch("main.logging"):
                SearXngMcpServer("http://localhost:8080")
                SearXngMcpServer("http://localhost:8080").start()

                mock_server.run.assert_called_once()


def test_register_tools():
    """Test tool registration."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from main import SearXngMcpServer

    with patch("main.SearxngAPI") as mock_api_class:
        mock_api_instance = MagicMock()
        mock_api_class.return_value = mock_api_instance

        with patch("main.FastMCP") as mock_mcp_class:
            mock_server = MagicMock()
            mock_mcp_class.return_value = mock_server

            mock_api_instance.search = MagicMock()
            mock_api_instance.some_method = MagicMock()

            with (
                patch("main.inspect.getmembers") as mock_getmembers,
                patch("main.inspect.ismethod") as mock_ismethod,
            ):
                mock_getmembers.return_value = [
                    ("search", MagicMock()),
                    ("some_method", MagicMock()),
                    ("_private_method", MagicMock()),
                    ("_private_method_http_info", MagicMock()),
                    ("method_without_preload_content", MagicMock()),
                ]
                mock_ismethod.return_value = True

                SearXngMcpServer("http://localhost:8080")

                assert mock_server.add_tool.call_count == 2


def test_main_function():
    """Test the main function with default environment variables."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from main import main

    with patch("main.SearXngMcpServer") as mock_server_class:
        mock_server_instance = MagicMock()
        mock_server_class.return_value = mock_server_instance

        with patch.object(mock_server_instance, "start"):
            os.environ["SEARXNG_URL"] = "http://localhost:8080"
            os.environ["TRANSPORT"] = "streamable-http"
            os.environ["PORT"] = "8080"
            os.environ["HOST"] = "0.0.0.0"

            main()

            mock_server_class.assert_called_once_with(
                searxng_url="http://localhost:8080",
                port=8080,
                host="0.0.0.0",
                transport="streamable-http",
            )


def test_main_function_sse():
    """Test the main function with SSE transport."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from main import main

    with patch("main.SearXngMcpServer") as mock_server_class:
        mock_server_instance = MagicMock()
        mock_server_class.return_value = mock_server_instance

        with patch.object(mock_server_instance, "start"):
            os.environ["SEARXNG_URL"] = "http://localhost:8080"
            os.environ["TRANSPORT"] = "sse"
            os.environ["PORT"] = "9090"
            os.environ["HOST"] = "127.0.0.1"

            main()

            mock_server_class.assert_called_once_with(
                searxng_url="http://localhost:8080",
                port=9090,
                host="127.0.0.1",
                transport="sse",
            )


def test_main_function_invalid_transport():
    """Test the main function with invalid transport."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    from main import main

    with patch("main.logger") as mock_logger:
        os.environ["SEARXNG_URL"] = "http://localhost:8080"
        os.environ["TRANSPORT"] = "invalid_transport"

        with pytest.raises(SystemExit):
            main()

        mock_logger.fatal.assert_called_once()
        mock_logger.fatal.assert_called_with(
            "Transport type not recognized. Must be one of %s",
            ("streamable-http", "sse"),
        )
