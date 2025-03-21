# TwilioManager MCP - Twilio Model Context Protocol Integration

TwilioManager MCP connects Claude AI to Twilio through the Model Context Protocol (MCP), enabling Claude to interact directly with Twilio's API. This integration allows for prompt-assisted Twilio account management, subaccount creation, phone number management, and regulatory compliance handling.

## Features

- **Two-way communication**: Connect Claude AI to Twilio through a socket-based server
- **Subaccount management**: Create, list, and manage Twilio subaccounts
- **Phone number control**: Transfer, configure, and manage phone numbers across accounts
- **Regulatory compliance**: Manage regulatory bundles and compliance requirements
- **Address management**: Create and manage addresses for regulatory compliance
- **Asynchronous API**: High-performance async implementation of Twilio API interactions

## Components

The system consists of two main components:

- **MCP Server** (`twilio_manager_mcp.py`): A Python server that implements the Model Context Protocol and provides tools for Twilio management
- **Async Twilio API** (`api/async_twilio_api.py`): An asynchronous wrapper around the Twilio API for efficient operations

## Installation

### Prerequisites

- Python 3.10 or newer
- `uv` package manager:

#### If you're on Mac:
```
brew install uv
```

#### On Windows:
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
set Path=C:\Users\[USERNAME]\.local\bin;%Path%
```

⚠️ Do not proceed before installing UV

### Claude for Desktop Integration

Go to Claude > Settings > Developer > Edit Config > `claude_desktop_config.json` to include the following:

```json
{
    "mcpServers": {
        "twilio": {
            "command": "uvx",
            "args": [
                "twilio-manager-mcp"
            ]
        }
    }
}
```

### Cursor Integration

Run twilio-manager-mcp without installing it permanently through uvx. Go to Cursor Settings > MCP and paste this as a command:

```
uvx twilio-manager-mcp
```

⚠️ Only run one instance of the MCP server (either on Cursor or Claude Desktop), not both

### Environment Setup

1. Clone this repository
2. Copy `.env.example` to `.env` and fill in your Twilio credentials:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   ```
3. Install dependencies:
   ```
   uv pip install -e .
   ```

## Usage

### Starting the Connection

1. Make sure your credentials are set in the `.env` file
2. Start the MCP server:
   ```
   uvx twilio-manager-mcp
   ```
3. In Claude, look for the Twilio MCP tool icon in the toolbar

### Using with Claude

Once the config file has been set on Claude and the MCP server is running, you will see a tool icon for the Twilio Manager MCP.

### Capabilities

- List and filter Twilio subaccounts
- View phone numbers associated with accounts
- Transfer phone numbers between accounts
- Create and manage addresses
- Handle regulatory compliance and bundles
- Execute comprehensive Twilio account management tasks

### Example Commands

Here are some examples of what you can ask Claude to do:

- "List all my Twilio subaccounts"
- "Show all phone numbers on my main account"
- "Transfer phone number X from account A to account B"
- "Create a new address for regulatory compliance"
- "Duplicate a regulatory bundle to a subaccount"
- "Show all phone numbers of a specific type"

## Troubleshooting

- **Connection issues**: Make sure the MCP server is running, and the MCP server is configured on Claude
- **Authentication errors**: Verify your Twilio credentials in the `.env` file
- **Rate limiting**: Twilio API has rate limits; consider adding delays between operations if hitting limits
- **Timeout errors**: Try simplifying your requests or breaking them into smaller steps

## Technical Details

### Communication Protocol

The system uses a JSON-based protocol over TCP sockets:

- Commands are sent as JSON objects with a type and optional params
- Responses are JSON objects with status and result or message

### Async Implementation

The Twilio API wrapper uses Python's asyncio for high-performance, non-blocking operations:

- Custom `AsyncTwilioHttpClient` for managing HTTP requests asynchronously
- Context manager pattern for resource management
- Error handling and retry logic

## Limitations & Security Considerations

- The system requires valid Twilio credentials with appropriate permissions
- Keep your `.env` file secure and never commit it to version control
- Consider adding additional validation for critical operations
- API keys should be rotated regularly for security
- Some operations may require multiple steps to complete successfully

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool interacts with a paid service (Twilio). Be aware that API calls made through this tool may incur charges to your Twilio account. Always test in development environments before using in production.
