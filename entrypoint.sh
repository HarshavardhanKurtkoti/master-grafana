#!/bin/sh
set -e

echo "=================================================="
echo " Starting Master Grafana + Prometheus Unified Stack "
echo "=================================================="

# Set Render PORT if provided (Render routes HTTP traffic to $PORT)
if [ -n "$PORT" ]; then
  export GF_SERVER_HTTP_PORT="$PORT"
  echo "[+] Detected Render PORT=$PORT, configuring Grafana to listen on $PORT"
fi

# Ensure Prometheus URL points to internal localhost if not explicitly overridden
export PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"
echo "[+] Grafana Prometheus DataSource URL: $PROMETHEUS_URL"

# 1. Start Prometheus daemon in background
echo "[+] Starting Prometheus on port 9090..."
/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.listen-address="0.0.0.0:9090" \
  --web.enable-lifecycle &
PROM_PID=$!

# 2. Wait a moment for Prometheus to bind port
sleep 1

# 3. Start Grafana in background
echo "[+] Starting Grafana on port ${GF_SERVER_HTTP_PORT:-3000}..."
/run.sh &
GRAFANA_PID=$!

# Handle graceful shutdown on Render SIGTERM / SIGINT
shutdown() {
  echo "[!] Caught shutdown signal, stopping Prometheus ($PROM_PID) and Grafana ($GRAFANA_PID)..."
  kill -TERM "$PROM_PID" "$GRAFANA_PID" 2>/dev/null || true
  wait "$PROM_PID" "$GRAFANA_PID" 2>/dev/null || true
  exit 0
}

trap shutdown TERM INT

# Wait for either process to terminate
wait -n "$PROM_PID" "$GRAFANA_PID"
EXIT_CODE=$?

echo "[!] One of the monitoring processes exited with code $EXIT_CODE. Stopping all..."
kill -TERM "$PROM_PID" "$GRAFANA_PID" 2>/dev/null || true
exit $EXIT_CODE
