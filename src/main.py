import os
import inspect
import logging

from fastmcp import FastMCP

from searxng_api import SearxngAPI

logger = logging.getLogger(__name__)


class SearXngMcpServer:
    """MCP Server that connects to searxng API."""

    def __init__(self, searxng_url: str, port: int = 8080, host: str = "0.0.0.0", transport: str = "streamable-http"):  # noqa: S104
        self._port = port
        self._host = host
        self._transport = transport

        self._client = SearxngAPI(searxng_url)
        self._server = FastMCP(name="Searxng MCP Server")

        self._register_tools()

    def start(self):
        logger.info(f"Starting MCP Searxng Server on {self._host}:{self._port} using {self._transport}")
        self._server.run(
            transport=self._transport,
            host=self._host,
            port=self._port,
        )

    def _register_tools(self):
        all_members = inspect.getmembers(self._client, inspect.ismethod)
        filtered_members = []
        for x in all_members:
            if not x[0].startswith("_") and not (
                x[0].endswith("_http_info") or x[0].endswith("without_preload_content")
            ):
                filtered_members.append(x)
        for member in filtered_members:
            self._server.add_tool(
                self._server.tool(
                    member[1],
                    name=member[0],
                    description=inspect.getdoc(filtered_members[0][1]),
                )
            )


def main():
    transport = os.environ.get("TRANSPORT", "streamable-http")
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get("HOST", "0.0.0.0")
    searxng_url = os.environ.get("SEARXNG_URL", None)
    assert searxng_url, "'SEARXNG_URL' not set."
    allowed_transports = ("streamable-http", "sse")
    if transport not in allowed_transports:
        logger.fatal("Transport type not recognized. Must be one of %s", allowed_transports)
        exit(1)

    server = SearXngMcpServer(host=host, port=port, transport=transport, searxng_url=searxng_url)
    server.start()


if __name__ == "__main__":
    main()
