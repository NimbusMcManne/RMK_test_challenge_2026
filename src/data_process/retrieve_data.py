"""
Example: Multiple Datasets with Estonia Statistics API

This example shows the simplest way to request multiple datasets
using the updated GETData class.
"""

import sys
from pathlib import Path
import pandas as pd

# Add src directory to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import directly from the modules
import sys
import os
sys.path.append(os.path.join(str(src_dir), 'data_process'))
sys.path.append(os.path.join(str(src_dir), 'API'))

from data_request import GETData
from data_validator import DataValidator

def main():
    """Example of requesting multiple datasets"""
    
    # Method 1: Simple dictionary approach (recommended)
    print("=== Method 1: Simple Dictionary ===")
    
    datasets = {
        "RV262": {  # Marriage data
            "query": [
                {
                    "code": "Abielu tüüp",
                    "selection": {
                        "filter": "item",
                        "values": ["1", "2", "3"]
                    }
                },
                {
                    "code": "Abiellumiskuu",
                    "selection": {
                        "filter": "item",
                        "values": ["1", "2", "3", "4", "5", "6"]
                    }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        },
        "RV271": {  # Another dataset example
            "query": [
                {
                    "code": "Vanuserühm",
                    "selection": {
                        "filter": "item",
                        "values": ["1", "2", "3"]
                    }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        }
    }
    
    # Create GETData instance and retrieve data
    data_fetcher = GETData(datasets)
    results = data_fetcher.get_data_through_API()
    
    print(f"Retrieved data for {len(results)} datasets")
    
    # Process each dataset
    validator = DataValidator()
    
    for dataset_id, api_response in results.items():
        if api_response is not None:
            print(f"\n=== Dataset: {dataset_id} ===")
            
            # Convert to DataFrame
            df, validation = validator.convert_to_dataframe(api_response)
            
            if validation.is_valid and not df.empty:
                print(f"DataFrame shape: {df.shape}")
                print(f"Columns: {list(df.columns)}")
                
                # Show first few rows
                print("Sample data:")
                print(df.head(3))
                
                # Basic statistics
                if 'value' in df.columns:
                    print(f"Value range: {df['value'].min()} - {df['value'].max()}")
                    print(f"Mean: {df['value'].mean():.2f}")
                
            else:
                print(f"✗ Data validation failed: {validation.errors}")
        else:
            print(f"\n=== Dataset: {dataset_id} ===")
            print("✗ No data retrieved")
    
    # Method 2: If you want to add datasets dynamically
    print("\n=== Method 2: Adding Datasets Dynamically ===")
    
    # You can add datasets at runtime
    data_fetcher.json_data["NEW_DATASET"] = {
        "query": [
            {
                "code": "Some_Variable",
                "selection": {
                    "filter": "item", 
                    "values": ["1", "2"]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }
    
    print("Added NEW_DATASET to the request queue")
    print(f"Total datasets now: {len(data_fetcher.json_data)}")

if __name__ == "__main__":
    main()
