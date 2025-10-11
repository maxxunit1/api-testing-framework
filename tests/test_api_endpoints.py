#!/usr/bin/env python3
"""
API Endpoints Tests
"""

import pytest
from framework.api_client import APIClient
from framework.validators import (
    validate_status_code,
    validate_response_time,
    validate_json_structure
)
from framework.helpers import generate_test_data


@pytest.fixture
def api_client():
    """Fixture for API client"""
    client = APIClient(base_url='https://jsonplaceholder.typicode.com')
    yield client
    client.close()


class TestUserEndpoints:
    """Tests for user endpoints"""

    def test_get_users_list(self, api_client):
        """Test getting list of users"""
        response = api_client.get('/users')

        # Validate response
        validate_status_code(response, 200)
        validate_response_time(response, max_time=2.0)

        # Check response data
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Validate first user structure
        first_user = data[0]
        validate_json_structure(first_user, ['id', 'name', 'email'])

    def test_get_user_by_id(self, api_client):
        """Test getting user by ID"""
        user_id = 1
        response = api_client.get(f'/users/{user_id}')

        validate_status_code(response, 200)

        data = response.json()
        assert data['id'] == user_id
        assert 'name' in data
        assert 'email' in data

    def test_get_nonexistent_user(self, api_client):
        """Test getting non-existent user"""
        response = api_client.get('/users/99999')
        validate_status_code(response, 404)

    def test_create_user(self, api_client):
        """Test creating new user"""
        user_data = generate_test_data('user')
        payload = {
            'name': user_data['name'],
            'email': user_data['email']
        }

        response = api_client.post('/users', json=payload)

        validate_status_code(response, 201)
        data = response.json()
        assert 'id' in data

    def test_update_user(self, api_client):
        """Test updating user"""
        user_id = 1
        payload = {
            'name': 'Updated Name',
            'email': 'updated@example.com'
        }

        response = api_client.put(f'/users/{user_id}', json=payload)

        validate_status_code(response, 200)
        data = response.json()
        assert data['name'] == payload['name']

    def test_delete_user(self, api_client):
        """Test deleting user"""
        user_id = 1
        response = api_client.delete(f'/users/{user_id}')
        validate_status_code(response, 200)


class TestPostEndpoints:
    """Tests for post endpoints"""

    def test_get_posts_list(self, api_client):
        """Test getting list of posts"""
        response = api_client.get('/posts')

        validate_status_code(response, 200)
        validate_response_time(response, max_time=2.0)

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_post_by_id(self, api_client):
        """Test getting post by ID"""
        post_id = 1
        response = api_client.get(f'/posts/{post_id}')

        validate_status_code(response, 200)

        data = response.json()
        assert data['id'] == post_id
        validate_json_structure(data, ['id', 'userId', 'title', 'body'])

    def test_create_post(self, api_client):
        """Test creating new post"""
        payload = {
            'title': 'Test Post',
            'body': 'This is a test post',
            'userId': 1
        }

        response = api_client.post('/posts', json=payload)

        validate_status_code(response, 201)
        data = response.json()
        assert data['title'] == payload['title']

    @pytest.mark.parametrize("post_id,expected_status", [
        (1, 200),
        (9999, 404)
    ])
    def test_get_post_parametrized(self, api_client, post_id, expected_status):
        """Test getting posts with different IDs"""
        response = api_client.get(f'/posts/{post_id}')
        validate_status_code(response, expected_status)


class TestCommentEndpoints:
    """Tests for comment endpoints"""

    def test_get_comments_for_post(self, api_client):
        """Test getting comments for specific post"""
        post_id = 1
        response = api_client.get(f'/posts/{post_id}/comments')

        validate_status_code(response, 200)

        data = response.json()
        assert isinstance(data, list)

        # Verify all comments belong to the post
        for comment in data:
            assert comment['postId'] == post_id

    def test_get_comments_list(self, api_client):
        """Test getting all comments"""
        response = api_client.get('/comments')

        validate_status_code(response, 200)
        validate_response_time(response, max_time=2.0)

        data = response.json()
        assert len(data) > 0

        # Validate comment structure
        comment = data[0]
        validate_json_structure(
            comment,
            ['id', 'postId', 'name', 'email', 'body']
        )


@pytest.mark.smoke
class TestSmokeTests:
    """Quick smoke tests"""

    def test_api_is_reachable(self, api_client):
        """Test that API is reachable"""
        response = api_client.get('/users')
        assert response.status_code < 500

    def test_response_format_is_json(self, api_client):
        """Test that responses are in JSON format"""
        response = api_client.get('/users')
        assert 'application/json' in response.headers.get('Content-Type', '')