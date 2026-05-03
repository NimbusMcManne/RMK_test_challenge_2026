"""
Example script demonstrating universal probability analysis
"""

import sys
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(current_dir))

from data_process.universal_probabilities import UniversalProbabilityAnalysis

def main():
    """
    Demonstrate universal probability analysis
    """
    print("=== Universal Probability Analysis Example ===")
    
    # Initialize the universal analysis
    universal_analysis = UniversalProbabilityAnalysis()
    
    # Test with all available datasets
    test_datasets = ['PKH7', 'PM09', 'KA10', 'KA30', 'RV262', 'RV271', 'TS093', 'VIG10']
    
    try:
        # Load and analyze specific datasets
        if universal_analysis.load_datasets(test_datasets):
            print("\n=== DATASET STRUCTURE ANALYSIS ===")
            for dataset_name in test_datasets:
                analysis = universal_analysis.analyze_dataset_structure(dataset_name)
                dataset_type = analysis['dataset_type']
                print(f"\n{dataset_name} ({dataset_type}):")
                print(f"  Shape: {analysis['shape'][0]} rows × {analysis['shape'][1]} columns")
                print(f"  Columns: {', '.join(analysis['columns'])}")
                print(f"  Value columns: {analysis['value_columns']}")
                print(f"  Year columns: {analysis['year_columns']}")
                print(f"  Category columns: {analysis['category_columns']}")
                print(f"  Location columns: {analysis['location_columns']}")
            
            # Calculate probabilities
            print("\n=== CALCULATING PROBABILITIES ===")
            universal_analysis.calculate_fish_probabilities()
            universal_analysis.calculate_emergency_probabilities()
            universal_analysis.calculate_mental_health_probabilities()
            universal_analysis.calculate_agricultural_probabilities()
            universal_analysis.calculate_marriage_statistics_probabilities()
            universal_analysis.calculate_demographics_probabilities()
            universal_analysis.calculate_traffic_safety_probabilities()
            universal_analysis.calculate_injury_causes_probabilities()
            universal_analysis.calculate_general_probabilities()
            
            # Generate comprehensive report
            print("\n=== GENERATING REPORT ===")
            report = universal_analysis.generate_comprehensive_report()
            print(report)
            
            # Create visualizations
            print("\n=== CREATING VISUALIZATIONS ===")
            
            # Visualize only available dataset types
            if 'fish' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('fish')
            if 'emergency' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('emergency')
            if 'mental_health' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('mental_health')
            if 'agricultural' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('agricultural')
            if 'marriage_statistics' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('marriage_statistics')
            if 'demographics' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('demographics')
            if 'traffic_safety' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('traffic_safety')
            if 'injury_causes' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('injury_causes')
            if 'general' in universal_analysis.probabilities:
                universal_analysis.visualize_probabilities('general')
            
            # Show specific examples
            print("\n=== SPECIFIC PROBABILITY EXAMPLES ===")
            
            # Mental health examples
            if 'mental_health' in universal_analysis.probabilities:
                mental_probs = universal_analysis.probabilities['mental_health']
                print(f"Most common diagnosis: {max(mental_probs['diagnosis_probabilities'].items(), key=lambda x: x[1])}")
                print(f"Highest probability year: {max(mental_probs['yearly_probabilities'].items(), key=lambda x: x[1])}")
            
            # Agricultural examples
            if 'agricultural' in universal_analysis.probabilities:
                agricultural_probs = universal_analysis.probabilities['agricultural']
                print(f"Most common animal type: {max(agricultural_probs['animal_type_probabilities'].items(), key=lambda x: x[1])}")
                print(f"Most common location: {max(agricultural_probs['location_probabilities'].items(), key=lambda x: x[1])}")
            
            # Marriage statistics examples
            if 'marriage_statistics' in universal_analysis.probabilities:
                marriage_probs = universal_analysis.probabilities['marriage_statistics']
                print(f"Most common marriage type: {max(marriage_probs['marriage_type_probabilities'].items(), key=lambda x: x[1])}")
                print(f"Most common marriage month: {max(marriage_probs['month_probabilities'].items(), key=lambda x: x[1])}")
            
            # Demographics examples
            if 'demographics' in universal_analysis.probabilities:
                demographics_probs = universal_analysis.probabilities['demographics']
                print(f"Most common gender: {max(demographics_probs['gender_probabilities'].items(), key=lambda x: x[1])}")
                print(f"Most common age group: {max(demographics_probs['age_group_probabilities'].items(), key=lambda x: x[1])}")
            
            # Traffic safety examples
            if 'traffic_safety' in universal_analysis.probabilities:
                traffic_probs = universal_analysis.probabilities['traffic_safety']
                print(f"Most common traffic indicator: {max(traffic_probs['indicator_probabilities'].items(), key=lambda x: x[1])}")
                print(f"Most common traffic month: {max(traffic_probs['month_probabilities'].items(), key=lambda x: x[1])}")
            
            # Injury causes examples
            if 'injury_causes' in universal_analysis.probabilities:
                injury_probs = universal_analysis.probabilities['injury_causes']
                print(f"Most common injury location: {max(injury_probs['location_probabilities'].items(), key=lambda x: x[1])}")
                print(f"Most common injury cause: {max(injury_probs['cause_probabilities'].items(), key=lambda x: x[1])}")
            
            # Fish examples
            if 'fish' in universal_analysis.probabilities:
                fish_probs = universal_analysis.probabilities['fish']
                if 'overall' in fish_probs:
                    yearly_probs = fish_probs['overall']['yearly_probabilities']
                    best_year = max(yearly_probs.items(), key=lambda x: x[1])
                    print(f"Best fishing year: {best_year[0]} ({best_year[1]:.2%})")
                
                if 'water_body' in fish_probs:
                    water_probs = fish_probs['water_body']['water_body_probabilities']
                    best_water = max(water_probs.items(), key=lambda x: x[1])
                    print(f"Best fishing location: {best_water[0]} ({best_water[1]:.2%})")
        
        print("\n=== Analysis Complete ===")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return

if __name__ == "__main__":
    main()
