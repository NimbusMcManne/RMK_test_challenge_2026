"""
Extract probabilities from multiple Estonian statistical datasets
"""

import pandas as pd
import sys
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(current_dir))

def extract_ka10_ocean_fishing_probabilities():
    """Extract shrimp and sardine probabilities from KA10 ocean fishing dataset"""
    print("Extracting KA10 ocean fishing probabilities...")
    
    ka10_df = pd.read_csv('output/KA10.csv')
    
    # Filter for relevant species
    shrimp_data = ka10_df[ka10_df['Kalaliik'] == 'Krevett']  # Shrimp
    sardine_data = ka10_df[ka10_df['Kalaliik'] == 'Sardiin']  # Sardine
    total_fish_data = ka10_df[ka10_df['Kalaliik'] == 'Kala kokku']  # Total fish
    
    # Calculate total catches over all years
    total_shrimp = shrimp_data['value'].sum()
    total_sardine = sardine_data['value'].sum()
    total_ocean_fish = total_fish_data['value'].sum()
    
    # Calculate shares
    shrimp_share = (total_shrimp / total_ocean_fish)
    sardine_share = (total_sardine / total_ocean_fish)
    
    return {
        'shrimp_share_ocean_fishing': shrimp_share,
        'sardine_share_ocean_fishing': sardine_share
    }

def extract_ka30_lake_fishing_probabilities():
    """Extract perch and pike probabilities from KA30 Lake Peipsi fishing dataset"""
    print("Extracting KA30 Lake Peipsi fishing probabilities...")
    
    ka30_df = pd.read_csv('output/KA30.csv')
    
    # Filter for Lake Peipsi data
    peipsi_data = ka30_df[ka30_df['Veekogu'] == 'Peipsi järv']
    
    # Filter for relevant species
    perch_data = peipsi_data[peipsi_data['Kalaliik'] == 'Ahven']  # Perch
    pike_data = peipsi_data[peipsi_data['Kalaliik'] == 'Haug']    # Pike
    
    # Calculate total catches in Lake Peipsi
    total_peipsi = peipsi_data['value'].sum()
    total_perch = perch_data['value'].sum()
    total_pike = pike_data['value'].sum()
    
    # Calculate probabilities
    perch_probability = (total_perch / total_peipsi)
    pike_probability = (total_pike / total_peipsi)
    
    # Yearly analysis for Lake Peipsi
    peipsi_years = sorted(peipsi_data['Aasta'].unique())
    yearly_perch_probabilities = []
    yearly_pike_probabilities = []
    
    for year in peipsi_years:
        year_perch = perch_data[perch_data['Aasta'] == year]['value'].sum()
        year_pike = pike_data[pike_data['Aasta'] == year]['value'].sum()
        year_total_peipsi = peipsi_data[peipsi_data['Aasta'] == year]['value'].sum()
        
        if year_total_peipsi > 0:
            perch_prob_year = (year_perch / year_total_peipsi)
            pike_prob_year = (year_pike / year_total_peipsi)
            yearly_perch_probabilities.append(perch_prob_year)
            yearly_pike_probabilities.append(pike_prob_year)
    
    # Calculate average yearly probabilities
    avg_perch_prob = sum(yearly_perch_probabilities) / len(yearly_perch_probabilities)
    avg_pike_prob = sum(yearly_pike_probabilities) / len(yearly_pike_probabilities)
    
    return {
        'perch_probability_peipsi': perch_probability,
        'pike_probability_peipsi': pike_probability,
        'avg_perch_probability_peipsi': avg_perch_prob,
        'avg_pike_probability_peipsi': avg_pike_prob,
        'yearly_perch_probabilities': dict(zip(peipsi_years, yearly_perch_probabilities)),
        'yearly_pike_probabilities': dict(zip(peipsi_years, yearly_pike_probabilities))
    }

