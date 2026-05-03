# Universal Probability Analysis System

This document explains the universal probability analysis system that can handle different dataset types including fish data and emergency medical data.

## Overview

The `UniversalProbabilityAnalysis` class in `src/data_process/universal_probabilities.py` provides comprehensive probability calculations for multiple dataset types:

- **Fish Data**: KA10.csv (overall), KA30.csv (water body specific)
- **Emergency Medical Data**: KE32.csv (hospital/medical statistics)
- **General Time Series**: Any dataset with value and time columns

## Key Features

### 1. Automatic Dataset Type Detection
The system automatically identifies dataset types based on column structure:

- **Fish Water Body**: Contains `Kalaliik` and `Veekogu` columns
- **Fish Overall**: Contains `Kalaliik` and `Aasta` columns
- **Emergency Medical**: Contains `Haigla liik` and `Saabumisviis` columns
- **General Time Series**: Contains `value` and year columns

### 2. Flexible Column Recognition
Recognizes multiple column name patterns:
- **Value columns**: `value`, `values`, `Value`, `Values`
- **Year columns**: `aasta`, `aastad`, `Aasta`, `Aastad`, `year`, `Year`
- **Category columns**: `Kalaliik`, `Haigla liik`, `Saabumisviis`
- **Location columns**: `Veekogu`, `Maakond`, `Elukoht`

### 3. Comprehensive Probability Calculations

#### **Fish Data Analysis:**
- **Species Probabilities**: P(Species) = Total catch of species / Total catch
- **Yearly Probabilities**: P(Year) = Total catch in year / Total catch across all years
- **Water Body Probabilities**: P(Water Body) = Total catch in water body / Total catch across all water bodies
- **Conditional Probabilities**: P(Species | Water Body) = Catch of species in water body / Total catch in water body

#### **Emergency Medical Data Analysis:**
- **Yearly Probabilities**: P(Year) = Emergency cases in year / Total emergency cases
- **Arrival Method Probabilities**: P(Arrival Method) = Cases by arrival method / Total cases
- **Hospital Probabilities**: P(Hospital) = Cases by hospital / Total cases
- **Age Group Probabilities**: P(Age Group) = Cases by age group / Total cases
- **Clinical Condition Probabilities**: P(Condition) = Cases by clinical condition / Total cases

#### **General Time Series Analysis:**
- **Yearly Probabilities**: P(Year) = Events in year / Total events
- **Trend Analysis**: Compares first half vs second half averages

### 4. Advanced Visualization System

#### **Fish Data Visualizations:**
1. **Yearly Catch Probabilities** - Line chart over time
2. **Fish Species Probabilities** - Horizontal bar chart
3. **Water Body Probabilities** - Horizontal bar chart
4. **Yearly Catch Totals** - Line chart of actual values
5. **Top Species Over Time** - Multi-line chart

#### **Emergency Medical Visualizations:**
1. **Yearly Emergency Probabilities** - Line chart
2. **Arrival Method Probabilities** - Horizontal bar chart
3. **Hospital Probabilities** - Horizontal bar chart
4. **Yearly Emergency Totals** - Line chart of actual values

#### **General Time Series Visualizations:**
- **Multi-dataset comparison** - Multiple line charts on same axes

## Usage Examples

### Fish Data Analysis:
```python
from src.data_process.universal_probabilities import UniversalProbabilityAnalysis

# Initialize analysis
analysis = UniversalProbabilityAnalysis()

# Load specific datasets
analysis.load_datasets(['KA10', 'KA30'])

# Calculate fish probabilities
analysis.calculate_fish_probabilities()

# Visualize results
analysis.visualize_probabilities('fish')
```

### Emergency Medical Data Analysis:
```python
# Load emergency data
analysis.load_datasets(['KE32'])

# Calculate emergency probabilities
analysis.calculate_emergency_probabilities()

# Visualize results
analysis.visualize_probabilities('emergency')
```

