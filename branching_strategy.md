git checkout main
mkdir -p docs
cat > docs/branching_strategy.md << 'EOF'
# Branching Strategy — Git Flow

## Overview
This project follows **Git Flow** branching strategy to ensure clean, 
reproducible, and production-ready code management across all MLOps pipeline stages.

---

## Branch Structure

| Branch | Purpose | Protected |
|--------|---------|-----------|
| `main` | Production-ready, stable releases only | Yes |
| `develop` | Integration branch for all features | Yes |
| `feature/*` | Individual feature development | No |
| `hotfix/*` | Emergency production bug fixes | No |

---

## Branch Descriptions

### main
- Always reflects production-ready state
- Only receives merges from develop via Pull Requests
- Every merge triggers the full CI/CD pipeline (lint, test, Docker build, push)
- Tagged for versioned releases (e.g., v1.0.0)

### develop
- Primary integration branch
- All feature branches merge here first
- CI/CD pipeline runs on every push to develop

### feature/*
Each MLOps task has its own feature branch:

| Feature Branch | Task Covered |
|----------------|-------------|
| feature/project-setup | Task 1 - Project initialization, README, .gitignore |
| feature/data-pipeline | Task 2 and 3 - DVC tracking, preprocessing, training, evaluation |
| feature/ci-cd | Task 5 - GitHub Actions workflow |
| feature/api-docker | Task 4 - FastAPI app and Dockerfile |
| feature/dvc-s3-remote | Task 2 - DVC S3 remote storage configuration |
| feature/monitoring | Task 7 - Evidently AI drift detection report |
| feature/devsecops | Task 8 - Trivy scan, compliance documentation |

### hotfix/*
- Created directly from main for critical production fixes
- Merged back into both main and develop

---

## Workflow

feature/project-setup  -> merge -> develop -> PR -> main
feature/data-pipeline  -> merge -> develop -> PR -> main
feature/ci-cd          -> merge -> develop -> PR -> main
feature/api-docker     -> merge -> develop -> PR -> main
feature/dvc-s3-remote  -> merge -> develop -> PR -> main
feature/monitoring     -> merge -> develop -> PR -> main
feature/devsecops      -> PR -> main

---

## Rules
- Direct push to main is not allowed
- All changes must go through Pull Requests
- PRs require passing CI/CD pipeline before merge
- --no-ff merge used to preserve branch history
- Branch deleted after successful merge

---

## Commit Message Convention

| Prefix | Purpose | Example |
|--------|---------|---------|
| feat: | New feature | feat: add FastAPI prediction endpoint |
| fix: | Bug fix | fix: correct DVC remote path |
| chore: | Maintenance | chore: update .gitignore |
| docs: | Documentation | docs: add architecture diagram |
| ci: | CI/CD changes | ci: add trivy scan step |
| data: | Dataset changes | data: add raw loan dataset via DVC |

---

## CI/CD Integration
- Pipeline triggers on push to main and develop
- Pipeline triggers on Pull Request to main and develop
- Stages: Lint, Test, DVC Pull, Docker Build, Trivy Scan, DockerHub Push
EOF

git add docs/branching_strategy.md
git commit -m "docs: add detailed branching strategy documentation"
git push origin main