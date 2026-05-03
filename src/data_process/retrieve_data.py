"""
Example: Multiple Datasets with Estonia Statistics API

This example shows the simplest way to request multiple datasets
using the updated GETData class.
"""

import sys
from pathlib import Path
import pandas as pd

# Add src directory to path for imports
current_dir = Path(__file__).parent.parent  # Go up to src directory
sys.path.insert(0, str(current_dir))

# Import from sibling packages
from data_process.data_request import GETData
from API.data_validator import DataValidator
from data_process.csv_converter import CSVConverter

def main():
    """Example of requesting multiple datasets"""
    
    # Method 1: Simple dictionary approach (recommended)
    print("=== Method 1: Simple Dictionary ===")
    
    datasets = {
        "https://andmed.stat.ee/api/v1/et/stat/RV262": {
            "query": [
                {
                "code": "Abielu tüüp",
                "selection": {
                    "filter": "item",
                    "values": [
                    "1",
                    "2",
                    "3"
                    ]
                }
                },
                {
                "code": "Abiellumiskuu",
                "selection": {
                    "filter": "item",
                    "values": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        },
        "https://andmed.stat.ee/api/v1/et/stat/RV271": {
            "query": [
                {
                "code": "Abielu tüüp",
                "selection": {
                    "filter": "item",
                    "values": [
                    "1",
                    "2",
                    "3"
                    ]
                }
                },
                {
                "code": "Vanuserühm",
                "selection": {
                    "filter": "item",
                    "values": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        },
        "https://andmed.stat.ee/api/v1/et/stat/TS093": {
            "query": [
                {
                "code": "Näitaja",
                "selection": {
                    "filter": "item",
                    "values": [
                    "3",
                    "4"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        }, 
        "https://andmed.stat.ee/api/v1/et/stat/PM09": {
            "query": [
                {
                "code": "Liik",
                "selection": {
                    "filter": "item",
                    "values": [
                    "ANIM2000",
                    "ANIM2001EE",
                    "ANIM2300",
                    "ANIM2300F",
                    "ANIM2130",
                    "ANIM4100",
                    "ANIM4200",
                    "ANIM1100",
                    "ANIM5110O"
                    ]
                }
                },
                {
                "code": "Maakond",
                "selection": {
                    "filter": "item",
                    "values": [
                    "EE"
                    ]
                }
                },
                {
                "code": "Vaatlusperiood",
                "selection": {
                    "filter": "item",
                    "values": [
                    "2000Q1",
                    "2000Q2",
                    "2000Q3",
                    "2000Q4",
                    "2001Q1",
                    "2001Q2",
                    "2001Q3",
                    "2001Q4",
                    "2002Q1",
                    "2002Q2",
                    "2002Q3",
                    "2002Q4",
                    "2003Q1",
                    "2003Q2",
                    "2003Q3",
                    "2003Q4",
                    "2004Q1",
                    "2004Q2",
                    "2004Q3",
                    "2004Q4",
                    "2005Q1",
                    "2005Q2",
                    "2005Q3",
                    "2005Q4",
                    "2006Q1",
                    "2006Q2",
                    "2006Q3",
                    "2006Q4",
                    "2007Q1",
                    "2007Q2",
                    "2007Q3",
                    "2007Q4",
                    "2008Q1",
                    "2008Q2",
                    "2008Q3",
                    "2008Q4",
                    "2009Q1",
                    "2009Q2",
                    "2009Q3",
                    "2009Q4",
                    "2010Q1",
                    "2010Q2",
                    "2010Q3",
                    "2010Q4",
                    "2011Q1",
                    "2011Q2",
                    "2011Q3",
                    "2011Q4",
                    "2012Q1",
                    "2012Q2",
                    "2012Q3",
                    "2012Q4",
                    "2013Q1",
                    "2013Q2",
                    "2013Q3",
                    "2013Q4",
                    "2014Q1",
                    "2014Q2",
                    "2014Q3",
                    "2014Q4",
                    "2015Q1",
                    "2015Q2",
                    "2015Q3",
                    "2015Q4",
                    "2016Q1",
                    "2016Q2",
                    "2016Q3",
                    "2016Q4",
                    "2017Q1",
                    "2017Q2",
                    "2017Q3",
                    "2017Q4",
                    "2018Q1",
                    "2018Q2",
                    "2018Q3",
                    "2018Q4",
                    "2019Q1",
                    "2019Q2",
                    "2019Q3",
                    "2019Q4",
                    "2020Q1",
                    "2020Q2",
                    "2020Q3",
                    "2020Q4",
                    "2021Q1",
                    "2021Q2",
                    "2021Q3",
                    "2021Q4",
                    "2022Q1",
                    "2022Q2",
                    "2022Q3",
                    "2022Q4",
                    "2023Q1",
                    "2023Q2",
                    "2023Q3",
                    "2023Q4",
                    "2024Q1",
                    "2024Q2",
                    "2024Q3",
                    "2024Q4",
                    "2025Q1",
                    "2025Q2",
                    "2025Q3",
                    "2025Q4"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        },
        "https://andmed.stat.ee/api/v1/et/stat/KA30": {
            "query": [
                {
                "code": "Veekogu",
                "selection": {
                    "filter": "item",
                    "values": [
                    "2",
                    "3"
                    ]
                }
                },
                {
                "code": "Kalaliik",
                "selection": {
                    "filter": "item",
                    "values": [
                    "1",
                    "2",
                    "3"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        }, 
        "https://andmed.stat.ee/api/v1/et/stat/KA10": {
            "query": [
                {
                "code": "Kalaliik",
                "selection": {
                    "filter": "item",
                    "values": [
                    "1",
                    "13",
                    "18",
                    "29"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat2"
            }
        }, 
        "https://statistika.tai.ee/api/v1/et/Andmebaas/02Haigestumus/05Psyyhikahaired/PKH7.px": {
            "query": [
                {
                "code": "Diagnoos (RHK-10)",
                "selection": {
                    "filter": "item",
                    "values": [
                    "F10.X-F19.X",
                    "F10.X",
                    "F12.X"
                    ]
                }
                },
                {
                "code": "Kliiniline seisund",
                "selection": {
                    "filter": "item",
                    "values": [
                    "0"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat"
            }
        }, 
        "https://statistika.tai.ee/api/v1/et/Andmebaas/02Haigestumus/09Vigastused/VIG10.px": {
            "query": [
                {
                "code": "Elukoht",
                "selection": {
                    "filter": "item",
                    "values": [
                    "0"
                    ]
                }
                },
                {
                "code": "Sugu",
                "selection": {
                    "filter": "item",
                    "values": [
                    "0"
                    ]
                }
                },
                {
                "code": "Välispõhjus (RHK-10)",
                "selection": {
                    "filter": "item",
                    "values": [
                    "V01-X59",
                    "V01-V99",
                    "V01-V09",
                    "V10-V19"
                    ]
                }
                },
                {
                "code": "Vanuserühm",
                "selection": {
                    "filter": "item",
                    "values": [
                    "0"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat"
            }
        },
        "https://statistika.tai.ee/api/v1/et/Andmebaas/03Tervishoiuteenused/03Kiirabi/KE32.px": {
            "query": [
                {
                "code": "Saabumisviis",
                "selection": {
                    "filter": "item",
                    "values": [
                    "1",
                    "3"
                    ]
                }
                },
                {
                "code": "Haigla liik",
                "selection": {
                    "filter": "item",
                    "values": [
                    "0"
                    ]
                }
                },
                {
                "code": "Vastuvõtt",
                "selection": {
                    "filter": "item",
                    "values": [
                    "0"
                    ]
                }
                },
                {
                "code": "Vanuserühm",
                "selection": {
                    "filter": "item",
                    "values": [
                    "0"
                    ]
                }
                }
            ],
            "response": {
                "format": "json-stat"
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
    
    # Convert all datasets to standardized CSV files
    print("\n=== Converting to CSV Format ===")
    
    converter = CSVConverter(output_dir="output")
    csv_files = converter.convert_batch(results)
    
    # Get summary of converted files
    summary = converter.get_summary()
    print(f"\n=== CSV Conversion Summary ===")
    print(f"Total files converted: {summary['total_files']}")
    print(f"Output directory: {summary['output_directory']}")
    
    for file_info in summary['files']:
        if 'shape' in file_info:
            print(f"  {file_info['name']}: {file_info['shape']} ({file_info['size_bytes']} bytes)")
        else:
            print(f"  {file_info['name']}: ERROR - {file_info.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
