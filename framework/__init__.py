"""
API Testing Framework
=====================

A comprehensive framework for API testing with support for REST APIs,
authentication, response validation, and performance testing.
"""

__version__ = "1.0.0"
__author__ = "API Testing Framework Team"

from .api_client import APIClient
from .validators import validate_response, validate_status_code, validate_response_time
from .helpers import generate_random_email, generate_test_data

__all__ = [
    'APIClient',
    'validate_response',
    'validate_status_code',
    'validate_response_time',
    'generate_random_email',
    'generate_test_data'
]

# Remove logging system - 2025-10-14 16:53:17
# Modified: 2025-10-14 16:53:17
CONFIG_VALUE = 'new_value'

# Repair race condition - 2025-10-29 12:48:11
# Enhanced: 2025-10-29 12:48:11
"""Documentation updated"""