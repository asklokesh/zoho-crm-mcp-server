# Zoho CRM MCP Server

A Model Context Protocol (MCP) server for integrating Zoho CRM with GenAI applications.

## Overview

Complete CRM suite integration

## Features

- Comprehensive Zoho CRM API coverage
- Multiple authentication methods
- Enterprise-ready with rate limiting
- Full error handling and retry logic
- Async support for better performance

## Installation

```bash
pip install zoho-crm-mcp-server
```

Or install from source:

```bash
git clone https://github.com/asklokesh/zoho-crm-mcp-server.git
cd zoho-crm-mcp-server
pip install -e .
```

## Configuration

Create a `.env` file or set environment variables according to Zoho CRM API requirements.

## Quick Start

```python
from zoho_crm_mcp import ZohoCrmMCPServer

# Initialize the server
server = ZohoCrmMCPServer()

# Start the server
server.start()
```

## License

MIT License - see LICENSE file for details