def extract_pkh7_mental_health_probabilities():
    """Extract cannabinoid and alcohol disorder probabilities from PKH7 dataset"""
    print("Extracting PKH7 mental health probabilities...")
    
    pkh7_df = pd.read_csv('output/PKH7.csv')
    
    # Filter for relevant diagnoses
    cannabinoids_data = pkh7_df[pkh7_df['Diagnoos (RHK-10)'].str.contains('Kannabinoididest', na=False)]
    alcohol_data = pkh7_df[pkh7_df['Diagnoos (RHK-10)'].str.contains('Alkoholist', na=False)]
    psychoactive_data = pkh7_df[pkh7_df['Diagnoos (RHK-10)'].str.contains('Psühhoaktiivsete ainete', na=False)]
    
    # Calculate total cases over all years
    total_cannabinoids = cannabinoids_data['value'].sum()
    total_alcohol = alcohol_data['value'].sum()
    total_psychoactive = psychoactive_data['value'].sum()
    
    # Calculate shares over all years
    cannabinoids_share_overall = (total_cannabinoids / total_psychoactive)
    alcohol_share_overall = (total_alcohol / total_psychoactive)
    
    # Yearly analysis for mental health
    pkh7_years = sorted(pkh7_df['Aasta'].unique())
    yearly_cannabinoids_shares = []
    yearly_alcohol_shares = []
    
    for year in pkh7_years:
        year_cannabinoids = cannabinoids_data[cannabinoids_data['Aasta'] == year]['value'].sum()
        year_alcohol = alcohol_data[alcohol_data['Aasta'] == year]['value'].sum()
        year_psychoactive = psychoactive_data[psychoactive_data['Aasta'] == year]['value'].sum()
        
        if year_psychoactive > 0:
            cannabinoids_share_year = (year_cannabinoids / year_psychoactive)
            alcohol_share_year = (year_alcohol / year_psychoactive)
            yearly_cannabinoids_shares.append(cannabinoids_share_year)
            yearly_alcohol_shares.append(alcohol_share_year)
    
    # Calculate average yearly shares
    avg_cannabinoids_share = sum(yearly_cannabinoids_shares) / len(yearly_cannabinoids_shares)
    avg_alcohol_share = sum(yearly_alcohol_shares) / len(yearly_alcohol_shares)
    
    return {
        'cannabinoids_share_pkh7': cannabinoids_share_overall,
        'alcohol_share_pkh7': alcohol_share_overall,
        'avg_cannabinoids_share_pkh7': avg_cannabinoids_share,
        'avg_alcohol_share_pkh7': avg_alcohol_share,
        'yearly_cannabinoids_shares': dict(zip(pkh7_years, yearly_cannabinoids_shares)),
        'yearly_alcohol_shares': dict(zip(pkh7_years, yearly_alcohol_shares))
    }

def extract_pm09_agricultural_probabilities():
    """Extract animal breeding probabilities from PM09 agricultural dataset"""
    print("Extracting PM09 agricultural probabilities...")
    
    pm09_df = pd.read_csv('output/PM09.csv')
    
    # Filter for Estonia data only
    estonia_data = pm09_df[pm09_df['Maakond'] == 'Eesti']
    
    # Get unique animal types
    animal_types = estonia_data['Liik'].unique()
    
    # Calculate total animals by type
    animal_totals = {}
    for animal_type in animal_types:
        animal_data = estonia_data[estonia_data['Liik'] == animal_type]
        total = animal_data['value'].sum()
        # Filter out animals with 0 values
        if total > 0:
            animal_totals[animal_type] = total
    
    # Calculate total animals (excluding 0-value animals)
    total_animals = sum(animal_totals.values())
    
    # Calculate shares and find the least bred animal
    animal_shares = {}
    for animal_type, total in animal_totals.items():
        share = (total / total_animals) * 100
        animal_shares[animal_type] = share
    
    # Find the animal bred the least and most
    least_bred_animal = min(animal_shares.items(), key=lambda x: x[1])
    most_bred_animal = max(animal_shares.items(), key=lambda x: x[1])
    
    probabilities = {
        'least_bred_animal_share': least_bred_animal[1],
        'least_bred_animal_name': least_bred_animal[0],
        'most_bred_animal_share': most_bred_animal[1]
    }
    
    # Store all animal shares in dictionary
    for animal_type, share in animal_shares.items():
        probabilities[f'{animal_type.lower()}_share'] = share
    
    return probabilities

