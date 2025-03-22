# Twilio Manager MCP

A Model Context Protocol (MCP) implementation for managing Twilio resources. This package provides tools for managing Twilio subaccounts, phone numbers, and regulatory bundles through a standardized MCP interface.

## Features

- List Twilio subaccounts
- Get phone numbers associated with subaccounts
- Transfer phone numbers between subaccounts
- Get regulatory bundle SIDs
- Support for both direct and Server-Sent Events (SSE) communication
- Integration with Claude Desktop, Cursor, and other MCP-compatible tools

## Installation

### Prerequisites

#### Install uv

On macOS:
```bash
brew install uv
```

On Windows:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Project Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/twilio_manager_mcp.git
cd twilio_manager_mcp
```

2. Install dependencies using uv:
```bash
uv sync
```

## Configuration

1. Create a `.env` file in the root directory with your Twilio credentials:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
```

2. Configure MCP for your tool (Cursor, Claude Desktop, etc.) by creating a `.cursor/mcp.json` file:

```json
{
  "mcpServers": { 
    "twilio_manager_mcp_abs": {
      "command": "uv",
      "args": ["--directory", "/path/to/twilio_manager_mcp", "run", "mcp", "run", "./twilio_manager_mcp.py"],
      "env": {
        "TWILIO_ACCOUNT_SID": "your_account_sid",
        "TWILIO_AUTH_TOKEN": "your_auth_token"
      }
    },
    "twilio_manager_mcp_uvx": {
      "command": "uvx",
      "args": [ "twilio-manager-mcp" ],
      "env": {
        "TWILIO_ACCOUNT_SID": "your_account_sid",
        "TWILIO_AUTH_TOKEN": "your_auth_token"
      }
    },
    "twilio_manager_mcp_sse": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## Docker

You can run Twilio Manager MCP using Docker for easier deployment and management.

### Using Docker Compose

The project includes a Docker Compose configuration that sets up:
- The Twilio Manager MCP service
- A Traefik reverse proxy with automatic HTTPS

1. Configure environment variables in your `.env` file:

```env
# Twilio credentials
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token

# Domain configuration for Traefik
DOMAIN_NAME=yourdomain.com
ACME_EMAIL=user@yourdomain.com

# Address details (optional)
ADDRESS_CUSTOMER_NAME=
ADDRESS_FRIENDLY_NAME=
ADDRESS_STREET=
ADDRESS_CITY=
ADDRESS_REGION=
ADDRESS_POSTAL_CODE=
ADDRESS_ISO_COUNTRY=
```

2. Start the services:

```bash
docker-compose up -d
```

The application will be available at your configured domain with HTTPS enabled.

### Using Docker Without Docker Compose

If you prefer to run just the Twilio Manager MCP container without Traefik:

1. Build the Docker image:

```bash
docker build -t twilio-manager-mcp .
```

2. Run the container:

```bash
docker run -p 8000:8000 \
  -e TWILIO_ACCOUNT_SID=your_account_sid \
  -e TWILIO_AUTH_TOKEN=your_auth_token \
  twilio-manager-mcp
```

The SSE endpoint will be available at `http://localhost:8000/sse`.

## Usage

### With Cursor, Claude Desktop, or other MCP-compatible tools

You have three options to use this MCP:

1. **Direct UVX Integration** (Recommended):
   - Use the `twilio_manager_mcp_uvx` configuration
   - This is the simplest method and works out of the box with uvx

2. **Direct UV Integration**:
   - Use the `twilio_manager_mcp_abs` configuration
   - Requires specifying the full path to your installation

3. **SSE Server**:
   - Use the `twilio_manager_mcp_sse` configuration
   - Start the SSE server first:
     ```bash
     uvicorn twilio_manager_mcp_sse:app --host 0.0.0.0 --port 8000
     ```

### Available Tools

| Tool Name | Description |
|-----------|-------------|
| `list_twilio_subaccounts` | List all Twilio subaccounts |
| `get_account_phone_numbers` | Get phone numbers for a specific subaccount |
| `get_all_phone_numbers` | Transfer phone numbers between subaccounts |
| `get_regulatory_bundle_sid` | Get regulatory bundle SID for a subaccount |

### Example Usage in Cursor/Claude Desktop

Once configured, you can use the tools directly in your AI assistant conversations:

1. List all subaccounts:
```python
# The AI will automatically use the MCP to list all subaccounts
# No need to write code - just ask "List all Twilio subaccounts"
```

2. Get phone numbers for a subaccount:
```python
# Simply ask: "Show me all phone numbers for subaccount AC..."
```

### Direct Python Usage

For direct programmatic usage:

```python
from mcp import ClientSession
from clients.client import MCPClient

async with MCPClient("uvx", ["twilio-manager-mcp"], env={}) as session:
    # List available tools
    tools = (await session.list_tools()).tools
    
    # List all subaccounts
    subaccounts = await session.invoke("list_twilio_subaccounts")
    
    # Get phone numbers for a subaccount
    numbers = await session.invoke("get_account_phone_numbers", {"account_sid": "AC..."})
```

## Project Structure

```
twilio_manager_mcp/
├── api/
│   └── async_twilio_api.py    # Async Twilio API implementation
├── clients/
│   ├── client.py              # Direct MCP client implementation
│   └── client_sse.py          # SSE client implementation
├── twilio_manager_mcp.py      # Core MCP server implementation
├── twilio_manager_mcp_sse.py  # SSE server wrapper
├── requirements.txt           # Project dependencies
└── README.md                 # This file
```

## Development

For development, you can use uv's virtual environment management:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix
.venv\Scripts\activate     # On Windows

# Install dependencies in development mode
uv pip install -e .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
