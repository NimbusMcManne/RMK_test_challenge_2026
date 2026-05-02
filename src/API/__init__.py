"""
RMK Test Challenge 2026 - Data Analysis Package

This package provides tools for API data retrieval and statistical analysis
including probability, correlations, and effect sizes.
"""

from .api_client import APIClient, APIResponse, create_api_client

__version__ = "1.0.0"
__all__ = ["APIClient", "APIResponse", "create_api_client"]
