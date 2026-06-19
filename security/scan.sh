#!/usr/bin/env bash
# ────────────────────────────────────────────────────
# security/scan.sh — Docker image security scan with Trivy
# ────────────────────────────────────────────────────
set -e

IMAGE_NAME="${1:-loan-risk-api:latest}"
REPORT_FILE="reports/trivy_report.json"

echo "🔍 Installing Trivy (if not present)..."
if ! command -v trivy &> /dev/null; then
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
fi

echo "🐳 Scanning image: $IMAGE_NAME"
mkdir -p reports

trivy image \
    --format json \
    --output "$REPORT_FILE" \
    --severity HIGH,CRITICAL \
    "$IMAGE_NAME"

echo ""
echo "📄 Human-readable summary:"
trivy image \
    --format table \
    --severity HIGH,CRITICAL \
    "$IMAGE_NAME"

echo ""
echo "✅ Security scan complete. Full report: $REPORT_FILE"
