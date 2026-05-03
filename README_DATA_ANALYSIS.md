# Data Analysis System

This document explains how to use the data analysis system for loading CSV files, creating DataFrames, and visualizing statistics data.

## Overview

The `Calculations` class in `src/data_process/calc_probabilities.py` provides a structured way to:

1. Load all CSV files from the output directory
2. Create and manage pandas DataFrames
3. Analyze column structures
4. Visualize data distributions
5. Extract specific datasets for analysis

## Quick Start

```python
from src.data_process.calc_probabilities import Calculations

# Initialize the class
calc = DataAnalysis()

# Load all CSV files
dataframes = calc.load_all_csv_files()

# Print comprehensive summary
calc.print_data_summary()

# Create overview visualization
calc.visualize_dataset_overview()

# Visualize specific dataset
calc.visualize_dataset('VIG10')
```

## Key Features

### 1. Column Detection

The system automatically detects common column names:
- **Value columns**: `value`, `values`, `Value`, `Values`
- **Year columns**: `aasta`, `aastad`, `Aasta`, `Aastad`, `year`, `Year`
- **Dataset column**: `dataset`

### 2. Available Methods

#### `load_all_csv_files()`
Loads all CSV files from the output directory into DataFrames.

#### `get_dataframe(dataset_name)`
Returns a specific DataFrame by dataset name.

#### `analyze_column_structure(dataset_name=None)`
Analyzes column structure across all datasets or a specific dataset.

#### `visualize_dataset_overview()`
Creates overview visualizations of all loaded datasets.

#### `visualize_dataset(dataset_name, max_categories=20)`
Creates detailed visualizations for a specific dataset.

#### `print_data_summary()`
Prints a comprehensive summary of all loaded datasets.

#### `get_datasets_with_columns(required_columns)`
Returns datasets that contain specific columns.

## Current Datasets

The system has successfully loaded 9 datasets:

| Dataset | Rows | Columns | Value Column | Year Column | Description |
|---------|------|---------|--------------|-------------|-------------|
| KA10 | 132 | 4 | ✓ | ✓ | Fish statistics |
| KA30 | 2,109 | 5 | ✓ | ✓ | Water body fish data |
| KE32 | 38 | 7 | ✓ | ✓ | Emergency medical data |
| PKH7 | 84 | 5 | ✓ | ✓ | Mental health data |
| PM09 | 321 | 7 | ✓ | ✗ | Agricultural data |
| RV262 | 1,274 | 5 | ✓ | ✓ | Marriage statistics |
| RV271 | 1,050 | 6 | ✓ | ✓ | Population data |
| TS093 | 708 | 5 | ✓ | ✓ | Traffic accidents |
| VIG10 | 36 | 7 | ✓ | ✓ | Injury causes |

## Example Usage

### Accessing Specific Data

```python
# Get VIG10 dataset
vig10_df = calc.get_dataframe('VIG10')

# Filter for specific years
years_2020_2022 = vig10_df[vig10_df['Aasta'].isin([2020, 2021, 2022])]

# Get value statistics
value_stats = vig10_df['value'].describe()
```

### Finding Datasets with Specific Columns

```python
# Find datasets with both value and year columns
datasets_with_value_year = calc.get_datasets_with_columns(['value', 'Aasta'])

# Find datasets with specific dimensions
datasets_with_location = calc.get_datasets_with_columns(['Elukoht'])
```

### Column Analysis

```python
# Analyze all datasets
analysis = calc.analyze_column_structure()

# Analyze specific dataset
vig10_analysis = calc.analyze_column_structure('VIG10')
print(f"Value columns: {vig10_analysis['VIG10']['value_columns']}")
print(f"Year columns: {vig10_analysis['VIG10']['year_columns']}")
```

## Next Steps

The system is now ready for probability calculations. You can:

1. Extract specific columns for analysis
2. Filter data by years, categories, or values
3. Perform statistical calculations
4. Create probability distributions
5. Generate reports

## File Structure

```
src/data_process/
├── calc_probabilities.py    # Main analysis class
├── csv_converter.py        # CSV conversion utilities
├── data_request.py         # API data retrieval
└── retrieve_data.py        # Data retrieval script

output/
├── KA10.csv                # Fish statistics
├── KA30.csv                # Water body fish data
├── KE32.csv                # Emergency medical data
├── PKH7.csv                # Mental health data
├── PM09.csv                # Agricultural data
├── RV262.csv               # Marriage statistics
├── RV271.csv               # Population data
├── TS093.csv               # Traffic accidents
└── VIG10.csv               # Injury causes
```

## Notes

- All CSV files are properly structured with consistent column naming
- The system handles both Estonian and English column names
- Visualizations automatically adapt to different data types
- The system is extensible for additional analysis methods
