#!/usr/bin/env python3
"""
Helpers - Utility functions for API testing
"""

import random
import string
import time
import logging
from typing import Any, Callable, Optional, Dict
from datetime import datetime, timedelta
from faker import Faker

logger = logging.getLogger(__name__)
fake = Faker()


def generate_random_email() -> str:
    """
    Generate random email address

    Returns:
        Random email address
    """
    return fake.email()


def generate_random_string(length: int = 10) -> str:
    """
    Generate random string

    Args:
        length: Length of string

    Returns:
        Random string
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_phone() -> str:
    """
    Generate random phone number

    Returns:
        Random phone number
    """
    return fake.phone_number()


def generate_random_name() -> str:
    """
    Generate random name

    Returns:
        Random full name
    """
    return fake.name()


def generate_random_address() -> Dict[str, str]:
    """
    Generate random address

    Returns:
        Dictionary with address components
    """
    return {
        'street': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'zip': fake.postcode(),
        'country': fake.country()
    }


def generate_test_data(data_type: str) -> Dict[str, Any]:
    """
    Generate test data based on type

    Args:
        data_type: Type of data (user, product, order, etc.)

    Returns:
        Dictionary with test data
    """
    generators = {
        'user': lambda: {
            'name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.address(),
            'company': fake.company(),
            'job': fake.job()
        },
        'product': lambda: {
            'name': fake.word().title(),
            'description': fake.text(max_nb_chars=200),
            'price': round(random.uniform(10.0, 1000.0), 2),
            'category': random.choice(['Electronics', 'Clothing', 'Food', 'Books']),
            'stock': random.randint(0, 100),
            'sku': generate_random_string(8).upper()
        },
        'order': lambda: {
            'order_id': generate_random_string(12).upper(),
            'customer_name': fake.name(),
            'total': round(random.uniform(20.0, 500.0), 2),
            'status': random.choice(['pending', 'processing', 'shipped', 'delivered']),
            'order_date': fake.date_time_this_year().isoformat(),
            'items_count': random.randint(1, 5)
        }
    }

    generator = generators.get(data_type, lambda: {})
    return generator()


def wait_for_condition(
        condition: Callable[[], bool],
        timeout: float = 30.0,
        interval: float = 1.0,
        error_message: Optional[str] = None
) -> bool:
    """
    Wait for condition to become true

    Args:
        condition: Callable that returns bool
        timeout: Maximum wait time in seconds
        interval: Check interval in seconds
        error_message: Custom error message

    Returns:
        True if condition met

    Raises:
        TimeoutError: If condition not met within timeout
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            if condition():
                logger.info("✓ Condition met")
                return True
        except Exception as e:
            logger.debug(f"Condition check failed: {e}")

        time.sleep(interval)

    message = error_message or "Condition not met within timeout"
    logger.error(f"Timeout: {message}")
    raise TimeoutError(message)


def retry_on_failure(
        func: Callable,
        max_attempts: int = 3,
        delay: float = 1.0,
        exceptions: tuple = (Exception,)
) -> Any:
    """
    Retry function on failure

    Args:
        func: Function to retry
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds
        exceptions: Tuple of exceptions to catch

    Returns:
        Function result

    Raises:
        Last exception if all attempts fail
    """
    last_exception = None

    for attempt in range(max_attempts):
        try:
            result = func()
            logger.info(f"✓ Function succeeded on attempt {attempt + 1}")
            return result
        except exceptions as e:
            last_exception = e
            logger.warning(
                f"Attempt {attempt + 1}/{max_attempts} failed: {e}"
            )

            if attempt < max_attempts - 1:
                time.sleep(delay)

    logger.error(f"All {max_attempts} attempts failed")
    raise last_exception


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format datetime to ISO 8601 string

    Args:
        dt: Datetime object (default: now)

    Returns:
        ISO 8601 formatted string
    """
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()


def parse_timestamp(timestamp: str) -> datetime:
    """
    Parse ISO 8601 timestamp

    Args:
        timestamp: ISO 8601 formatted string

    Returns:
        Datetime object
    """
    return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))


def generate_date_range(days: int = 7) -> tuple:
    """
    Generate date range

    Args:
        days: Number of days in range

    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return (start_date, end_date)


def mask_sensitive_data(data: Dict[str, Any], fields: list) -> Dict[str, Any]:
    """
    Mask sensitive fields in data

    Args:
        data: Dictionary with data
        fields: List of field names to mask

    Returns:
        Dictionary with masked fields
    """
    masked_data = data.copy()

    for field in fields:
        if field in masked_data:
            value = str(masked_data[field])
            if len(value) > 4:
                masked_data[field] = value[:2] + '*' * (len(value) - 4) + value[-2:]
            else:
                masked_data[field] = '*' * len(value)

    return masked_data


def calculate_percentage(part: float, total: float) -> float:
    """
    Calculate percentage

    Args:
        part: Part value
        total: Total value

    Returns:
        Percentage value
    """
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries

    Args:
        dict1: First dictionary
        dict2: Second dictionary

    Returns:
        Merged dictionary
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def measure_execution_time(func: Callable) -> tuple:
    """
    Measure function execution time

    Args:
        func: Function to measure

    Returns:
        Tuple of (result, execution_time)
    """
    start_time = time.time()
    result = func()
    execution_time = time.time() - start_time

    logger.info(f"Execution time: {execution_time:.3f}s")
    return result, execution_time