"""
Data Preprocessing Module
Handles loading, cleaning, feature engineering, and train/test splitting.
"""

import os
import yaml
import logging
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_params(params_path: str = "params.yaml") -> dict:
    with open(params_path) as f:
        return yaml.safe_load(f)


def load_data(path: str) -> pd.DataFrame:
    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path)
    logger.info(f"Dataset shape: {df.shape}")
    return df


def clean_data(df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    logger.info("Cleaning dataset...")

    # Drop Loan_ID if present
    if "Loan_ID" in df.columns:
        df = df.drop(columns=["Loan_ID"])

    # Encode target
    df[target_col] = df[target_col].map({"Y": 1, "N": 0})
    df = df.dropna(subset=[target_col])

    logger.info(f"After cleaning: {df.shape}, Target distribution:\n{df[target_col].value_counts()}")
    return df


def build_preprocessor(df: pd.DataFrame, target_col: str):
    feature_cols = [c for c in df.columns if c != target_col]
    cat_cols = df[feature_cols].select_dtypes(include="object").columns.tolist()
    num_cols = df[feature_cols].select_dtypes(include=np.number).columns.tolist()

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, num_cols),
        ("cat", categorical_pipeline, cat_cols),
    ])

    logger.info(f"Numeric columns: {num_cols}")
    logger.info(f"Categorical columns: {cat_cols}")
    return preprocessor


def main():
    params = load_params()
    prepare_cfg = params["prepare"]

    df = load_data("data/raw/loan_data.csv")
    df = clean_data(df, prepare_cfg["target_column"])

    target = prepare_cfg["target_column"]
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=prepare_cfg["test_size"],
        random_state=prepare_cfg["random_state"],
        stratify=y,
    )

    preprocessor = build_preprocessor(X_train, target)
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    os.makedirs("data/processed", exist_ok=True)

    pd.DataFrame(X_train_proc).to_csv("data/processed/X_train.csv", index=False)
    pd.DataFrame(X_test_proc).to_csv("data/processed/X_test.csv", index=False)
    pd.DataFrame(y_train).to_csv("data/processed/y_train.csv", index=False)
    pd.DataFrame(y_test).to_csv("data/processed/y_test.csv", index=False)

    joblib.dump(preprocessor, "data/processed/preprocessor.joblib")
    logger.info("Preprocessing complete. Artifacts saved.")


if __name__ == "__main__":
    main()
