# ⚡ Quick Setup Guide

## Step-by-Step (copy-paste friendly)

### Step 1 — Prerequisites
```bash
# Check versions
python --version      # need 3.10+
docker --version      # need 24+
git --version         # need 2.40+
```

### Step 2 — Clone & Install
```bash
git clone https://github.com/<YOUR_USERNAME>/loan-risk-mlops.git
cd loan-risk-mlops

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Step 3 — Initialize Git & DVC
```bash
git init                        # (skip if already cloned)
dvc init
git add .
git commit -m "chore: project initialization"
```

### Step 4 — Add Dataset
1. Download a loan dataset CSV (e.g. from Kaggle)
2. Save it as `data/raw/loan_data.csv`

Expected columns:
`Loan_ID, Gender, Married, Dependents, Education, Self_Employed,
ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term,
Credit_History, Property_Area, Loan_Status`

```bash
dvc add data/raw/loan_data.csv
git add data/raw/loan_data.csv.dvc .gitignore
git commit -m "data: add raw loan dataset via DVC"
```

### Step 5 — Run ML Pipeline
```bash
dvc repro
# Runs: preprocess → train → evaluate
```

### Step 6 — View Metrics
```bash
dvc metrics show
cat reports/metrics.json
```

### Step 7 — Launch MLflow
```bash
mlflow ui --port 5000
# Visit http://localhost:5000
```

### Step 8 — Start API Locally
```bash
uvicorn src.app:app --reload --port 8000
# Visit http://localhost:8000/docs
```

### Step 9 — Test API
```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"applicant_income": 5000, "loan_amount": 150, "loan_amount_term": 360}'
```

### Step 10 — Run Tests
```bash
pytest tests/ -v
```

### Step 11 — Docker
```bash
# Build
docker build -t loan-risk-api .

# Run
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data/processed:/app/data/processed \
  loan-risk-api
```

### Step 12 — Full Stack (Docker Compose)
```bash
docker-compose up --build
# API:        http://localhost:8000
# MLflow:     http://localhost:5000
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000  (admin / admin123)
```

### Step 13 — Drift Detection
```bash
python monitoring/drift_report.py
# Opens reports/drift_report.html
```

### Step 14 — Security Scan
```bash
chmod +x security/scan.sh
bash security/scan.sh loan-risk-api:latest
```

---

## GitHub Secrets to Configure

| Secret | Purpose |
|--------|---------|
| `DOCKERHUB_USERNAME` | DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub access token |
| `AWS_ACCESS_KEY_ID` | S3 DVC remote (optional) |
| `AWS_SECRET_ACCESS_KEY` | S3 DVC remote (optional) |

Go to: **GitHub repo → Settings → Secrets and variables → Actions**
