#!/usr/bin/env python3
"""
Data Validation Tests
"""

import pytest
from framework.api_client import APIClient
from framework.validators import (
    validate_json_structure,
    validate_field_type,
    validate_field_value,
    validate_headers
)


@pytest.fixture
def api_client():
    """Fixture for API client"""
    client = APIClient(base_url='https://jsonplaceholder.typicode.com')
    yield client
    client.close()


class TestResponseStructure:
    """Tests for response structure validation"""

    def test_user_structure(self, api_client):
        """Test user object structure"""
        response = api_client.get('/users/1')
        data = response.json()

        # Validate required fields
        required_fields = ['id', 'name', 'username', 'email', 'address', 'phone']
        validate_json_structure(data, required_fields)

        # Validate nested address structure
        address_fields = ['street', 'suite', 'city', 'zipcode', 'geo']
        validate_json_structure(data['address'], address_fields)

    def test_post_structure(self, api_client):
        """Test post object structure"""
        response = api_client.get('/posts/1')
        data = response.json()

        required_fields = ['userId', 'id', 'title', 'body']
        validate_json_structure(data, required_fields)

    def test_comment_structure(self, api_client):
        """Test comment object structure"""
        response = api_client.get('/comments/1')
        data = response.json()

        required_fields = ['postId', 'id', 'name', 'email', 'body']
        validate_json_structure(data, required_fields)


class TestFieldTypes:
    """Tests for field type validation"""

    def test_user_field_types(self, api_client):
        """Test user field data types"""
        response = api_client.get('/users/1')
        data = response.json()

        # Validate field types
        validate_field_type(data, 'id', int)
        validate_field_type(data, 'name', str)
        validate_field_type(data, 'email', str)
        validate_field_type(data, 'address', dict)

    def test_post_field_types(self, api_client):
        """Test post field data types"""
        response = api_client.get('/posts/1')
        data = response.json()

        validate_field_type(data, 'id', int)
        validate_field_type(data, 'userId', int)
        validate_field_type(data, 'title', str)
        validate_field_type(data, 'body', str)

    def test_array_response_type(self, api_client):
        """Test array response type"""
        response = api_client.get('/users')
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        # Validate first item is dict
        assert isinstance(data[0], dict)


class TestFieldValues:
    """Tests for field value validation"""

    def test_user_id_value(self, api_client):
        """Test specific user ID value"""
        user_id = 1
        response = api_client.get(f'/users/{user_id}')
        data = response.json()

        validate_field_value(data, 'id', user_id)

    def test_post_user_id(self, api_client):
        """Test post belongs to correct user"""
        response = api_client.get('/posts/1')
        data = response.json()

        # Post 1 should belong to user 1
        validate_field_value(data, 'userId', 1)

    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    def test_multiple_user_ids(self, api_client, user_id):
        """Test multiple user IDs"""
        response = api_client.get(f'/users/{user_id}')
        data = response.json()

        validate_field_value(data, 'id', user_id)


class TestHeaderValidation:
    """Tests for HTTP header validation"""

    def test_content_type_header(self, api_client):
        """Test Content-Type header"""
        response = api_client.get('/users')

        expected_headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        validate_headers(response, expected_headers)

    def test_response_headers_present(self, api_client):
        """Test that expected headers are present"""
        response = api_client.get('/users')

        # Check important headers exist
        assert 'Content-Type' in response.headers
        assert 'Date' in response.headers
        assert 'Connection' in response.headers


class TestDataConstraints:
    """Tests for data constraints and business rules"""

    def test_email_format(self, api_client):
        """Test email field contains valid format"""
        response = api_client.get('/users/1')
        data = response.json()

        email = data['email']
        assert '@' in email
        assert '.' in email.split('@')[1]

    def test_positive_ids(self, api_client):
        """Test that IDs are positive integers"""
        response = api_client.get('/users')
        data = response.json()

        for user in data:
            assert user['id'] > 0

    def test_non_empty_strings(self, api_client):
        """Test that string fields are not empty"""
        response = api_client.get('/users/1')
        data = response.json()

        assert len(data['name']) > 0
        assert len(data['email']) > 0
        assert len(data['username']) > 0

    def test_nested_data_integrity(self, api_client):
        """Test nested data structure integrity"""
        response = api_client.get('/users/1')
        data = response.json()

        # Address should have geo coordinates
        geo = data['address']['geo']
        assert 'lat' in geo
        assert 'lng' in geo

        # Coordinates should be strings (as per API spec)
        assert isinstance(geo['lat'], str)
        assert isinstance(geo['lng'], str)


class TestErrorResponses:
    """Tests for error response validation"""

    def test_404_response_structure(self, api_client):
        """Test 404 error response structure"""
        response = api_client.get('/users/99999')

        assert response.status_code == 404
        # JSONPlaceholder returns empty object for 404
        data = response.json()
        assert data == {}

    def test_invalid_endpoint_response(self, api_client):
        """Test response for invalid endpoint"""
        response = api_client.get('/invalid-endpoint')
        assert response.status_code == 404

# Fix memory leak in deployment pipeline - 2025-10-28 00:51:54
def handle_error(error):
    """Handle error gracefully"""
    logger.error(f'Error: {error}')
    return None

# Refactor deployment script in notification service - 2025-11-05 07:10:24
# Refactored for better performance
def optimized_function():
    return list(map(process, data))