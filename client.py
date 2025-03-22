import asyncio
import os

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


class MCPClient:
    def __init__(self, command: str, args: list[str], env: dict[str, str]):
        self.server_params = StdioServerParameters(
            command="uv",
            args=["run", "mcp", "run", "./twilio_manager_mcp.py"],
            env=env,
        )
        self.session = None

    async def initialize(self):
        streams_context = stdio_client(self.server_params)
        streams = await streams_context.__aenter__()
        self._session_context = ClientSession(*streams)
        self.session = await self._session_context.__aenter__()
        await self.session.initialize()
        print("Session with mcp server initialized")

    async def __aenter__(self):
        await self.initialize()
        if self.session is None:
            raise ValueError("Session not initialized")
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self._session_context.__aexit__(exc_type, exc_val, exc_tb)
            self.session = None


async def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=str, default="uv")
    parser.add_argument(
        "--args", nargs="+", default=["run", "mcp", "run", "./twilio_manager_mcp.py"]
    )
    args = parser.parse_args()
    env = {
        "TWILIO_ACCOUNT_SID": os.getenv("TWILIO_ACCOUNT_SID"),
        "TWILIO_AUTH_TOKEN": os.getenv("TWILIO_AUTH_TOKEN"),
    }
    if env["TWILIO_ACCOUNT_SID"] is None or env["TWILIO_AUTH_TOKEN"] is None:
        raise ValueError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set")

    async with MCPClient(args.command, args.args, env=env) as session:  # type: ignore
        print(await session.send_ping())
        tools = (await session.list_tools()).tools
        print([tool.name for tool in tools])


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    asyncio.run(main())
