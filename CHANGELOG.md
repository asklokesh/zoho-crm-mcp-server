# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-26

### Added
- Initial release of Zoho CRM MCP Server
- OAuth 2.0 authentication with automatic token refresh
- Five MCP tools:
  - `get_leads` - Retrieve leads with pagination
  - `create_lead` - Create new leads
  - `get_contacts` - Fetch contacts
  - `get_deals` - Get deals
  - `search_records` - Search any module with custom criteria
- Rate limiting to respect API quotas
- Automatic retry logic with exponential backoff
- Comprehensive error handling and logging
- Configuration management via environment variables
- Complete test suite with pytest
- GitHub Actions CI/CD workflow
- Documentation:
  - Comprehensive README with examples
  - CONTRIBUTING guide
  - Example scripts
  - Health check script
- Support for Python 3.8+

### Technical Details
- Uses `requests` library for HTTP communication
- Dataclass-based configuration
- Async/await support throughout
- Graceful fallbacks for optional dependencies
- Clean modular architecture (server, client, config)

[0.1.0]: https://github.com/asklokesh/zoho-crm-mcp-server/releases/tag/v0.1.0
