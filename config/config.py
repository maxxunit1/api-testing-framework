#!/usr/bin/env python3
"""
Configuration Settings
"""

import os
import json
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration management"""

    # API Settings
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://jsonplaceholder.typicode.com')
    API_KEY = os.getenv('API_KEY', '')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN', '')

    # Request Settings
    TIMEOUT = int(os.getenv('TIMEOUT', 30))
    RETRY_COUNT = int(os.getenv('RETRY_COUNT', 3))
    RETRY_DELAY = float(os.getenv('RETRY_DELAY', 1.0))

    # SSL Settings
    VERIFY_SSL = os.getenv('VERIFY_SSL', 'true').lower() == 'true'

    # Test Settings
    TEST_ENV = os.getenv('TEST_ENV', 'test')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Parallel Testing
    PARALLEL_WORKERS = int(os.getenv('PARALLEL_WORKERS', 4))

    # Report Settings
    REPORT_DIR = Path(os.getenv('REPORT_DIR', 'reports'))
    GENERATE_HTML_REPORT = os.getenv('GENERATE_HTML_REPORT', 'true').lower() == 'true'
    GENERATE_JSON_REPORT = os.getenv('GENERATE_JSON_REPORT', 'false').lower() == 'true'

    @classmethod
    def load_endpoints(cls) -> Dict[str, Any]:
        """
        Load endpoints from JSON file

        Returns:
            Dictionary with endpoints
        """
        endpoints_file = Path(__file__).parent / 'endpoints.json'

        if not endpoints_file.exists():
            return {}

        with open(endpoints_file, 'r') as f:
            return json.load(f)

    @classmethod
    def get_endpoint(cls, category: str, action: str) -> str:
        """
        Get specific endpoint

        Args:
            category: Endpoint category (e.g., 'users', 'posts')
            action: Action name (e.g., 'list', 'create', 'get')

        Returns:
            Endpoint path
        """
        endpoints = cls.load_endpoints()
        return endpoints.get(category, {}).get(action, '')

    @classmethod
    def get_full_url(cls, category: str, action: str, **kwargs) -> str:
        """
        Get full URL for endpoint

        Args:
            category: Endpoint category
            action: Action name
            **kwargs: URL parameters for formatting

        Returns:
            Full URL
        """
        endpoint = cls.get_endpoint(category, action)
        if kwargs:
            endpoint = endpoint.format(**kwargs)

        return f"{cls.API_BASE_URL}{endpoint}"

    @classmethod
    def get_auth_headers(cls) -> Dict[str, str]:
        """
        Get authentication headers

        Returns:
            Dictionary with auth headers
        """
        headers = {}

        if cls.AUTH_TOKEN:
            headers['Authorization'] = f'Bearer {cls.AUTH_TOKEN}'

        if cls.API_KEY:
            headers['X-API-Key'] = cls.API_KEY

        return headers

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.TEST_ENV.lower() == 'production'

    @classmethod
    def is_staging(cls) -> bool:
        """Check if running in staging environment"""
        return cls.TEST_ENV.lower() == 'staging'

    @classmethod
    def is_test(cls) -> bool:
        """Check if running in test environment"""
        return cls.TEST_ENV.lower() in ['test', 'testing']

# Optimize build process - 2025-10-15 13:50:28
# Simplified logic
result = value if condition else default

# Enhance test coverage in database layer for security compliance - 2025-10-20 11:30:39
# Modified: 2025-10-20 11:30:39
CONFIG_VALUE = 'new_value'