def extract_rv262_marriage_month_probabilities():
    """Extract marriage month probabilities from RV262 marriage statistics dataset"""
    print("Extracting RV262 marriage month probabilities...")
    
    rv262_df = pd.read_csv('output/RV262.csv')
    
    # Filter for total marriages
    total_marriages_data = rv262_df[rv262_df['Abielu tüüp'] == 'Abielusid kokku']
    
    # Calculate total marriages by month
    monthly_marriages = total_marriages_data.groupby('Abiellumiskuu')['value'].sum()
    total_marriages = monthly_marriages.sum()
    
    # Calculate probabilities for each month
    monthly_probabilities = {}
    for month, marriages in monthly_marriages.items():
        probability = (marriages / total_marriages)
        monthly_probabilities[month] = probability
    
    # Find most and least likely months
    most_likely_month = max(monthly_probabilities.items(), key=lambda x: x[1])
    least_likely_month = min(monthly_probabilities.items(), key=lambda x: x[1])
    
    probabilities = {
        'most_likely_marriage_month_share': most_likely_month[1],
        'most_likely_marriage_month_name': most_likely_month[0],
        'least_likely_marriage_month_share': least_likely_month[1],
        'least_likely_marriage_month_name': least_likely_month[0]
    }
    
    # Store all month probabilities in dictionary
    for month, probability in monthly_probabilities.items():
        probabilities[f'{month.lower()}_marriage_share'] = probability
    
    return probabilities

def extract_rv271_marriage_age_probabilities():
    """Extract marriage age group probabilities from RV271 demographics dataset"""
    print("Extracting RV271 marriage age probabilities...")
    
    rv271_df = pd.read_csv('output/RV271.csv')
    
    # Filter for total marriages
    total_marriages_data = rv271_df[rv271_df['Abielu tüüp'] == 'Abielusid kokku']
    
    # Calculate total marriages by age group (combining both genders)
    age_group_marriages = total_marriages_data.groupby('Vanuserühm')['value'].sum()
    total_marriages_age = age_group_marriages.sum()
    
    # Calculate probabilities for each age group
    age_group_probabilities = {}
    for age_group, marriages in age_group_marriages.items():
        probability = (marriages / total_marriages_age)
        age_group_probabilities[age_group] = probability
    
    # Find most common age group
    most_common_age_group = max(age_group_probabilities.items(), key=lambda x: x[1])
    
    probabilities = {
        'most_common_marriage_age_group_share': most_common_age_group[1],
        'most_common_marriage_age_group_name': most_common_age_group[0]
    }
    
    # Store all age group probabilities in dictionary
    for age_group, probability in age_group_probabilities.items():
        probabilities[f'{age_group.lower().replace(" ", "_").replace("-", "_")}_marriage_share'] = probability
    
    return probabilities

