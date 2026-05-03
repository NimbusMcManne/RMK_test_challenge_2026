"""
Example script demonstrating fish probability calculations
"""

import sys
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(current_dir))

from data_process.fish_probabilities import FishProbabilityAnalysis

def main():
    """
    Demonstrate fish probability calculations
    """
    print("=== Fish Probability Analysis Example ===")
    
    # Initialize the fish probability analysis
    fish_analysis = FishProbabilityAnalysis()
    
    # Run complete analysis
    try:
        probabilities = fish_analysis.run_complete_analysis()
        
        # Show some specific examples
        if probabilities:
            print("\n=== SPECIFIC PROBABILITY EXAMPLES ===")
            
            # Example 1: Most likely fish species
            if 'species' in probabilities:
                species_probs = probabilities['species']['probabilities']
                most_likely_species = max(species_probs.items(), key=lambda x: x[1])
                print(f"Most likely fish species: {most_likely_species[0]} ({most_likely_species[1]:.2%})")
            
            # Example 2: Year with highest probability
            if 'yearly' in probabilities:
                yearly_probs = probabilities['yearly']['probabilities']
                highest_year = max(yearly_probs.items(), key=lambda x: x[1])
                print(f"Year with highest catch probability: {highest_year[0]} ({highest_year[1]:.2%})")
            
            # Example 3: Most productive water body
            if 'water_bodies' in probabilities:
                water_probs = probabilities['water_bodies']['probabilities']
                best_water_body = max(water_probs.items(), key=lambda x: x[1])
                print(f"Most productive water body: {best_water_body[0]} ({best_water_body[1]:.2%})")
            
            # Example 4: Conditional probability example
            if 'conditional' in probabilities:
                conditional = probabilities['conditional']
                if conditional:
                    first_water_body = list(conditional.keys())[0]
                    species_in_water = conditional[first_water_body]
                    if species_in_water:
                        most_likely_in_water = max(species_in_water.items(), key=lambda x: x[1])
                        print(f"In {first_water_body}, most likely species: {most_likely_in_water[0]} ({most_likely_in_water[1]:.2%})")
        
        print("\n=== Analysis Complete ===")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return

if __name__ == "__main__":
    main()
