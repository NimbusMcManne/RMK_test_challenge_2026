# API Request System for Data Analysis

This document explains how to use the API request system to retrieve data for probability, correlation, and effect size analysis.

## Overview

The API request system consists of:

- **`APIClient`**: Main client for making HTTP requests with retry logic and error handling
- **`DataValidator`**: Validates API responses and converts data to DataFrames ready for analysis
- **Example scripts**: Demonstrate different usage patterns

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Basic Usage

```python
from src.api_client import create_api_client
from src.data_validator import validate_api_response

# Create API client
client = create_api_client(base_url="https://api.example.com")

# Make a GET request
response = client.get_data("/data/endpoint")

# Validate and convert to DataFrame
if response.success:
    df, validation = validate_api_response(response.data, analysis_type="correlation")
    if validation.is_valid:
        print(f"Data ready for analysis: {df.shape}")
    else:
        print(f"Validation issues: {validation.errors}")
```

## API Client Features

### Authentication

```python
# Bearer token authentication
client.set_auth_token("your_token_here")

# API key authentication
client.set_api_key("your_api_key_here")
```

### Request Methods

```python
# GET request with parameters
response = client.get_data("/data", params={"limit": 100, "format": "json"})

# POST request with JSON data
data = {"query": "financial_data", "date_range": "2023"}
response = client.post_data("/query", json_data=data)

# Custom request
response = client.make_request(
    endpoint="/custom",
    method="PUT",
    json_data={"data": "value"},
    params={"param": "value"}
)
```

### Error Handling

The API client automatically handles:
- **Rate limiting**: Waits for `Retry-After` header
- **Server errors**: Retries with exponential backoff
- **Timeouts**: Configurable timeout periods
- **Connection issues**: Automatic retry logic

## Data Validation

### Response Structure Validation

```python
from src.data_validator import DataValidator

validator = DataValidator()

# Validate basic structure
validation = validator.validate_response_structure(data)
```

### DataFrame Conversion

```python
# Convert API response to DataFrame
df, validation = validator.convert_to_dataframe(api_response_data)

if validation.is_valid:
    print(f"DataFrame created: {df.shape}")
else:
    print(f"Errors: {validation.errors}")
```

### Analysis-Specific Validation

```python
# For correlation analysis
corr_validation = validator.validate_for_correlation_analysis(df)

# For probability analysis  
prob_validation = validator.validate_for_probability_analysis(df)
```

## Example API Request JSON

Here's an example of how to structure your API request JSON:

```python
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

response = client.post_data("https://api.example.com/data/query", json_data=api_request_data)
```

## Working with Different Response Formats

The validator handles common API response patterns:

### 1. Direct List Response
```json
[
    {"date": "2023-01-01", "price": 100.5, "volume": 1000},
    {"date": "2023-01-02", "price": 101.2, "volume": 1200}
]
```

### 2. Object with Data Property
```json
{
    "status": "success",
    "data": [
        {"date": "2023-01-01", "price": 100.5},
        {"date": "2023-01-02", "price": 101.2}
    ],
    "total": 2
}
```

### 3. Nested Structure
```json
{
    "results": {
        "items": [
            {"symbol": "AAPL", "metrics": {"price": 150, "volume": 1000000}},
            {"symbol": "GOOGL", "metrics": {"price": 2800, "volume": 500000}}
        ]
    }
}
```

## Error Handling Best Practices

```python
response = client.get_data("/data")

if not response.success:
    if response.status_code == 401:
        print("Authentication failed - check your API token")
    elif response.status_code == 429:
        print("Rate limited - please wait")
    elif response.status_code >= 500:
        print("Server error - try again later")
    else:
        print(f"Request failed: {response.data}")
else:
    # Process successful response
    df, validation = validate_api_response(response.data)
    
    if not validation.is_valid:
        print(f"Data validation warnings: {validation.warnings}")
        print(f"Data validation errors: {validation.errors}")
    
    # Continue with analysis...
```

## Configuration Options

```python
# Create client with custom settings
client = create_api_client(
    base_url="https://api.example.com",
    timeout=60,  # 60 second timeout
    max_retries=5  # 5 retry attempts
)

# Set custom headers
client.session.headers.update({
    'Accept': 'application/json',
    'User-Agent': 'MyDataAnalysisApp/1.0'
})
```

## Next Steps

Once you have validated data, you can proceed with:

1. **Correlation Analysis**: Use the numeric columns to calculate correlations
2. **Probability Analysis**: Use categorical/binary columns for probability calculations  
3. **Effect Size Analysis**: Compare groups and calculate effect sizes

The validated DataFrame is ready for statistical analysis using pandas, numpy, scipy, or other analysis libraries.

## Troubleshooting

### Common Issues

1. **Empty DataFrame**: Check if the API response structure matches expected format
2. **Missing Numeric Columns**: Verify field names in your API request
3. **Authentication Errors**: Ensure proper token/API key setup
4. **Rate Limiting**: Implement delays between requests or use retry logic

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show detailed request/response information for troubleshooting.
