"""
Tests for training module.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier


def test_train_model_basic():
    from src.train import train_model

    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)

    cfg = {
        "n_estimators": 10,
        "max_depth": 3,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "random_state": 42,
        "class_weight": "balanced",
    }

    model = train_model(X, y, cfg)
    assert isinstance(model, RandomForestClassifier)
    assert model.n_estimators == 10
    preds = model.predict(X)
    assert len(preds) == 100
