import asyncio

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client

load_dotenv()  # load environment variables from .env


class MCPClientSSE:
    def __init__(self, server_url: str):
        # Initialize client configuration
        self.server_url = server_url

        # These will hold our active connections
        self._streams = None
        self._streams_context = None
        self._session_context = None

    async def __aenter__(self) -> ClientSession:
        """Async context manager entry point that handles connection setup"""
        await self.connect_to_sse_server(self.server_url)
        if self.session is None:
            raise ValueError("Session not initialized")
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit that handles cleanup"""
        await self.cleanup()

    async def connect_to_sse_server(self, server_url: str):
        """Connect to an MCP server running with SSE transport"""
        # Create and store the persistent connections
        self._streams_context = sse_client(url=server_url)
        self._streams = await self._streams_context.__aenter__()

        self._session_context = ClientSession(*self._streams)
        self.session = await self._session_context.__aenter__()

        # Initialize the session
        await self.session.initialize()

        # List available tools to verify connection
        print("Initialized SSE client...")
        print("Listing tools...")
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def cleanup(self):
        """Properly clean up the session and streams in reverse order"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
            self.session = None
            self._session_context = None

        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)
            self._streams = None
            self._streams_context = None


async def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--server-url", type=str, default="http://localhost:8000/sse")
    args = parser.parse_args()

    async with MCPClientSSE(server_url=args.server_url) as session:
        print(await session.send_ping())
        pass


if __name__ == "__main__":
    asyncio.run(main())
