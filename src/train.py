"""
Model Training Module
Trains a Random Forest classifier with MLflow experiment tracking.
"""

import os
import yaml
import logging
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_params(params_path: str = "params.yaml") -> dict:
    with open(params_path) as f:
        return yaml.safe_load(f)


def load_data():
    X_train = pd.read_csv("data/processed/X_train.csv").values
    y_train = pd.read_csv("data/processed/y_train.csv").values.ravel()
    logger.info(f"Training data shape: {X_train.shape}")
    return X_train, y_train


def train_model(X_train, y_train, cfg: dict):
    model = RandomForestClassifier(
        n_estimators=cfg["n_estimators"],
        max_depth=cfg["max_depth"],
        min_samples_split=cfg["min_samples_split"],
        min_samples_leaf=cfg["min_samples_leaf"],
        random_state=cfg["random_state"],
        class_weight=cfg["class_weight"],
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def main():
    params = load_params()
    train_cfg = params["train"]

    mlflow.set_experiment("loan-risk-prediction")

    with mlflow.start_run(run_name="rf-training"):
        mlflow.log_params(train_cfg)

        X_train, y_train = load_data()
        model = train_model(X_train, y_train, train_cfg)

        os.makedirs("models", exist_ok=True)
        model_path = "models/loan_risk_model.joblib"
        joblib.dump(model, model_path)

        mlflow.sklearn.log_model(model, "model")
        mlflow.log_artifact(model_path)

        logger.info(f"Model saved to {model_path}")
        logger.info(f"MLflow run ID: {mlflow.active_run().info.run_id}")


if __name__ == "__main__":
    main()
