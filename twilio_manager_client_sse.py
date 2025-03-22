# client_first_mcp.py
import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client


async def run():
    print("Connexion au serveur MCP 'Mon Premier Serveur MCP'...")

    # Établir une connexion avec le serveur MCP
    async with sse_client(url="http://localhost:8000/sse") as (read_stream, write_stream):
        # Créer une session client
        async with ClientSession(read_stream, write_stream) as session:
            # Initialiser la connexion
            await session.initialize()

            # Lister les outils disponibles
            tools = await session.list_tools()
            print("\n Outils disponibles sur le serveur:")
            for tool in tools:
                print(f"- {tool}")

            # Appeler l'outil get_user_context avec l'ID 42
            print("\nRécupération des informations de l'utilisateur avec ID=42...")
            user_info = await session.call_tool("get_user_context", arguments={"id": 42})
            print(f"Informations utilisateur: {user_info}")

            # Appeler l'outil get_user_money
            print("\nRécupération des informations bancaires...")
            money_info = await session.call_tool("get_user_money")
            print(f"Informations bancaires: {money_info}")

            # Calculer le solde total
            if isinstance(money_info, dict):
                total = sum(money_info.values())
                print(f"Solde total: {total} €")


if __name__ == "__main__":
    asyncio.run(run())
