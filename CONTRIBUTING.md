# Contributing to Zoho CRM MCP Server

Thank you for your interest in contributing to Zoho CRM MCP Server! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We're building this project together.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Python version and environment details
6. Any relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

1. A clear description of the enhancement
2. Use cases and benefits
3. Possible implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**:
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
3. **Ensure tests pass**: Run `pytest` before submitting
4. **Lint your code**: Run `ruff check src/ tests/` and `ruff format src/ tests/`
5. **Commit your changes**: Use clear, descriptive commit messages
6. **Push to your fork** and submit a pull request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/asklokesh/zoho-crm-mcp-server.git
cd zoho-crm-mcp-server

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linting
ruff check src/ tests/
ruff format src/ tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Write docstrings for all functions, classes, and modules
- Keep functions focused and single-purpose
- Maximum line length: 120 characters

## Testing

- Write tests for all new functionality
- Maintain or improve code coverage
- Use descriptive test names
- Mock external API calls

## Documentation

- Update README.md if adding new features
- Add docstrings to all public APIs
- Include usage examples for new functionality
- Update CHANGELOG.md (if exists)

## Commit Messages

Write clear, concise commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Keep first line under 72 characters
- Add detailed description if needed (after blank line)

Examples:
```
Add search functionality for accounts module

Implement search_records method to support custom search
criteria across all Zoho CRM modules. Includes rate limiting
and error handling.
```

## Review Process

1. All PRs require at least one review
2. CI checks must pass
3. Address review comments promptly
4. Squash commits before merging (if requested)

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing! 🎉
