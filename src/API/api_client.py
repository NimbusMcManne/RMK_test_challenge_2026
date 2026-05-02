"""
API Client Module for Data Retrieval

This module provides a robust API client for making HTTP requests to retrieve data
that will be processed for probability/correlation/effect size analysis.
"""

import requests
import json
import time
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """Container for API response data and metadata"""
    status_code: int
    data: Union[Dict, list, str]
    headers: Dict[str, str]
    response_time: float
    success: bool


class APIClient:
    """
    A robust API client for making HTTP requests with error handling,
    retry logic, and response validation.
    """
    
    def __init__(self, base_url: str = "", timeout: int = 30, max_retries: int = 3):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for API endpoints
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'DataAnalysisClient/1.0'
        })
    
    def set_auth_token(self, token: str) -> None:
        """Set authentication token for API requests."""
        self.session.headers['Authorization'] = f'Bearer {token}'
    
    def set_api_key(self, api_key: str, header_name: str = 'X-API-Key') -> None:
        """Set API key for authentication."""
        self.session.headers[header_name] = api_key
    
    def make_request(
        self, 
        endpoint: str, 
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> APIResponse:
        """
        Make an HTTP request to the API with retry logic.
        
        Args:
            endpoint: API endpoint (relative to base_url or full URL)
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            params: URL parameters for GET requests
            data: Form data for POST requests
            json_data: JSON data for POST requests
            
        Returns:
            APIResponse object with response data and metadata
        """
        # Construct full URL
        if endpoint.startswith('http'):
            url = endpoint
        else:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            start_time = time.time()
            
            try:
                logger.info(f"Making {method} request to {url} (attempt {attempt + 1})")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    timeout=self.timeout
                )
                
                response_time = time.time() - start_time
                
                # Parse response data
                try:
                    if response.headers.get('content-type', '').startswith('application/json'):
                        response_data = response.json()
                    else:
                        response_data = response.text
                except json.JSONDecodeError:
                    response_data = response.text
                
                # Create response object
                api_response = APIResponse(
                    status_code=response.status_code,
                    data=response_data,
                    headers=dict(response.headers),
                    response_time=response_time,
                    success=response.status_code < 400
                )
                
                # Log response info
                logger.info(f"Response: {response.status_code} in {response_time:.2f}s")
                
                # Handle different status codes
                if response.status_code == 429:  # Rate limit
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                if response.status_code >= 500:  # Server error
                    if attempt < self.max_retries:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.warning(f"Server error. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                
                # Success or client error - return response
                return api_response
                
            except requests.exceptions.Timeout:
                last_exception = "Request timed out"
                logger.warning(f"Request timeout (attempt {attempt + 1})")
                
            except requests.exceptions.ConnectionError:
                last_exception = "Connection error"
                logger.warning(f"Connection error (attempt {attempt + 1})")
                
            except requests.exceptions.RequestException as e:
                last_exception = str(e)
                logger.warning(f"Request exception: {e} (attempt {attempt + 1})")
            
            # Wait before retry (except on last attempt)
            if attempt < self.max_retries:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        
        # All retries failed
        error_response = APIResponse(
            status_code=0,
            data={"error": last_exception or "Unknown error"},
            headers={},
            response_time=0,
            success=False
        )
        
        logger.error(f"All retry attempts failed: {last_exception}")
        return error_response
    
    def get_data(self, endpoint: str, params: Optional[Dict] = None) -> APIResponse:
        """Convenience method for GET requests."""
        return self.make_request(endpoint, method='GET', params=params)
    
    def post_data(self, endpoint: str, json_data: Optional[Dict] = None) -> APIResponse:
        """Convenience method for POST requests with JSON data."""
        return self.make_request(endpoint, method='POST', json_data=json_data)


def create_api_client(base_url: str = "", **kwargs) -> APIClient:
    """
    Factory function to create an API client instance.
    
    Args:
        base_url: Base URL for the API
        **kwargs: Additional arguments for APIClient
        
    Returns:
        Configured APIClient instance
    """
    return APIClient(base_url=base_url, **kwargs)
