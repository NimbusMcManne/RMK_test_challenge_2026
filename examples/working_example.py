"""
Working Example: Estonia Statistics API Data Retrieval and Visualization

This example shows the correct way to retrieve data from the Estonia Statistics API
and convert it to a usable DataFrame for analysis.
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from API.api_client import create_api_client
from API.data_validator import DataValidator

def get_working_data():
    """Get working data from Estonia Statistics API"""
    
    # Simple working query
    query_json = {
        "query": [
            {
                "code": "Abielu tüüp",
                "selection": {
                    "filter": "item",
                    "values": ["1"]  # Just get one type for simplicity
                }
            },
            {
                "code": "Abiellumiskuu",
                "selection": {
                    "filter": "item",
                    "values": ["1", "2", "3"]  # First few months
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }
    
    # Make API request
    client = create_api_client(base_url="https://andmed.stat.ee/api/v1/et/stat")
    response = client.post_data("RV262", json_data=query_json)
    
    if not response.success:
        print(f"API request failed: {response.data}")
        return None, None
    
    print(f"API request successful in {response.response_time:.2f}s")
    
    # Convert to DataFrame using our validator
    validator = DataValidator()
    df, validation = validator.convert_to_dataframe(response.data)
    
    if validation.is_valid:
        print(f"DataFrame created successfully: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst few rows:")
        print(df.head(10))
        
        # Additional validation
        prob_validation = validator.validate_for_probability_analysis(df)
        print(f"\nProbability analysis validation: {prob_validation}")
        
        return df, validation
    else:
        print(f"DataFrame creation failed: {validation.errors}")
        return None, validation

def visualize_data(df):
    """Simple visualization of the data"""
    if df is None or df.empty:
        print("No data to visualize")
        return
    
    print("\n=== Data Visualization ===")
    
    # If we have a 'value' column, plot it
    if 'value' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(df['value'])
        plt.title('Estonia Marriage Data Values')
        plt.xlabel('Data Point Index')
        plt.ylabel('Value')
        plt.grid(True)
        plt.show()
    
    # Show basic statistics
    print("\n=== Basic Statistics ===")
    print(df.describe())

def main():
    """Main function to demonstrate data retrieval and analysis"""
    
    print("=== Estonia Statistics API Data Retrieval ===")
    
    # Get the data
    df, validation = get_working_data()
    
    if df is not None:
        # Visualize the data
        visualize_data(df)
        
        print("\n=== Data Ready for Analysis ===")
        print("You can now use this DataFrame for:")
        print("- Probability analysis")
        print("- Correlation analysis") 
        print("- Statistical calculations")
        print(f"\nDataFrame shape: {df.shape}")
        print(f"Data columns: {list(df.columns)}")
    else:
        print("Failed to retrieve usable data")

if __name__ == "__main__":
    main()
