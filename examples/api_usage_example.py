"""
Example Usage of API Client for Data Retrieval

This example demonstrates how to use the API client to fetch data
that will be processed for statistical analysis.
"""

import sys
import os
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api_client import APIClient, create_api_client


def example_get_request():
    """Example of making a GET request to retrieve data."""
    print("=== GET Request Example ===")
    
    # Create API client
    client = create_api_client(base_url="https://api.example.com")
    
    # Make a GET request
    response = client.get_data("/data/endpoint", params={"limit": 100})
    
    if response.success:
        print(f"✅ Success! Retrieved data in {response.response_time:.2f}s")
        print(f"Status Code: {response.status_code}")
        print(f"Data Type: {type(response.data)}")
        
        # Handle different response types
        if isinstance(response.data, dict):
            print(f"Keys in response: {list(response.data.keys())[:5]}...")
        elif isinstance(response.data, list):
            print(f"Number of items: {len(response.data)}")
            if response.data:
                print(f"First item keys: {list(response.data[0].keys()) if isinstance(response.data[0], dict) else 'Not a dict'}")
    else:
        print(f"❌ Request failed: {response.data}")


def example_post_request():
    """Example of making a POST request with JSON data."""
    print("\n=== POST Request Example ===")
    
    # Create API client
    client = create_api_client()
    
    # Example JSON data for your API request
    api_request_data = {
        "dataset": "financial_data",
        "time_range": {
            "start": "2023-01-01",
            "end": "2023-12-31"
        },
        "fields": [
            "price", "volume", "market_cap", 
            "volatility", "returns", "trading_activity"
        ],
        "filters": {
            "market": "NASDAQ",
            "sector": ["Technology", "Healthcare"],
            "min_market_cap": 1000000000
        },
        "aggregation": {
            "frequency": "daily",
            "functions": ["mean", "std", "correlation"]
        }
    }
    
    # Make POST request
    response = client.post_data(
        "https://api.example.com/data/query",
        json_data=api_request_data
    )
    
    if response.success:
        print(f"✅ Success! Data retrieved in {response.response_time:.2f}s")
        print(f"Status Code: {response.status_code}")
        
        # Process the retrieved data
        if isinstance(response.data, dict) and 'data' in response.data:
            dataset = response.data['data']
            print(f"Dataset contains {len(dataset) if isinstance(dataset, list) else 'N/A'} records")
            
            # Show sample of data structure
            if isinstance(dataset, list) and dataset:
                print(f"Sample record keys: {list(dataset[0].keys())}")
                print(f"First record: {dataset[0]}")
        else:
            print(f"Response data: {response.data}")
    else:
        print(f"❌ Request failed: {response.data}")


def example_with_authentication():
    """Example of using authentication with the API client."""
    print("\n=== Authentication Example ===")
    
    # Create client with authentication
    client = create_api_client(base_url="https://api.example.com")
    
    # Option 1: Bearer token
    client.set_auth_token("your_bearer_token_here")
    
    # Option 2: API key
    # client.set_api_key("your_api_key_here")
    
    # Make authenticated request
    response = client.get_data("/protected/data")
    
    if response.success:
        print(f"✅ Authenticated request successful!")
        print(f"Data retrieved: {len(response.data) if isinstance(response.data, list) else 'N/A'} items")
    else:
        print(f"❌ Authentication failed: {response.data}")


def example_error_handling():
    """Example of handling different error scenarios."""
    print("\n=== Error Handling Example ===")
    
    client = create_api_client()
    
    # Test with invalid URL
    response = client.get_data("https://invalid-url-that-doesnt-exist.com/data")
    
    if not response.success:
        print(f"❌ Expected error caught: {response.data}")
        print(f"Status code: {response.status_code}")
    
    # Test with timeout
    client_slow = create_api_client(timeout=1)  # 1 second timeout
    response = client_slow.get_data("https://httpbin.org/delay/5")  # 5 second delay
    
    if not response.success:
        print(f"❌ Timeout error caught: {response.data}")


if __name__ == "__main__":
    print("API Client Usage Examples")
    print("=" * 50)
    
    # Run examples (comment out the ones you don't want to run)
    try:
        example_get_request()
        example_post_request()
        example_with_authentication()
        example_error_handling()
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Note: Some examples may fail without actual API endpoints")
    
    print("\n" + "=" * 50)
    print("Examples completed!")
