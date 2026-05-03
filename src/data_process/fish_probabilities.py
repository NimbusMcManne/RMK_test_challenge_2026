"""
Fish Probability Calculations Module

This module calculates various probabilities related to fish catch data
from KA10.csv (overall fish statistics) and KA30.csv (water body specific data).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class FishProbabilityAnalysis:
    """
    Class for calculating probabilities related to fish catch data
    """
    
    def __init__(self, data_dir: str = "output"):
        """
        Initialize the fish probability analysis
        
        Args:
            data_dir: Directory containing CSV files
        """
        self.data_dir = Path(data_dir)
        self.ka10_df = None
        self.ka30_df = None
        self.probabilities = {}
        
    def load_fish_data(self) -> bool:
        """
        Load fish datasets KA10.csv and KA30.csv
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load KA10.csv (overall fish statistics)
            ka10_path = self.data_dir / "KA10.csv"
            if ka10_path.exists():
                self.ka10_df = pd.read_csv(ka10_path, encoding='utf-8')
                print(f"Loaded KA10: {self.ka10_df.shape[0]} rows, {self.ka10_df.shape[1]} columns")
            else:
                print("KA10.csv not found")
                return False
            
            # Load KA30.csv (water body specific data)
            ka30_path = self.data_dir / "KA30.csv"
            if ka30_path.exists():
                self.ka30_df = pd.read_csv(ka30_path, encoding='utf-8')
                print(f"Loaded KA30: {self.ka30_df.shape[0]} rows, {self.ka30_df.shape[1]} columns")
            else:
                print("KA30.csv not found")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error loading fish data: {e}")
            return False
    
    def analyze_data_structure(self):
        """
        Analyze the structure of the fish datasets
        """
        if self.ka10_df is None or self.ka30_df is None:
            print("Data not loaded. Call load_fish_data() first.")
            return
        
        print("\n=== DATA STRUCTURE ANALYSIS ===")
        
        # KA10 Analysis
        print(f"\nKA10 (Overall Fish Statistics):")
        print(f"  Columns: {list(self.ka10_df.columns)}")
        print(f"  Years: {sorted(self.ka10_df['Aasta'].unique())}")
        print(f"  Fish types: {sorted(self.ka10_df['Kalaliik'].unique())}")
        print(f"  Value range: {self.ka10_df['value'].min():.1f} - {self.ka10_df['value'].max():.1f}")
        print(f"  Total catch: {self.ka10_df['value'].sum():.1f}")
        
        # KA30 Analysis
        print(f"\nKA30 (Water Body Specific):")
        print(f"  Columns: {list(self.ka30_df.columns)}")
        print(f"  Years: {sorted(self.ka30_df['Aasta'].unique())}")
        print(f"  Water bodies: {sorted(self.ka30_df['Veekogu'].unique())}")
        print(f"  Fish types: {sorted(self.ka30_df['Kalaliik'].unique())}")
        print(f"  Value range: {self.ka30_df['value'].min():.1f} - {self.ka30_df['value'].max():.1f}")
        print(f"  Total catch: {self.ka30_df['value'].sum():.1f}")
    
    def calculate_fish_species_probabilities(self) -> Dict:
        """
        Calculate probabilities of catching different fish species
        
        Returns:
            Dictionary with fish species probabilities
        """
        if self.ka30_df is None:
            print("Data not loaded. Call load_fish_data() first.")
            return {}
        
        # Filter out "Kala kokku" (total fish) to get individual species
        species_data = self.ka30_df[self.ka30_df['Kalaliik'] != 'Kala kokku'].copy()
        
        if species_data.empty:
            print("No individual fish species data found")
            return {}
        
        # Calculate total catch for each species across all years and water bodies
        species_totals = species_data.groupby('Kalaliik')['value'].sum()
        total_catch = species_totals.sum()
        
        # Calculate probabilities
        species_probabilities = (species_totals / total_catch).to_dict()
        
        # Store results
        self.probabilities['species'] = {
            'probabilities': species_probabilities,
            'totals': species_totals.to_dict(),
            'total_catch': total_catch
        }
        
        print(f"\n=== FISH SPECIES PROBABILITIES ===")
        print(f"Total catch (excluding 'Kala kokku'): {total_catch:.1f}")
        print(f"Number of species: {len(species_probabilities)}")
        
        # Sort by probability and display
        sorted_probs = sorted(species_probabilities.items(), key=lambda x: x[1], reverse=True)
        for species, prob in sorted_probs:
            print(f"  {species}: {prob:.4f} ({prob*100:.2f}%)")
        
        return self.probabilities['species']
    
    def calculate_yearly_probabilities(self) -> Dict:
        """
        Calculate yearly catch probabilities and trends
        
        Returns:
            Dictionary with yearly probabilities
        """
        if self.ka10_df is None:
            print("Data not loaded. Call load_fish_data() first.")
            return {}
        
        # Calculate yearly totals
        yearly_totals = self.ka10_df.groupby('Aasta')['value'].sum()
        total_overall = yearly_totals.sum()
        
        # Calculate probabilities for each year
        yearly_probabilities = (yearly_totals / total_overall).to_dict()
        
        # Calculate year-over-year changes
        yearly_changes = yearly_totals.pct_change().to_dict()
        
        # Store results
        self.probabilities['yearly'] = {
            'probabilities': yearly_probabilities,
            'totals': yearly_totals.to_dict(),
            'changes': yearly_changes,
            'total_overall': total_overall
        }
        
        print(f"\n=== YEARLY PROBABILITIES ===")
        print(f"Total catch across all years: {total_overall:.1f}")
        print(f"Year range: {min(yearly_totals.index)} - {max(yearly_totals.index)}")
        
        # Display yearly data
        for year in sorted(yearly_probabilities.keys()):
            change = yearly_changes.get(year, 'N/A')
            if isinstance(change, (int, float)):
                change_str = f"{change:+.2%}"
            else:
                change_str = "N/A"
            print(f"  {year}: {yearly_probabilities[year]:.4f} ({yearly_probabilities[year]*100:.2f}%) - Change: {change_str}")
        
        return self.probabilities['yearly']
    
    def calculate_water_body_probabilities(self) -> Dict:
        """
        Calculate probabilities for different water bodies
        
        Returns:
            Dictionary with water body probabilities
        """
        if self.ka30_df is None:
            print("Data not loaded. Call load_fish_data() first.")
            return {}
        
        # Calculate totals for each water body
        water_body_totals = self.ka30_df.groupby('Veekogu')['value'].sum()
        total_catch = water_body_totals.sum()
        
        # Calculate probabilities
        water_body_probabilities = (water_body_totals / total_catch).to_dict()
        
        # Store results
        self.probabilities['water_bodies'] = {
            'probabilities': water_body_probabilities,
            'totals': water_body_totals.to_dict(),
            'total_catch': total_catch
        }
        
        print(f"\n=== WATER BODY PROBABILITIES ===")
        print(f"Total catch across all water bodies: {total_catch:.1f}")
        print(f"Number of water bodies: {len(water_body_probabilities)}")
        
        # Sort by probability and display
        sorted_probs = sorted(water_body_probabilities.items(), key=lambda x: x[1], reverse=True)
        for water_body, prob in sorted_probs:
            print(f"  {water_body}: {prob:.4f} ({prob*100:.2f}%)")
        
        return self.probabilities['water_bodies']
    
    def calculate_conditional_probabilities(self) -> Dict:
        """
        Calculate conditional probabilities (e.g., probability of species given water body)
        
        Returns:
            Dictionary with conditional probabilities
        """
        if self.ka30_df is None:
            print("Data not loaded. Call load_fish_data() first.")
            return {}
        
        # Filter out "Kala kokku" to get individual species
        species_data = self.ka30_df[self.ka30_df['Kalaliik'] != 'Kala kokku'].copy()
        
        if species_data.empty:
            print("No individual fish species data found")
            return {}
        
        # Calculate P(Species | Water Body)
        conditional_probs = {}
        
        for water_body in species_data['Veekogu'].unique():
            water_body_data = species_data[species_data['Veekogu'] == water_body]
            water_body_total = water_body_data['value'].sum()
            
            if water_body_total > 0:
                species_given_water_body = {}
                for species in water_body_data['Kalaliik'].unique():
                    species_total = water_body_data[water_body_data['Kalaliik'] == species]['value'].sum()
                    species_given_water_body[species] = species_total / water_body_total
                
                conditional_probs[water_body] = species_given_water_body
        
        # Store results
        self.probabilities['conditional'] = conditional_probs
        
        print(f"\n=== CONDITIONAL PROBABILITIES ===")
        print(f"P(Species | Water Body)")
        
        for water_body, species_probs in conditional_probs.items():
            print(f"\n  {water_body}:")
            sorted_species = sorted(species_probs.items(), key=lambda x: x[1], reverse=True)
            for species, prob in sorted_species:
                print(f"    {species}: {prob:.4f} ({prob*100:.2f}%)")
        
        return self.probabilities['conditional']
    
    def calculate_trend_probabilities(self) -> Dict:
        """
        Calculate trend-based probabilities (increasing/decreasing trends)
        
        Returns:
            Dictionary with trend probabilities
        """
        if self.ka10_df is None:
            print("Data not loaded. Call load_fish_data() first.")
            return {}
        
        # Calculate yearly totals
        yearly_totals = self.ka10_df.groupby('Aasta')['value'].sum().sort_index()
        
        # Calculate trends
        trend_data = {}
        
        # Simple trend analysis: compare first half vs second half
        years = sorted(yearly_totals.index)
        mid_point = len(years) // 2
        
        if mid_point > 0:
            first_half_avg = yearly_totals.iloc[:mid_point].mean()
            second_half_avg = yearly_totals.iloc[mid_point:].mean()
            
            trend_direction = "increasing" if second_half_avg > first_half_avg else "decreasing"
            trend_magnitude = abs(second_half_avg - first_half_avg) / first_half_avg if first_half_avg > 0 else 0
            
            trend_data = {
                'direction': trend_direction,
                'magnitude': trend_magnitude,
                'first_half_avg': first_half_avg,
                'second_half_avg': second_half_avg,
                'yearly_trends': yearly_totals.pct_change().to_dict()
            }
        
        # Store results
        self.probabilities['trends'] = trend_data
        
        print(f"\n=== TREND PROBABILITIES ===")
        if trend_data:
            print(f"Overall trend: {trend_data['direction']}")
            print(f"Trend magnitude: {trend_data['magnitude']:.2%}")
            print(f"First half average: {trend_data['first_half_avg']:.1f}")
            print(f"Second half average: {trend_data['second_half_avg']:.1f}")
        
        return self.probabilities['trends']
    
    def visualize_probabilities(self):
        """
        Create visualizations for all probability calculations
        """
        if not self.probabilities:
            print("No probabilities calculated. Run calculation methods first.")
            return
        
        # Create subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Fish Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Species probabilities
        if 'species' in self.probabilities:
            species_probs = self.probabilities['species']['probabilities']
            if species_probs:
                species_df = pd.DataFrame(list(species_probs.items()), columns=['Species', 'Probability'])
                species_df = species_df.sort_values('Probability', ascending=True)
                
                axes[0, 0].barh(species_df['Species'], species_df['Probability'])
                axes[0, 0].set_title('Fish Species Probabilities')
                axes[0, 0].set_xlabel('Probability')
        
        # 2. Yearly probabilities
        if 'yearly' in self.probabilities:
            yearly_probs = self.probabilities['yearly']['probabilities']
            if yearly_probs:
                years = sorted(yearly_probs.keys())
                probs = [yearly_probs[year] for year in years]
                
                axes[0, 1].plot(years, probs, marker='o')
                axes[0, 1].set_title('Yearly Catch Probabilities')
                axes[0, 1].set_xlabel('Year')
                axes[0, 1].set_ylabel('Probability')
                axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Water body probabilities
        if 'water_bodies' in self.probabilities:
            water_probs = self.probabilities['water_bodies']['probabilities']
            if water_probs:
                water_df = pd.DataFrame(list(water_probs.items()), columns=['Water Body', 'Probability'])
                water_df = water_df.sort_values('Probability', ascending=True)
                
                axes[0, 2].barh(water_df['Water Body'], water_df['Probability'])
                axes[0, 2].set_title('Water Body Probabilities')
                axes[0, 2].set_xlabel('Probability')
        
        # 4. Yearly totals (actual values)
        if 'yearly' in self.probabilities:
            yearly_totals = self.probabilities['yearly']['totals']
            if yearly_totals:
                years = sorted(yearly_totals.keys())
                totals = [yearly_totals[year] for year in years]
                
                axes[1, 0].plot(years, totals, marker='s', color='orange')
                axes[1, 0].set_title('Yearly Catch Totals')
                axes[1, 0].set_xlabel('Year')
                axes[1, 0].set_ylabel('Total Catch')
                axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 5. Species distribution over time
        if self.ka30_df is not None:
            species_data = self.ka30_df[self.ka30_df['Kalaliik'] != 'Kala kokku']
            if not species_data.empty:
                pivot_data = species_data.pivot_table(values='value', index='Aasta', columns='Kalaliik', aggfunc='sum', fill_value=0)
                
                # Plot top 5 species by total catch
                species_totals = pivot_data.sum().sort_values(ascending=False).head(5)
                top_species = species_totals.index
                
                for species in top_species:
                    axes[1, 1].plot(pivot_data.index, pivot_data[species], marker='o', label=species)
                
                axes[1, 1].set_title('Top 5 Species Over Time')
                axes[1, 1].set_xlabel('Year')
                axes[1, 1].set_ylabel('Catch')
                axes[1, 1].legend()
                axes[1, 1].tick_params(axis='x', rotation=45)
        
        # 6. Water body comparison
        if self.ka30_df is not None:
            water_yearly = self.ka30_df.pivot_table(values='value', index='Aasta', columns='Veekogu', aggfunc='sum', fill_value=0)
            
            for water_body in water_yearly.columns:
                axes[1, 2].plot(water_yearly.index, water_yearly[water_body], marker='s', label=water_body)
            
            axes[1, 2].set_title('Water Bodies Over Time')
            axes[1, 2].set_xlabel('Year')
            axes[1, 2].set_ylabel('Catch')
            axes[1, 2].legend()
            axes[1, 2].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def generate_probability_report(self) -> str:
        """
        Generate a comprehensive probability report
        
        Returns:
            String containing the probability report
        """
        if not self.probabilities:
            return "No probabilities calculated. Run calculation methods first."
        
        report = []
        report.append("=" * 80)
        report.append("FISH PROBABILITY ANALYSIS REPORT")
        report.append("=" * 80)
        
        # Species probabilities
        if 'species' in self.probabilities:
            report.append("\n1. FISH SPECIES PROBABILITIES")
            report.append("-" * 40)
            species_probs = self.probabilities['species']['probabilities']
            sorted_species = sorted(species_probs.items(), key=lambda x: x[1], reverse=True)
            
            for species, prob in sorted_species:
                report.append(f"   {species}: {prob:.4f} ({prob*100:.2f}%)")
        
        # Yearly probabilities
        if 'yearly' in self.probabilities:
            report.append("\n2. YEARLY PROBABILITIES")
            report.append("-" * 40)
            yearly_probs = self.probabilities['yearly']['probabilities']
            
            for year in sorted(yearly_probs.keys()):
                prob = yearly_probs[year]
                report.append(f"   {year}: {prob:.4f} ({prob*100:.2f}%)")
        
        # Water body probabilities
        if 'water_bodies' in self.probabilities:
            report.append("\n3. WATER BODY PROBABILITIES")
            report.append("-" * 40)
            water_probs = self.probabilities['water_bodies']['probabilities']
            sorted_water = sorted(water_probs.items(), key=lambda x: x[1], reverse=True)
            
            for water_body, prob in sorted_water:
                report.append(f"   {water_body}: {prob:.4f} ({prob*100:.2f}%)")
        
        # Trends
        if 'trends' in self.probabilities:
            report.append("\n4. TREND ANALYSIS")
            report.append("-" * 40)
            trend_data = self.probabilities['trends']
            if trend_data:
                report.append(f"   Overall trend: {trend_data['direction']}")
                report.append(f"   Trend magnitude: {trend_data['magnitude']:.2%}")
        
        return "\n".join(report)
    
    def run_complete_analysis(self):
        """
        Run all probability calculations and visualizations
        """
        print("=== STARTING COMPLETE FISH PROBABILITY ANALYSIS ===")
        
        # Load data
        if not self.load_fish_data():
            print("Failed to load data. Aborting analysis.")
            return
        
        # Analyze data structure
        self.analyze_data_structure()
        
        # Calculate all probabilities
        self.calculate_fish_species_probabilities()
        self.calculate_yearly_probabilities()
        self.calculate_water_body_probabilities()
        self.calculate_conditional_probabilities()
        self.calculate_trend_probabilities()
        
        # Generate report
        report = self.generate_probability_report()
        print(report)
        
        # Create visualizations
        self.visualize_probabilities()
        
        print("\n=== ANALYSIS COMPLETE ===")
        return self.probabilities
