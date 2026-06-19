"""
Loan Risk Prediction API
FastAPI application with Prometheus metrics and request logging.
"""

import os
import time
import logging
import joblib
import numpy as np
import pandas as pd
from contextlib import asynccontextmanager
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ── Prometheus metrics ──────────────────────────────────────────────────────
REQUEST_COUNT = Counter(
    "api_requests_total", "Total API requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds", "API request latency", ["endpoint"]
)
PREDICTION_COUNT = Counter(
    "predictions_total", "Total predictions made", ["result"]
)

# ── Global model / preprocessor ─────────────────────────────────────────────
MODEL = None
PREPROCESSOR = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global MODEL, PREPROCESSOR
    model_path = os.getenv("MODEL_PATH", "models/loan_risk_model.joblib")
    prep_path  = os.getenv("PREPROCESSOR_PATH", "data/processed/preprocessor.joblib")

    if os.path.exists(model_path) and os.path.exists(prep_path):
        MODEL = joblib.load(model_path)
        PREPROCESSOR = joblib.load(prep_path)
        logger.info("Model and preprocessor loaded successfully.")
    else:
        logger.warning("Model files not found. Running in demo mode.")
    yield


app = FastAPI(
    title="Loan Risk Prediction API",
    description="Production-grade MLOps API for predicting loan risk.",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Schemas ─────────────────────────────────────────────────────────────────
class LoanApplication(BaseModel):
    gender: Optional[str] = Field(None, example="Male")
    married: Optional[str] = Field(None, example="Yes")
    dependents: Optional[str] = Field(None, example="0")
    education: Optional[str] = Field(None, example="Graduate")
    self_employed: Optional[str] = Field(None, example="No")
    applicant_income: float = Field(..., example=5000)
    coapplicant_income: float = Field(0.0, example=0.0)
    loan_amount: float = Field(..., example=150)
    loan_amount_term: float = Field(360.0, example=360.0)
    credit_history: Optional[float] = Field(None, example=1.0)
    property_area: Optional[str] = Field(None, example="Urban")


class PredictionResponse(BaseModel):
    loan_status: str
    probability: float
    risk_level: str


class BatchRequest(BaseModel):
    applications: List[LoanApplication]


# ── Middleware ───────────────────────────────────────────────────────────────
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)

    logger.info(f"{request.method} {request.url.path} {response.status_code} {latency:.3f}s")
    return response


# ── Helpers ──────────────────────────────────────────────────────────────────
def application_to_df(app_data: LoanApplication) -> pd.DataFrame:
    return pd.DataFrame([{
        "Gender": app_data.gender,
        "Married": app_data.married,
        "Dependents": app_data.dependents,
        "Education": app_data.education,
        "Self_Employed": app_data.self_employed,
        "ApplicantIncome": app_data.applicant_income,
        "CoapplicantIncome": app_data.coapplicant_income,
        "LoanAmount": app_data.loan_amount,
        "Loan_Amount_Term": app_data.loan_amount_term,
        "Credit_History": app_data.credit_history,
        "Property_Area": app_data.property_area,
    }])


def make_prediction(df: pd.DataFrame) -> PredictionResponse:
    if MODEL is None or PREPROCESSOR is None:
        # Demo mode: return a dummy prediction
        return PredictionResponse(
            loan_status="Approved (Demo)",
            probability=0.75,
            risk_level="Low",
        )

    X = PREPROCESSOR.transform(df)
    prob = float(MODEL.predict_proba(X)[0][1])
    label = "Approved" if prob >= 0.5 else "Rejected"
    risk = "Low" if prob >= 0.7 else ("Medium" if prob >= 0.4 else "High")

    PREDICTION_COUNT.labels(result=label).inc()

    return PredictionResponse(
        loan_status=label,
        probability=round(prob, 4),
        risk_level=risk,
    )


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "Loan Risk Prediction API", "status": "running", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "model_loaded": MODEL is not None,
        "preprocessor_loaded": PREPROCESSOR is not None,
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(application: LoanApplication):
    try:
        df = application_to_df(application)
        return make_prediction(df)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", tags=["Prediction"])
def predict_batch(batch: BatchRequest):
    results = []
    for app_data in batch.applications:
        df = application_to_df(app_data)
        results.append(make_prediction(df).model_dump())
    return {"predictions": results, "count": len(results)}


@app.get("/metrics", tags=["Monitoring"])
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
