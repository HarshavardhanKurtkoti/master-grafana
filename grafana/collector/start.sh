#!/bin/bash
set -eu
public_port=${PORT:-${GF_SERVER_HTTP_PORT:-3000}}
export GF_SERVER_HTTP_ADDR=127.0.0.1 GF_SERVER_HTTP_PORT=13000
export GF_SERVER_ROOT_URL="${GF_SERVER_ROOT_URL:-%(protocol)s://%(domain)s:$public_port/}"
sed "s/PUBLIC_PORT/$public_port/" /opt/portfolio/nginx.conf > /tmp/portfolio-nginx.conf

nginx -e stderr -t -c /tmp/portfolio-nginx.conf
pids=""
stop() {
    trap - INT TERM EXIT
    if [ -n "$pids" ]; then
        kill -TERM $pids 2>/dev/null || true
        wait || true
    fi
}
trap stop EXIT
trap 'exit 0' INT TERM

if [ "${EMBEDDED_PROMETHEUS:-0}" = "1" ]; then
    export PROMETHEUS_URL="${PROMETHEUS_URL:-http://127.0.0.1:9090}"
    if [ "$PROMETHEUS_URL" = 'http://localhost:9090' ]; then export PROMETHEUS_URL=http://127.0.0.1:9090; fi
    sed -e 's/"grafana:3000"/"127.0.0.1:13000"/' \
        -e '/job_name: "portfolio_website"/,$s/scheme: "https"/scheme: "http"/' \
        -e 's/"grafana.harshakurtkoti.in"/"127.0.0.1:13001"/' \
        /etc/prometheus/prometheus.yml > /tmp/portfolio-prometheus.yml
    /bin/prometheus --config.file=/tmp/portfolio-prometheus.yml --storage.tsdb.path=/prometheus \
        --web.listen-address=127.0.0.1:9090 --web.enable-lifecycle &
    pids="$!"
fi
node /opt/portfolio/server.mjs &
pids="$pids $!"
/run.sh "$@" &
pids="$pids $!"
nginx -e stderr -c /tmp/portfolio-nginx.conf -g 'daemon off;' &
pids="$pids $!"
wait -n
