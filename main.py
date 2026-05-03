#!/usr/bin/env python3
"""
RMK Estonian Statistical Data Analysis Pipeline

This script runs the complete data analysis process from API calls to visualization:
1. Retrieves data from RMK API
2. Processes and cleans the data
3. Extracts 15 key probabilities
4. Generates visualizations (horizontal scale and pie chart)

Author: RMK Data Team Intern
"""

import sys
import os
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(current_dir))

def main():
    """Main pipeline function"""
    print("=" * 60)
    print("RMK Estonian Statistical Data Analysis Pipeline")
    print("=" * 60)
    
    try:
        # Step 1: Data Retrieval
        print("\n[DATA] Step 1: Retrieving data from RMK API...")
        from data_process.retrieve_data import main as retrieve_data
        retrieve_data()
        print("[DONE] Data retrieval completed successfully")
        
        # Step 2: Probability Extraction and Visualization
        print("\n[ANALYSIS] Step 2: Extracting probabilities and generating visualizations...")
        from prob_extraction.extract_probabilities import extract_15_specific_probabilities, visualize_probabilities, create_pie_chart
        
        # Extract the 15 specific probabilities
        results = extract_15_specific_probabilities()
        
        # Create visualizations
        fig1, ax1 = visualize_probabilities(results)
        fig2, ax2 = create_pie_chart(results)
        
        # Create images folder if it doesn't exist
        os.makedirs('images', exist_ok=True)
        
        # Save both plots to images folder
        import matplotlib.pyplot as plt
        plt.figure(fig1.number)
        plt.savefig('images/15_probabilities_horizontal_scale.png', dpi=300, bbox_inches='tight')
        
        plt.figure(fig2.number)
        plt.savefig('images/15_probabilities_pie_chart.png', dpi=300, bbox_inches='tight')
        
        print("[DONE] Probability extraction and visualization completed successfully")
        
        # Step 3: Display results
        print("\n[RESULTS] Step 3: Analysis Results")
        print("=" * 40)
        
        sorted_probabilities = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
        print("\n[TOP 5] Most Probable Events:")
        for i, (event, prob) in enumerate(list(sorted_probabilities.items())[:5], 1):
            print(f"{i}. {event}: {prob:.4f}")
        
        print("\n[BOTTOM 5] Least Probable Events:")
        for i, (event, prob) in enumerate(list(sorted_probabilities.items())[-5:], len(sorted_probabilities)-4):
            print(f"{i}. {event}: {prob:.4f}")
        
        print(f"\n[SUMMARY] Total probabilities analyzed: {len(sorted_probabilities)}")
        
        # Display file locations
        print("\n[FILES] Generated Files:")
        print(f"- Data files: ./output/ (CSV files from RMK API)")
        print(f"- Horizontal scale visualization: ./images/15_probabilities_horizontal_scale.png")
        print(f"- Pie chart visualization: ./images/15_probabilities_pie_chart.png")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Pipeline completed successfully!")
        print("=" * 60)
        
        # Show plots
        plt.show()
        
    except ImportError as e:
        print(f"[ERROR] Import Error: {e}")
        print("Please ensure all required modules are available in the src/ directory")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Pipeline Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
