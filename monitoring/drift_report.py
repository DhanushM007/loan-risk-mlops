"""
Data Drift Detection using Evidently AI
Run after production data is collected to compare with training distribution.
"""

import os
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from evidently.metrics import DatasetDriftMetric, DatasetMissingValuesSummaryMetric

REPORTS_DIR = "reports"


def generate_drift_report(reference_path: str, current_path: str):
    """Generate a data drift report comparing reference vs current data."""
    print("Loading data...")
    reference_data = pd.read_csv(reference_path)
    current_data   = pd.read_csv(current_path)

    print("Generating drift report...")
    report = Report(metrics=[
        DataDriftPreset(),
        DatasetDriftMetric(),
        DatasetMissingValuesSummaryMetric(),
    ])

    report.run(reference_data=reference_data, current_data=current_data)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    output_path = os.path.join(REPORTS_DIR, "drift_report.html")
    report.save_html(output_path)
    print(f"Drift report saved to {output_path}")

    # Print summary
    result = report.as_dict()
    drift_detected = result["metrics"][1]["result"]["dataset_drift"]
    drift_share = result["metrics"][1]["result"]["share_of_drifted_columns"]
    print(f"\n{'='*40}")
    print(f"Dataset Drift Detected : {drift_detected}")
    print(f"Drifted Columns Share  : {drift_share:.2%}")
    print(f"{'='*40}\n")


if __name__ == "__main__":
    # Example usage — replace with actual paths
    # reference = training data, current = recent production data
    generate_drift_report(
        reference_path="data/processed/X_train.csv",
        current_path="data/processed/X_test.csv",
    )
