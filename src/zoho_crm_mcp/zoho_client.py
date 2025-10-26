"""Zoho CRM API client implementation."""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from .config import Config

logger = logging.getLogger(__name__)


class ZohoCRMClient:
    """Client for Zoho CRM API."""

    def __init__(self, config: Config):
        """Initialize Zoho CRM client."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required. Install with: pip install requests")
        
        self.config = config
        self.access_token: Optional[str] = config.zoho_access_token
        self.token_expires_at: Optional[datetime] = None
        self.session: Optional[requests.Session] = None
        self._request_count = 0
        self._request_window_start = datetime.now()

    async def initialize(self):
        """Initialize the client."""
        self.session = requests.Session()
        self.session.timeout = 30.0
        if not self.access_token:
            await self.refresh_access_token()

    async def close(self):
        """Close the client."""
        if self.session:
            self.session.close()

    async def refresh_access_token(self):
        """Refresh the access token using refresh token."""
        try:
            logger.info("Refreshing Zoho access token...")
            
            if not self.config.zoho_refresh_token:
                raise ValueError("Refresh token is not configured")

            params = {
                "refresh_token": self.config.zoho_refresh_token,
                "client_id": self.config.zoho_client_id,
                "client_secret": self.config.zoho_client_secret,
                "grant_type": "refresh_token"
            }

            response = requests.post(
                self.config.zoho_accounts_url,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            self.access_token = data.get("access_token")
            expires_in = data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Access token refreshed successfully")

        except Exception as e:
            logger.error(f"Error refreshing access token: {e}")
            raise

    async def _ensure_token_valid(self):
        """Ensure access token is valid, refresh if needed."""
        if not self.access_token or (
            self.token_expires_at and datetime.now() >= self.token_expires_at - timedelta(minutes=5)
        ):
            await self.refresh_access_token()

    async def _check_rate_limit(self):
        """Check and enforce rate limiting."""
        now = datetime.now()
        if (now - self._request_window_start).seconds >= self.config.rate_limit_period:
            self._request_count = 0
            self._request_window_start = now

        if self._request_count >= self.config.rate_limit_requests:
            wait_time = self.config.rate_limit_period - (now - self._request_window_start).seconds
            if wait_time > 0:
                logger.warning(f"Rate limit reached, waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                self._request_count = 0
                self._request_window_start = datetime.now()

        self._request_count += 1

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Make an authenticated request to Zoho CRM API."""
        await self._ensure_token_valid()
        await self._check_rate_limit()

        if not self.session:
            raise RuntimeError("Client not initialized")

        headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}"
        }

        url = f"{self.config.zoho_api_domain}/crm/v6/{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.HTTPError as e:
            if e.response.status_code == 401 and retry_count < self.config.max_retries:
                # Token might be invalid, try refreshing
                logger.warning("Got 401, refreshing token and retrying...")
                await self.refresh_access_token()
                return await self._make_request(method, endpoint, params, json, retry_count + 1)
            
            logger.error(f"HTTP error: {e}")
            raise

        except Exception as e:
            if retry_count < self.config.max_retries:
                wait_time = self.config.retry_delay * (2 ** retry_count)
                logger.warning(f"Request failed, retrying in {wait_time}s... (attempt {retry_count + 1}/{self.config.max_retries})")
                await asyncio.sleep(wait_time)
                return await self._make_request(method, endpoint, params, json, retry_count + 1)
            
            logger.error(f"Request failed after {self.config.max_retries} retries: {e}")
            raise

    async def get_leads(self, page: int = 1, per_page: int = 200) -> Dict[str, Any]:
        """Get leads from Zoho CRM."""
        params = {
            "page": page,
            "per_page": min(per_page, 200)
        }
        return await self._make_request("GET", "Leads", params=params)

    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead in Zoho CRM."""
        data = {
            "data": [lead_data]
        }
        return await self._make_request("POST", "Leads", json=data)

    async def get_contacts(self, page: int = 1, per_page: int = 200) -> Dict[str, Any]:
        """Get contacts from Zoho CRM."""
        params = {
            "page": page,
            "per_page": min(per_page, 200)
        }
        return await self._make_request("GET", "Contacts", params=params)

    async def get_deals(self, page: int = 1, per_page: int = 200) -> Dict[str, Any]:
        """Get deals from Zoho CRM."""
        params = {
            "page": page,
            "per_page": min(per_page, 200)
        }
        return await self._make_request("GET", "Deals", params=params)

    async def search_records(self, module: str, criteria: str) -> Dict[str, Any]:
        """Search records in Zoho CRM."""
        params = {
            "criteria": criteria
        }
        return await self._make_request("GET", f"{module}/search", params=params)

    async def get_record(self, module: str, record_id: str) -> Dict[str, Any]:
        """Get a specific record from Zoho CRM."""
        return await self._make_request("GET", f"{module}/{record_id}")

    async def update_record(self, module: str, record_id: str, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record in Zoho CRM."""
        data = {
            "data": [record_data]
        }
        return await self._make_request("PUT", f"{module}/{record_id}", json=data)

    async def delete_record(self, module: str, record_id: str) -> Dict[str, Any]:
        """Delete a record from Zoho CRM."""
        return await self._make_request("DELETE", f"{module}/{record_id}")
