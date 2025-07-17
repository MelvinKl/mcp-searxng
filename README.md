# MCP-Searxng

A Model Context Protocol (MCP) server that connects to the `searxng` API through either streamable-http (default) or sse. This server provides access to search engines to AI clients using the MCP interface.

# Configuration

The following configuration can be set with env variables:
| Env var | Default value | Description|
|-------|--------|-------|
|`HOST`|`0.0.0.0`|Address to listen to.|
|`PORT`|`8080`|Port to listen on.|
|`TRANSPORT`|`streamable-http`|Transport used by the mcp server. Must be `streamable-http`or `sse`.|
|`SEARXNG_URL`|-|URL to the searxng server|

# Requirements
It is recommended to use the provided Dockerimage, which requires only Docker to be installed.

If you want to install from source the following packages are required:
- Python 3.13
- Poetry

# Installation
## (Recommended) Using the Dockerimage
```bash
    docker run -p 8080:8080 ghcr.io/melvinkl/mcp-weather/server:latest
```
## Using source
1. Clone the repository
```bash
    git clone https://github.com/MelvinKl/mcp-weather.git
```
2. Install the dependencies
```bash
    poetry install --no-root
```
3. Runs the server
```bash
    poetry run python src/main.py
```

# License

Apache 2

# Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
