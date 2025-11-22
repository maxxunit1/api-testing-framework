# Contributing to API Testing Framework

Thank you for your interest in contributing! 🎉

## 🤝 How to Contribute

### 1. Fork the Repository
Click the "Fork" button on the GitHub repository page.

### 2. Clone Your Fork
```bash
git clone https://github.com/your-username/api-testing-framework.git
cd api-testing-framework
```

### 3. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 5. Make Your Changes
- Add new features
- Fix bugs
- Improve documentation
- Add tests

### 6. Run Tests
```bash
pytest
pytest --cov=framework --cov-report=html
```

### 7. Commit Your Changes
```bash
git add .
git commit -m "Add: description of your changes"
```

### 8. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 9. Create a Pull Request
Go to your fork on GitHub and click "New Pull Request".

## 📋 Contribution Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Add type hints where appropriate

### Documentation
- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update examples if behavior changes
- Document complex logic with comments

### Testing
- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage (>80%)
- Include both positive and negative test cases
- Use pytest markers appropriately

### Commit Messages
Use clear and descriptive commit messages:
- `Add: New feature description`
- `Fix: Bug fix description`
- `Update: Update description`
- `Refactor: Refactoring description`
- `Docs: Documentation changes`
- `Test: Test additions/changes`

## 🛠️ Development Setup

### Install Development Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists
```

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=framework

# Run specific test file
pytest tests/test_api_endpoints.py

# Run with markers
pytest -m smoke
pytest -m "not slow"

# Run in parallel
pytest -n 4
```

### Code Quality Checks
```bash
# Linting
flake8 framework/ tests/

# Type checking
mypy framework/

# Format code
black framework/ tests/
```

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Description** - Clear description of the problem
2. **Steps to Reproduce** - How to reproduce the issue
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Environment** - OS, Python version, etc.
6. **Error Messages** - Full error messages and stack traces
7. **Screenshots** - If applicable

## ✨ Feature Requests

For feature requests, please include:

1. **Description** - Clear description of the feature
2. **Use Case** - Why this feature would be useful
3. **Implementation Ideas** - How you think it could work
4. **Examples** - Example code or usage
5. **Priority** - High/Medium/Low priority

## 🏷️ Pull Request Template

When creating a pull request, please include:

- **Description** - What changes are being made
- **Type of Change**
  - [ ] Bug fix
  - [ ] New feature
  - [ ] Documentation update
  - [ ] Refactoring
  - [ ] Performance improvement
- **Testing** - How you tested the changes
- **Breaking Changes** - Any breaking changes and migration guide
- **Checklist**
  - [ ] Tests pass
  - [ ] Documentation updated
  - [ ] Code follows style guidelines
  - [ ] Added tests for new features

## 🔒 Security

If you discover a security vulnerability:

1. **Do NOT** create a public issue
2. Email the maintainers directly
3. Include detailed information about the vulnerability
4. Wait for confirmation before disclosing publicly

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## 💬 Questions?

- Open an issue for general questions
- Check existing issues and documentation
- Review the README.md for basic usage

Thank you for contributing! 🚀

## Update 2025-10-21 07:36:02
# Enhanced: 2025-10-21 07:36:02
"""Documentation updated"""

## Update 2025-11-04 20:13:59
# Simplified logic
result = value if condition else default

## Update 2025-11-22 13:27:38
# Improved readability
data = [
    item
    for item in collection
    if item.is_valid()
]