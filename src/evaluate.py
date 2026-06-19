"""
Model Evaluation Module
Computes metrics and logs to MLflow. Outputs metrics.json for DVC tracking.
"""

import json
import logging
import os
import joblib
import pandas as pd
import mlflow
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_data():
    X_test = pd.read_csv("data/processed/X_test.csv").values
    y_test = pd.read_csv("data/processed/y_test.csv").values.ravel()
    return X_test, y_test


def compute_metrics(y_true, y_pred, y_prob) -> dict:
    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_true, y_prob), 4),
    }


def main():
    X_test, y_test = load_data()
    model = joblib.load("models/loan_risk_model.joblib")

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = compute_metrics(y_test, y_pred, y_prob)
    logger.info(f"Evaluation metrics: {metrics}")
    logger.info(f"\n{classification_report(y_test, y_pred)}")

    os.makedirs("reports", exist_ok=True)
    with open("reports/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    cm = confusion_matrix(y_test, y_pred).tolist()
    with open("reports/confusion_matrix.json", "w") as f:
        json.dump({"confusion_matrix": cm}, f)

    mlflow.set_experiment("loan-risk-prediction")
    with mlflow.start_run(run_name="evaluation"):
        mlflow.log_metrics(metrics)
        mlflow.log_artifact("reports/metrics.json")

    logger.info("Evaluation complete. Reports saved to reports/")


if __name__ == "__main__":
    main()
