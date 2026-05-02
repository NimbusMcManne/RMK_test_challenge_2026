"""
Data Validation Module

This module provides validation functions for API responses and data integrity checks
before processing for statistical analysis.
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Container for validation results"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    data_shape: Optional[tuple] = None
    data_types: Optional[Dict] = None


class DataValidator:
    """
    Validates API response data for statistical analysis readiness.
    """
    
    def __init__(self):
        self.required_numeric_types = ['int64', 'float64', 'int32', 'float32']
    
    def validate_response_structure(self, data: Any) -> ValidationResult:
        """
        Validate basic response structure.
        
        Args:
            data: Response data from API
            
        Returns:
            ValidationResult with validation status and issues
        """
        errors = []
        warnings = []
        
        # Check if data is empty
        if data is None:
            errors.append("Response data is None")
            return ValidationResult(False, errors, warnings)
        
        if isinstance(data, (dict, list)):
            if isinstance(data, dict) and not data:
                errors.append("Response dictionary is empty")
            elif isinstance(data, list) and not data:
                warnings.append("Response list is empty")
        else:
            warnings.append(f"Unexpected data type: {type(data)}")
        
        return ValidationResult(len(errors) == 0, errors, warnings)
    
    def _convert_json_stat_to_dataframe(self, data: Dict) -> pd.DataFrame:
        """
        Convert JSON-STAT format (Estonia Statistics API) to DataFrame.
        
        Args:
            data: JSON-STAT response data
            
        Returns:
            DataFrame with the data
        """
        try:
            variables = data.get('variables', [])
            
            # Check if we have actual data values (not just metadata)
            if len(variables) == 0:
                return pd.DataFrame()
            
            # Extract variable information
            var_info = {}
            for var in variables:
                code = var.get('code', '')
                values = var.get('values', [])
                value_texts = var.get('valueTexts', [])
                
                if values and value_texts:
                    # Create mapping from value codes to text labels
                    var_info[code] = dict(zip(values, value_texts))
                elif values:
                    var_info[code] = values
            
            # If we only have metadata (no actual data values), create a summary DataFrame
            if not var_info:
                return pd.DataFrame()
            
            # Create a DataFrame with variable information
            rows = []
            max_length = max(len(vals) if isinstance(vals, list) else 0 for vals in var_info.values())
            
            if max_length == 0:
                return pd.DataFrame()
            
            for i in range(max_length):
                row = {}
                for code, values in var_info.items():
                    if isinstance(values, list) and i < len(values):
                        row[code] = values[i]
                    elif isinstance(values, dict):
                        # For dict, we'll need actual data points to map
                        pass
                rows.append(row)
            
            df = pd.DataFrame(rows)
            
            # If DataFrame is empty, create a summary of available variables
            if df.empty:
                summary_data = []
                for var in variables:
                    summary_data.append({
                        'variable_code': var.get('code', ''),
                        'variable_text': var.get('text', ''),
                        'num_values': len(var.get('values', [])),
                        'sample_values': var.get('values', [])[:5]
                    })
                df = pd.DataFrame(summary_data)
            
            return df
            
        except Exception as e:
            logger.error(f"Error converting JSON-STAT to DataFrame: {str(e)}")
            return pd.DataFrame()
    
    def _convert_json_stat_with_data(self, data: Dict) -> pd.DataFrame:
        """
        Convert JSON-STAT format with actual data values to DataFrame.
        
        Args:
            data: JSON-STAT response data with 'dimension' and 'value' keys
            
        Returns:
            DataFrame with actual data
        """
        try:
            dimensions = data.get('dimension', {})
            values = data.get('value', [])
            
            if not values:
                return pd.DataFrame()
            
            # Extract dimension information
            dimension_info = {}
            for dim_id, dim_data in dimensions.items():
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
            
            # Get dimension sizes in order
            dim_ids = list(dimensions.keys())
            dim_sizes = [dimension_info[dim_id]['size'] for dim_id in dim_ids]
            
            # Calculate the stride for each dimension
            strides = []
            stride = 1
            for size in reversed(dim_sizes[1:]):
                strides.insert(0, stride)
                stride *= size
            strides.insert(0, stride)  # First dimension has stride 1
            
            # Create rows for each data point
            rows = []
            for i, value in enumerate(values):
                if value is None:
                    continue
                
                row = {'value': value}
                
                # Calculate the multi-dimensional indices for this data point
                remaining = i
                for j, dim_id in enumerate(dim_ids):
                    dim_size = dim_sizes[j]
                    stride = strides[j]
                    dim_index = remaining // stride
                    remaining = remaining % stride
                    
                    # Get the label for this dimension index
                    index_to_label = dimension_info[dim_id]['index_to_label']
                    if dim_index in index_to_label:
                        row[dim_id] = index_to_label[dim_index]
                    else:
                        row[dim_id] = dim_index
                
                rows.append(row)
            
            if rows:
                df = pd.DataFrame(rows)
                return df
            else:
                # If we couldn't parse the complex structure, return a simple DataFrame
                return pd.DataFrame({'value': values})
                
        except Exception as e:
            logger.error(f"Error converting JSON-STAT with data to DataFrame: {str(e)}")
            # Fallback: return simple DataFrame with values
            try:
                values = data.get('value', [])
                return pd.DataFrame({'value': values})
            except:
                return pd.DataFrame()
    
    def validate_dataframe_structure(self, df: pd.DataFrame) -> ValidationResult:
        """
        Validate DataFrame structure for statistical analysis.
        
        Args:
            df: Pandas DataFrame to validate
            
        Returns:
            ValidationResult with validation status and issues
        """
        errors = []
        warnings = []
        
        if df.empty:
            errors.append("DataFrame is empty")
            return ValidationResult(False, errors, warnings)
        
        # Check for missing values
        missing_counts = df.isnull().sum()
        high_missing_cols = missing_counts[missing_counts > len(df) * 0.5]
        
        if not high_missing_cols.empty:
            warnings.append(f"Columns with >50% missing values: {list(high_missing_cols.index)}")
        
        # Check data types
        numeric_cols = df.select_dtypes(include=np.number).columns
        if len(numeric_cols) == 0:
            warnings.append("No numeric columns found for statistical analysis")
        
        # Check for duplicate rows
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            warnings.append(f"Found {duplicates} duplicate rows")
        
        return ValidationResult(
            len(errors) == 0,
            errors,
            warnings,
            data_shape=df.shape,
            data_types=dict(df.dtypes)
        )
    
    def convert_to_dataframe(self, data: Any) -> tuple:
        """
        Convert API response data to DataFrame with validation.
        
        Args:
            data: Response data from API
            
        Returns:
            Tuple of (DataFrame, ValidationResult)
        """
        errors = []
        warnings = []
        
        try:
            if isinstance(data, list):
                # List of dictionaries
                if all(isinstance(item, dict) for item in data):
                    df = pd.DataFrame(data)
                else:
                    errors.append("List contains non-dictionary items")
                    return pd.DataFrame(), ValidationResult(False, errors, warnings)
            
            elif isinstance(data, dict):
                # Handle JSON-STAT format (Estonia Statistics API)
                if 'variables' in data and isinstance(data['variables'], list):
                    df = self._convert_json_stat_to_dataframe(data)
                elif 'dimension' in data and 'value' in data:
                    # Handle full JSON-STAT response with actual data
                    df = self._convert_json_stat_with_data(data)
                # Try to find the main data array
                elif 'data' in data and isinstance(data['data'], list):
                    df = pd.DataFrame(data['data'])
                elif 'results' in data and isinstance(data['results'], list):
                    df = pd.DataFrame(data['results'])
                elif 'items' in data and isinstance(data['items'], list):
                    df = pd.DataFrame(data['items'])
                else:
                    # Try to convert dict directly
                    df = pd.DataFrame([data])
            else:
                errors.append(f"Cannot convert {type(data)} to DataFrame")
                return pd.DataFrame(), ValidationResult(False, errors, warnings)
            
            # Validate the resulting DataFrame
            validation_result = self.validate_dataframe_structure(df)
            return df, validation_result
            
        except Exception as e:
            errors.append(f"Error converting to DataFrame: {str(e)}")
            return pd.DataFrame(), ValidationResult(False, errors, warnings)
    
    def validate_for_correlation_analysis(self, df: pd.DataFrame) -> ValidationResult:
        """
        Validate DataFrame suitability for correlation analysis.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            ValidationResult with correlation-specific validation
        """
        errors = []
        warnings = []
        
        if df.empty:
            errors.append("DataFrame is empty")
            return ValidationResult(False, errors, warnings)
        
        # Check for sufficient numeric columns
        numeric_cols = df.select_dtypes(include=np.number).columns
        if len(numeric_cols) < 2:
            errors.append("Need at least 2 numeric columns for correlation analysis")
        
        # Check for sufficient data points
        if len(df) < 10:
            warnings.append("Dataset has fewer than 10 observations - correlations may be unreliable")
        
        # Check for constant columns (zero variance)
        numeric_df = df[numeric_cols]
        constant_cols = numeric_df.columns[numeric_df.var() == 0]
        
        if not constant_cols.empty:
            warnings.append(f"Constant columns (zero variance): {list(constant_cols)}")
        
        return ValidationResult(
            len(errors) == 0,
            errors,
            warnings,
            data_shape=df.shape,
            data_types={'numeric_columns': list(numeric_cols)}
        )
    
    def validate_for_probability_analysis(self, df: pd.DataFrame) -> ValidationResult:
        """
        Validate DataFrame suitability for probability analysis.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            ValidationResult with probability-specific validation
        """
        errors = []
        warnings = []
        
        if df.empty:
            errors.append("DataFrame is empty")
            return ValidationResult(False, errors, warnings)
        
        # Check for categorical data
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) == 0:
            warnings.append("No categorical columns found for probability analysis")
        
        # Check for binary/categorical variables suitable for probability
        binary_cols = []
        for col in df.columns:
            unique_vals = df[col].dropna().nunique()
            if unique_vals == 2:
                binary_cols.append(col)
        
        if not binary_cols:
            warnings.append("No binary variables found - consider creating binary features")
        
        # Check sample size for probability estimates
        if len(df) < 30:
            warnings.append("Small sample size (<30) - probability estimates may be unreliable")
        
        return ValidationResult(
            len(errors) == 0,
            errors,
            warnings,
            data_shape=df.shape,
            data_types={
                'categorical_columns': list(categorical_cols),
                'binary_columns': binary_cols
            }
        )


def validate_api_response(data: Any, analysis_type: str = "general") -> tuple:
    """
    Convenience function to validate API response for specific analysis type.
    
    Args:
        data: API response data
        analysis_type: Type of analysis ("correlation", "probability", "general")
        
    Returns:
        Tuple of (DataFrame, ValidationResult)
    """
    validator = DataValidator()
    
    # Convert to DataFrame
    df, structure_validation = validator.convert_to_dataframe(data)
    
    if not structure_validation.is_valid:
        return df, structure_validation
    
    # Perform analysis-specific validation
    if analysis_type == "correlation":
        analysis_validation = validator.validate_for_correlation_analysis(df)
    elif analysis_type == "probability":
        analysis_validation = validator.validate_for_probability_analysis(df)
    else:
        analysis_validation = ValidationResult(True, [], [])
    
    # Combine validation results
    combined_errors = structure_validation.errors + analysis_validation.errors
    combined_warnings = structure_validation.warnings + analysis_validation.warnings
    
    combined_validation = ValidationResult(
        is_valid=len(combined_errors) == 0,
        errors=combined_errors,
        warnings=combined_warnings,
        data_shape=df.shape,
        data_types={**(structure_validation.data_types or {}), **(analysis_validation.data_types or {})}
    )
    
    return df, combined_validation
