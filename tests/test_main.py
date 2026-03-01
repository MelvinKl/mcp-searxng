import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from main import SearXngMcpServer


class TestSearXngMcpServer:
    def test_init_default_values(self):
        with patch("main.FastMCP"):
            with patch("main.SearxngAPI"):
                server = SearXngMcpServer("https://example.com")
                assert server._port == 8080
                assert server._host == "0.0.0.0"
                assert server._transport == "streamable-http"

    def test_init_custom_values(self):
        with patch("main.FastMCP"):
            with patch("main.SearxngAPI"):
                server = SearXngMcpServer(
                    "https://example.com", port=9000, host="127.0.0.1", transport="sse"
                )
                assert server._port == 9000
                assert server._host == "127.0.0.1"
                assert server._transport == "sse"

    def test_start(self):
        with patch("main.FastMCP") as mock_mcp:
            mock_server_instance = MagicMock()
            mock_mcp.return_value = mock_server_instance

            with patch("main.SearxngAPI"):
                server = SearXngMcpServer("https://example.com")
                server.start()

                mock_server_instance.run.assert_called_once_with(
                    transport="streamable-http",
                    host="0.0.0.0",
                    port=8080,
                )


class TestMain:
    @patch.dict(
        os.environ,
        {
            "SEARXNG_URL": "https://example.com",
            "TRANSPORT": "streamable-http",
            "PORT": "9000",
            "HOST": "127.0.0.1",
        },
    )
    @patch("main.SearXngMcpServer")
    def test_main_with_valid_transport(self, mock_server_class):
        from main import main

        mock_server_instance = MagicMock()
        mock_server_class.return_value = mock_server_instance

        main()

        mock_server_class.assert_called_once_with(
            host="127.0.0.1",
            port=9000,
            transport="streamable-http",
            searxng_url="https://example.com",
        )
        mock_server_instance.start.assert_called_once()

    @patch.dict(os.environ, {"SEARXNG_URL": "https://example.com"}, clear=False)
    @patch("main.SearXngMcpServer")
    def test_main_with_invalid_transport(self, mock_server_class):
        with patch.dict(os.environ, {"TRANSPORT": "invalid-transport"}):
            from main import main

            with pytest.raises(SystemExit):
                main()

    @patch.dict(os.environ, {"TRANSPORT": "streamable-http"}, clear=False)
    @patch("main.SearXngMcpServer")
    def test_main_without_searxng_url(self, mock_server_class):
        with patch.dict(os.environ, {}, clear=True):
            with patch.dict(os.environ, {"TRANSPORT": "streamable-http"}):
                from main import main

                with pytest.raises(AssertionError):
                    main()
