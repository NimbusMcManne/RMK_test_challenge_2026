"""
Extract probabilities from multiple Estonian statistical datasets
"""

import pandas as pd
import sys
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(current_dir))

def calculate_category_probabilities(csv_file, category_column, value_column, category_filters, denominator_filter=None, additional_filters=None):
    """
    Dynamic function to calculate probabilities for specific categories within a dataset
    
    Args:
        csv_file: Path to CSV file
        category_column: Column containing categories to analyze
        value_column: Column containing values to sum
        category_filters: Dict of {category_name: filter_value_or_function}
        denominator_filter: Filter for denominator (total) calculation
        additional_filters: Dict of additional filters to apply to all data
    
    Returns:
        Dict with probabilities and category names
    """
    print(f"Extracting probabilities from {csv_file}...")
    
    df = pd.read_csv(csv_file)
    
    # Apply additional filters if provided
    if additional_filters:
        for col, filter_val in additional_filters.items():
            if callable(filter_val):
                df = df[df[col].apply(filter_val)]
            else:
                df = df[df[col] == filter_val]
    
    # Calculate denominator (total)
    if denominator_filter:
        if callable(denominator_filter):
            denominator_data = df[df[category_column].apply(denominator_filter)]
        else:
            denominator_data = df[df[category_column] == denominator_filter]
    else:
        denominator_data = df
    
    total_denominator = denominator_data[value_column].sum()
    
    results = {}
    
    # Calculate probabilities for each category
    for category_name, category_filter in category_filters.items():
        if callable(category_filter):
            category_data = df[df[category_column].apply(category_filter)]
        else:
            category_data = df[df[category_column] == category_filter]
        
        category_total = category_data[value_column].sum()
        probability = category_total / total_denominator if total_denominator > 0 else 0
        
        # Store probability and category name for later use
        results[f'{category_name}_probability'] = probability
        results[f'{category_name}_name'] = category_filter if not callable(category_filter) else category_name
        results[f'{category_name}_total'] = category_total
    
    results['total_denominator'] = total_denominator
    return results

def calculate_group_probabilities(csv_file, group_column, value_column, group_filters, additional_filters=None):
    """
    Dynamic function to calculate probabilities for groups (e.g., months, age groups)
    
    Args:
        csv_file: Path to CSV file
        group_column: Column containing groups (e.g., months, age groups)
        value_column: Column containing values to sum
        group_filters: Dict of filters to apply before grouping
        additional_filters: Dict of additional filters to apply
    
    Returns:
        Dict with group probabilities and most/least likely groups
    """
    print(f"Extracting group probabilities from {csv_file}...")
    
    df = pd.read_csv(csv_file)
    
    # Apply group filters
    for col, filter_val in group_filters.items():
        if callable(filter_val):
            df = df[df[col].apply(filter_val)]
        else:
            df = df[df[col] == filter_val]
    
    # Apply additional filters
    if additional_filters:
        for col, filter_val in additional_filters.items():
            if callable(filter_val):
                df = df[df[col].apply(filter_val)]
            else:
                df = df[df[col] == filter_val]
    
    # Group by the specified column
    group_totals = df.groupby(group_column)[value_column].sum()
    total_value = group_totals.sum()
    
    # Calculate probabilities for each group
    group_probabilities = {}
    for group, total in group_totals.items():
        probability = total / total_value if total_value > 0 else 0
        group_probabilities[group] = probability
    
    # Find most and least likely groups
    most_likely_group = max(group_probabilities.items(), key=lambda x: x[1])
    least_likely_group = min(group_probabilities.items(), key=lambda x: x[1])
    
    results = {
        'group_probabilities': group_probabilities,
        'most_likely_group': most_likely_group[0],
        'most_likely_probability': most_likely_group[1],
        'least_likely_group': least_likely_group[0],
        'least_likely_probability': least_likely_group[1],
        'total_value': total_value
    }
    
    return results