def extract_ts093_traffic_safety_probabilities():
    """Extract traffic accident and drunk driver probabilities from TS093 dataset"""
    print("Extracting TS093 traffic safety probabilities...")
    
    ts093_df = pd.read_csv('output/TS093.csv')
    
    # Filter for relevant indicators
    total_accidents_data = ts093_df[ts093_df['Näitaja'] == 'Liiklusõnnetused']
    drunk_drivers_data = ts093_df[ts093_df['Näitaja'] == 'Liiklusõnnetused joobes mootorsõidukijuhi osalusel']
    
    # Calculate total accidents by month
    monthly_accidents = total_accidents_data.groupby('Kuu')['value'].sum()
    total_accidents = monthly_accidents.sum()
    
    # Find month with most accidents
    most_accident_month = max(monthly_accidents.items(), key=lambda x: x[1])
    most_accident_month_share = (most_accident_month[1] / total_accidents)
    
    # Calculate drunk drivers share
    total_drunk_accidents = drunk_drivers_data['value'].sum()
    drunk_drivers_share = (total_drunk_accidents / total_accidents)
    
    probabilities = {
        'most_accident_month_share': most_accident_month_share,
        'most_accident_month_name': most_accident_month[0],
        'drunk_drivers_share': drunk_drivers_share
    }
    
    # Store all month probabilities in dictionary
    for month, accidents in monthly_accidents.items():
        probability = (accidents / total_accidents)
        probabilities[f'{month.lower()}_accident_share'] = probability
    
    return probabilities

def extract_vig10_injury_causes_probabilities():
    """Extract pedestrian and cyclist injury probabilities from VIG10 dataset"""
    print("Extracting VIG10 injury causes probabilities...")
    
    vig10_df = pd.read_csv('output/VIG10.csv')
    
    # Filter for relevant injury causes
    total_injuries_data = vig10_df[vig10_df['Välispõhjus (RHK-10)'] == 'Vigastuste välispõhjused kokku (V01-Y34 või põhjus teadmata)']
    pedestrian_injuries_data = vig10_df[vig10_df['Välispõhjus (RHK-10)'] == '....Sõidukiõnnetuses vigastatud jalakäija (V01-V09)']
    cyclist_injuries_data = vig10_df[vig10_df['Välispõhjus (RHK-10)'] == '....Sõidukiõnnetuses vigastatud jalgrattur (V10-V19)']
    
    # Calculate total injuries
    total_injuries = total_injuries_data['value'].sum()
    total_pedestrian_injuries = pedestrian_injuries_data['value'].sum()
    total_cyclist_injuries = cyclist_injuries_data['value'].sum()
    
    # Calculate shares
    pedestrian_share = (total_pedestrian_injuries / total_injuries)
    cyclist_share = (total_cyclist_injuries / total_injuries)
    
    return {
        'pedestrian_injuries_share': pedestrian_share,
        'cyclist_injuries_share': cyclist_share,
        'total_pedestrian_injuries': total_pedestrian_injuries,
        'total_cyclist_injuries': total_cyclist_injuries,
        'total_all_injuries': total_injuries
    }

def extract_ke32_emergency_medical_probabilities():
    """Extract ambulance transport probability from KE32 emergency medical dataset"""
    print("Extracting KE32 emergency medical probabilities...")
    
    ke32_df = pd.read_csv('output/KE32.csv')
    
    # Filter for relevant arrival methods
    total_emergency_data = ke32_df[ke32_df['Saabumisviis'] == 'Erakorralisi patsiente kokku']
    ambulance_data = ke32_df[ke32_df['Saabumisviis'] == 'Toodi kiirabiga']
    
    # Calculate total emergency patients
    total_emergency_patients = total_emergency_data['value'].sum()
    total_ambulance_patients = ambulance_data['value'].sum()
    
    # Calculate probability
    ambulance_probability = (total_ambulance_patients / total_emergency_patients)
    
    return {
        'ambulance_transport_probability': ambulance_probability,
        'total_emergency_patients': total_emergency_patients,
        'total_ambulance_patients': total_ambulance_patients
    }

