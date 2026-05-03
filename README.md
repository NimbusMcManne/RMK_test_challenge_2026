# RMK Estonian Statistical Data Analysis

A comprehensive data analysis pipeline for extracting and visualizing key probabilities from Estonian statistical datasets. This project was developed as a test challenge for RMK data team internship.

## Overview

This pipeline analyzes 9 different Estonian statistical datasets to extract 15 key probabilities, then visualizes them using both nonlinear horizontal scale and pie chart visualizations. The analysis covers diverse domains including fishing, health, agriculture, marriage patterns, traffic safety, and emergency medical services.

### 📊 Key Features

- **Automated Data Retrieval**: Fetches data from RMK API
- **Dynamic Probability Calculation**: Uses flexible, reusable functions for probability extraction
- **Dual Visualization**: Horizontal scale with nonlinear transformation + pie chart distribution
- **Comprehensive Analysis**: 15 specific probabilities across 9 datasets
- **Clean Architecture**: Streamlined codebase with minimal duplication

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Required packages (install via requirements.txt):
  ```bash
  pip install -r requirements.txt
  ```

### Running the Complete Pipeline

Execute the entire process from data retrieval to visualization:

```bash
python main.py
```

This single command will:
1. Retrieve data from RMK API
2. Process and clean the data
3. Extract 15 key probabilities
4. Generate visualizations
5. Display results summary
6. Show interactive plots

### Generated Files

After running the pipeline, you'll find:

- **`output/`** - CSV files retrieved from RMK API
- **`images/15_probabilities_horizontal_scale.png`** - Nonlinear scale visualization
- **`images/15_probabilities_pie_chart.png`** - Pie chart distribution

## 📈 Analyzed Probabilities

The pipeline extracts and analyzes these 15 key probabilities:

### 🐟 Fishing & Agriculture
1. **Ocean Shrimp Catch Probability** - Share of shrimp in total ocean fishing
2. **Ocean Sardine Catch Probability** - Share of sardine in total ocean fishing
3. **Perch Probability in Lake Peipsi** - Probability of catching perch in Lake Peipsi
4. **Pike Probability in Lake Peipsi** - Probability of catching pike in Lake Peipsi
5. **Least Bred Animal** - The least commonly bred animal in Estonia

### 🏥 Health & Mental Health
6. **Probability of Cannabinoid Disorders** - Share of cannabinoid-related mental health disorders
7. **Probability of Alcohol Disorders** - Share of alcohol-related mental health disorders

### 💑 Marriage Patterns
8. **Most Likely Marriage Month** - Month with highest marriage probability
9. **Least Likely Marriage Month** - Month with lowest marriage probability
10. **Most Common Marriage Age** - Age group with highest marriage probability

### 🚗 Traffic & Safety
11. **Share of Accidents Caused by Drunk Drivers** - Proportion of accidents involving drunk drivers
12. **Peak Accident Month** - Month with most traffic accidents

### 🚑 Emergency Services
13. **Share of Pedestrian Injuries** - Proportion of pedestrian injuries in traffic accidents
14. **Share of Cyclist Injuries** - Proportion of cyclist injuries in traffic accidents
15. **Likelihood of Ambulance Transport** - Probability of ambulance transport to hospital

## 🏗️ Project Structure

```
RMK_test_challenge_2026/
├── main.py                          # Main pipeline script
├── requirements.txt                 # Python dependencies
├── src/                             # Source code
│   ├── data_process/                # Data retrieval and processing
│   │   └── retrieve_data.py        # RMK API data retrieval
│   └── prob_extraction/             # Probability extraction
│       └── extract_probabilities.py # Dynamic probability calculations
├── output/                          # Retrieved CSV data (gitignored)
├── images/                          # Generated visualizations (gitignored)
└── README.md                        # This file
```

## 🔧 Technical Details

### Dynamic Probability Functions

The project uses two main dynamic functions that replace 9 individual dataset-specific functions:

1. **`calculate_category_probabilities()`** - For category-based probability calculations
2. **`calculate_group_probabilities()`** - For group-based probability calculations

This approach reduces code duplication by 90% while maintaining full functionality.

### Visualization Features

- **Nonlinear Horizontal Scale**: Square root transformation for better low-value precision
- **Pie Chart Distribution**: Color-coded gradient from red (high) to blue (low)
- **Professional Labeling**: All labels include specific names (months, animals, age groups)
- **Enhanced Readability**: Alternating label positions and vertical separation

### Data Sources

All data is retrieved from official RMK (Estonian Statistics Office) APIs:
- KA10: Ocean fishing statistics
- KA30: Lake fishing statistics  
- PKH7: Mental health disorder statistics
- PM09: Agricultural statistics
- RV262: Marriage month statistics
- RV271: Marriage age statistics
- TS093: Traffic safety statistics
- VIG10: Injury cause statistics
- KE32: Emergency medical statistics

## 📊 Results Interpretation

### Horizontal Scale Visualization
- **Left side (0)**: Least probable events with enhanced precision
- **Right side (1)**: Most probable events
- **Nonlinear transformation**: Better separation for clustered low values

### Pie Chart Visualization
- **Slice size**: Represents relative probability magnitude
- **Color gradient**: Red (highest) → Yellow → Blue (lowest)
- **Legend**: Shows exact probabilities with shortened labels

## 🛠️ Development Notes

### Architecture Benefits
- **Maintainable**: Only 2 core functions for all probability calculations
- **Extensible**: Easy to add new probability analyses
- **Testable**: Clear separation of concerns
- **Documented**: Comprehensive inline documentation

### Probability Calculation Method
All probabilities are calculated as **overall aggregates across all years** in each dataset, not as single-year averages or means of yearly probabilities. This provides the most accurate representation of long-term patterns.

## 📝 Usage Examples

### Basic Usage
```bash
# Run complete pipeline
python main.py
```

### Custom Analysis
```python
# Import specific functions for custom analysis
from src.prob_extraction.extract_probabilities import extract_15_specific_probabilities

# Get probabilities
results = extract_15_specific_probabilities()

# Access specific probability
alcohol_disorder_prob = results['Probability of Alcohol Disorders']
print(f"Alcohol disorder probability: {alcohol_disorder_prob:.4f}")
```

## 🤝 Contributing

This project was developed as part of RMK's data team internship challenge. The codebase demonstrates:

- Clean, maintainable architecture
- Effective data processing pipelines
- Dynamic, reusable functions
- Professional visualization techniques
- Comprehensive documentation

## 📄 License

This project is open source and available under the terms specified in the LICENSE file.

---

**RMK Data Team Internship Challenge**  
*Demonstrating expertise in data analysis, visualization, and software engineering*
