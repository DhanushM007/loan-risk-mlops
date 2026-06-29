# System Architecture

## Pipeline Flow

Dataset → DVC Versioning → Preprocessing → Training → Evaluation → MLflow Tracking → FastAPI → Docker → CI/CD → Prometheus → Drift Detection → Trivy Security

## Component Diagram

Dataset (Kaggle)

│

▼

┌─────────────────┐

│  DVC Tracking   │  ← Raw data versioned with DVC + S3

└────────┬────────┘

│

▼

┌─────────────────┐

│  Preprocessing  │  ← preprocess.py (imputation, encoding, scaling)

└────────┬────────┘

│

▼

┌─────────────────┐

│    Training     │  ← train.py (RandomForest + MLflow tracking)

└────────┬────────┘

│

▼

┌─────────────────┐

│   Evaluation    │  ← evaluate.py (metrics.json, confusion matrix)

└────────┬────────┘

│

▼

┌─────────────────┐

│  MLflow Server  │  ← Experiment tracking, model registry

└────────┬────────┘

│

▼

┌─────────────────┐

│  FastAPI + Docker│ ← REST API, containerized, Prometheus metrics

└────────┬────────┘

│

▼

┌─────────────────┐

│  CI/CD Pipeline │  ← GitHub Actions: lint→test→dvc→build→scan→push

└────────┬────────┘

│

▼

┌─────────────────┐

│   Monitoring    │  ← Prometheus + Grafana + Evidently AI drift

└────────┬────────┘

│

▼

┌─────────────────┐

│ Security (Trivy)│  ← Docker image scanning, secrets management

└─────────────────┘

## Tools Used

| Component | Tool |
|-----------|------|
| Version Control | Git + GitHub |
| Data Versioning | DVC + AWS S3 |
| Experiment Tracking | MLflow |
| ML Pipeline | DVC Pipelines |
| API | FastAPI |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |
| Drift Detection | Evidently AI |
| Security | Trivy + GitHub Secrets |