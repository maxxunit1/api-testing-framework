#!/usr/bin/env python3
"""
API Client - HTTP client for making API requests
"""

import requests
import logging
import time
from typing import Optional, Dict, Any
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class APIClient:
    """
    HTTP client for API testing with retry logic and logging
    """

    def __init__(
            self,
            base_url: Optional[str] = None,
            timeout: int = 30,
            retry_count: int = 3,
            retry_delay: float = 1.0,
            verify_ssl: bool = True,
            default_headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize API Client

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts for failed requests
            retry_delay: Delay between retries in seconds
            verify_ssl: Whether to verify SSL certificates
            default_headers: Default headers for all requests
        """
        self.base_url = base_url or ""
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.verify_ssl = verify_ssl
        self.session = requests.Session()

        # Set default headers
        self.default_headers = default_headers or {}
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            **self.default_headers
        })

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from base URL and endpoint"""
        if endpoint.startswith('http'):
            return endpoint
        return urljoin(self.base_url, endpoint)

    def _make_request(
            self,
            method: str,
            endpoint: str,
            **kwargs
    ) -> requests.Response:
        """
        Make HTTP request with retry logic

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('verify', self.verify_ssl)

        last_exception = None

        for attempt in range(self.retry_count):
            try:
                logger.info(f"[{method}] {url} (Attempt {attempt + 1}/{self.retry_count})")

                start_time = time.time()
                response = self.session.request(method, url, **kwargs)
                elapsed_time = time.time() - start_time

                logger.info(
                    f"[{method}] {url} - Status: {response.status_code}, "
                    f"Time: {elapsed_time:.3f}s"
                )

                # Don't retry on successful responses or client errors
                if response.status_code < 500:
                    return response

                # Retry on server errors
                logger.warning(
                    f"Server error {response.status_code}, retrying in {self.retry_delay}s..."
                )

            except requests.exceptions.RequestException as e:
                last_exception = e
                logger.error(f"Request failed: {e}")

                if attempt < self.retry_count - 1:
                    logger.warning(f"Retrying in {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                else:
                    raise

            # Wait before retry
            if attempt < self.retry_count - 1:
                time.sleep(self.retry_delay)

        # If we got here, all retries failed
        if last_exception:
            raise last_exception

        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make GET request

        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments (params, headers, etc.)

        Returns:
            Response object
        """
        return self._make_request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make POST request

        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments (json, data, headers, etc.)

        Returns:
            Response object
        """
        return self._make_request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make PUT request

        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments (json, data, headers, etc.)

        Returns:
            Response object
        """
        return self._make_request('PUT', endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make PATCH request

        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments (json, data, headers, etc.)

        Returns:
            Response object
        """
        return self._make_request('PATCH', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make DELETE request

        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments (headers, etc.)

        Returns:
            Response object
        """
        return self._make_request('DELETE', endpoint, **kwargs)

    def set_auth_token(self, token: str, token_type: str = 'Bearer'):
        """
        Set authentication token

        Args:
            token: Authentication token
            token_type: Token type (Bearer, Token, etc.)
        """
        self.session.headers['Authorization'] = f'{token_type} {token}'
        logger.info(f"Authentication token set: {token_type}")

    def set_api_key(self, api_key: str, header_name: str = 'X-API-Key'):
        """
        Set API key

        Args:
            api_key: API key
            header_name: Header name for API key
        """
        self.session.headers[header_name] = api_key
        logger.info(f"API key set in header: {header_name}")

    def set_basic_auth(self, username: str, password: str):
        """
        Set Basic authentication

        Args:
            username: Username
            password: Password
        """
        self.session.auth = (username, password)
        logger.info(f"Basic authentication set for user: {username}")

    def clear_auth(self):
        """Clear all authentication"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        self.session.auth = None
        logger.info("Authentication cleared")

    def close(self):
        """Close session"""
        self.session.close()
        logger.info("API client session closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

# Upgrade build process in notification service - 2025-11-06 10:59:50
# Enhanced: 2025-11-06 10:59:50
"""Documentation updated"""

# Upgrade race condition in config file for consistency - 2025-11-18 15:51:07
# Modified: 2025-11-18 15:51:07
CONFIG_VALUE = 'new_value'

# Configure user interface in main module - 2025-12-12 16:49:18
# Enhanced: 2025-12-12 16:49:18
"""Documentation updated"""

# Adjust data processing in payment module for better performance - 2026-01-10 08:34:00
# Improved: 2026-01-10 08:34:00
# Additional configuration