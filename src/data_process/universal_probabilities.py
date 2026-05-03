"""
Universal Probability Analysis Module

This module calculates probabilities for different types of datasets:
- Fish data (KA10.csv, KA30.csv)
- Emergency medical data (KE32.csv)
- Other datasets with similar structures
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings

class UniversalProbabilityAnalysis:
    """
    Universal class for calculating probabilities from different dataset types
    """
    
    def __init__(self, data_dir: str = "output"):
        """
        Initialize the universal probability analysis
        
        Args:
            data_dir: Directory containing CSV files
        """
        self.data_dir = Path(data_dir)
        self.datasets = {}
        self.probabilities = {}
        
        # Column name patterns for different data types
        self.value_columns = ['value', 'values', 'Value', 'Values']
        self.year_columns = ['aasta', 'aastad', 'Aasta', 'Aastad', 'year', 'Year']
        self.category_columns = ['Kalaliik', 'Haigla liik', 'Saabumisviis', 'Näitaja', 'Liik', 'Maakond', 'Põllumajanduslik üksus']
        self.location_columns = ['Veekogu', 'Maakond', 'Elukoht']
        
    def load_datasets(self, dataset_names: List[str] = None) -> bool:
        """
        Load specified datasets or all available datasets
        
        Args:
            dataset_names: List of dataset names to load, or None for all
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Find all CSV files
            csv_files = list(self.data_dir.glob("*.csv"))
            
            if dataset_names is None:
                # Load all datasets
                for csv_file in csv_files:
                    dataset_name = csv_file.stem
                    try:
                        df = pd.read_csv(csv_file, encoding='utf-8')
                        self.datasets[dataset_name] = df
                        print(f"Loaded {dataset_name}: {df.shape[0]} rows, {df.shape[1]} columns")
                    except Exception as e:
                        print(f"Error loading {dataset_name}: {e}")
                        continue
            else:
                # Load specific datasets
                for dataset_name in dataset_names:
                    csv_file = self.data_dir / f"{dataset_name}.csv"
                    if csv_file.exists():
                        try:
                            df = pd.read_csv(csv_file, encoding='utf-8')
                            self.datasets[dataset_name] = df
                            print(f"Loaded {dataset_name}: {df.shape[0]} rows, {df.shape[1]} columns")
                        except Exception as e:
                            print(f"Error loading {dataset_name}: {e}")
                            return False
                    else:
                        print(f"Dataset {dataset_name}.csv not found")
                        return False
            
            return True
            
        except Exception as e:
            print(f"Error loading datasets: {e}")
            return False
    
    def analyze_dataset_structure(self, dataset_name: str) -> Dict:
        """
        Analyze structure of a specific dataset
        
        Args:
            dataset_name: Name of dataset to analyze
            
        Returns:
            Dictionary with dataset analysis
        """
        if dataset_name not in self.datasets:
            print(f"Dataset {dataset_name} not loaded.")
            return {}
        
        df = self.datasets[dataset_name]
        
        analysis = {
            'shape': df.shape,
            'columns': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'null_counts': df.isnull().sum().to_dict(),
            'sample_data': df.head(3).to_dict('records') if not df.empty else []
        }
        
        # Identify column types
        value_cols = df.columns[df.columns.isin(self.value_columns)].tolist()
        year_cols = df.columns[df.columns.isin(self.year_columns)].tolist()
        category_cols = df.columns[df.columns.isin(self.category_columns)].tolist()
        location_cols = df.columns[df.columns.isin(self.location_columns)].tolist()
        
        analysis.update({
            'value_columns': value_cols,
            'year_columns': year_cols,
            'category_columns': category_cols,
            'location_columns': location_cols,
            'dataset_type': self._identify_dataset_type(df)
        })
        
        return analysis
    
    def _identify_dataset_type(self, df: pd.DataFrame) -> str:
        """
        Identify the type of dataset based on column structure
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            String identifying dataset type
        """
        columns = set(df.columns)
        
        if 'Kalaliik' in columns and 'Veekogu' in columns:
            return 'fish_water_body'
        elif 'Kalaliik' in columns and 'Aasta' in columns:
            return 'fish_overall'
        elif any('Diagnoos' in col for col in columns) and 'Aasta' in columns and 'Kliiniline seisund' in columns:
            return 'mental_health'
        elif 'Näitaja' in columns and 'Liik' in columns and 'Maakond' in columns:
            return 'agricultural'
        elif 'Abielu tüüp' in columns and 'Abiellumiskuu' in columns:
            return 'marriage_statistics'
        elif 'Sugu' in columns and 'Vanuserühm' in columns and 'Abielu tüüp' in columns:
            return 'demographics'
        elif 'Näitaja' in columns and 'Kuu' in columns and 'Aasta' in columns:
            return 'traffic_safety'
        elif any('Välispõhjus' in col for col in columns) and 'Elukoht' in columns and 'Vanuserühm' in columns:
            return 'injury_causes'
        elif 'value' in columns and any(col in columns for col in ['Aasta', 'year']):
            return 'general_time_series'
        else:
            return 'unknown'
    
    def calculate_fish_probabilities(self) -> Dict:
        """
        Calculate probabilities for fish datasets (KA10, KA30)
        
        Returns:
            Dictionary with fish probability calculations
        """
        fish_datasets = {name: df for name, df in self.datasets.items() 
                      if self._identify_dataset_type(df) in ['fish_overall', 'fish_water_body']}
        
        if not fish_datasets:
            print("No fish datasets found.")
            return {}
        
        # Process KA10 (overall statistics)
        if 'KA10' in fish_datasets:
            ka10_df = fish_datasets['KA10']
            yearly_totals = ka10_df.groupby('Aasta')['value'].sum()
            total_catch = yearly_totals.sum()
            yearly_probabilities = (yearly_totals / total_catch).to_dict()
            
            # Species analysis (excluding "Kala kokku")
            species_data = ka10_df[ka10_df['Kalaliik'] != 'Kala kokku']
            if not species_data.empty:
                species_totals = species_data.groupby('Kalaliik')['value'].sum()
                species_probabilities = (species_totals / species_totals.sum()).to_dict()
            
            self.probabilities['fish'] = {
                'overall': {
                    'yearly_probabilities': yearly_probabilities,
                    'yearly_totals': yearly_totals.to_dict(),
                    'total_catch': total_catch,
                    'species_probabilities': species_probabilities if not species_data.empty else {}
                }
            }
        
        # Process KA30 (water body specific)
        if 'KA30' in fish_datasets:
            ka30_df = fish_datasets['KA30']
            
            # Filter out "Kala kokku" to get individual species
            species_data = ka30_df[ka30_df['Kalaliik'] != 'Kala kokku']
            if not species_data.empty:
                species_totals = species_data.groupby('Kalaliik')['value'].sum()
                total_species_catch = species_totals.sum()
                species_probabilities = (species_totals / total_species_catch).to_dict()
            
            # Water body analysis
            water_body_totals = ka30_df.groupby('Veekogu')['value'].sum()
            total_water_catch = water_body_totals.sum()
            water_body_probabilities = (water_body_totals / total_water_catch).to_dict()
            
            # Conditional probabilities P(Species | Water Body)
            conditional_probs = {}
            for water_body in species_data['Veekogu'].unique():
                water_body_data = species_data[species_data['Veekogu'] == water_body]
                water_body_total = water_body_data['value'].sum()
                
                if water_body_total > 0:
                    species_given_water = {}
                    for species in water_body_data['Kalaliik'].unique():
                        species_total = water_body_data[water_body_data['Kalaliik'] == species]['value'].sum()
                        species_given_water[species] = species_total / water_body_total
                    
                    conditional_probs[water_body] = species_given_water
            
            self.probabilities['fish'].update({
                'water_body': {
                    'species_probabilities': species_probabilities if not species_data.empty else {},
                    'water_body_probabilities': water_body_probabilities,
                    'total_catch': total_water_catch,
                    'conditional_probabilities': conditional_probs
                }
            })
        
        return self.probabilities.get('fish', {})
    
    def calculate_emergency_probabilities(self) -> Dict:
        """
        Calculate probabilities for emergency medical data (KE32)
        
        Returns:
            Dictionary with emergency probability calculations
        """
        if 'KE32' not in self.datasets:
            print("KE32 dataset not found.")
            return {}
        
        ke32_df = self.datasets['KE32']
        
        # Yearly analysis
        yearly_totals = ke32_df.groupby('Aasta')['value'].sum()
        total_emergency = yearly_totals.sum()
        yearly_probabilities = (yearly_totals / total_emergency).to_dict()
        
        # Arrival method analysis
        arrival_method_totals = ke32_df.groupby('Saabumisviis')['value'].sum()
        arrival_method_probabilities = (arrival_method_totals / total_emergency).to_dict()
        
        # Hospital department analysis
        hospital_totals = ke32_df.groupby('Vastuvõtt')['value'].sum()
        hospital_probabilities = (hospital_totals / total_emergency).to_dict()
        
        # Age group analysis
        age_group_totals = ke32_df.groupby('Vanuserühm')['value'].sum()
        age_group_probabilities = (age_group_totals / total_emergency).to_dict()
        
        # Clinical condition analysis
        condition_totals = ke32_df.groupby('Haigla liik')['value'].sum()
        condition_probabilities = (condition_totals / total_emergency).to_dict()
        
        self.probabilities['emergency'] = {
            'yearly_probabilities': yearly_probabilities,
            'yearly_totals': yearly_totals.to_dict(),
            'total_emergency': total_emergency,
            'arrival_method_probabilities': arrival_method_probabilities,
            'arrival_method_totals': arrival_method_totals.to_dict(),
            'hospital_probabilities': hospital_probabilities,
            'hospital_totals': hospital_totals.to_dict(),
            'age_group_probabilities': age_group_probabilities,
            'age_group_totals': age_group_totals.to_dict(),
            'condition_probabilities': condition_probabilities,
            'condition_totals': condition_totals.to_dict()
        }
        
        return self.probabilities['emergency']
    
    def calculate_mental_health_probabilities(self) -> Dict:
        """
        Calculate probabilities for mental health data (PKH7)
        
        Returns:
            Dictionary with mental health probability calculations
        """
        if 'PKH7' not in self.datasets:
            print("PKH7 dataset not found.")
            return {}
        
        pkh7_df = self.datasets['PKH7']
        
        # Yearly analysis
        yearly_totals = pkh7_df.groupby('Aasta')['value'].sum()
        total_mental_health = yearly_totals.sum()
        yearly_probabilities = (yearly_totals / total_mental_health).to_dict()
        
        # Diagnosis analysis
        diagnosis_column = [col for col in pkh7_df.columns if 'Diagnoos' in col][0]
        diagnosis_totals = pkh7_df.groupby(diagnosis_column)['value'].sum()
        diagnosis_probabilities = (diagnosis_totals / total_mental_health).to_dict()
        
        # Clinical status analysis
        status_totals = pkh7_df.groupby('Kliiniline seisund')['value'].sum()
        status_probabilities = (status_totals / total_mental_health).to_dict()
        
        self.probabilities['mental_health'] = {
            'yearly_probabilities': yearly_probabilities,
            'yearly_totals': yearly_totals.to_dict(),
            'total_mental_health': total_mental_health,
            'diagnosis_probabilities': diagnosis_probabilities,
            'diagnosis_totals': diagnosis_totals.to_dict(),
            'status_probabilities': status_probabilities,
            'status_totals': status_totals.to_dict()
        }
        
        return self.probabilities['mental_health']
    
    def calculate_agricultural_probabilities(self) -> Dict:
        """
        Calculate probabilities for agricultural data (PM09)
        
        Returns:
            Dictionary with agricultural probability calculations
        """
        if 'PM09' not in self.datasets:
            print("PM09 dataset not found.")
            return {}
        
        pm09_df = self.datasets['PM09']
        
        # Yearly analysis (if available)
        yearly_probabilities = {}
        yearly_totals = {}
        
        if 'Aasta' in pm09_df.columns:
            yearly_totals = pm09_df.groupby('Aasta')['value'].sum()
            total_agricultural = yearly_totals.sum()
            yearly_probabilities = (yearly_totals / total_agricultural).to_dict()
        else:
            # If no year column, calculate total directly
            total_agricultural = pm09_df['value'].sum()
        
        # Animal type analysis
        animal_type_totals = pm09_df.groupby('Liik')['value'].sum()
        animal_type_probabilities = (animal_type_totals / total_agricultural).to_dict()
        
        # Location analysis
        location_totals = pm09_df.groupby('Maakond')['value'].sum()
        location_probabilities = (location_totals / total_agricultural).to_dict()
        
        # Agricultural unit analysis
        agri_unit_totals = pm09_df.groupby('Põllumajanduslik üksus')['value'].sum()
        agri_unit_probabilities = (agri_unit_totals / total_agricultural).to_dict()
        
        # Observation period analysis
        period_totals = pm09_df.groupby('Vaatlusperiood')['value'].sum()
        period_probabilities = (period_totals / total_agricultural).to_dict()
        
        self.probabilities['agricultural'] = {
            'yearly_probabilities': yearly_probabilities,
            'yearly_totals': yearly_totals,
            'total_agricultural': total_agricultural,
            'animal_type_probabilities': animal_type_probabilities,
            'animal_type_totals': animal_type_totals.to_dict(),
            'location_probabilities': location_probabilities,
            'location_totals': location_totals.to_dict(),
            'agri_unit_probabilities': agri_unit_probabilities,
            'agri_unit_totals': agri_unit_totals.to_dict(),
            'period_probabilities': period_probabilities,
            'period_totals': period_totals.to_dict()
        }
        
        return self.probabilities['agricultural']
    
    def calculate_marriage_statistics_probabilities(self) -> Dict:
        """
        Calculate probabilities for marriage statistics (RV262)
        
        Returns:
            Dictionary with marriage statistics probability calculations
        """
        if 'RV262' not in self.datasets:
            print("RV262 dataset not found.")
            return {}
        
        rv262_df = self.datasets['RV262']
        
        # Yearly analysis
        yearly_totals = rv262_df.groupby('Aasta')['value'].sum()
        total_marriages = yearly_totals.sum()
        yearly_probabilities = (yearly_totals / total_marriages).to_dict()
        
        # Marriage type analysis
        marriage_type_totals = rv262_df.groupby('Abielu tüüp')['value'].sum()
        marriage_type_probabilities = (marriage_type_totals / total_marriages).to_dict()
        
        # Marriage month analysis
        month_totals = rv262_df.groupby('Abiellumiskuu')['value'].sum()
        month_probabilities = (month_totals / total_marriages).to_dict()
        
        self.probabilities['marriage_statistics'] = {
            'yearly_probabilities': yearly_probabilities,
            'yearly_totals': yearly_totals.to_dict(),
            'total_marriages': total_marriages,
            'marriage_type_probabilities': marriage_type_probabilities,
            'marriage_type_totals': marriage_type_totals.to_dict(),
            'month_probabilities': month_probabilities,
            'month_totals': month_totals.to_dict()
        }
        
        return self.probabilities['marriage_statistics']
    
    def calculate_demographics_probabilities(self) -> Dict:
        """
        Calculate probabilities for demographics (RV271)
        
        Returns:
            Dictionary with demographics probability calculations
        """
        if 'RV271' not in self.datasets:
            print("RV271 dataset not found.")
            return {}
        
        rv271_df = self.datasets['RV271']
        
        # Yearly analysis
        yearly_totals = rv271_df.groupby('Aasta')['value'].sum()
        total_demographics = yearly_totals.sum()
        yearly_probabilities = (yearly_totals / total_demographics).to_dict()
        
        # Gender analysis
        gender_totals = rv271_df.groupby('Sugu')['value'].sum()
        gender_probabilities = (gender_totals / total_demographics).to_dict()
        
        # Marriage type analysis
        marriage_type_totals = rv271_df.groupby('Abielu tüüp')['value'].sum()
        marriage_type_probabilities = (marriage_type_totals / total_demographics).to_dict()
        
        # Age group analysis
        age_group_totals = rv271_df.groupby('Vanuserühm')['value'].sum()
        age_group_probabilities = (age_group_totals / total_demographics).to_dict()
        
        self.probabilities['demographics'] = {
            'yearly_probabilities': yearly_probabilities,
            'yearly_totals': yearly_totals.to_dict(),
            'total_demographics': total_demographics,
            'gender_probabilities': gender_probabilities,
            'gender_totals': gender_totals.to_dict(),
            'marriage_type_probabilities': marriage_type_probabilities,
            'marriage_type_totals': marriage_type_totals.to_dict(),
            'age_group_probabilities': age_group_probabilities,
            'age_group_totals': age_group_totals.to_dict()
        }
        
        return self.probabilities['demographics']
    
    def calculate_traffic_safety_probabilities(self) -> Dict:
        """
        Calculate probabilities for traffic safety (TS093)
        
        Returns:
            Dictionary with traffic safety probability calculations
        """
        if 'TS093' not in self.datasets:
            print("TS093 dataset not found.")
            return {}
        
        ts093_df = self.datasets['TS093']
        
        # Yearly analysis
        yearly_totals = ts093_df.groupby('Aasta')['value'].sum()
        total_traffic = yearly_totals.sum()
        yearly_probabilities = (yearly_totals / total_traffic).to_dict()
        
        # Indicator analysis
        indicator_totals = ts093_df.groupby('Näitaja')['value'].sum()
        indicator_probabilities = (indicator_totals / total_traffic).to_dict()
        
        # Month analysis
        month_totals = ts093_df.groupby('Kuu')['value'].sum()
        month_probabilities = (month_totals / total_traffic).to_dict()
        
        self.probabilities['traffic_safety'] = {
            'yearly_probabilities': yearly_probabilities,
            'yearly_totals': yearly_totals.to_dict(),
            'total_traffic': total_traffic,
            'indicator_probabilities': indicator_probabilities,
            'indicator_totals': indicator_totals.to_dict(),
            'month_probabilities': month_probabilities,
            'month_totals': month_totals.to_dict()
        }
        
        return self.probabilities['traffic_safety']
    
    def calculate_injury_causes_probabilities(self) -> Dict:
        """
        Calculate probabilities for injury causes (VIG10)
        
        Returns:
            Dictionary with injury causes probability calculations
        """
        if 'VIG10' not in self.datasets:
            print("VIG10 dataset not found.")
            return {}
        
        vig10_df = self.datasets['VIG10']
        
        # Yearly analysis
        yearly_totals = vig10_df.groupby('Aasta')['value'].sum()
        total_injuries = yearly_totals.sum()
        yearly_probabilities = (yearly_totals / total_injuries).to_dict()
        
        # Location analysis
        location_totals = vig10_df.groupby('Elukoht')['value'].sum()
        location_probabilities = (location_totals / total_injuries).to_dict()
        
        # Gender analysis
        gender_totals = vig10_df.groupby('Sugu')['value'].sum()
        gender_probabilities = (gender_totals / total_injuries).to_dict()
        
        # External cause analysis
        cause_column = [col for col in vig10_df.columns if 'Välispõhjus' in col][0]
        cause_totals = vig10_df.groupby(cause_column)['value'].sum()
        cause_probabilities = (cause_totals / total_injuries).to_dict()
        
        # Age group analysis
        age_group_totals = vig10_df.groupby('Vanuserühm')['value'].sum()
        age_group_probabilities = (age_group_totals / total_injuries).to_dict()
        
        self.probabilities['injury_causes'] = {
            'yearly_probabilities': yearly_probabilities,
            'yearly_totals': yearly_totals.to_dict(),
            'total_injuries': total_injuries,
            'location_probabilities': location_probabilities,
            'location_totals': location_totals.to_dict(),
            'gender_probabilities': gender_probabilities,
            'gender_totals': gender_totals.to_dict(),
            'cause_probabilities': cause_probabilities,
            'cause_totals': cause_totals.to_dict(),
            'age_group_probabilities': age_group_probabilities,
            'age_group_totals': age_group_totals.to_dict()
        }
        
        return self.probabilities['injury_causes']
    
    def calculate_general_probabilities(self) -> Dict:
        """
        Calculate probabilities for general time series datasets
        
        Returns:
            Dictionary with general probability calculations
        """
        general_datasets = {name: df for name, df in self.datasets.items() 
                         if self._identify_dataset_type(df) == 'general_time_series'}
        
        if not general_datasets:
            print("No general time series datasets found.")
            return {}
        
        results = {}
        
        for dataset_name, df in general_datasets.items():
            # Yearly analysis
            if any(col in df.columns for col in self.year_columns):
                yearly_totals = df.groupby(df.columns[df.columns.isin(self.year_columns)][0])['value'].sum()
                total = yearly_totals.sum()
                yearly_probabilities = (yearly_totals / total).to_dict()
                
                results[dataset_name] = {
                    'yearly_probabilities': yearly_probabilities,
                    'yearly_totals': yearly_totals.to_dict(),
                    'total': total
                }
        
        self.probabilities['general'] = results
        return self.probabilities
    
    def visualize_probabilities(self, dataset_type: str = None):
        """
        Create visualizations for probability calculations
        
        Args:
            dataset_type: Type of dataset to visualize ('fish', 'emergency', 'general', or None for all)
        """
        if not self.probabilities:
            print("No probabilities calculated. Run calculation methods first.")
            return
        
        # Create subplots based on dataset type
        if dataset_type == 'fish' or dataset_type is None and 'fish' in self.probabilities:
            self._visualize_fish_probabilities()
        elif dataset_type == 'emergency' or dataset_type is None and 'emergency' in self.probabilities:
            self._visualize_emergency_probabilities()
        elif dataset_type == 'mental_health' or dataset_type is None and 'mental_health' in self.probabilities:
            self._visualize_mental_health_probabilities()
        elif dataset_type == 'agricultural' or dataset_type is None and 'agricultural' in self.probabilities:
            self._visualize_agricultural_probabilities()
        elif dataset_type == 'marriage_statistics' or dataset_type is None and 'marriage_statistics' in self.probabilities:
            self._visualize_marriage_statistics_probabilities()
        elif dataset_type == 'demographics' or dataset_type is None and 'demographics' in self.probabilities:
            self._visualize_demographics_probabilities()
        elif dataset_type == 'traffic_safety' or dataset_type is None and 'traffic_safety' in self.probabilities:
            self._visualize_traffic_safety_probabilities()
        elif dataset_type == 'injury_causes' or dataset_type is None and 'injury_causes' in self.probabilities:
            self._visualize_injury_causes_probabilities()
        elif dataset_type == 'general' or dataset_type is None and 'general' in self.probabilities:
            self._visualize_general_probabilities()
        else:
            print(f"Unknown dataset type: {dataset_type}")
    
    def _visualize_mental_health_probabilities(self):
        """
        Visualize mental health probability calculations
        """
        mental_health_probs = self.probabilities['mental_health']
        
        if not mental_health_probs:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Mental Health Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities
        yearly_probs = mental_health_probs['yearly_probabilities']
        if yearly_probs:
            years = sorted(yearly_probs.keys())
            probs = [yearly_probs[year] for year in years]
            
            axes[0, 0].plot(years, probs, marker='o', linewidth=2)
            axes[0, 0].set_title('Yearly Mental Health Probabilities')
            axes[0, 0].set_xlabel('Year')
            axes[0, 0].set_ylabel('Probability')
            axes[0, 0].tick_params(axis='x', rotation=45)
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Diagnosis probabilities
        diagnosis_probs = mental_health_probs['diagnosis_probabilities']
        if diagnosis_probs:
            diagnosis_df = pd.DataFrame(list(diagnosis_probs.items()), columns=['Diagnosis', 'Probability'])
            diagnosis_df = diagnosis_df.sort_values('Probability', ascending=True)
            
            axes[0, 1].barh(diagnosis_df['Diagnosis'], diagnosis_df['Probability'])
            axes[0, 1].set_title('Diagnosis Probabilities')
            axes[0, 1].set_xlabel('Probability')
        
        # 3. Clinical status probabilities
        status_probs = mental_health_probs['status_probabilities']
        if status_probs:
            status_df = pd.DataFrame(list(status_probs.items()), columns=['Clinical Status', 'Probability'])
            status_df = status_df.sort_values('Probability', ascending=True)
            
            axes[1, 0].barh(status_df['Clinical Status'], status_df['Probability'])
            axes[1, 0].set_title('Clinical Status Probabilities')
            axes[1, 0].set_xlabel('Probability')
        
        # 4. Yearly totals
        yearly_totals = mental_health_probs['yearly_totals']
        years = sorted(yearly_totals.keys())
        totals = [yearly_totals[year] for year in years]
        
        axes[1, 0].plot(years, totals, marker='s', color='purple')
        axes[1, 0].set_title('Yearly Mental Health Totals')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Total Cases')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_agricultural_probabilities(self):
        """
        Visualize agricultural probability calculations
        """
        agricultural_probs = self.probabilities['agricultural']
        
        if not agricultural_probs:
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Agricultural Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities
        yearly_probs = agricultural_probs['yearly_probabilities']
        if yearly_probs:
            years = sorted(yearly_probs.keys())
            probs = [yearly_probs[year] for year in years]
            
            axes[0, 0].plot(years, probs, marker='o', linewidth=2)
            axes[0, 0].set_title('Yearly Agricultural Probabilities')
            axes[0, 0].set_xlabel('Year')
            axes[0, 0].set_ylabel('Probability')
            axes[0, 0].tick_params(axis='x', rotation=45)
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Animal type probabilities
        animal_type_probs = agricultural_probs['animal_type_probabilities']
        if animal_type_probs:
            animal_df = pd.DataFrame(list(animal_type_probs.items()), columns=['Animal Type', 'Probability'])
            animal_df = animal_df.sort_values('Probability', ascending=True)
            
            axes[0, 1].barh(animal_df['Animal Type'], animal_df['Probability'])
            axes[0, 1].set_title('Animal Type Probabilities')
            axes[0, 1].set_xlabel('Probability')
        
        # 3. Location probabilities
        location_probs = agricultural_probs['location_probabilities']
        if location_probs:
            location_df = pd.DataFrame(list(location_probs.items()), columns=['Location', 'Probability'])
            location_df = location_df.sort_values('Probability', ascending=True)
            
            axes[0, 2].barh(location_df['Location'], location_df['Probability'])
            axes[0, 2].set_title('Location Probabilities')
            axes[0, 2].set_xlabel('Probability')
        
        # 4. Yearly totals
        yearly_totals = agricultural_probs['yearly_totals']
        years = sorted(yearly_totals.keys())
        totals = [yearly_totals[year] for year in years]
        
        axes[1, 0].plot(years, totals, marker='s', color='green')
        axes[1, 0].set_title('Yearly Agricultural Totals')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Total Units')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Observation period probabilities
        period_probs = agricultural_probs['period_probabilities']
        if period_probs:
            period_df = pd.DataFrame(list(period_probs.items()), columns=['Observation Period', 'Probability'])
            period_df = period_df.sort_values('Probability', ascending=True)
            
            axes[1, 1].barh(period_df['Observation Period'], period_df['Probability'])
            axes[1, 1].set_title('Observation Period Probabilities')
            axes[1, 1].set_xlabel('Probability')
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_marriage_statistics_probabilities(self):
        """
        Visualize marriage statistics probability calculations
        """
        marriage_probs = self.probabilities['marriage_statistics']
        
        if not marriage_probs:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Marriage Statistics Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities
        yearly_probs = marriage_probs['yearly_probabilities']
        years = sorted(yearly_probs.keys())
        probs = [yearly_probs[year] for year in years]
        
        axes[0, 0].plot(years, probs, marker='o', linewidth=2)
        axes[0, 0].set_title('Yearly Marriage Probabilities')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Probability')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Marriage type probabilities
        marriage_type_probs = marriage_probs['marriage_type_probabilities']
        marriage_type_df = pd.DataFrame(list(marriage_type_probs.items()), columns=['Marriage Type', 'Probability'])
        marriage_type_df = marriage_type_df.sort_values('Probability', ascending=True)
        
        axes[0, 1].barh(marriage_type_df['Marriage Type'], marriage_type_df['Probability'])
        axes[0, 1].set_title('Marriage Type Probabilities')
        axes[0, 1].set_xlabel('Probability')
        
        # 3. Month probabilities
        month_probs = marriage_probs['month_probabilities']
        month_df = pd.DataFrame(list(month_probs.items()), columns=['Month', 'Probability'])
        month_df = month_df.sort_values('Probability', ascending=True)
        
        axes[1, 0].barh(month_df['Month'], month_df['Probability'])
        axes[1, 0].set_title('Marriage Month Probabilities')
        axes[1, 0].set_xlabel('Probability')
        
        # 4. Yearly totals
        yearly_totals = marriage_probs['yearly_totals']
        years = sorted(yearly_totals.keys())
        totals = [yearly_totals[year] for year in years]
        
        axes[1, 1].plot(years, totals, marker='s', color='pink')
        axes[1, 1].set_title('Yearly Marriage Totals')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Total Marriages')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_demographics_probabilities(self):
        """
        Visualize demographics probability calculations
        """
        demographics_probs = self.probabilities['demographics']
        
        if not demographics_probs:
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Demographics Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities
        yearly_probs = demographics_probs['yearly_probabilities']
        years = sorted(yearly_probs.keys())
        probs = [yearly_probs[year] for year in years]
        
        axes[0, 0].plot(years, probs, marker='o', linewidth=2)
        axes[0, 0].set_title('Yearly Demographics Probabilities')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Probability')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Gender probabilities
        gender_probs = demographics_probs['gender_probabilities']
        gender_df = pd.DataFrame(list(gender_probs.items()), columns=['Gender', 'Probability'])
        gender_df = gender_df.sort_values('Probability', ascending=True)
        
        axes[0, 1].barh(gender_df['Gender'], gender_df['Probability'])
        axes[0, 1].set_title('Gender Probabilities')
        axes[0, 1].set_xlabel('Probability')
        
        # 3. Marriage type probabilities
        marriage_type_probs = demographics_probs['marriage_type_probabilities']
        marriage_type_df = pd.DataFrame(list(marriage_type_probs.items()), columns=['Marriage Type', 'Probability'])
        marriage_type_df = marriage_type_df.sort_values('Probability', ascending=True)
        
        axes[0, 2].barh(marriage_type_df['Marriage Type'], marriage_type_df['Probability'])
        axes[0, 2].set_title('Marriage Type Probabilities')
        axes[0, 2].set_xlabel('Probability')
        
        # 4. Age group probabilities
        age_group_probs = demographics_probs['age_group_probabilities']
        age_group_df = pd.DataFrame(list(age_group_probs.items()), columns=['Age Group', 'Probability'])
        age_group_df = age_group_df.sort_values('Probability', ascending=True)
        
        axes[1, 0].barh(age_group_df['Age Group'], age_group_df['Probability'])
        axes[1, 0].set_title('Age Group Probabilities')
        axes[1, 0].set_xlabel('Probability')
        
        # 5. Yearly totals
        yearly_totals = demographics_probs['yearly_totals']
        years = sorted(yearly_totals.keys())
        totals = [yearly_totals[year] for year in years]
        
        axes[1, 1].plot(years, totals, marker='s', color='blue')
        axes[1, 1].set_title('Yearly Demographics Totals')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Total Population')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_traffic_safety_probabilities(self):
        """
        Visualize traffic safety probability calculations
        """
        traffic_probs = self.probabilities['traffic_safety']
        
        if not traffic_probs:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Traffic Safety Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities
        yearly_probs = traffic_probs['yearly_probabilities']
        years = sorted(yearly_probs.keys())
        probs = [yearly_probs[year] for year in years]
        
        axes[0, 0].plot(years, probs, marker='o', linewidth=2)
        axes[0, 0].set_title('Yearly Traffic Safety Probabilities')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Probability')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Indicator probabilities
        indicator_probs = traffic_probs['indicator_probabilities']
        indicator_df = pd.DataFrame(list(indicator_probs.items()), columns=['Indicator', 'Probability'])
        indicator_df = indicator_df.sort_values('Probability', ascending=True)
        
        axes[0, 1].barh(indicator_df['Indicator'], indicator_df['Probability'])
        axes[0, 1].set_title('Traffic Safety Indicator Probabilities')
        axes[0, 1].set_xlabel('Probability')
        
        # 3. Month probabilities
        month_probs = traffic_probs['month_probabilities']
        month_df = pd.DataFrame(list(month_probs.items()), columns=['Month', 'Probability'])
        month_df = month_df.sort_values('Probability', ascending=True)
        
        axes[1, 0].barh(month_df['Month'], month_df['Probability'])
        axes[1, 0].set_title('Traffic Safety Month Probabilities')
        axes[1, 0].set_xlabel('Probability')
        
        # 4. Yearly totals
        yearly_totals = traffic_probs['yearly_totals']
        years = sorted(yearly_totals.keys())
        totals = [yearly_totals[year] for year in years]
        
        axes[1, 1].plot(years, totals, marker='s', color='orange')
        axes[1, 1].set_title('Yearly Traffic Safety Totals')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Total Incidents')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_injury_causes_probabilities(self):
        """
        Visualize injury causes probability calculations
        """
        injury_probs = self.probabilities['injury_causes']
        
        if not injury_probs:
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Injury Causes Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities
        yearly_probs = injury_probs['yearly_probabilities']
        years = sorted(yearly_probs.keys())
        probs = [yearly_probs[year] for year in years]
        
        axes[0, 0].plot(years, probs, marker='o', linewidth=2)
        axes[0, 0].set_title('Yearly Injury Probabilities')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Probability')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Location probabilities
        location_probs = injury_probs['location_probabilities']
        location_df = pd.DataFrame(list(location_probs.items()), columns=['Location', 'Probability'])
        location_df = location_df.sort_values('Probability', ascending=True)
        
        axes[0, 1].barh(location_df['Location'], location_df['Probability'])
        axes[0, 1].set_title('Injury Location Probabilities')
        axes[0, 1].set_xlabel('Probability')
        
        # 3. Gender probabilities
        gender_probs = injury_probs['gender_probabilities']
        gender_df = pd.DataFrame(list(gender_probs.items()), columns=['Gender', 'Probability'])
        gender_df = gender_df.sort_values('Probability', ascending=True)
        
        axes[0, 2].barh(gender_df['Gender'], gender_df['Probability'])
        axes[0, 2].set_title('Injury Gender Probabilities')
        axes[0, 2].set_xlabel('Probability')
        
        # 4. External cause probabilities
        cause_probs = injury_probs['cause_probabilities']
        cause_df = pd.DataFrame(list(cause_probs.items()), columns=['External Cause', 'Probability'])
        cause_df = cause_df.sort_values('Probability', ascending=True)
        
        axes[1, 0].barh(cause_df['External Cause'], cause_df['Probability'])
        axes[1, 0].set_title('External Cause Probabilities')
        axes[1, 0].set_xlabel('Probability')
        
        # 5. Age group probabilities
        age_group_probs = injury_probs['age_group_probabilities']
        age_group_df = pd.DataFrame(list(age_group_probs.items()), columns=['Age Group', 'Probability'])
        age_group_df = age_group_df.sort_values('Probability', ascending=True)
        
        axes[1, 1].barh(age_group_df['Age Group'], age_group_df['Probability'])
        axes[1, 1].set_title('Injury Age Group Probabilities')
        axes[1, 1].set_xlabel('Probability')
        
        # 6. Yearly totals
        yearly_totals = injury_probs['yearly_totals']
        years = sorted(yearly_totals.keys())
        totals = [yearly_totals[year] for year in years]
        
        axes[1, 2].plot(years, totals, marker='s', color='red')
        axes[1, 2].set_title('Yearly Injury Totals')
        axes[1, 2].set_xlabel('Year')
        axes[1, 2].set_ylabel('Total Injuries')
        axes[1, 2].tick_params(axis='x', rotation=45)
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_fish_probabilities(self):
        """
        Visualize fish probability calculations with separate windows for each dataset
        """
        fish_probs = self.probabilities['fish']
        
        if not fish_probs:
            return
        
        # Create separate visualizations for KA10 and KA30
        if 'overall' in fish_probs:
            self._visualize_ka10_probabilities(fish_probs['overall'])
        
        if 'water_body' in fish_probs:
            self._visualize_ka30_probabilities(fish_probs['water_body'])
    
    def _visualize_ka10_probabilities(self, overall_probs):
        """
        Visualize KA10 (overall fish statistics) probabilities
        """
        if not overall_probs:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('KA10 - Overall Fish Statistics Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities
        yearly_probs = overall_probs['yearly_probabilities']
        yearly_totals = overall_probs['yearly_totals']
        
        years = sorted(yearly_probs.keys())
        probs = [yearly_probs[year] for year in years]
        
        axes[0, 0].plot(years, probs, marker='o', linewidth=2, color='blue')
        axes[0, 0].set_title('KA10 - Yearly Catch Probabilities')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Probability')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Species probabilities
        if 'species_probabilities' in overall_probs:
            species_probs = overall_probs['species_probabilities']
            if species_probs:
                species_df = pd.DataFrame(list(species_probs.items()), columns=['Species', 'Probability'])
                species_df = species_df.sort_values('Probability', ascending=True)
                
                axes[0, 1].barh(species_df['Species'], species_df['Probability'], color='green')
                axes[0, 1].set_title('KA10 - Fish Species Probabilities')
                axes[0, 1].set_xlabel('Probability')
        
        # 3. Yearly totals
        axes[1, 0].plot(sorted(yearly_totals.keys()), 
                           [yearly_totals[year] for year in sorted(yearly_totals.keys())], 
                           marker='s', color='red')
        axes[1, 0].set_title('KA10 - Yearly Catch Totals')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Total Catch')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Total catch summary
        total_catch = overall_probs.get('total_catch', 0)
        years_analyzed = len(yearly_probs)
        
        axes[1, 1].text(0.1, 0.8, f'Total Catch: {total_catch:,.0f}', fontsize=12, fontweight='bold')
        axes[1, 1].text(0.1, 0.6, f'Years Analyzed: {years_analyzed}', fontsize=12, fontweight='bold')
        axes[1, 1].text(0.1, 0.4, f'Data Source: KA10.csv', fontsize=12, fontweight='bold')
        axes[1, 1].set_title('KA10 - Summary Statistics')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_ka30_probabilities(self, water_body_probs):
        """
        Visualize KA30 (water body fish statistics) probabilities
        """
        if not water_body_probs:
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('KA30 - Water Body Fish Statistics Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities (if available)
        if 'yearly_probabilities' in water_body_probs:
            yearly_probs = water_body_probs['yearly_probabilities']
            yearly_totals = water_body_probs['yearly_totals']
            
            years = sorted(yearly_probs.keys())
            probs = [yearly_probs[year] for year in years]
            
            axes[0, 0].plot(years, probs, marker='o', linewidth=2, color='blue')
            axes[0, 0].set_title('KA30 - Yearly Catch Probabilities')
            axes[0, 0].set_xlabel('Year')
            axes[0, 0].set_ylabel('Probability')
            axes[0, 0].tick_params(axis='x', rotation=45)
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Species probabilities
        if 'species_probabilities' in water_body_probs:
            species_probs = water_body_probs['species_probabilities']
            if species_probs:
                species_df = pd.DataFrame(list(species_probs.items()), columns=['Species', 'Probability'])
                species_df = species_df.sort_values('Probability', ascending=True)
                
                axes[0, 1].barh(species_df['Species'], species_df['Probability'], color='green')
                axes[0, 1].set_title('KA30 - Fish Species Probabilities')
                axes[0, 1].set_xlabel('Probability')
        
        # 3. Water body probabilities
        if 'water_body_probabilities' in water_body_probs:
            water_probs = water_body_probs['water_body_probabilities']
            if water_probs:
                water_df = pd.DataFrame(list(water_probs.items()), columns=['Water Body', 'Probability'])
                water_df = water_df.sort_values('Probability', ascending=True)
                
                axes[0, 2].barh(water_df['Water Body'], water_df['Probability'], color='orange')
                axes[0, 2].set_title('KA30 - Water Body Probabilities')
                axes[0, 2].set_xlabel('Probability')
        
        # 4. Conditional probabilities (Species | Water Body)
        if 'conditional_probabilities' in water_body_probs:
            cond_probs = water_body_probs['conditional_probabilities']
            if cond_probs:
                # Create heatmap for conditional probabilities
                water_bodies = list(cond_probs.keys())
                species = list(set([s for probs in cond_probs.values() for s in probs.keys()]))
                
                # Create matrix for heatmap
                prob_matrix = []
                for water_body in water_bodies:
                    row = []
                    for sp in species:
                        row.append(cond_probs[water_body].get(sp, 0))
                    prob_matrix.append(row)
                
                im = axes[1, 0].imshow(prob_matrix, cmap='YlOrRd', aspect='auto')
                axes[1, 0].set_xticks(range(len(species)))
                axes[1, 0].set_yticks(range(len(water_bodies)))
                axes[1, 0].set_xticklabels(species, rotation=45)
                axes[1, 0].set_yticklabels(water_bodies)
                axes[1, 0].set_title('KA30 - P(Species | Water Body)')
                axes[1, 0].set_xlabel('Species')
                axes[1, 0].set_ylabel('Water Body')
        
        # 5. Yearly totals
        if 'yearly_totals' in water_body_probs:
            yearly_totals = water_body_probs['yearly_totals']
            years = sorted(yearly_totals.keys())
            totals = [yearly_totals[year] for year in years]
            
            axes[1, 1].plot(years, totals, marker='s', color='red')
            axes[1, 1].set_title('KA30 - Yearly Catch Totals')
            axes[1, 1].set_xlabel('Year')
            axes[1, 1].set_ylabel('Total Catch')
            axes[1, 1].tick_params(axis='x', rotation=45)
            axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Summary statistics
        total_catch = water_body_probs.get('total_catch', 0)
        years_analyzed = len(water_body_probs.get('yearly_probabilities', {}))
        
        axes[1, 2].text(0.1, 0.8, f'Total Catch: {total_catch:,.0f}', fontsize=12, fontweight='bold')
        axes[1, 2].text(0.1, 0.6, f'Years Analyzed: {years_analyzed}', fontsize=12, fontweight='bold')
        axes[1, 2].text(0.1, 0.4, f'Data Source: KA30.csv', fontsize=12, fontweight='bold')
        axes[1, 2].set_title('KA30 - Summary Statistics')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_emergency_probabilities(self):
        """
        Visualize emergency medical probability calculations
        """
        emergency_probs = self.probabilities['emergency']
        
        if not emergency_probs:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Emergency Medical Probability Analysis', fontsize=16, fontweight='bold')
        
        # 1. Yearly probabilities
        yearly_probs = emergency_probs['yearly_probabilities']
        years = sorted(yearly_probs.keys())
        probs = [yearly_probs[year] for year in years]
        
        axes[0, 0].plot(years, probs, marker='o', linewidth=2)
        axes[0, 0].set_title('Yearly Emergency Probabilities')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Probability')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Arrival method probabilities
        arrival_probs = emergency_probs['arrival_method_probabilities']
        if arrival_probs:
            arrival_df = pd.DataFrame(list(arrival_probs.items()), columns=['Arrival Method', 'Probability'])
            arrival_df = arrival_df.sort_values('Probability', ascending=True)
            
            axes[0, 1].barh(arrival_df['Arrival Method'], arrival_df['Probability'])
            axes[0, 1].set_title('Arrival Method Probabilities')
            axes[0, 1].set_xlabel('Probability')
        
        # 3. Hospital probabilities
        hospital_probs = emergency_probs['hospital_probabilities']
        if hospital_probs:
            hospital_df = pd.DataFrame(list(hospital_probs.items()), columns=['Hospital', 'Probability'])
            hospital_df = hospital_df.sort_values('Probability', ascending=True)
            
            axes[1, 0].barh(hospital_df['Hospital'], hospital_df['Probability'])
            axes[1, 0].set_title('Hospital Probabilities')
            axes[1, 0].set_xlabel('Probability')
        
        # 4. Yearly totals
        yearly_totals = emergency_probs['yearly_totals']
        years = sorted(yearly_totals.keys())
        totals = [yearly_totals[year] for year in years]
        
        axes[1, 1].plot(years, totals, marker='s', color='red')
        axes[1, 1].set_title('Yearly Emergency Totals')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Total Cases')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _visualize_general_probabilities(self):
        """
        Visualize general time series probabilities
        """
        general_probs = self.probabilities['general']
        
        if not general_probs:
            return
        
        fig, axes = plt.subplots(len(general_probs), 1, figsize=(15, 5*len(general_probs)))
        fig.suptitle('General Time Series Probability Analysis', fontsize=16, fontweight='bold')
        
        for i, (dataset_name, data) in enumerate(general_probs.items()):
            ax = axes[i] if len(general_probs) > 1 else axes
            
            # Yearly probabilities
            yearly_probs = data['yearly_probabilities']
            years = sorted(yearly_probs.keys())
            probs = [yearly_probs[year] for year in years]
            
            ax.plot(years, probs, marker='o', label=dataset_name)
            ax.set_title(f'{dataset_name} Yearly Probabilities')
            ax.set_xlabel('Year')
            ax.set_ylabel('Probability')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
            ax.legend()
        
        plt.tight_layout()
        plt.show()
    
    def generate_comprehensive_report(self) -> str:
        """
        Generate a comprehensive probability report for all datasets
        """
        if not self.probabilities:
            return "No probabilities calculated. Run calculation methods first."
        
        report = []
        report.append("=" * 80)
        report.append("UNIVERSAL PROBABILITY ANALYSIS REPORT")
        report.append("=" * 80)
        
        # Fish probabilities
        if 'fish' in self.probabilities:
            report.append("\n1. FISH PROBABILITY ANALYSIS")
            report.append("-" * 40)
            
            fish_probs = self.probabilities['fish']
            
            if 'overall' in fish_probs:
                overall = fish_probs['overall']
                report.append(f"Total fish catch: {overall['total_catch']:,.0f}")
                report.append(f"Years analyzed: {len(overall['yearly_probabilities'])}")
                
                # Most likely year
                best_year = max(overall['yearly_probabilities'].items(), key=lambda x: x[1])
                report.append(f"Highest probability year: {best_year[0]} ({best_year[1]:.2%})")
            
            if 'water_body' in fish_probs:
                water_body = fish_probs['water_body']
                report.append(f"Total water body catch: {water_body['total_catch']:,.0f}")
                
                # Best water body
                if water_body['water_body_probabilities']:
                    best_water = max(water_body['water_body_probabilities'].items(), key=lambda x: x[1])
                    report.append(f"Most productive water body: {best_water[0]} ({best_water[1]:.2%})")
        
        # Emergency probabilities
        if 'emergency' in self.probabilities:
            report.append("\n2. EMERGENCY MEDICAL PROBABILITY ANALYSIS")
            report.append("-" * 40)
            
            emergency = self.probabilities['emergency']
            report.append(f"Total emergency cases: {emergency['total_emergency']:,.0f}")
            report.append(f"Years analyzed: {len(emergency['yearly_probabilities'])}")
            
            # Most common arrival method
            if emergency['arrival_method_probabilities']:
                best_arrival = max(emergency['arrival_method_probabilities'].items(), key=lambda x: x[1])
                report.append(f"Most common arrival method: {best_arrival[0]} ({best_arrival[1]:.2%})")
            
            # Most common hospital
            if emergency['hospital_probabilities']:
                best_hospital = max(emergency['hospital_probabilities'].items(), key=lambda x: x[1])
                report.append(f"Most common hospital: {best_hospital[0]} ({best_hospital[1]:.2%})")
        
        # General probabilities
        if 'general' in self.probabilities:
            report.append("\n3. GENERAL TIME SERIES PROBABILITY ANALYSIS")
            report.append("-" * 40)
            
            for dataset_name, data in self.probabilities['general'].items():
                report.append(f"\n{dataset_name}:")
                report.append(f"  Total events: {data['total']:,.0f}")
                report.append(f"  Years analyzed: {len(data['yearly_probabilities'])}")
                
                # Best year
                best_year = max(data['yearly_probabilities'].items(), key=lambda x: x[1])
                report.append(f"  Highest probability year: {best_year[0]} ({best_year[1]:.2%})")
        
        return "\n".join(report)
    
    def run_complete_analysis(self, dataset_names: List[str] = None):
        """
        Run complete probability analysis on specified or all datasets
        
        Args:
            dataset_names: List of dataset names to analyze, or None for all
        """
        print("=== STARTING UNIVERSAL PROBABILITY ANALYSIS ===")
        
        # Load datasets
        if not self.load_datasets(dataset_names):
            print("Failed to load datasets. Aborting analysis.")
            return
        
        # Analyze dataset structures
        print("\n=== DATASET STRUCTURE ANALYSIS ===")
        for dataset_name in self.datasets.keys():
            analysis = self.analyze_dataset_structure(dataset_name)
            dataset_type = analysis['dataset_type']
            print(f"\n{dataset_name} ({dataset_type}):")
            print(f"  Shape: {analysis['shape'][0]} rows × {analysis['shape'][1]} columns")
            print(f"  Columns: {', '.join(analysis['columns'])}")
            print(f"  Value columns: {analysis['value_columns']}")
            print(f"  Year columns: {analysis['year_columns']}")
            print(f"  Category columns: {analysis['category_columns']}")
            print(f"  Location columns: {analysis['location_columns']}")
        
        # Calculate probabilities for each dataset type
        print("\n=== CALCULATING PROBABILITIES ===")
        
        self.calculate_fish_probabilities()
        self.calculate_emergency_probabilities()
        self.calculate_general_probabilities()
        
        # Generate comprehensive report
        report = self.generate_comprehensive_report()
        print(report)
        
        # Create visualizations
        print("\n=== GENERATING VISUALIZATIONS ===")
        self.visualize_probabilities()
        
        print("\n=== ANALYSIS COMPLETE ===")
        return self.probabilities
