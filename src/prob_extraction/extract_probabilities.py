"""
Extract probabilities from multiple Estonian statistical datasets
"""

import pandas as pd


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

    if total_denominator <= 0:
<<<<<<< HEAD
=======
        # Fail loudly: a 0 denominator almost always means a filter doesn't
        # match any rows (e.g. filtering on an index code when the CSV holds
        # the expanded label). Silently returning 0 would hide this.
>>>>>>> 1d96c3491e3f82c12f827415d1ce2a15f6fb4c9a
        raise ValueError(
            f"Empty denominator for {csv_file} "
            f"(category_column={category_column!r}, "
            f"denominator_filter={denominator_filter!r}, "
            f"additional_filters={additional_filters!r}). "
            "Check that your filter values match the CSV's actual labels."
        )

    results = {}

    # Calculate probabilities for each category
    for category_name, category_filter in category_filters.items():
        if callable(category_filter):
            category_data = df[df[category_column].apply(category_filter)]
        else:
            category_data = df[df[category_column] == category_filter]

        category_total = category_data[value_column].sum()
        probability = category_total / total_denominator
        
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

    if total_value <= 0:
        raise ValueError(
            f"Empty group total for {csv_file} "
            f"(group_column={group_column!r}, group_filters={group_filters!r}, "
            f"additional_filters={additional_filters!r}). "
            "Check that your filter values match the CSV's actual labels."
        )

    # Calculate probabilities for each group
    group_probabilities = {}
    for group, total in group_totals.items():
        probability = total / total_value
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



# Estonian -> English translation tables for dynamic group labels.
<<<<<<< HEAD
=======
# The marriage and accident datasets return month/age-band labels in
# Estonian; everything else on the chart is in English, so we translate.
>>>>>>> 1d96c3491e3f82c12f827415d1ce2a15f6fb4c9a
ESTONIAN_MONTH_TO_EN = {
    'Jaanuar': 'January', 'Veebruar': 'February', 'Märts': 'March',
    'Aprill': 'April', 'Mai': 'May', 'Juuni': 'June', 'Juuli': 'July',
    'August': 'August', 'September': 'September', 'Oktoober': 'October',
    'November': 'November', 'Detsember': 'December',
}


def _en_month(estonian_label):
    return ESTONIAN_MONTH_TO_EN.get(estonian_label, estonian_label)


