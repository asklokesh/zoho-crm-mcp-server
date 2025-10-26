"""Test configuration module."""

import pytest
import os
from zoho_crm_mcp.config import Config


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    config.zoho_client_id = "test_id"
    config.zoho_client_secret = "test_secret"
    config.zoho_refresh_token = "test_token"
    
    assert config.zoho_client_id == "test_id"
    assert config.zoho_client_secret == "test_secret"
    assert config.zoho_refresh_token == "test_token"
    assert config.zoho_api_domain == "https://www.zohoapis.com"
    assert config.rate_limit_requests == 100
    assert config.rate_limit_period == 60
    assert config.max_retries == 3


def test_config_from_env():
    """Test configuration from environment variables."""
    os.environ["ZOHO_CLIENT_ID"] = "env_id"
    os.environ["ZOHO_CLIENT_SECRET"] = "env_secret"
    os.environ["ZOHO_REFRESH_TOKEN"] = "env_token"
    
    config = Config()
    
    assert config.zoho_client_id == "env_id"
    assert config.zoho_client_secret == "env_secret"
    assert config.zoho_refresh_token == "env_token"
    
    # Clean up
    del os.environ["ZOHO_CLIENT_ID"]
    del os.environ["ZOHO_CLIENT_SECRET"]
    del os.environ["ZOHO_REFRESH_TOKEN"]


def test_config_validation():
    """Test configuration validation."""
    config = Config()
    
    with pytest.raises(ValueError, match="ZOHO_CLIENT_ID must be set"):
        config.validate_required_fields()


def test_config_custom_values():
    """Test custom configuration values."""
    os.environ["ZOHO_CLIENT_ID"] = "custom_id"
    os.environ["ZOHO_CLIENT_SECRET"] = "custom_secret"
    os.environ["ZOHO_REFRESH_TOKEN"] = "custom_token"
    os.environ["RATE_LIMIT_REQUESTS"] = "50"
    os.environ["MAX_RETRIES"] = "5"
    
    config = Config()
    
    assert config.rate_limit_requests == 50
    assert config.max_retries == 5
    
    # Clean up
    for key in ["ZOHO_CLIENT_ID", "ZOHO_CLIENT_SECRET", "ZOHO_REFRESH_TOKEN", "RATE_LIMIT_REQUESTS", "MAX_RETRIES"]:
        if key in os.environ:
            del os.environ[key]