def extract_15_specific_probabilities():
    """
    Extract only the 15 specific probabilities requested
    Returns dictionary with exactly 15 probabilities as decimals (0-1)
    """
    print("Extracting 15 specific probabilities...")
    
    # Initialize results dictionary with short, clean names
    probabilities = {}
    
    # 1-2: KA10 Ocean Fishing Probabilities
    ka10_probs = extract_ka10_ocean_fishing_probabilities()
    probabilities['Ocean Shrimp Catch Probability'] = ka10_probs['shrimp_share_ocean_fishing']
    probabilities['Ocean Sardine Catch Probabilty'] = ka10_probs['sardine_share_ocean_fishing']
    
    # 3-4: KA30 Lake Peipsi Fishing Probabilities
    ka30_probs = extract_ka30_lake_fishing_probabilities()
    probabilities['Perch Probability in Lake Peipsi'] = ka30_probs['perch_probability_peipsi']
    probabilities['Pike Probability in Lake Peipsi'] = ka30_probs['pike_probability_peipsi']
    
    # 5-6: PKH7 Mental Health Probabilities
    pkh7_probs = extract_pkh7_mental_health_probabilities()
    probabilities['Probability of Cannabinoid Disorders'] = pkh7_probs['cannabinoids_share_pkh7'] 
    probabilities['Probability of Alcohol Disorders'] = pkh7_probs['alcohol_share_pkh7']
    
    # 7: PM09 Agricultural Probabilities
    pm09_probs = extract_pm09_agricultural_probabilities()
    least_bred_name = pm09_probs['least_bred_animal_name']
    probabilities[f'Least Bred Animal: {least_bred_name}'] = pm09_probs['least_bred_animal_share'] 
    
    # 8-9: RV262 Marriage Month Probabilities
    rv262_probs = extract_rv262_marriage_month_probabilities()
    most_likely_month = rv262_probs['most_likely_marriage_month_name']
    least_likely_month = rv262_probs['least_likely_marriage_month_name']
    probabilities[f'Most Likely Marriage Month: {most_likely_month}'] = rv262_probs['most_likely_marriage_month_share']
    probabilities[f'Least Likely Marriage Month: {least_likely_month}'] = rv262_probs['least_likely_marriage_month_share'] 
    
    # 10: RV271 Marriage Age Probabilities
    rv271_probs = extract_rv271_marriage_age_probabilities()
    most_common_age_group = rv271_probs['most_common_marriage_age_group_name']
    probabilities[f'Most Common Marriage Age: {most_common_age_group}'] = rv271_probs['most_common_marriage_age_group_share'] 
    
    # 11-12: TS093 Traffic Safety Probabilities
    ts093_probs = extract_ts093_traffic_safety_probabilities()
    peak_accident_month = ts093_probs['most_accident_month_name']
    probabilities['Share of Accidents Caused by Drunk Drivers'] = ts093_probs['drunk_drivers_share'] 
    probabilities[f'Peak Accident Month: {peak_accident_month}'] = ts093_probs['most_accident_month_share']
    
    # 13-14: VIG10 Injury Causes Probabilities
    vig10_probs = extract_vig10_injury_causes_probabilities()
    probabilities['Share of Pedestrian Injuries From All Types of Injuries'] = vig10_probs['pedestrian_injuries_share'] 
    probabilities['Share of Cyclist Injuries From All Types of Injuries'] = vig10_probs['cyclist_injuries_share'] 
    
    # 15: KE32 Emergency Medical Probabilities
    ke32_probs = extract_ke32_emergency_medical_probabilities()
    probabilities['Likelyhood of Ambulance Transporting to Hospital'] = ke32_probs['ambulance_transport_probability']
    
    # Sort probabilities by value (descending)
    sorted_probabilities = dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
    
    print("\n=== 15 Specific Probabilities (Descending) ===")
    for key, value in sorted_probabilities.items():
        print(f"{key}: {value:.4f}")
    
    return probabilities

# def extract_all_probabilities():
#     """
#     Extract probabilities from all datasets
#     Returns comprehensive dictionary of all probabilities
#     """
#     print("Extracting probabilities from all datasets...")
    
#     # Initialize results dictionary
#     probabilities = {}
    
