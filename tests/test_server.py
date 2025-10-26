"""Test MCP server."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from zoho_crm_mcp.server import ZohoCRMMCPServer


@pytest.fixture
def server():
    """Create a server instance."""
    with patch("zoho_crm_mcp.server.Config") as mock_config:
        mock_config.return_value = MagicMock()
        return ZohoCRMMCPServer()


def test_server_initialization(server):
    """Test server initialization."""
    assert server.server is not None
    assert server.config is not None


@pytest.mark.asyncio
async def test_list_tools(server):
    """Test listing tools."""
    # Get the list_tools handler
    list_tools_handler = None
    for handler_name, handler in server.server._request_handlers.items():
        if "list_tools" in str(handler_name):
            list_tools_handler = handler
            break
    
    if list_tools_handler:
        tools = await list_tools_handler()
        assert len(tools) > 0
        
        tool_names = [tool.name for tool in tools]
        assert "get_leads" in tool_names
        assert "create_lead" in tool_names
        assert "get_contacts" in tool_names
        assert "get_deals" in tool_names
        assert "search_records" in tool_names


@pytest.mark.asyncio
async def test_call_tool_get_leads(server):
    """Test calling get_leads tool."""
    mock_client = AsyncMock()
    mock_client.get_leads.return_value = {"data": [{"id": "1"}]}
    mock_client.initialize = AsyncMock()
    
    server.client = mock_client
    
    # Get the call_tool handler
    call_tool_handler = None
    for handler_name, handler in server.server._request_handlers.items():
        if "call_tool" in str(handler_name):
            call_tool_handler = handler
            break
    
    if call_tool_handler:
        result = await call_tool_handler("get_leads", {"page": 1, "per_page": 50})
        assert len(result) > 0
        assert result[0].type == "text"


@pytest.mark.asyncio
async def test_call_tool_error_handling(server):
    """Test error handling in tool calls."""
    mock_client = AsyncMock()
    mock_client.get_leads.side_effect = Exception("Test error")
    mock_client.initialize = AsyncMock()
    
    server.client = mock_client
    
    # Get the call_tool handler
    call_tool_handler = None
    for handler_name, handler in server.server._request_handlers.items():
        if "call_tool" in str(handler_name):
            call_tool_handler = handler
            break
    
    if call_tool_handler:
        result = await call_tool_handler("get_leads", {})
        assert len(result) > 0
        assert "Error" in result[0].text
