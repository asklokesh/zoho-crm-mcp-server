"""Configuration management for Zoho CRM MCP Server."""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for Zoho CRM MCP Server."""
    
    # Zoho OAuth credentials
    zoho_client_id: str = ""
    zoho_client_secret: str = ""
    zoho_refresh_token: str = ""
    zoho_access_token: Optional[str] = None
    
    # Zoho API settings
    zoho_api_domain: str = "https://www.zohoapis.com"
    zoho_accounts_url: str = "https://accounts.zoho.com/oauth/v2/token"
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds
    
    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Logging
    log_level: str = "INFO"

    def __init__(self):
        """Initialize configuration from environment variables."""
        self.zoho_client_id = os.getenv("ZOHO_CLIENT_ID", "")
        self.zoho_client_secret = os.getenv("ZOHO_CLIENT_SECRET", "")
        self.zoho_refresh_token = os.getenv("ZOHO_REFRESH_TOKEN", "")
        self.zoho_access_token = os.getenv("ZOHO_ACCESS_TOKEN")
        self.zoho_api_domain = os.getenv("ZOHO_API_DOMAIN", "https://www.zohoapis.com")
        self.zoho_accounts_url = os.getenv("ZOHO_ACCOUNTS_URL", "https://accounts.zoho.com/oauth/v2/token")
        self.rate_limit_requests = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        self.rate_limit_period = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.retry_delay = float(os.getenv("RETRY_DELAY", "1.0"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate_required_fields(self):
        """Validate that required fields are set."""
        if not self.zoho_client_id:
            raise ValueError("ZOHO_CLIENT_ID must be set")
        if not self.zoho_client_secret:
            raise ValueError("ZOHO_CLIENT_SECRET must be set")
        if not self.zoho_refresh_token:
            raise ValueError("ZOHO_REFRESH_TOKEN must be set")