#     # Extract probabilities from all datasets
#     ka10_probs = extract_ka10_ocean_fishing_probabilities()
#     ka30_probs = extract_ka30_lake_fishing_probabilities()
#     pkh7_probs = extract_pkh7_mental_health_probabilities()
#     pm09_probs = extract_pm09_agricultural_probabilities()
#     rv262_probs = extract_rv262_marriage_month_probabilities()
#     rv271_probs = extract_rv271_marriage_age_probabilities()
#     ts093_probs = extract_ts093_traffic_safety_probabilities()
#     vig10_probs = extract_vig10_injury_causes_probabilities()
#     ke32_probs = extract_ke32_emergency_medical_probabilities()
    
#     # Merge all probabilities
#     probabilities.update(ka10_probs)
#     probabilities.update(ka30_probs)
#     probabilities.update(pkh7_probs)
#     probabilities.update(pm09_probs)
#     probabilities.update(rv262_probs)
#     probabilities.update(rv271_probs)
#     probabilities.update(ts093_probs)
#     probabilities.update(vig10_probs)
#     probabilities.update(ke32_probs)
    
#     # Sort only float values in probabilities dictionary by value (descending)
#     float_probabilities = {k: v for k, v in probabilities.items() if isinstance(v, float)}
#     sorted_probabilities = dict(sorted(float_probabilities.items(), key=lambda x: x[1], reverse=True))
    
#     print("\n=== Sorted Probabilities (Descending) ===")
#     for key, value in sorted_probabilities.items():
#         print(f"{key}: {value:.2f}%")
    
#     # Return the full probabilities dictionary (including non-float values)
#     return probabilities

