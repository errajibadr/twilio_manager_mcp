# client_first_mcp.py
import asyncio
import os

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import get_default_environment, stdio_client

# Créer les paramètres pour une connexion stdio
# server_params = StdioServerParameters(
#     command="uv",  # Exécutable
#     args=["run", "mcp", "run", "./twilio_manager_mcp.py"],  # Arguments de ligne de commande
# )

load_dotenv()

server_params = StdioServerParameters(
    command="uvx",  # Exécutable
    args=["twilio-manager-mcp"],  # Arguments de ligne de commande
    env=get_default_environment()
    | {
        "TWILIO_ACCOUNT_SID": os.getenv("TWILIO_ACCOUNT_SID", ""),
        "TWILIO_AUTH_TOKEN": os.getenv("TWILIO_AUTH_TOKEN", ""),
    },
)

# server_params = StdioServerParameters(
#     command="uvx",  # Exécutable
#     args=["mcp-server-time"],
# )


async def run():
    print("Connexion au serveur MCP 'Mon Premier Serveur MCP'...")

    # Établir une connexion avec le serveur MCP
    async with stdio_client(server_params) as (read, write):
        # Créer une session client
        async with ClientSession(read, write) as session:
            # Initialiser la connexion
            await session.initialize()

            # Lister les outils disponibles
            tools = (await session.list_tools()).tools
            print("\n Outils disponibles sur le serveur:")
            for tool in tools:
                print(f"- {tool.name}")

            # Appeler l'outil get_user_money
            print("\nliste des subaccounts")
            subaccounts = await session.call_tool("list_twilio_subaccounts")
            # print(f"Subaccounts: {subaccounts}")


if __name__ == "__main__":
    asyncio.run(run())
