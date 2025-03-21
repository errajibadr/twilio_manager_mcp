# twilio_manager_mcp.py
import os
from typing import Dict, List, Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from api.async_twilio_api import AsyncTwilioManager

load_dotenv()

# Créer un serveur MCP
mcp = FastMCP("Twilio Manager MCP")

# Twilio credentials - should be configured properly in production
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

assert TWILIO_ACCOUNT_SID is not None
assert TWILIO_AUTH_TOKEN is not None

# Create a global AsyncTwilioManager instance
async_twilio_manager = AsyncTwilioManager(
    account_sid=TWILIO_ACCOUNT_SID, auth_token=TWILIO_AUTH_TOKEN
)


@mcp.tool()
async def list_twilio_subaccounts(friendly_name: Optional[str] = None) -> List[Dict]:
    """
    Liste tous les sous-comptes Twilio ou filtre par nom convivial.

    Args:
        friendly_name: Filtre optionnel par nom convivial

    Returns:
        Liste des détails des sous-comptes
    """
    async with async_twilio_manager:
        return await async_twilio_manager.list_subaccounts(friendly_name)


@mcp.tool()
async def get_account_phone_numbers(account_sid: Optional[str] = None) -> List[Dict]:
    """
    Récupère tous les numéros de téléphone associés à un compte ou sous-compte.

    Args:
        account_sid: L'identifiant SID du sous-compte. Si non fourni, utilise le compte principal.

    Returns:
        Liste des numéros de téléphone et leurs détails
    """
    async with async_twilio_manager:
        return await async_twilio_manager.get_account_numbers(account_sid)


if __name__ == "__main__":
    mcp.run()
