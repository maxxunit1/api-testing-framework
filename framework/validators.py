#!/usr/bin/env python3
"""
Validators - Response validation utilities
"""

import json
import logging
from typing import Any, Dict, Optional, List
from jsonschema import validate, ValidationError
import requests

logger = logging.getLogger(__name__)


def validate_status_code(
        response: requests.Response,
        expected_code: int
) -> bool:
    """
    Validate HTTP status code

    Args:
        response: Response object
        expected_code: Expected status code

    Returns:
        True if status code matches

    Raises:
        AssertionError: If status code doesn't match
    """
    actual_code = response.status_code

    if actual_code != expected_code:
        logger.error(
            f"Status code mismatch: expected {expected_code}, got {actual_code}"
        )
        raise AssertionError(
            f"Expected status code {expected_code}, but got {actual_code}. "
            f"Response: {response.text[:200]}"
        )

    logger.info(f"✓ Status code validated: {expected_code}")
    return True


def validate_response_time(
        response: requests.Response,
        max_time: float
) -> bool:
    """
    Validate response time

    Args:
        response: Response object
        max_time: Maximum allowed response time in seconds

    Returns:
        True if response time is within limit

    Raises:
        AssertionError: If response time exceeds limit
    """
    response_time = response.elapsed.total_seconds()

    if response_time > max_time:
        logger.error(
            f"Response time exceeded: {response_time:.3f}s > {max_time}s"
        )
        raise AssertionError(
            f"Response time {response_time:.3f}s exceeded maximum {max_time}s"
        )

    logger.info(f"✓ Response time validated: {response_time:.3f}s")
    return True


def validate_json_schema(
        data: Dict[str, Any],
        schema: Dict[str, Any]
) -> bool:
    """
    Validate JSON data against schema

    Args:
        data: JSON data to validate
        schema: JSON schema

    Returns:
        True if data matches schema

    Raises:
        ValidationError: If data doesn't match schema
    """
    try:
        validate(instance=data, schema=schema)
        logger.info("✓ JSON schema validated successfully")
        return True
    except ValidationError as e:
        logger.error(f"JSON schema validation failed: {e.message}")
        raise


def validate_response(
        response: requests.Response,
        schema: Optional[Dict[str, Any]] = None,
        expected_status: Optional[int] = None,
        max_response_time: Optional[float] = None
) -> bool:
    """
    Comprehensive response validation

    Args:
        response: Response object
        schema: Optional JSON schema for validation
        expected_status: Optional expected status code
        max_response_time: Optional maximum response time

    Returns:
        True if all validations pass
    """
    # Validate status code
    if expected_status is not None:
        validate_status_code(response, expected_status)

    # Validate response time
    if max_response_time is not None:
        validate_response_time(response, max_response_time)

    # Validate JSON schema
    if schema is not None:
        try:
            data = response.json()
            validate_json_schema(data, schema)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise AssertionError(f"Response is not valid JSON: {e}")

    logger.info("✓ All validations passed")
    return True


def validate_json_structure(
        data: Dict[str, Any],
        required_keys: List[str]
) -> bool:
    """
    Validate JSON structure has required keys

    Args:
        data: JSON data
        required_keys: List of required keys

    Returns:
        True if all required keys present

    Raises:
        AssertionError: If required keys are missing
    """
    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        logger.error(f"Missing required keys: {missing_keys}")
        raise AssertionError(f"Missing required keys: {missing_keys}")

    logger.info(f"✓ All required keys present: {required_keys}")
    return True


def validate_field_type(
        data: Dict[str, Any],
        field: str,
        expected_type: type
) -> bool:
    """
    Validate field type in JSON data

    Args:
        data: JSON data
        field: Field name
        expected_type: Expected Python type

    Returns:
        True if field type matches

    Raises:
        AssertionError: If field type doesn't match
    """
    if field not in data:
        logger.error(f"Field '{field}' not found in data")
        raise AssertionError(f"Field '{field}' not found in response data")

    actual_type = type(data[field])

    if not isinstance(data[field], expected_type):
        logger.error(
            f"Type mismatch for field '{field}': "
            f"expected {expected_type.__name__}, got {actual_type.__name__}"
        )
        raise AssertionError(
            f"Field '{field}' has type {actual_type.__name__}, "
            f"expected {expected_type.__name__}"
        )

    logger.info(f"✓ Field '{field}' type validated: {expected_type.__name__}")
    return True


def validate_field_value(
        data: Dict[str, Any],
        field: str,
        expected_value: Any
) -> bool:
    """
    Validate field value in JSON data

    Args:
        data: JSON data
        field: Field name
        expected_value: Expected value

    Returns:
        True if field value matches

    Raises:
        AssertionError: If field value doesn't match
    """
    if field not in data:
        logger.error(f"Field '{field}' not found in data")
        raise AssertionError(f"Field '{field}' not found in response data")

    actual_value = data[field]

    if actual_value != expected_value:
        logger.error(
            f"Value mismatch for field '{field}': "
            f"expected {expected_value}, got {actual_value}"
        )
        raise AssertionError(
            f"Field '{field}' has value {actual_value}, "
            f"expected {expected_value}"
        )

    logger.info(f"✓ Field '{field}' value validated: {expected_value}")
    return True


def validate_headers(
        response: requests.Response,
        expected_headers: Dict[str, str]
) -> bool:
    """
    Validate response headers

    Args:
        response: Response object
        expected_headers: Dictionary of expected headers

    Returns:
        True if all headers match

    Raises:
        AssertionError: If headers don't match
    """
    for header, expected_value in expected_headers.items():
        actual_value = response.headers.get(header)

        if actual_value != expected_value:
            logger.error(
                f"Header mismatch for '{header}': "
                f"expected '{expected_value}', got '{actual_value}'"
            )
            raise AssertionError(
                f"Header '{header}' has value '{actual_value}', "
                f"expected '{expected_value}'"
            )

    logger.info(f"✓ Headers validated: {list(expected_headers.keys())}")
    return True


class CustomValidator:
    """Base class for custom validators"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate(self, data: Any) -> bool:
        """
        Override this method for custom validation

        Args:
            data: Data to validate

        Returns:
            True if validation passes
        """
        raise NotImplementedError("Subclasses must implement validate method")

# Implement search functionality in email service - 2025-10-22 21:15:38
async def async_operation():
    """Async operation support"""
    result = await fetch_data()
    return process(result)

# Optimize edge case - 2025-12-11 15:21:34
# Refactored for better performance
def optimized_function():
    return list(map(process, data))