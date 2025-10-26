#!/usr/bin/env python3
"""
Health check script for Zoho CRM MCP Server.

This script verifies that:
1. All required dependencies are installed
2. Configuration is properly set up
3. The server can be initialized

Usage:
    python check_health.py
"""

import sys
import os


def check_imports():
    """Check if all required modules can be imported."""
    print("Checking imports...")
    errors = []
    
    # Check standard library
    try:
        import asyncio
        print("  ✓ asyncio")
    except ImportError as e:
        errors.append(f"  ✗ asyncio: {e}")
    
    try:
        import json
        print("  ✓ json")
    except ImportError as e:
        errors.append(f"  ✗ json: {e}")
    
    try:
        import logging
        print("  ✓ logging")
    except ImportError as e:
        errors.append(f"  ✗ logging: {e}")
    
    # Check third-party dependencies
    try:
        import requests
        print(f"  ✓ requests (version: {requests.__version__})")
    except ImportError as e:
        errors.append(f"  ✗ requests: {e}")
    
    try:
        import dotenv
        print("  ✓ python-dotenv")
    except ImportError as e:
        print(f"  ⚠ python-dotenv: {e} (optional)")
    
    # Check MCP SDK (optional for now)
    try:
        import mcp
        print(f"  ✓ mcp")
    except ImportError:
        print("  ⚠ mcp: Not installed (install with: pip install mcp)")
    
    # Check our package
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    try:
        import zoho_crm_mcp
        print(f"  ✓ zoho_crm_mcp (version: {zoho_crm_mcp.__version__})")
    except ImportError as e:
        errors.append(f"  ✗ zoho_crm_mcp: {e}")
    
    return errors


def check_configuration():
    """Check if configuration is set up."""
    print("\nChecking configuration...")
    
    required_vars = [
        "ZOHO_CLIENT_ID",
        "ZOHO_CLIENT_SECRET", 
        "ZOHO_REFRESH_TOKEN"
    ]
    
    missing = []
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✓ {var} is set")
        else:
            print(f"  ✗ {var} is not set")
            missing.append(var)
    
    optional_vars = [
        "ZOHO_ACCESS_TOKEN",
        "ZOHO_API_DOMAIN",
        "RATE_LIMIT_REQUESTS",
        "MAX_RETRIES"
    ]
    
    print("\n  Optional configuration:")
    for var in optional_vars:
        if os.getenv(var):
            print(f"    ✓ {var} is set")
        else:
            print(f"    - {var} (using default)")
    
    return missing


def check_server_initialization():
    """Check if the server can be initialized."""
    print("\nChecking server initialization...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from zoho_crm_mcp import Config, ZohoCRMClient
        
        # Test config
        config = Config()
        print("  ✓ Configuration object created")
        
        # Test client
        client = ZohoCRMClient(config)
        print("  ✓ Zoho CRM client created")
        
        return True
    except Exception as e:
        print(f"  ✗ Server initialization failed: {e}")
        return False


def main():
    """Run all health checks."""
    print("=" * 60)
    print("Zoho CRM MCP Server - Health Check")
    print("=" * 60)
    
    # Check imports
    import_errors = check_imports()
    
    # Check configuration
    config_missing = check_configuration()
    
    # Check server initialization
    server_ok = check_server_initialization()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_ok = True
    
    if import_errors:
        all_ok = False
        print("\n❌ Import errors detected:")
        for error in import_errors:
            print(f"  {error}")
        print("\nInstall missing dependencies with:")
        print("  pip install -e .")
    else:
        print("✅ All required imports working")
    
    if config_missing:
        all_ok = False
        print("\n⚠️  Missing configuration variables:")
        for var in config_missing:
            print(f"  - {var}")
        print("\nSet these environment variables or create a .env file")
        print("See .env.example for reference")
    else:
        print("✅ Configuration complete")
    
    if not server_ok:
        all_ok = False
        print("\n❌ Server initialization failed")
    else:
        print("✅ Server can be initialized")
    
    if all_ok:
        print("\n" + "=" * 60)
        print("🎉 All checks passed! The server is ready to use.")
        print("=" * 60)
        print("\nTo start the server, run:")
        print("  zoho-crm-mcp")
        print("\nOr in Python:")
        print("  from zoho_crm_mcp import ZohoCRMMCPServer")
        print("  import asyncio")
        print("  asyncio.run(ZohoCRMMCPServer().run())")
        return 0
    else:
        print("\n" + "=" * 60)
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
