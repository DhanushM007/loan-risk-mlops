# 🏦 Loan Risk Prediction — End-to-End MLOps Pipeline

> M.Tech Assignment: Advanced MLOps and DevOps Engineering

## 📌 Overview

A production-grade MLOps pipeline for loan risk prediction covering data versioning, experiment tracking, modular ML pipelines, REST API serving, Docker containerization, CI/CD automation, monitoring, drift detection, and DevSecOps.

---

## 🗂️ Project Structure

```
loan-risk-mlops/
├── data/
│   ├── raw/                    # Raw datasets (tracked by DVC)
│   └── processed/              # Preprocessed datasets
├── models/                     # Trained model artifacts
├── notebooks/                  # EDA and experimentation notebooks
├── src/
│   ├── preprocess.py           # Data preprocessing module
│   ├── train.py                # Model training module
│   ├── evaluate.py             # Model evaluation module
│   └── app.py                  # FastAPI application
├── tests/
│   ├── test_preprocess.py
│   ├── test_train.py
│   └── test_api.py
├── monitoring/
│   ├── prometheus.yml          # Prometheus configuration
│   └── drift_report.py        # Evidently AI drift detection
├── security/
│   └── scan.sh                 # Trivy security scan script
├── reports/                    # Evaluation reports and drift reports
├── .github/workflows/
│   └── mlops_pipeline.yml     # GitHub Actions CI/CD workflow
├── dvc.yaml                    # DVC pipeline definition
├── dvc.lock                    # DVC lock file (auto-generated)
├── params.yaml                 # Hyperparameters
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose for full stack
├── .env.example                # Example environment variables (no secrets)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | ≥ 3.10 | https://python.org |
| Git | ≥ 2.40 | https://git-scm.com |
| Docker | ≥ 24.0 | https://docker.com |
| DVC | ≥ 3.x | `pip install dvc` |
| MLflow | ≥ 2.x | `pip install mlflow` |

---

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/loan-risk-mlops.git
cd loan-risk-mlops
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and fill in your values
```

### 5. Initialize DVC

```bash
dvc init
# If using remote storage (e.g., Google Drive / S3):
dvc remote add -d myremote s3://your-bucket/dvc-store
```

### 6. Download Dataset

Place your dataset CSV in `data/raw/loan_data.csv`.

Recommended sources:
- [Kaggle Loan Dataset](https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset)
- UCI ML Repository

Then track with DVC:
```bash
dvc add data/raw/loan_data.csv
git add data/raw/loan_data.csv.dvc .gitignore
git commit -m "chore: add raw dataset via DVC"
```

### 7. Run the ML Pipeline

```bash
dvc repro
```

This executes: **preprocess → train → evaluate** in order.

### 8. Launch MLflow UI

```bash
mlflow ui --port 5000
# Open http://localhost:5000
```

### 9. Start the API (Local)

```bash
uvicorn src.app:app --reload --port 8000
# Open http://localhost:8000/docs
```

### 10. Run with Docker

```bash
docker build -t loan-risk-api .
docker run -p 8000:8000 loan-risk-api
```

### 11. Full Stack with Docker Compose

```bash
docker-compose up --build
```

Services started:
- **API**: http://localhost:8000
- **MLflow**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

---

## 🧪 Running Tests

```bash
pytest tests/ -v --tb=short
```

---

## 🔒 Security Scan

```bash
bash security/scan.sh
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health status |
| POST | `/predict` | Single prediction |
| POST | `/predict/batch` | Batch predictions |
| GET | `/metrics` | Prometheus metrics |

### Example Prediction Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "property_area": "Urban"
  }'
```

---

## 🔄 CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/mlops_pipeline.yml`) runs on every push:

1. ✅ Lint with `flake8`
2. ✅ Unit tests with `pytest`
3. ✅ DVC pipeline reproduction
4. 🐳 Docker image build
5. 🔐 Trivy security scan
6. 📦 Push to DockerHub (on `main` branch)

---

## 📈 Monitoring

- **Prometheus** scrapes `/metrics` every 15s
- **Grafana** dashboards show request rate, latency, error rate
- **Evidently AI** generates data drift reports: `python monitoring/drift_report.py`

---

## 🌿 Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch |
| `feature/*` | New features |
| `hotfix/*` | Emergency fixes |

---

## 📚 References

- [DVC Documentation](https://dvc.org/doc)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Evidently AI](https://docs.evidentlyai.com)
- [Prometheus](https://prometheus.io/docs)
