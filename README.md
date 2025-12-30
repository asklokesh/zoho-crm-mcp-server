# Zoho CRM MCP Server

<!-- mcp-name: io.github.asklokesh/zoho-crm-mcp-server -->

<div align="center">

# Zoho Crm Mcp Server

[![GitHub stars](https://img.shields.io/github/stars/LokiMCPUniverse/zoho-crm-mcp-server?style=social)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/LokiMCPUniverse/zoho-crm-mcp-server?style=social)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/network)
[![GitHub watchers](https://img.shields.io/github/watchers/LokiMCPUniverse/zoho-crm-mcp-server?style=social)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/watchers)

[![License](https://img.shields.io/github/license/LokiMCPUniverse/zoho-crm-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/LokiMCPUniverse/zoho-crm-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/LokiMCPUniverse/zoho-crm-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/LokiMCPUniverse/zoho-crm-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/commits)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-DC143C?style=for-the-badge)](https://modelcontextprotocol.io)

[![Commit Activity](https://img.shields.io/github/commit-activity/m/LokiMCPUniverse/zoho-crm-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/pulse)
[![Code Size](https://img.shields.io/github/languages/code-size/LokiMCPUniverse/zoho-crm-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server)
[![Contributors](https://img.shields.io/github/contributors/LokiMCPUniverse/zoho-crm-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/zoho-crm-mcp-server/graphs/contributors)

</div>

A Model Context Protocol (MCP) server for integrating Zoho CRM with GenAI applications.

## Overview

This MCP server provides seamless integration with Zoho CRM, enabling AI assistants and applications to interact with your CRM data through a standardized interface.

## Features

- 🔐 **OAuth 2.0 Authentication** - Secure authentication with automatic token refresh
- 📊 **Comprehensive CRM Operations** - Full support for Leads, Contacts, Deals, and more
- ⚡ **Rate Limiting** - Built-in rate limiting to respect API quotas
- 🔄 **Automatic Retry Logic** - Intelligent retry mechanism with exponential backoff
- 🛡️ **Error Handling** - Robust error handling and logging
- 🎯 **MCP Protocol Compliance** - Full compliance with Model Context Protocol specification
- 🚀 **Async Support** - Asynchronous operations for better performance

## Available Tools

The server exposes the following MCP tools:

1. **get_leads** - Retrieve leads from Zoho CRM with pagination
2. **create_lead** - Create new leads in Zoho CRM
3. **get_contacts** - Fetch contacts with pagination support
4. **get_deals** - Get deals from Zoho CRM
5. **search_records** - Search across any module with custom criteria

## Installation

### From PyPI (when published)

```bash
pip install zoho-crm-mcp-server
```

### From Source

```bash
git clone https://github.com/asklokesh/zoho-crm-mcp-server.git
cd zoho-crm-mcp-server
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Configuration

### 1. Set Up Zoho OAuth Credentials

1. Go to [Zoho API Console](https://api-console.zoho.com/)
2. Create a new Self Client application
3. Note your Client ID and Client Secret
4. Generate a refresh token with required scopes:
   - `ZohoCRM.modules.ALL`
   - `ZohoCRM.settings.ALL`

### 2. Create Environment Configuration

Copy the example configuration:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
ZOHO_CLIENT_ID=your_client_id_here
ZOHO_CLIENT_SECRET=your_client_secret_here
ZOHO_REFRESH_TOKEN=your_refresh_token_here

# Optional configurations
ZOHO_API_DOMAIN=https://www.zohoapis.com
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60
MAX_RETRIES=3
LOG_LEVEL=INFO
```

## Usage

### As a Standalone Server

```bash
zoho-crm-mcp
```

### In Python Code

```python
from zoho_crm_mcp import ZohoCRMMCPServer
import asyncio

async def main():
    server = ZohoCRMMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Using the Zoho CRM Client

```python
from zoho_crm_mcp import ZohoCRMClient, Config
import asyncio

async def main():
    config = Config()
    client = ZohoCRMClient(config)
    
    await client.initialize()
    
    # Get leads
    leads = await client.get_leads(page=1, per_page=50)
    print(f"Found {len(leads['data'])} leads")
    
    # Create a new lead
    new_lead = await client.create_lead({
        "Last_Name": "Doe",
        "First_Name": "John",
        "Email": "john.doe@example.com",
        "Company": "Acme Corp"
    })
    
    # Search for records
    results = await client.search_records(
        "Leads",
        "(Email:equals:john.doe@example.com)"
    )
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Development

### Running Tests

```bash
pytest tests/ -v --cov=zoho_crm_mcp
```

### Linting

```bash
ruff check src/ tests/
ruff format src/ tests/
```

### Building

```bash
python -m build
```

## CI/CD

This project includes GitHub Actions workflows for:

- ✅ Automated testing across Python 3.8-3.12
- 🔍 Code quality checks with Ruff
- 📦 Package building and validation
- 📊 Code coverage reporting

## Architecture

```
zoho-crm-mcp-server/
├── src/zoho_crm_mcp/
│   ├── __init__.py       # Package initialization
│   ├── server.py         # MCP server implementation
│   ├── zoho_client.py    # Zoho CRM API client
│   └── config.py         # Configuration management
├── tests/                # Comprehensive test suite
├── .github/workflows/    # CI/CD pipelines
└── pyproject.toml        # Project configuration
```

## Error Handling

The server includes comprehensive error handling:

- **Token Expiry**: Automatic token refresh when tokens expire
- **Rate Limiting**: Respects API rate limits with intelligent backoff
- **Network Errors**: Automatic retry with exponential backoff
- **Validation Errors**: Clear error messages for invalid configurations

## Logging

The server uses Python's built-in logging module. Configure log level via environment variable:

```bash
export LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'mcp'`
**Solution**: Install the MCP SDK: `pip install mcp`

**Issue**: Token refresh fails
**Solution**: Verify your refresh token is valid and has the required scopes

**Issue**: Rate limit errors
**Solution**: Adjust `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_PERIOD` in your `.env` file

## Requirements

- Python 3.8+
- requests >= 2.25.0
- mcp >= 1.0.0
- python-dotenv >= 0.19.0

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

For issues, questions, or contributions, please visit:
- [GitHub Issues](https://github.com/asklokesh/zoho-crm-mcp-server/issues)
- [GitHub Discussions](https://github.com/asklokesh/zoho-crm-mcp-server/discussions)

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification
- [Zoho CRM API](https://www.zoho.com/crm/developer/docs/api/) - API documentation
- All contributors who help improve this project

---

Made with ❤️ for the MCP community
