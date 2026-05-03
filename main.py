#!/usr/bin/env python3
"""
Estonian Probability Scale -- pipeline entry point.

Runs the full pipeline:
  1. Pull a curated set of datasets from the Statistics Estonia
     (andmed.stat.ee) and TAI (statistika.tai.ee) JSON-STAT2 APIs
     and write them as standardised CSVs to ./output/.
  2. Compute conditional probabilities (shares) from those CSVs.
  3. Render a single horizontal probability scale to ./images/.

Run:  python main.py
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    print("=" * 60)
    print("Estonian Probability Scale")
    print("=" * 60)

    print("\n[1/3] Retrieving data from Statistics Estonia / TAI APIs...")
    from data_process.retrieve_data import main as retrieve_data
    retrieve_data()
    print("      Done.")

    print("\n[2/3] Computing probabilities and rendering chart...")
    from prob_extraction.extract_probabilities import (
        extract_specific_probabilities,
        visualize_probabilities,
    )

    results = extract_specific_probabilities()

    fig, _ = visualize_probabilities(results)
    os.makedirs('images', exist_ok=True)
    chart_path = 'images/probabilities_horizontal_scale.png'

    import matplotlib
    import matplotlib.pyplot as plt
    fig.savefig(chart_path, dpi=300, bbox_inches='tight')

    print("\n[3/3] Summary")
    print("-" * 40)
    sorted_probs = sorted(results.items(), key=lambda x: x[1], reverse=True)
    print(f"  {len(sorted_probs)} probabilities computed.")
    print("  Top 3:")
    for label, prob in sorted_probs[:3]:
        print(f"    {prob:.4f}  {label}")
    print("  Bottom 3:")
    for label, prob in sorted_probs[-3:]:
        print(f"    {prob:.4f}  {label}")
    print(f"\n  Source CSVs: ./output/")
    print(f"  Chart:       ./{chart_path}")

    # Only pop a window if a GUI backend is actually available.
    if matplotlib.get_backend().lower() not in ("agg", "pdf", "ps", "svg", "cairo"):
        plt.show()


if __name__ == "__main__":
    main()
