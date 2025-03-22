from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route

from twilio_manager_mcp import mcp

# Initialize SSE transport
sse = SseServerTransport("/messages")


# SSE handlers
async def handle_sse(scope, receive, send):
    """Handle SSE connections."""
    async with sse.connect_sse(scope, receive, send) as streams:
        await mcp._mcp_server.run(
            streams[0], streams[1], mcp._mcp_server.create_initialization_options()
        )


async def handle_messages(scope, receive, send):
    """Handle POST messages."""
    await sse.handle_post_message(scope, receive, send)


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


if __name__ == "__main__":
    mcp_server = mcp._mcp_server
    import uvicorn

    app = create_starlette_app(mcp_server)
    uvicorn.run(app, host="0.0.0.0", port=8000)
