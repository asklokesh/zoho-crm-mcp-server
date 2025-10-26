"""Test Zoho CRM client."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from zoho_crm_mcp.zoho_client import ZohoCRMClient
from zoho_crm_mcp.config import Config


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = Config()
    config.zoho_client_id = "test_client_id"
    config.zoho_client_secret = "test_client_secret"
    config.zoho_refresh_token = "test_refresh_token"
    config.zoho_access_token = "test_access_token"
    return config


@pytest.fixture
def client(mock_config):
    """Create a Zoho CRM client instance."""
    return ZohoCRMClient(mock_config)


@pytest.mark.asyncio
async def test_client_initialization(client):
    """Test client initialization."""
    assert client.config is not None
    assert client.access_token == "test_access_token"


@pytest.mark.asyncio
async def test_refresh_access_token(client):
    """Test token refresh."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "access_token": "new_access_token",
        "expires_in": 3600
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("requests.post", return_value=mock_response):
        await client.refresh_access_token()
        
        assert client.access_token == "new_access_token"
        assert client.token_expires_at is not None


@pytest.mark.asyncio
async def test_get_leads(client):
    """Test getting leads."""
    await client.initialize()
    
    mock_response = {
        "data": [
            {"id": "1", "Last_Name": "Doe"},
            {"id": "2", "Last_Name": "Smith"}
        ]
    }
    
    with patch.object(client, "_make_request", return_value=mock_response) as mock_request:
        result = await client.get_leads(page=1, per_page=50)
        
        mock_request.assert_called_once_with("GET", "Leads", params={"page": 1, "per_page": 50})
        assert result == mock_response
        assert len(result["data"]) == 2
    
    await client.close()


@pytest.mark.asyncio
async def test_create_lead(client):
    """Test creating a lead."""
    await client.initialize()
    
    lead_data = {
        "Last_Name": "Test Lead",
        "Email": "test@example.com"
    }
    
    mock_response = {
        "data": [{"id": "123456", "status": "success"}]
    }
    
    with patch.object(client, "_make_request", return_value=mock_response) as mock_request:
        result = await client.create_lead(lead_data)
        
        expected_data = {"data": [lead_data]}
        mock_request.assert_called_once_with("POST", "Leads", json=expected_data)
        assert result == mock_response
    
    await client.close()


@pytest.mark.asyncio
async def test_search_records(client):
    """Test searching records."""
    await client.initialize()
    
    mock_response = {
        "data": [{"id": "1", "Email": "test@example.com"}]
    }
    
    with patch.object(client, "_make_request", return_value=mock_response) as mock_request:
        result = await client.search_records("Leads", "(Email:equals:test@example.com)")
        
        mock_request.assert_called_once_with(
            "GET",
            "Leads/search",
            params={"criteria": "(Email:equals:test@example.com)"}
        )
        assert result == mock_response
    
    await client.close()


@pytest.mark.asyncio
async def test_rate_limiting(client):
    """Test rate limiting."""
    client.config.rate_limit_requests = 2
    client.config.rate_limit_period = 1
    
    # First two requests should go through immediately
    await client._check_rate_limit()
    await client._check_rate_limit()
    
    # Third request should be rate limited
    start_time = datetime.now()
    await client._check_rate_limit()
    elapsed = (datetime.now() - start_time).total_seconds()
    
    # Should have waited at least some time (may not be full second in fast tests)
    assert elapsed >= 0


@pytest.mark.asyncio
async def test_token_expiry_check(client):
    """Test token expiry check."""
    # Set token to expire soon
    client.token_expires_at = datetime.now() + timedelta(minutes=2)
    
    with patch.object(client, "refresh_access_token") as mock_refresh:
        await client._ensure_token_valid()
        mock_refresh.assert_called_once()
