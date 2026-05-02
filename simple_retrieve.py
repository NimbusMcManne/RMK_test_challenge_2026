"""
Simple standalone script to retrieve multiple datasets
"""

import sys
from pathlib import Path

# Direct import approach
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.append(str(Path(__file__).parent / "src" / "data_process"))
sys.path.append(str(Path(__file__).parent / "src" / "API"))

try:
    from data_request import GETData
    from data_validator import DataValidator
    print("Imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

def main():
    """Simple example of requesting multiple datasets"""
    
    # Simple dictionary approach
    datasets = {
        "RV262": {
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
        "RV271": {
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
    
    print("=== Retrieving Multiple Datasets ===")
    
    # Create GETData instance
    data_fetcher = GETData(datasets)
    results = data_fetcher.get_data_through_API()
    
    print(f"Retrieved data for {len(results)} datasets")
    
    # Process results
    validator = DataValidator()
    
    for dataset_id, api_response in results.items():
        if api_response is not None:
            print(f"\n=== Dataset: {dataset_id} ===")
            
            # Convert to DataFrame
            df, validation = validator.convert_to_dataframe(api_response)
            
            if validation.is_valid and not df.empty:
                print(f"DataFrame shape: {df.shape}")
                print(f"Columns: {list(df.columns)}")
                
                # Show sample
                print("Sample data:")
                print(df.head(2))
            else:
                print(f"Validation failed: {validation.errors}")
        else:
            print(f"\n=== Dataset: {dataset_id} ===")
            print("✗ No data retrieved")

if __name__ == "__main__":
    main()
