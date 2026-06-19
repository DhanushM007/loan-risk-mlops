"""
Tests for preprocessing module.
"""

import pytest
import pandas as pd
import numpy as np


def test_load_params():
    import yaml
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    assert "prepare" in params
    assert "train" in params
    assert "evaluate" in params


def test_clean_data_target_encoding():
    from src.preprocess import clean_data

    df = pd.DataFrame({
        "ApplicantIncome": [5000, 3000, 8000],
        "LoanAmount": [150, 100, 200],
        "Loan_Status": ["Y", "N", "Y"],
    })
    result = clean_data(df, "Loan_Status")
    assert set(result["Loan_Status"].unique()).issubset({0, 1})


def test_clean_data_drops_loan_id():
    from src.preprocess import clean_data

    df = pd.DataFrame({
        "Loan_ID": ["LP001", "LP002"],
        "ApplicantIncome": [5000, 3000],
        "Loan_Status": ["Y", "N"],
    })
    result = clean_data(df, "Loan_Status")
    assert "Loan_ID" not in result.columns


def test_build_preprocessor():
    from src.preprocess import build_preprocessor

    df = pd.DataFrame({
        "ApplicantIncome": [5000, 3000, 8000],
        "Gender": ["Male", "Female", "Male"],
        "Loan_Status": [1, 0, 1],
    })
    prep = build_preprocessor(df, "Loan_Status")
    assert prep is not None