def extract_15_specific_probabilities():
    """
    Extract only the 15 specific probabilities requested using dynamic functions
    Returns dictionary with exactly 15 probabilities as decimals (0-1)
    """
    print("Extracting 15 specific probabilities...")
    
    # Initialize results dictionary
    probabilities = {}
    
    # 1-2: KA10 Ocean Fishing Probabilities
    ka10_probs = calculate_category_probabilities(
        'output/KA10.csv',
        category_column='Kalaliik',
        value_column='value',
        category_filters={
            'shrimp': 'Krevett',
            'sardine': 'Sardiin'
        },
        denominator_filter='Kala kokku'
    )
    probabilities['Ocean Shrimp Catch Probability'] = ka10_probs['shrimp_probability']
    probabilities['Ocean Sardine Catch Probabilty'] = ka10_probs['sardine_probability']
    
    # 3-4: KA30 Lake Peipsi Fishing Probabilities
    ka30_probs = calculate_category_probabilities(
        'output/KA30.csv',
        category_column='Kalaliik',
        value_column='value',
        category_filters={
            'perch': 'Ahven',
            'pike': 'Haug'
        },
        denominator_filter=None,  # Use all data as denominator
        additional_filters={'Veekogu': 'Peipsi järv'}
    )
    probabilities['Perch Probability in Lake Peipsi'] = ka30_probs['perch_probability']
    probabilities['Pike Probability in Lake Peipsi'] = ka30_probs['pike_probability']
    
    # 5-6: PKH7 Mental Health Probabilities
    pkh7_probs = calculate_category_probabilities(
        'output/PKH7.csv',
        category_column='Diagnoos (RHK-10)',
        value_column='value',
        category_filters={
            'cannabinoids': lambda x: 'Kannabinoididest' in str(x),
            'alcohol': lambda x: 'Alkoholist' in str(x)
        },
        denominator_filter=lambda x: 'Psühhoaktiivsete ainete' in str(x)
    )
    probabilities['Probability of Cannabinoid Disorders'] = pkh7_probs['cannabinoids_probability']
    probabilities['Probability of Alcohol Disorders'] = pkh7_probs['alcohol_probability']
    
    # 7: PM09 Agricultural Probabilities - Find least bred animal
    pm09_probs = calculate_group_probabilities(
        'output/PM09.csv',
        group_column='Liik',
        value_column='value',
        group_filters={'Maakond': 'Eesti'}
    )
    
    # Find the animal with minimum probability (excluding zero values)
    non_zero_probs = {k: v for k, v in pm09_probs['group_probabilities'].items() if v > 0}
    if non_zero_probs:
        least_bred_animal = min(non_zero_probs.items(), key=lambda x: x[1])
        probabilities[f'Least Bred Animal: {least_bred_animal[0]}'] = least_bred_animal[1]
    else:
        probabilities['Least Bred Animal: None'] = 0.0
    
    # 8-9: RV262 Marriage Month Probabilities
    rv262_probs = calculate_group_probabilities(
        'output/RV262.csv',
        group_column='Abiellumiskuu',
        value_column='value',
        group_filters={'Abielu tüüp': 'Abielusid kokku'}
    )
    probabilities[f'Most Likely Marriage Month: {rv262_probs["most_likely_group"]}'] = rv262_probs['most_likely_probability']
    probabilities[f'Least Likely Marriage Month: {rv262_probs["least_likely_group"]}'] = rv262_probs['least_likely_probability']
    
    # 10: RV271 Marriage Age Probabilities
    rv271_probs = calculate_group_probabilities(
        'output/RV271.csv',
        group_column='Vanuserühm',
        value_column='value',
        group_filters={'Abielu tüüp': 'Abielusid kokku'}
    )
    probabilities[f'Most Common Marriage Age: {rv271_probs["most_likely_group"]}'] = rv271_probs['most_likely_probability']
    
    # 11-12: TS093 Traffic Safety Probabilities
    # Drunk drivers probability
    drunk_driver_probs = calculate_category_probabilities(
        'output/TS093.csv',
        category_column='Näitaja',
        value_column='value',
        category_filters={
            'drunk_drivers': 'Liiklusõnnetused joobes mootorsõidukijuhi osalusel'
        },
        denominator_filter='Liiklusõnnetused'
    )
    probabilities['Share of Accidents Caused by Drunk Drivers'] = drunk_driver_probs['drunk_drivers_probability']
    
    # Peak accident month
    ts093_month_probs = calculate_group_probabilities(
        'output/TS093.csv',
        group_column='Kuu',
        value_column='value',
        group_filters={'Näitaja': 'Liiklusõnnetused'}
    )
    probabilities[f'Peak Accident Month: {ts093_month_probs["most_likely_group"]}'] = ts093_month_probs['most_likely_probability']
    
    # 13-14: VIG10 Injury Causes Probabilities
    vig10_probs = calculate_category_probabilities(
        'output/VIG10.csv',
        category_column='Välispõhjus (RHK-10)',
        value_column='value',
        category_filters={
            'pedestrian': '....Sõidukiõnnetuses vigastatud jalakäija (V01-V09)',
            'cyclist': '....Sõidukiõnnetuses vigastatud jalgrattur (V10-V19)'
        },
        denominator_filter='..Sõidukiõnnetused (V01-V99)',
        additional_filters={'Elukoht': '00'}
    )
    probabilities['Share of Pedestrian Injuries From All Types of Injuries'] = vig10_probs['pedestrian_probability']
    probabilities['Share of Cyclist Injuries From All Types of Injuries'] = vig10_probs['cyclist_probability']
    
    # 15: KE32 Emergency Medical Probabilities
    ke32_probs = calculate_category_probabilities(
        'output/KE32.csv',
        category_column='Saabumisviis',
        value_column='value',
        category_filters={
            'ambulance': 'Toodi kiirabiga'
        },
        denominator_filter='Erakorralisi patsiente kokku'
    )
    probabilities['Likelyhood of Ambulance Transporting to Hospital'] = ke32_probs['ambulance_probability']
    
    # Sort probabilities by value (descending)
    sorted_probabilities = dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
    
    print("\n=== 15 Specific Probabilities (Descending) ===")
    for key, value in sorted_probabilities.items():
        print(f"{key}: {value:.4f}")
    
    return probabilities


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
