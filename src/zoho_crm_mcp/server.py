"""Main MCP server implementation for Zoho CRM."""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # Fallback types for when MCP is not installed
    class Tool:
        def __init__(self, name, description, inputSchema):
            self.name = name
            self.description = description
            self.inputSchema = inputSchema
    
    class TextContent:
        def __init__(self, type, text):
            self.type = type
            self.text = text
    
    Server = None
    stdio_server = None

from .zoho_client import ZohoCRMClient
from .config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ZohoCRMMCPServer:
    """MCP Server for Zoho CRM integration."""

    def __init__(self):
        """Initialize the MCP server."""
        if not MCP_AVAILABLE:
            logger.warning("MCP SDK not installed. Install with: pip install mcp")
        
        self.server = Server("zoho-crm-mcp-server") if MCP_AVAILABLE else None
        self.config = Config()
        self.client: Optional[ZohoCRMClient] = None
        
        # Register handlers
        if MCP_AVAILABLE:
            self._register_handlers()

    def _register_handlers(self):
        """Register MCP handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available Zoho CRM tools."""
            return [
                Tool(
                    name="get_leads",
                    description="Get leads from Zoho CRM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "number",
                                "description": "Page number (default: 1)"
                            },
                            "per_page": {
                                "type": "number",
                                "description": "Records per page (default: 200, max: 200)"
                            }
                        }
                    }
                ),
                Tool(
                    name="create_lead",
                    description="Create a new lead in Zoho CRM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "last_name": {
                                "type": "string",
                                "description": "Lead's last name (required)"
                            },
                            "first_name": {
                                "type": "string",
                                "description": "Lead's first name"
                            },
                            "email": {
                                "type": "string",
                                "description": "Lead's email"
                            },
                            "company": {
                                "type": "string",
                                "description": "Lead's company"
                            },
                            "phone": {
                                "type": "string",
                                "description": "Lead's phone number"
                            }
                        },
                        "required": ["last_name"]
                    }
                ),
                Tool(
                    name="get_contacts",
                    description="Get contacts from Zoho CRM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "number",
                                "description": "Page number (default: 1)"
                            },
                            "per_page": {
                                "type": "number",
                                "description": "Records per page (default: 200, max: 200)"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_deals",
                    description="Get deals from Zoho CRM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "number",
                                "description": "Page number (default: 1)"
                            },
                            "per_page": {
                                "type": "number",
                                "description": "Records per page (default: 200, max: 200)"
                            }
                        }
                    }
                ),
                Tool(
                    name="search_records",
                    description="Search records in Zoho CRM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "module": {
                                "type": "string",
                                "description": "Module name (e.g., Leads, Contacts, Deals)"
                            },
                            "criteria": {
                                "type": "string",
                                "description": "Search criteria (e.g., (Email:equals:test@example.com))"
                            }
                        },
                        "required": ["module", "criteria"]
                    }
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Call a Zoho CRM tool."""
            try:
                # Initialize client if not already done
                if self.client is None:
                    self.client = ZohoCRMClient(self.config)
                    await self.client.initialize()

                # Route to appropriate handler
                if name == "get_leads":
                    result = await self.client.get_leads(
                        page=arguments.get("page", 1),
                        per_page=arguments.get("per_page", 200)
                    )
                elif name == "create_lead":
                    result = await self.client.create_lead(arguments)
                elif name == "get_contacts":
                    result = await self.client.get_contacts(
                        page=arguments.get("page", 1),
                        per_page=arguments.get("per_page", 200)
                    )
                elif name == "get_deals":
                    result = await self.client.get_deals(
                        page=arguments.get("page", 1),
                        per_page=arguments.get("per_page", 200)
                    )
                elif name == "search_records":
                    result = await self.client.search_records(
                        module=arguments["module"],
                        criteria=arguments["criteria"]
                    )
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(type="text", text=str(result))]

            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def run(self):
        """Run the MCP server."""
        if not MCP_AVAILABLE:
            raise RuntimeError("MCP SDK is required. Install with: pip install mcp")
        
        logger.info("Starting Zoho CRM MCP Server...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point for the server."""
    server = ZohoCRMMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