def create_pie_chart(probabilities_dict, figsize=(12, 8)):
    """
    Create a pie chart visualization of all probabilities
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Filter only float values and sort by value (descending)
    float_probabilities = {k: v for k, v in probabilities_dict.items() if isinstance(v, float)}
    sorted_probs = dict(sorted(float_probabilities.items(), key=lambda x: x[1], reverse=True))
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Prepare data for pie chart
    labels = list(sorted_probs.keys())
    sizes = list(sorted_probs.values())
    
    # Create color scheme - use a gradient from red (high) to blue (low)
    colors = plt.cm.RdYlBu_r(np.linspace(0, 1, len(sizes)))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=None, colors=colors, autopct='%1.2f%%',
                                      startangle=90, textprops={'fontsize': 8})
    
    # Customize the chart
    ax.set_title('15 Estonian Statistical Probabilities Distribution', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Create legend with shortened labels for better readability
    legend_labels = []
    for label in labels:
        # Shorten labels for legend
        if len(label) > 30:
            shortened = label[:27] + "..."
        else:
            shortened = label
        legend_labels.append(f"{shortened}: {sorted_probs[label]:.4f}")
    
    ax.legend(wedges, legend_labels, title="Probabilities", loc="center left", 
             bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
    
    # Make the pie chart circular
    ax.axis('equal')
    
    plt.tight_layout()
    return fig, ax

def visualize_probabilities(probabilities_dict, figsize=(16, 10)):
    """
    Visualize all probabilities on a horizontal scale with nonlinear transformation
    More precision at low values (left), less precision at high values (right)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Filter only float values (already in decimal format)
    float_probabilities = {k: v for k, v in probabilities_dict.items() if isinstance(v, float)}
    
    # Sort by probability value (ascending for left-to-right display)
    sorted_probs = dict(sorted(float_probabilities.items(), key=lambda x: x[1]))
    
    # Apply nonlinear transformation: sqrt transformation for better low-value precision
    # This stretches the left side (low values) and compresses the right side (high values)
    def transform_probability(p):
        """Apply square root transformation to stretch low values"""
        return np.sqrt(p)
    
    def inverse_transform(x):
        """Inverse of square root transformation"""
        return x ** 2
    
    # Transform probabilities for positioning
    transformed_probs = {k: transform_probability(v) for k, v in sorted_probs.items()}
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create horizontal scale from 0 to 1 (transformed space)
    ax.axhline(y=0, color='black', linewidth=2, alpha=0.3)
    
    # Add scale markers and labels (show original probability values)
    scale_positions_transformed = np.linspace(0, 1, 11)  # 0, 0.1, 0.2, ..., 1.0
    for pos_transformed in scale_positions_transformed:
        pos_original = inverse_transform(pos_transformed)
        ax.plot([pos_transformed, pos_transformed], [-0.02, 0.02], 'k-', linewidth=1)
        ax.text(pos_transformed, -0.05, f'{pos_original:.3f}', ha='center', va='top', fontsize=10)
    
    # Plot each probability as a point on the scale
    colors = plt.cm.rainbow(np.linspace(0, 1, len(sorted_probs)))
    
    for i, (label, prob) in enumerate(sorted_probs.items()):
        # Use transformed position for plotting
        transformed_pos = transform_probability(prob)
        
        # Plot point on scale (using transformed position)
        ax.scatter(transformed_pos, 0, color=colors[i], s=100, zorder=5)
        
        # Alternate labels above and below the line with greater separation
        if i % 2 == 0:
            # Even index: label above the line
            # Create more widely spaced heights for even positions
            if (i // 2) % 3 == 0:
                y_pos = 0.12  # First even position
            elif (i // 2) % 3 == 1:
                y_pos = 0.20  # Second even position
            else:
                y_pos = 0.28  # Third even position
            va_alignment = 'bottom'
        else:
            # Odd index: label below the line
            # Create more widely spaced depths for odd positions
            if ((i - 1) // 2) % 3 == 0:
                y_pos = -0.12  # First odd position
            elif ((i - 1) // 2) % 3 == 1:
                y_pos = -0.20  # Second odd position
            else:
                y_pos = -0.28  # Third odd position
            va_alignment = 'top'
        
        # Add connecting line from point to label (using transformed position)
        ax.plot([transformed_pos, transformed_pos], [0, y_pos], color=colors[i], linewidth=1, alpha=0.6)
        
        # Add decimal value to label
        label_text = f"{label}\n({prob:.4f})"
        ax.text(transformed_pos, y_pos, label_text, ha='center', va=va_alignment, 
                fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[i], alpha=0.7))
    
    # Set up the plot
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.40, 0.40)
    ax.set_xlabel('Probability (Nonlinear Scale: More Precision at Low Values)', fontsize=12, fontweight='bold')
    ax.set_title('15 Estonian Statistical Probabilities (Nonlinear Scale)', fontsize=14, fontweight='bold', pad=20)
    
    # Remove y-axis as it's not meaningful
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_position(('outward', 10))
    
    # Add grid for better readability
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    return fig, ax

if __name__ == "__main__":
    # Extract only the 15 specific probabilities requested
    results = extract_15_specific_probabilities()
    
    # Create horizontal scale visualization for the 15 probabilities
    fig1, ax1 = visualize_probabilities(results)
    
    # Create pie chart visualization for the 15 probabilities
    fig2, ax2 = create_pie_chart(results)
    
    # Create images folder if it doesn't exist
    import os
    os.makedirs('images', exist_ok=True)
    
    # Save both plots to images folder
    import matplotlib.pyplot as plt
    plt.figure(fig1.number)
    plt.savefig('images/15_probabilities_horizontal_scale.png', dpi=300, bbox_inches='tight')
    
    plt.figure(fig2.number)
    plt.savefig('images/15_probabilities_pie_chart.png', dpi=300, bbox_inches='tight')
    
    plt.show()
    
    print("\nVisualizations saved to images folder:")
    print("- 'images/15_probabilities_horizontal_scale.png' (Nonlinear scale)")
    print("- 'images/15_probabilities_pie_chart.png' (Pie chart distribution)")