def extract_specific_probabilities():
    """
    Extract a curated set of 14 conditional probabilities (shares) from the
    Estonian statistical CSVs in ./output/.

    Each value is a fraction in [0, 1]. The labels are written as
    "<X> share of <Y>" so that the conditional / share-of nature is
    explicit -- these are *not* lifetime event probabilities.

<<<<<<< HEAD
=======
    Note: the previous version included a 15th value derived from PM09
    (livestock counts), but PM09 mixes leaf categories with hierarchical
    aggregates (e.g. "Sead" includes the various Nuumsead subcategories),
    so dividing by the sum across all `Liik` rows double-counts and
    produces a meaningless near-zero result. Fixing this properly needs
    the PM09 hierarchy metadata; until then the entry is omitted rather
    than reported wrong.
>>>>>>> 1d96c3491e3f82c12f827415d1ce2a15f6fb4c9a
    """
    print("Extracting probabilities...")

    probabilities = {}

    # KA10 - Ocean fishing: shrimp / sardine share of total ocean catch (kg)
    ka10_probs = calculate_category_probabilities(
        'output/KA10.csv',
        category_column='Kalaliik',
        value_column='value',
        category_filters={'shrimp': 'Krevett', 'sardine': 'Sardiin'},
        denominator_filter='Kala kokku',
    )
    probabilities['Shrimp share of EE ocean catch'] = ka10_probs['shrimp_probability']
    probabilities['Sardine share of EE ocean catch'] = ka10_probs['sardine_probability']

    # KA30 - Lake Peipsi: perch / pike share of Lake Peipsi catch
    ka30_probs = calculate_category_probabilities(
        'output/KA30.csv',
        category_column='Kalaliik',
        value_column='value',
        category_filters={'perch': 'Ahven', 'pike': 'Haug'},
        denominator_filter=None,
        additional_filters={'Veekogu': 'Peipsi järv'},
    )
    probabilities['Perch share of L. Peipsi catch'] = ka30_probs['perch_probability']
    probabilities['Pike share of L. Peipsi catch'] = ka30_probs['pike_probability']

    # PKH7 - Mental health: alcohol / cannabinoid share of psychoactive
    # substance disorder cases (ICD-10 F10-F19).
    pkh7_probs = calculate_category_probabilities(
        'output/PKH7.csv',
        category_column='Diagnoos (RHK-10)',
        value_column='value',
        category_filters={
            'cannabinoids': lambda x: 'Kannabinoididest' in str(x),
            'alcohol': lambda x: 'Alkoholist' in str(x),
        },
        denominator_filter=lambda x: 'Psühhoaktiivsete ainete' in str(x),
    )
    probabilities['Cannabinoids share of F10-F19 cases'] = pkh7_probs['cannabinoids_probability']
    probabilities['Alcohol share of F10-F19 cases'] = pkh7_probs['alcohol_probability']

    # RV262 - Marriages by month: most/least common marriage month
    rv262_probs = calculate_group_probabilities(
        'output/RV262.csv',
        group_column='Abiellumiskuu',
        value_column='value',
        group_filters={'Abielu tüüp': 'Abielusid kokku'},
    )
    probabilities[
        f'{_en_month(rv262_probs["most_likely_group"])} share of all EE marriages'
    ] = rv262_probs['most_likely_probability']
    probabilities[
        f'{_en_month(rv262_probs["least_likely_group"])} share of all EE marriages'
    ] = rv262_probs['least_likely_probability']

    # RV271 - Marriages by age band: most common bride/groom age band
    rv271_probs = calculate_group_probabilities(
        'output/RV271.csv',
        group_column='Vanuserühm',
        value_column='value',
        group_filters={'Abielu tüüp': 'Abielusid kokku'},
    )
    probabilities[
        f'Age {rv271_probs["most_likely_group"]} share of EE marriages'
    ] = rv271_probs['most_likely_probability']

    # TS093 - Traffic safety: share of accidents involving an intoxicated driver
    drunk_driver_probs = calculate_category_probabilities(
        'output/TS093.csv',
        category_column='Näitaja',
        value_column='value',
        category_filters={'drunk_drivers': 'Liiklusõnnetused joobes mootorsõidukijuhi osalusel'},
        denominator_filter='Liiklusõnnetused',
    )
    probabilities['Drunk-driver share of EE road accidents'] = drunk_driver_probs['drunk_drivers_probability']

    # TS093 - Peak accident month: share of yearly road accidents
    ts093_month_probs = calculate_group_probabilities(
        'output/TS093.csv',
        group_column='Kuu',
        value_column='value',
        group_filters={'Näitaja': 'Liiklusõnnetused'},
    )
    probabilities[
        f'{_en_month(ts093_month_probs["most_likely_group"])} share of yearly road accidents'
    ] = ts093_month_probs['most_likely_probability']

    # VIG10 - Vehicle-accident injury type: pedestrian / cyclist share
    vig10_probs = calculate_category_probabilities(
        'output/VIG10.csv',
        category_column='Välispõhjus (RHK-10)',
        value_column='value',
        category_filters={
            'pedestrian': '....Sõidukiõnnetuses vigastatud jalakäija (V01-V09)',
            'cyclist': '....Sõidukiõnnetuses vigastatud jalgrattur (V10-V19)',
        },
        denominator_filter='..Sõidukiõnnetused (V01-V99)',
        additional_filters={'Elukoht': 'Eesti'},
    )
    probabilities['Pedestrian share of vehicle-accident injuries'] = vig10_probs['pedestrian_probability']
    probabilities['Cyclist share of vehicle-accident injuries'] = vig10_probs['cyclist_probability']

    # KE32 - Emergency care: share of ER patients arriving by ambulance
    ke32_probs = calculate_category_probabilities(
        'output/KE32.csv',
        category_column='Saabumisviis',
        value_column='value',
        category_filters={'ambulance': 'Toodi kiirabiga'},
        denominator_filter='Erakorralisi patsiente kokku',
    )
    probabilities['Ambulance share of EE ER arrivals'] = ke32_probs['ambulance_probability']

    sorted_probabilities = dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))

    print(f"\n=== {len(sorted_probabilities)} Probabilities (descending) ===")
    for key, value in sorted_probabilities.items():
        print(f"  {key}: {value:.4f}")

    return probabilities


<<<<<<< HEAD
=======
# Backwards-compatible alias for any external callers still using the
# old name. Yields 14 (not 15) probabilities; see extract_specific_probabilities
# for the rationale.
>>>>>>> 1d96c3491e3f82c12f827415d1ce2a15f6fb4c9a
extract_15_specific_probabilities = extract_specific_probabilities


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
    ax.set_xlabel('Probability (sqrt scale -- more resolution at low values)', fontsize=12, fontweight='bold')
    ax.set_title(
        f'{len(sorted_probs)} conditional probabilities from Estonian statistics',
        fontsize=14, fontweight='bold', pad=20,
    )
    
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
    import os
    import matplotlib.pyplot as plt

    results = extract_specific_probabilities()
    fig, _ = visualize_probabilities(results)

    os.makedirs('images', exist_ok=True)
    out_path = 'images/probabilities_horizontal_scale.png'
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved to {out_path}")
