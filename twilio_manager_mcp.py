# twilio_manager_mcp.py
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from api.async_twilio_api import AsyncTwilioManager

# Créer un serveur MCP
mcp = FastMCP(
    "Twilio Manager MCP",
    instructions="Twilio Manager through the Model Context Protocol",
)

# Twilio credentials - should be configured properly in production
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

assert TWILIO_ACCOUNT_SID is not None
assert TWILIO_AUTH_TOKEN is not None

async_twilio_manager = AsyncTwilioManager(
    account_sid=TWILIO_ACCOUNT_SID, auth_token=TWILIO_AUTH_TOKEN
)


@mcp.tool(
    name="list_twilio_subaccounts",
    description="List all Twilio subaccounts or filter by friendly name. Provide an empty string for all subaccounts",
)
async def list_all_twilio_subaccounts() -> list[dict]:
    """
    List all Twilio subaccounts or filter by friendly name.
    Args:
        friendly_name: Optional filter by friendly name (empty string for all)
    Returns:
        List of subaccount details
    """
    async with async_twilio_manager:
        return await async_twilio_manager.list_subaccounts()


async def get_all_phone_numbers() -> list[dict]:
    """
    Get all phone numbers associated with a Twilio subaccount
    """
    async with async_twilio_manager:
        return await async_twilio_manager.get_account_numbers()


@mcp.tool(
    name="get_account_phone_numbers",
    description="Get all phone numbers associated with a Twilio subaccount",
)
async def get_account_phone_numbers_for_subaccount(account_sid: str) -> list[dict]:
    """
    Get all phone numbers associated with a Twilio subaccount
    Args:
        account_sid: The SID of the Twilio subaccount
    Returns:
        List of phone numbers and their details
    """
    async with async_twilio_manager:
        return await async_twilio_manager.get_account_numbers(account_sid)


@mcp.tool(
    name="get_all_phone_numbers",
    description="Get all phone numbers associated with a Twilio subaccount",
)
async def transfer_phone_number(
    source_account_sid: str,
    phone_number_sid: str,
    target_account_sid: str,
) -> dict:
    """
    Transfer a phone number from one Twilio subaccount to another
    Args:
        source_account_sid: The SID of the Twilio subaccount to transfer the phone number from
        phone_number_sid: The SID of the phone number to transfer
        target_account_sid: The SID of the Twilio subaccount to transfer the phone number to
    Returns:
        Dictionary containing the transfer details
    """
    async with async_twilio_manager:
        return await async_twilio_manager.transfer_phone_number(
            source_account_sid, phone_number_sid, target_account_sid
        )


@mcp.tool(
    name="get_regulatory_bundle_sid",
    description="Get the regulatory bundle SID for a Twilio subaccount",
)
async def get_regulatory_bundle_sid(subaccount_sid: str) -> str | None:
    """
    Get the regulatory bundle SID for a Twilio subaccount
    Args:
        subaccount_sid: The SID of the Twilio subaccount
    Returns:
        The regulatory bundle SID for the Twilio subaccount
    """
    async with async_twilio_manager:
        return await async_twilio_manager.get_bundle_sid(subaccount_sid)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
