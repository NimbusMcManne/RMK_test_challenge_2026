"""
Example script demonstrating how to use the Calculations class
to load CSV data, create DataFrames, and visualize statistics
"""

import sys
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(current_dir))

from data_process.data_analysis import DataAnalysis

def main():
    """
    Demonstrate the data loading and visualization capabilities
    """
    print("=== Data Analysis Example ===")
    
    # Initialize the calculations class
    calc = DataAnalysis()
    
    try:
        # Load all CSV files
        print("\n1. Loading CSV files...")
        dataframes = calc.load_all_csv_files()
        
        # Print comprehensive data summary
        print("\n2. Data Summary:")
        calc.print_data_summary()
        
        # Analyze column structure
        print("\n3. Column Structure Analysis:")
        analysis = calc.analyze_column_structure()
        
        for dataset_name, info in analysis.items():
            print(f"\n{dataset_name}:")
            print(f"  Value columns: {info['value_columns']}")
            print(f"  Year columns: {info['year_columns']}")
            print(f"  Has dataset column: {info['has_dataset_column']}")
        
        # Find datasets with value and year columns
        print("\n4. Finding datasets with value and year columns...")
        datasets_with_value_year = calc.get_datasets_with_columns(['value', 'Aasta'])
        print(f"Datasets with both 'value' and 'Aasta' columns: {datasets_with_value_year}")
        
        # Create overview visualization
        print("\n5. Creating overview visualization...")
        calc.visualize_dataset_overview()
        
        # Visualize specific datasets
        print("\n6. Visualizing specific datasets...")
        
        # Visualize a few example datasets
        example_datasets = ['VIG10', 'RV262', 'KA10']
        
        for dataset_name in example_datasets:
            if dataset_name in dataframes:
                print(f"\nVisualizing {dataset_name}...")
                calc.visualize_dataset(dataset_name)
            else:
                print(f"Dataset {dataset_name} not found.")
        
        print("\n=== Analysis Complete ===")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return
    
    # Example of accessing specific data
    print("\n7. Example data access:")
    
    # Get VIG10 data
    vig10_df = calc.get_dataframe('VIG10')
    if vig10_df is not None:
        print(f"VIG10 dataset shape: {vig10_df.shape}")
        print(f"VIG10 columns: {list(vig10_df.columns)}")
        
        # Show first few rows
        print("\nFirst 5 rows of VIG10:")
        print(vig10_df.head())
        
        # Show value statistics
        if 'value' in vig10_df.columns:
            print(f"\nValue statistics:")
            print(vig10_df['value'].describe())

if __name__ == "__main__":
    main()
