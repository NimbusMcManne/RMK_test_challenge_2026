import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path
import os
from typing import Dict, List, Optional, Tuple

class DataAnalysis:
    """
    Class for loading CSV data, creating DataFrames, and visualizing statistics data
    """
    
    def __init__(self, data_dir: str = "output"):
        """
        Initialize the Calculations class
        
        Args:
            data_dir: Directory containing CSV files
        """
        self.data_dir = Path(data_dir)
        self.dataframes = {}
        self.data_info = {}
        
        # Common column names to look for
        self.value_columns = ['value', 'values', 'Value', 'Values']
        self.year_columns = ['aasta', 'aastad', 'Aasta', 'Aastad', 'year', 'Year', 'Vaatlusperiood', 'Periood']
        self.dataset_column = 'dataset'
        
    def load_all_csv_files(self) -> Dict[str, pd.DataFrame]:
        """
        Load all CSV files from the data directory into DataFrames
        
        Returns:
            Dictionary mapping dataset names to DataFrames
        """
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory {self.data_dir} does not exist")
        
        csv_files = list(self.data_dir.glob("*.csv"))
        
        if not csv_files:
            raise ValueError(f"No CSV files found in {self.data_dir}")
        
        print(f"Found {len(csv_files)} CSV files:")
        
        for csv_file in csv_files:
            dataset_name = csv_file.stem
            
            try:
                # Load CSV with proper encoding
                df = pd.read_csv(csv_file, encoding='utf-8')
                
                # Store the DataFrame
                self.dataframes[dataset_name] = df
                
                # Store metadata about the dataset
                self.data_info[dataset_name] = {
                    'file_path': str(csv_file),
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'file_size': csv_file.stat().st_size
                }
                
                print(f"  + {dataset_name}: {df.shape[0]} rows, {df.shape[1]} columns")
                
            except Exception as e:
                print(f"  - Error loading {dataset_name}: {e}")
                continue
        
        return self.dataframes
    
    def get_dataframe(self, dataset_name: str) -> Optional[pd.DataFrame]:
        """
        Get a specific DataFrame by dataset name
        
        Args:
            dataset_name: Name of the dataset
            
        Returns:
            DataFrame if found, None otherwise
        """
        return self.dataframes.get(dataset_name)
    
    def analyze_column_structure(self, dataset_name: str = None) -> Dict:
        """
        Analyze column structure across all datasets or a specific dataset
        
        Args:
            dataset_name: Specific dataset to analyze, or None for all
            
        Returns:
            Dictionary with column analysis
        """
        analysis = {}
        
        datasets_to_analyze = [dataset_name] if dataset_name else list(self.dataframes.keys())
        
        for name in datasets_to_analyze:
            if name not in self.dataframes:
                continue
                
            df = self.dataframes[name]
            
            # Find value and year columns using pandas built-in methods
            value_cols = df.columns[df.columns.isin(self.value_columns)].tolist()
            year_cols = df.columns[df.columns.isin(self.year_columns)].tolist()
            
            # Alternative approach using pandas string methods (more flexible)
            # value_cols = df.columns[df.columns.str.contains('|'.join(self.value_columns), case=False, na=False)].tolist()
            # year_cols = df.columns[df.columns.str.contains('|'.join(self.year_columns), case=False, na=False)].tolist()
            
            # Get sample data
            sample_data = df.head(3).to_dict('records') if not df.empty else []
            
            analysis[name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'value_columns': value_cols,
                'year_columns': year_cols,
                'has_dataset_column': self.dataset_column in df.columns,
                'sample_data': sample_data,
                'data_types': df.dtypes.to_dict(),
                'null_counts': df.isnull().sum().to_dict()
            }
        
        return analysis
    
    def visualize_dataset_overview(self):
        """
        Create an overview visualization of all loaded datasets
        """
        if not self.dataframes:
            print("No data loaded. Call load_all_csv_files() first.")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Dataset Overview', fontsize=16, fontweight='bold')
        
        # 1. Dataset sizes (number of rows)
        dataset_names = list(self.dataframes.keys())
        row_counts = [self.dataframes[name].shape[0] for name in dataset_names]
        
        axes[0, 0].bar(dataset_names, row_counts)
        axes[0, 0].set_title('Number of Rows per Dataset')
        axes[0, 0].set_ylabel('Rows')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Dataset file sizes
        file_sizes = [self.data_info[name]['file_size'] for name in dataset_names]
        
        axes[0, 1].bar(dataset_names, file_sizes)
        axes[0, 1].set_title('File Size (bytes)')
        axes[0, 1].set_ylabel('Bytes')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Column counts
        col_counts = [self.dataframes[name].shape[1] for name in dataset_names]
        
        axes[1, 0].bar(dataset_names, col_counts)
        axes[1, 0].set_title('Number of Columns per Dataset')
        axes[1, 0].set_ylabel('Columns')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Value column presence
        has_value_col = []
        for name in dataset_names:
            df = self.dataframes[name]
            has_value = any(col in self.value_columns for col in df.columns)
            has_value_col.append(1 if has_value else 0)
        
        axes[1, 1].bar(dataset_names, has_value_col)
        axes[1, 1].set_title('Has Value Column')
        axes[1, 1].set_ylabel('Yes/No')
        axes[1, 1].set_ylim(0, 1.1)
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def visualize_dataset(self, dataset_name: str, max_categories: int = 20):
        """
        Create detailed visualizations for a specific dataset
        
        Args:
            dataset_name: Name of the dataset to visualize
            max_categories: Maximum number of categories to show in categorical plots
        """
        if dataset_name not in self.dataframes:
            print(f"Dataset {dataset_name} not found.")
            return
        
        df = self.dataframes[dataset_name]
        
        if df.empty:
            print(f"Dataset {dataset_name} is empty.")
            return
        
        # Find value and year columns using pandas built-in methods
        value_cols = df.columns[df.columns.isin(self.value_columns)].tolist()
        year_cols = df.columns[df.columns.isin(self.year_columns)].tolist()
        
        value_col = value_cols[0] if value_cols else None
        year_col = year_cols[0] if year_cols else None
        
        print(f"Visualizing {dataset_name}")
        print(f"Shape: {df.shape}")
        print(f"Value column: {value_col}")
        print(f"Year column: {year_col}")
        
        # Create figure
        n_cols = min(3, len(df.columns))
        n_rows = (len(df.columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        fig.suptitle(f'Dataset: {dataset_name}', fontsize=16, fontweight='bold')
        
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        for i, column in enumerate(df.columns):
            ax = axes[i] if i < len(axes) else None
            if ax is None:
                continue
            
            # Skip if column is all null
            if df[column].isnull().all():
                ax.text(0.5, 0.5, f'{column}\n(All null)', 
                       ha='center', va='center', transform=ax.transAxes)
                ax.set_title(column)
                continue
            
            # Determine column type and plot accordingly
            if df[column].dtype in ['int64', 'float64']:
                # Numeric column
                if df[column].nunique() < 20:
                    # Discrete values - bar chart
                    value_counts = df[column].value_counts().head(max_categories)
                    ax.bar(range(len(value_counts)), value_counts.values)
                    ax.set_xticks(range(len(value_counts)))
                    ax.set_xticklabels(value_counts.index, rotation=45)
                    ax.set_title(f'{column} (Discrete)')
                else:
                    # Continuous values - histogram
                    ax.hist(df[column].dropna(), bins=30, alpha=0.7)
                    ax.set_title(f'{column} (Continuous)')
                ax.set_ylabel('Frequency')
                
            else:
                # Categorical column
                value_counts = df[column].value_counts().head(max_categories)
                ax.bar(range(len(value_counts)), value_counts.values)
                ax.set_xticks(range(len(value_counts)))
                ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
                ax.set_title(f'{column} (Categorical)')
                ax.set_ylabel('Count')
        
        # Hide unused subplots
        for i in range(len(df.columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.show()
    
    def print_data_summary(self):
        """
        Print a comprehensive summary of all loaded datasets
        """
        if not self.dataframes:
            print("No data loaded. Call load_all_csv_files() first.")
            return
        
        print("\n" + "="*80)
        print("DATA SUMMARY")
        print("="*80)
        
        for dataset_name in sorted(self.dataframes.keys()):
            df = self.dataframes[dataset_name]
            info = self.data_info[dataset_name]
            
            print(f"\n[Dataset] {dataset_name}")
            print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            print(f"   File size: {info['file_size']:,} bytes")
            print(f"   Columns: {', '.join(df.columns)}")
            
            # Find value and year columns using pandas built-in methods
            value_cols = df.columns[df.columns.isin(self.value_columns)].tolist()
            year_cols = df.columns[df.columns.isin(self.year_columns)].tolist()
            
            if value_cols:
                print(f"   Value columns: {', '.join(value_cols)}")
                for col in value_cols:
                    if df[col].dtype in ['int64', 'float64']:
                        print(f"     {col}: min={df[col].min():,.0f}, max={df[col].max():,.0f}, mean={df[col].mean():,.1f}")
            
            if year_cols:
                print(f"   Year columns: {', '.join(year_cols)}")
                for col in year_cols:
                    unique_years = df[col].dropna().unique()
                    if len(unique_years) <= 10:
                        print(f"     {col}: {sorted(unique_years)}")
                    else:
                        print(f"     {col}: {df[col].min()}-{df[col].max()} ({len(unique_years)} unique years)")
            
            # Show sample data
            print(f"   Sample data:")
            sample = df.head(3)
            for i, row in sample.iterrows():
                print(f"     Row {i}: {dict(row)}")
        
        print("\n" + "="*80)
    
    def get_datasets_with_columns(self, required_columns: List[str]) -> List[str]:
        """
        Get list of datasets that contain specific columns
        
        Args:
            required_columns: List of column names to look for
            
        Returns:
            List of dataset names that contain all required columns
        """
        matching_datasets = []
        
        for dataset_name, df in self.dataframes.items():
            # Use pandas built-in method to check if all required columns exist
            if df.columns.isin(required_columns).sum() >= len(required_columns):
                matching_datasets.append(dataset_name)
        
        return matching_datasets