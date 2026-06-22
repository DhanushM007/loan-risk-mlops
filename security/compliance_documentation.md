# Security and Compliance Documentation

## 1. Secrets Management
- All API keys and credentials stored in GitHub Secrets (never in code)
- `.env` file excluded via `.gitignore`
- `.env.example` provided as template with no real values

## 2. Docker Security
- Multi-stage Docker build to minimize image size
- Non-root user (`appuser`) used inside container
- Docker image scanned with Trivy for HIGH/CRITICAL CVEs on every CI run

## 3. Data Compliance
- No PII stored in repository
- Raw dataset sourced from public Kaggle repository
- Model artifacts managed via DVC + S3 (not stored in Git)
- AWS IAM user has minimal permissions (S3FullAccess only)

## 4. API Security
- No hardcoded credentials in source code
- Environment variables used for all sensitive config
- Health check endpoint available for monitoring

## 5. Dependency Security
- All dependencies pinned to exact versions in `requirements.txt`
- Trivy scans catch vulnerable base image packages