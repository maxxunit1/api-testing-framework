# API Testing Framework

Comprehensive API testing framework with support for REST, GraphQL, and WebSocket testing. Built with Python for automated API validation and performance testing.

## ✨ Features

- 🌐 **REST API Testing** - Complete HTTP methods support (GET, POST, PUT, DELETE, PATCH)
- 🔐 **Authentication** - Support for Bearer tokens, OAuth2, API keys, Basic Auth
- ✅ **Response Validation** - JSON Schema validation, status code checking, response time monitoring
- 📊 **Performance Testing** - Load testing capabilities with concurrent requests
- 📝 **Detailed Reporting** - HTML and JSON test reports with detailed metrics
- 🔄 **CI/CD Integration** - Easy integration with Jenkins, GitHub Actions, GitLab CI
- 🎯 **Data-Driven Testing** - Parameterized tests with CSV/JSON data sources
- 🛠️ **Custom Assertions** - Extensible assertion library for complex validations

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/api-testing-framework.git
cd api-testing-framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api_endpoints.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=framework --cov-report=html

# Run tests in parallel
pytest -n 4
```

## 📋 Configuration

### Environment Setup

Create a `.env` file in the root directory:

```env
API_BASE_URL=https://api.example.com
API_KEY=your-api-key-here
AUTH_TOKEN=your-auth-token
TIMEOUT=30
```

### Endpoints Configuration

Edit `config/endpoints.json` to define your API endpoints:

```json
{
  "users": {
    "list": "/api/v1/users",
    "create": "/api/v1/users",
    "get": "/api/v1/users/{id}",
    "update": "/api/v1/users/{id}",
    "delete": "/api/v1/users/{id}"
  },
  "posts": {
    "list": "/api/v1/posts",
    "create": "/api/v1/posts"
  }
}
```

## 🧪 Writing Tests

### Simple GET Request Test

```python
from framework.api_client import APIClient
from framework.validators import validate_response

