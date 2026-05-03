"""
CSV Converter for Estonia Statistics API Data

This module converts DataFrames from different API formats into standardized CSV files
that can be easily processed for probability analysis.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, Any, Optional
import json

class CSVConverter:
    """Converts DataFrames from various API formats to standardized CSV files"""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize CSV converter
        
        Args:
            output_dir: Directory to save CSV files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def _extract_dataset_name(self, dataset_url: str) -> str:
        """
        Extract clean dataset name from URL
        
        Args:
            dataset_url: Full URL of dataset
            
        Returns:
            Clean dataset name for filename
        """
        # Extract the last part of the URL
        dataset_id = dataset_url.split('/')[-1]
        # Remove file extension if present
        if '.' in dataset_id:
            dataset_id = dataset_id.split('.')[0]
        return dataset_id
    
    def _normalize_dataframe(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """
        Normalize DataFrame to standard format
        
        Args:
            df: Input DataFrame
            dataset_name: Name of the dataset
            
        Returns:
            Normalized DataFrame
        """
        # Create a copy to avoid modifying original
        normalized_df = df.copy()
        
        # Handle different DataFrame structures
        
        # Case 1: Single column with nested data (like the PKH7 example)
        if len(normalized_df.columns) == 1 and normalized_df.columns[0] in ['dataset', 'RV262']:
            print(f"Processing nested data structure for {dataset_name}")
            
            # Extract the nested data
            nested_data = normalized_df.iloc[0, 0]
            
            if isinstance(nested_data, dict):
                # Check if it has status data (like PKH7) - prioritize this over JSON-STAT
                if 'status' in nested_data:
                    return self._convert_status_data(nested_data, dataset_name)
                # Check if it's JSON-STAT format with dimensions and values
                elif 'dimension' in nested_data and 'value' in nested_data:
                    return self._convert_json_stat_to_flat(nested_data, dataset_name)
                else:
                    # Try to flatten the nested structure
                    return self._flatten_nested_dict(nested_data, dataset_name)
            else:
                # If it's not a dict, create a simple DataFrame
                return pd.DataFrame({'value': [nested_data], 'dataset': [dataset_name]})
        
        # Case 2: Already structured DataFrame (most common case)
        else:
            # Ensure we have standard column names
            if 'value' not in normalized_df.columns:
                # Try to find a numeric column to rename as 'value'
                numeric_cols = normalized_df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    normalized_df = normalized_df.rename(columns={numeric_cols[0]: 'value'})
                else:
                    # If no numeric column, add a placeholder
                    normalized_df['value'] = 1
            
            # Add dataset name column if not present
            if 'dataset' not in normalized_df.columns:
                normalized_df['dataset'] = dataset_name
            
            # Reorder columns: dataset, value, then others
            cols = ['dataset', 'value'] + [col for col in normalized_df.columns if col not in ['dataset', 'value']]
            normalized_df = normalized_df[cols]
            
            return normalized_df
    
    def _convert_json_stat_to_flat(self, json_stat_data: Dict, dataset_name: str) -> pd.DataFrame:
        """
        Convert JSON-STAT format to flat DataFrame
        
        Args:
            json_stat_data: JSON-STAT format data
            dataset_name: Name of the dataset
            
        Returns:
            Flat DataFrame
        """
        try:
            # Check if we have actual values to process
            values = json_stat_data.get('value', [])
            
            # If we have status data but no values, try status conversion
            if 'status' in json_stat_data and not values:
                return self._convert_status_data(json_stat_data, dataset_name)
            
            dimensions = json_stat_data.get('dimension', {})
            
            if not values:
                return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
            
            # Extract dimension information in proper order
            dimension_info = {}
            dimension_order = []
            dimension_sizes = []
            
            for dim_id, dim_data in dimensions.items():
                # Skip non-dimension fields like 'id', 'size', 'role'
                if dim_id in ['id', 'size', 'role']:
                    continue
                    
                if 'category' in dim_data:
                    labels = dim_data['category'].get('label', {})
                    indices = dim_data['category'].get('index', {})
                    
                    # Create mapping from index to label
                    index_to_label = {}
                    for code, idx in indices.items():
                        if code in labels:
                            index_to_label[idx] = labels[code]
                    
                    dimension_info[dim_id] = {
                        'index_to_label': index_to_label,
                        'size': len(indices)
                    }
                    dimension_order.append(dim_id)
                    dimension_sizes.append(len(indices))
            
            # Create rows by mapping values to dimension combinations
            rows = []
            
            for i, value in enumerate(values):
                if value is None or value == 0:
                    continue
                
                # Calculate dimension indices for this value
                remaining = i
                dim_indices = []
                for size in reversed(dimension_sizes):
                    dim_indices.insert(0, remaining % size)
                    remaining = remaining // size
                
                # Create row with dimension labels
                row = {'value': value}
                for j, dim_id in enumerate(dimension_order):
                    if j < len(dim_indices):
                        dim_idx = dim_indices[j]
                        if dim_idx in dimension_info[dim_id]['index_to_label']:
                            row[dim_id] = dimension_info[dim_id]['index_to_label'][dim_idx]
                        else:
                            row[dim_id] = dim_idx
                    else:
                        row[dim_id] = None
                
                rows.append(row)
            
            if rows:
                df = pd.DataFrame(rows)
                # Reorder columns to put dimensions first, then value
                cols = dimension_order + ['value']
                df = df[[col for col in cols if col in df.columns]]
                df['dataset'] = dataset_name
                return df
            else:
                return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
                
        except Exception as e:
            print(f"Error converting JSON-STAT to flat: {e}")
            # Fallback: extract values with indices for large datasets
            values = json_stat_data.get('value', [])
            if values:
                rows = []
                # Limit to first 1000 non-zero values to avoid huge files
                non_zero_count = 0
                for i, value in enumerate(values):
                    if value is not None and value != 0:
                        rows.append({
                            'dataset': dataset_name,
                            'index': i,
                            'value': value
                        })
                        non_zero_count += 1
                        if non_zero_count >= 1000:  # Limit to prevent huge files
                            break
                
                if rows:
                    df = pd.DataFrame(rows)
                    return df
                else:
                    return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
            else:
                return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
    
    def _convert_status_data(self, json_stat_data: Dict, dataset_name: str) -> pd.DataFrame:
        """
        Convert status data (like PKH7) to DataFrame
        
        Args:
            json_stat_data: JSON data with 'status' field
            dataset_name: Name of the dataset
            
        Returns:
            DataFrame with status data
        """
        try:
            # Check if we have actual values (like PKH7)
            values = json_stat_data.get('value', [])
            if values and len(values) > 1:
                # This is a dataset with both status and values (like PKH7)
                return self._convert_mixed_status_value_data(json_stat_data, dataset_name)
            
            status_data = json_stat_data.get('status', {})
            
            if not status_data:
                return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
            
            rows = []
            
            # Convert each year/status pair to a row
            for year_code, status_value in status_data.items():
                # Skip if status is just a dot (missing data indicator)
                if status_value == '.' or status_value == '..':
                    continue
                
                # Try to convert year to integer and status to numeric
                try:
                    year = int(year_code)
                except (ValueError, TypeError):
                    year = year_code  # Keep as string if not convertible
                
                # Try to convert status to numeric, otherwise keep as string
                try:
                    value = float(status_value) if status_value not in ['.', '..'] else None
                except (ValueError, TypeError):
                    value = status_value
                
                row = {
                    'dataset': dataset_name,
                    'year': year,
                    'value': value,
                    'status': status_value
                }
                rows.append(row)
            
            if rows:
                df = pd.DataFrame(rows)
                # Reorder columns
                cols = ['dataset', 'year', 'value', 'status']
                df = df[[col for col in cols if col in df.columns]]
                return df
            else:
                # If no valid data found, create a summary row
                summary_row = {
                    'dataset': dataset_name,
                    'year': 'summary',
                    'value': None,
                    'status': f"Status data with {len(status_data)} entries, all missing"
                }
                return pd.DataFrame([summary_row])
                
        except Exception as e:
            print(f"Error converting status data: {e}")
            return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
    
    def _convert_mixed_status_value_data(self, json_stat_data: Dict, dataset_name: str) -> pd.DataFrame:
        """
        Convert datasets with both status and value data (like PKH7) to DataFrame
        
        Args:
            json_stat_data: JSON data with both 'status' and 'value' fields
            dataset_name: Name of the dataset
            
        Returns:
            DataFrame with value data
        """
        try:
            values = json_stat_data.get('value', [])
            dimensions = json_stat_data.get('dimension', {})
            
            if not values:
                return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
            
            # For PKH7 and similar datasets, create simple rows with the values
            # Don't try to use dimensions as they may be incomplete
            rows = []
            for i, value in enumerate(values):
                if value is None:
                    continue
                
                row = {
                    'dataset': dataset_name,
                    'index': i,
                    'value': value
                }
                rows.append(row)
            
            if rows:
                df = pd.DataFrame(rows)
                # Reorder columns
                cols = ['dataset', 'index', 'value']
                df = df[[col for col in cols if col in df.columns]]
                return df
            else:
                return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
                
        except Exception as e:
            print(f"Error converting mixed status/value data: {e}")
            return pd.DataFrame({'dataset': [dataset_name], 'value': [None]})
    
    def _flatten_nested_dict(self, nested_data: Dict, dataset_name: str) -> pd.DataFrame:
        """
        Flatten nested dictionary structure
        
        Args:
            nested_data: Nested dictionary
            dataset_name: Name of the dataset
            
        Returns:
            Flattened DataFrame
        """
        try:
            rows = []
            
            def flatten_dict(d, parent_key='', sep='_'):
                items = []
                for k, v in d.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key, sep=sep).items())
                    else:
                        items.append((new_key, v))
                return dict(items)
            
            flattened = flatten_dict(nested_data)
            
            # Create a single row with all flattened data
            row = {'dataset': dataset_name}
            row.update(flattened)
            
            # Try to find a numeric value
            numeric_values = [v for v in flattened.values() if isinstance(v, (int, float)) and v is not None]
            if numeric_values:
                row['value'] = numeric_values[0]
            else:
                row['value'] = 1
            
            rows.append(row)
            
            return pd.DataFrame(rows)
            
        except Exception as e:
            print(f"Error flattening nested dict: {e}")
            return pd.DataFrame({'dataset': [dataset_name], 'value': [1]})
    
    def convert_and_save(self, dataset_url: str, api_response: Any, df: Optional[pd.DataFrame] = None) -> str:
        """
        Convert dataset response to standardized CSV and save
        
        Args:
            dataset_url: URL of the dataset
            api_response: Raw API response (if df is None)
            df: Pre-processed DataFrame (optional)
            
        Returns:
            Path to saved CSV file
        """
        dataset_name = self._extract_dataset_name(dataset_url)
        
        # If DataFrame is not provided, try to create it from API response
        if df is None:
            try:
                # Try to import DataValidator to convert API response
                from API.data_validator import DataValidator
                validator = DataValidator()
                df, validation = validator.convert_to_dataframe(api_response)
                
                if not validation.is_valid or df.empty:
                    print(f"Warning: Could not convert {dataset_name} to DataFrame")
                    return None
            except Exception as e:
                print(f"Error converting {dataset_name}: {e}")
                return None
        
        # Normalize the DataFrame
        normalized_df = self._normalize_dataframe(df, dataset_name)
        
        # Generate filename
        csv_filename = f"{dataset_name}.csv"
        csv_path = self.output_dir / csv_filename
        
        # Save to CSV
        try:
            normalized_df.to_csv(csv_path, index=False, encoding='utf-8')
            print(f"Saved {dataset_name}: {normalized_df.shape} -> {csv_path}")
            return str(csv_path)
        except Exception as e:
            print(f"Error saving {dataset_name}: {e}")
            return None
    
    def convert_batch(self, results: Dict[str, Any]) -> Dict[str, str]:
        """
        Convert multiple datasets to CSV files
        
        Args:
            results: Dictionary of {dataset_url: api_response}
            
        Returns:
            Dictionary of {dataset_name: csv_path}
        """
        csv_files = {}
        
        for dataset_url, api_response in results.items():
            if api_response is not None:
                csv_path = self.convert_and_save(dataset_url, api_response)
                if csv_path:
                    dataset_name = self._extract_dataset_name(dataset_url)
                    csv_files[dataset_name] = csv_path
        
        print(f"\nConverted {len(csv_files)} datasets to CSV format")
        return csv_files
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of converted CSV files
        
        Returns:
            Summary statistics
        """
        csv_files = list(self.output_dir.glob("*.csv"))
        
        summary = {
            'total_files': len(csv_files),
            'output_directory': str(self.output_dir),
            'files': []
        }
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                file_info = {
                    'name': csv_file.name,
                    'path': str(csv_file),
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'size_bytes': csv_file.stat().st_size
                }
                summary['files'].append(file_info)
            except Exception as e:
                summary['files'].append({
                    'name': csv_file.name,
                    'path': str(csv_file),
                    'error': str(e)
                })
        
        return summary