### Universal Analysis (All Datasets):
```python
# Load all available datasets
analysis.load_datasets()  # None means load all

# Calculate all applicable probabilities
analysis.calculate_fish_probabilities()
analysis.calculate_emergency_probabilities()
analysis.calculate_general_probabilities()

# Generate comprehensive report
report = analysis.generate_comprehensive_report()
print(report)

# Visualize all datasets
analysis.visualize_probabilities()  # None means visualize all
```

## KE32 Dataset Analysis Results

### Data Structure:
- **Dataset Type**: Emergency Medical Data
- **Shape**: 38 rows × 7 columns
- **Time Period**: 2006-2022 (19 years)
- **Total Cases**: 7,973,640 emergency cases

### Key Findings:
- **Most Common Arrival Method**: "Pördus ise" (Self-referral) at 77.99%
- **Most Common Hospital**: "Erakorralise meditsiini osakond ja muu erakorraline vastuvõtt / traumapunkt kokku" (Emergency department + other emergency reception) at 100.00%
- **Highest Probability Year**: 2007 (8.98% of cases)
- **Age Distribution**: Cases distributed across different age groups

### Probability Calculations Available:
- **Yearly Probabilities**: Distribution of emergency cases across years
- **Method Probabilities**: Likelihood of different arrival methods
- **Hospital Probabilities**: Distribution across different hospitals
- **Age Group Probabilities**: Distribution across age categories
- **Clinical Condition Probabilities**: Distribution across medical conditions

## Technical Implementation

### Data Type Detection Algorithm:
```python
def _identify_dataset_type(self, df: pd.DataFrame) -> str:
    columns = set(df.columns)
    
    if 'Kalaliik' in columns and 'Veekogu' in columns:
        return 'fish_water_body'
    elif 'Kalaliik' in columns and 'Aasta' in columns:
        return 'fish_overall'
    elif 'Haigla liik' in columns and 'Saabumisviis' in columns:
        return 'emergency_medical'
    elif 'value' in columns and any(col in columns for col in ['Aasta', 'year']):
        return 'general_time_series'
    else:
        return 'unknown'
```

### Probability Calculation Methods:
- **Pandas Built-in Methods**: Uses efficient vectorized operations
- **Type Hints**: Comprehensive type annotations
- **Error Handling**: Robust exception handling and data validation
- **Modular Design**: Separate methods for different calculation types

## Applications

### Fisheries Management:
- Species distribution analysis for conservation planning
- Water body productivity assessment
- Yearly trend analysis for policy making

### Healthcare Planning:
- Emergency service demand forecasting
- Hospital capacity planning
- Age group risk assessment

### General Statistical Analysis:
- Time series probability analysis
- Trend detection and forecasting
- Multi-dataset comparison

## File Structure

```
src/data_process/
├── universal_probabilities.py    # Universal probability analysis
├── fish_probabilities.py         # Fish-specific analysis
└── csv_converter.py             # CSV conversion utilities

examples/
├── universal_probability_example.py    # Example usage script
└── fish_probability_example.py      # Fish-specific example

output/
├── KA10.csv                       # Overall fish statistics
├── KA30.csv                       # Water body specific fish data
└── KE32.csv                       # Emergency medical data
```

## Advantages

1. **Universal Compatibility**: Works with any dataset structure
2. **Automatic Type Detection**: No manual configuration needed
3. **Comprehensive Analysis**: Multiple probability calculation methods
4. **Rich Visualizations**: Dataset-appropriate chart types
5. **Scalable Design**: Easy to extend for new dataset types
6. **Robust Error Handling**: Graceful handling of missing or malformed data

## Future Extensions

The system can be extended to include:
- Predictive modeling and forecasting
- Correlation analysis between variables
- Geographic/spatial analysis
- Economic impact assessment
- Comparative analysis across regions
- Machine learning integration
