"""
Tests for the FastAPI prediction endpoints.
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_predict_endpoint_demo_mode():
    payload = {
        "gender": "Male",
        "married": "Yes",
        "dependents": "0",
        "education": "Graduate",
        "self_employed": "No",
        "applicant_income": 5000,
        "coapplicant_income": 0,
        "loan_amount": 150,
        "loan_amount_term": 360,
        "credit_history": 1.0,
        "property_area": "Urban",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "loan_status" in data
    assert "probability" in data
    assert "risk_level" in data


def test_predict_batch():
    payload = {
        "applications": [
            {
                "applicant_income": 5000,
                "coapplicant_income": 0,
                "loan_amount": 150,
                "loan_amount_term": 360,
            },
            {
                "applicant_income": 3000,
                "coapplicant_income": 1000,
                "loan_amount": 100,
                "loan_amount_term": 240,
            },
        ]
    }
    response = client.post("/predict/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["predictions"]) == 2


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
