#!/usr/bin/env bash
# ==============================================================================
# Health Probe Script for Grafana & Prometheus
# Usage:
#   ./scripts/healthcheck.sh
#   GRAFANA_URL="https://my-grafana.onrender.com" PROMETHEUS_URL="https://my-prometheus.onrender.com" ./scripts/healthcheck.sh
# ==============================================================================

set -euo pipefail

GRAFANA_HOST="${GRAFANA_URL:-http://localhost:3000}"
PROMETHEUS_HOST="${PROMETHEUS_URL:-http://localhost:9090}"

echo "=========================================="
echo "  Probing Master Grafana & Prometheus     "
echo "=========================================="
echo "Grafana Target:    $GRAFANA_HOST"
echo "Prometheus Target: $PROMETHEUS_HOST"
echo "------------------------------------------"

# 1. Prometheus Health Check
echo -n "[+] Testing Prometheus Health (GET $PROMETHEUS_HOST/-/healthy)... "
HTTP_PROM=$(curl -s -o /dev/null -w "%{http_code}" "$PROMETHEUS_HOST/-/healthy" || echo "000")
if [ "$HTTP_PROM" -eq 200 ]; then
  PROM_BODY=$(curl -s "$PROMETHEUS_HOST/-/healthy")
  echo "SUCCESS (HTTP $HTTP_PROM: $PROM_BODY)"
else
  echo "FAILED (HTTP $HTTP_PROM)"
fi

# 2. Prometheus Ready Check
echo -n "[+] Testing Prometheus Readiness (GET $PROMETHEUS_HOST/-/ready)... "
HTTP_PROM_READY=$(curl -s -o /dev/null -w "%{http_code}" "$PROMETHEUS_HOST/-/ready" || echo "000")
if [ "$HTTP_PROM_READY" -eq 200 ]; then
  PROM_READY_BODY=$(curl -s "$PROMETHEUS_HOST/-/ready")
  echo "SUCCESS (HTTP $HTTP_PROM_READY: $PROM_READY_BODY)"
else
  echo "FAILED (HTTP $HTTP_PROM_READY)"
fi

# 3. Grafana Health Check
echo -n "[+] Testing Grafana Health (GET $GRAFANA_HOST/api/health)... "
HTTP_GRAFANA=$(curl -s -o /dev/null -w "%{http_code}" "$GRAFANA_HOST/api/health" || echo "000")
if [ "$HTTP_GRAFANA" -eq 200 ]; then
  GRAFANA_BODY=$(curl -s "$GRAFANA_HOST/api/health")
  echo "SUCCESS (HTTP $HTTP_GRAFANA)"
  echo "    Response: $GRAFANA_BODY"
else
  echo "FAILED (HTTP $HTTP_GRAFANA)"
fi

echo "------------------------------------------"
if [ "$HTTP_PROM" -eq 200 ] && [ "$HTTP_GRAFANA" -eq 200 ]; then
  echo "All monitoring services are HEALTHY and OPERATIONAL!"
  exit 0
else
  echo "One or more monitoring services are UNHEALTHY or UNREACHABLE."
  exit 1
fi
