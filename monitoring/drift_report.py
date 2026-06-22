"""
Data Drift Detection using Evidently AI
Run after production data is collected to compare with training distribution.
"""

import os
import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

REPORTS_DIR = "reports"


def generate_drift_report(reference_path: str, current_path: str):
    """Generate a data drift report comparing reference vs current data."""

    print("Loading data...")

    reference_data = pd.read_csv(reference_path)
    current_data = pd.read_csv(current_path)

    print("Generating drift report...")

    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    report.run(
        reference_data=reference_data,
        current_data=current_data,
    )

    os.makedirs(REPORTS_DIR, exist_ok=True)

    output_path = os.path.join(REPORTS_DIR, "drift_report.html")
    report.save_html(output_path)

    print(f"Drift report saved to {output_path}")

    print("\nDrift analysis completed successfully.")


if __name__ == "__main__":
    generate_drift_report(
        reference_path="data/processed/X_train.csv",
        current_path="data/processed/X_test.csv",
    )