def test_get_users():
    client = APIClient()
    response = client.get('/api/v1/users')
    
    # Validate response
    assert response.status_code == 200
    validate_response(response, 'users_schema.json')
    
    # Check response data
    data = response.json()
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'email' in data[0]
```

### POST Request with Authentication

```python
def test_create_user():
    client = APIClient()
    
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "role": "user"
    }
    
    response = client.post(
        '/api/v1/users',
        json=payload,
        headers={'Authorization': 'Bearer token123'}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == payload['email']
```

### Data-Driven Testing

```python
import pytest

@pytest.mark.parametrize("user_id,expected_status", [
    (1, 200),
    (999, 404),
    (0, 400)
])
def test_get_user_by_id(user_id, expected_status):
    client = APIClient()
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == expected_status
```

## 📊 Test Reporting

### Generate HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

### Generate JSON Report

```bash
pytest --json-report --json-report-file=reports/report.json
```

### View Coverage Report

```bash
pytest --cov=framework --cov-report=html
open htmlcov/index.html
```

## 🔧 Framework Components

### API Client (`framework/api_client.py`)

The core HTTP client with built-in retry logic, timeout handling, and logging:

```python
from framework.api_client import APIClient

client = APIClient(
    base_url='https://api.example.com',
    timeout=30,
    retry_count=3
)

# Make requests
response = client.get('/endpoint')
response = client.post('/endpoint', json=data)
response = client.put('/endpoint/{id}', json=data)
response = client.delete('/endpoint/{id}')
```

### Validators (`framework/validators.py`)

Response validation utilities:

```python
from framework.validators import (
    validate_response,
    validate_status_code,
    validate_response_time,
    validate_json_schema
)

# Validate response
validate_response(response, schema_file='user_schema.json')

# Validate specific aspects
validate_status_code(response, 200)
validate_response_time(response, max_time=2.0)
validate_json_schema(response.json(), schema)
```

### Helpers (`framework/helpers.py`)

Utility functions for common tasks:

```python
from framework.helpers import (
    generate_random_email,
    generate_test_data,
    wait_for_condition,
    retry_on_failure
)

# Generate test data
email = generate_random_email()
data = generate_test_data('user')

# Wait for condition
wait_for_condition(lambda: check_status(), timeout=30)
```

## 🎯 Advanced Features

### Performance Testing

```python
from framework.api_client import APIClient
from concurrent.futures import ThreadPoolExecutor
import time

def test_load_testing():
    client = APIClient()
    
    def make_request():
        return client.get('/api/v1/users')
    
    start_time = time.time()
    
    # Send 100 concurrent requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        responses = [f.result() for f in futures]
    
    duration = time.time() - start_time
    
    # Calculate metrics
    success_rate = sum(1 for r in responses if r.status_code == 200) / len(responses)
    avg_response_time = sum(r.elapsed.total_seconds() for r in responses) / len(responses)
    
    print(f"Duration: {duration:.2f}s")
    print(f"Success Rate: {success_rate * 100:.2f}%")
    print(f"Avg Response Time: {avg_response_time:.3f}s")
    
    assert success_rate >= 0.95  # 95% success rate
    assert avg_response_time < 1.0  # Under 1 second
```

### Custom Assertions

```python
from framework.validators import CustomValidator

class UserValidator(CustomValidator):
    def validate_user_data(self, user):
        assert 'id' in user, "User must have ID"
        assert 'email' in user, "User must have email"
        assert '@' in user['email'], "Invalid email format"
        assert user['id'] > 0, "User ID must be positive"
        return True

validator = UserValidator()
validator.validate_user_data(response.json())
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest --html=reports/report.html
        env:
          API_BASE_URL: ${{ secrets.API_BASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
      
      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: reports/
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest --junitxml=reports/junit.xml'
            }
        }
        
        stage('Report') {
            steps {
                junit 'reports/junit.xml'
            }
        }
    }
}
```

## 📚 Project Structure

```
api-testing-framework/
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_api_endpoints.py  # Endpoint tests
│   ├── test_authentication.py # Auth tests
│   └── test_data_validation.py # Data validation tests
├── framework/                  # Core framework code
│   ├── __init__.py
│   ├── api_client.py          # HTTP client
│   ├── validators.py          # Response validators
│   └── helpers.py             # Utility functions
├── config/                     # Configuration files
│   ├── __init__.py
│   ├── config.py              # Settings
│   └── endpoints.json         # API endpoints
├── reports/                    # Test reports
├── schemas/                    # JSON schemas
├── README.md                   # Documentation
├── requirements.txt            # Dependencies
├── pytest.ini                  # Pytest configuration
└── .gitignore                 # Git ignore rules
```

## 🛠️ Troubleshooting

### Common Issues

**Issue: SSL Certificate Verification Failed**
```python
client = APIClient(verify_ssl=False)
```

**Issue: Timeout Errors**
```python
client = APIClient(timeout=60)  # Increase timeout
```

**Issue: Connection Refused**
- Check if API server is running
- Verify correct base URL
- Check firewall settings

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Requests](https://requests.readthedocs.io/) - HTTP library
- [pytest](https://pytest.org/) - Testing framework
- [jsonschema](https://python-jsonschema.readthedocs.io/) - JSON Schema validation

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check documentation
- Review existing test examples

---

**Built with ❤️ for API testing automation**

## Update 2025-10-13 17:36:42
# Improved: 2025-10-13 17:36:42
# Additional configuration

## Update 2025-10-22 23:30:54
async def async_operation():
    """Async operation support"""
    result = await fetch_data()
    return process(result)

## Update 2026-01-01 23:08:23
# Simplified logic
result = value if condition else default

## Update 2026-02-08 16:41:50
# Modified: 2026-02-08 16:41:50
CONFIG_VALUE = 'new_value'