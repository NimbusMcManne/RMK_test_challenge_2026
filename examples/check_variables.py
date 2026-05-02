import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from API.api_client import create_api_client

def check_available_variables():
    """Check what variables are actually available in the API"""
    
    client = create_api_client(base_url="https://andmed.stat.ee/api/v1/et/stat")
    
    # Get basic metadata first
    response = client.get_data("RV262")
    
    print("Available variables in RV262:")
    variables = response.data.get('variables', [])
    
    for i, var in enumerate(variables):
        print(f"{i+1}. Code: '{var.get('code', 'N/A')}'")
        print(f"   Text: '{var.get('text', 'N/A')}'")
        print(f"   Values: {var.get('values', [])[:5]}...")  # Show first 5 values
        print(f"   Value Texts: {var.get('valueTexts', [])[:5]}...")  # Show first 5 value texts
        print()

if __name__ == "__main__":
    check_available_variables()
