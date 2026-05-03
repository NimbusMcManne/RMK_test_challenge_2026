"""
HTTP client and JSON-STAT2 conversion utilities for the
Statistics Estonia (andmed.stat.ee) and TAI (statistika.tai.ee) APIs.
"""

from .api_client import APIClient, APIResponse, create_api_client

__version__ = "1.0.0"
__all__ = ["APIClient", "APIResponse", "create_api_client"]
