# ==============================================================================
# Master Grafana & Prometheus Unified Docker Image
# Optimized for 1-Click Deployment on Render Web Services
# ==============================================================================

# Stage 1: Extract Prometheus binary & console libraries
FROM prom/prometheus:v3.2.1 AS prometheus_source

# Stage 2: Build Unified Monitoring Stack on Grafana Base
FROM grafana/grafana:11.5.2

LABEL maintainer="SalesCentri DevOps <devops@salescentri.com>"
LABEL description="Unified Grafana and Prometheus monitoring stack for single-service cloud deployments"

USER root

# Install curl for container health checks
RUN apk add --no-cache curl nodejs nginx
COPY grafana/collector /opt/portfolio

# Copy Prometheus binaries from stage 1
COPY --from=prometheus_source /bin/prometheus /bin/prometheus
COPY --from=prometheus_source /bin/promtool /bin/promtool

# Copy Prometheus configuration
COPY prometheus/prometheus.yml /etc/prometheus/prometheus.yml

# Copy Grafana configuration & provisioning
COPY grafana/grafana.ini /etc/grafana/grafana.ini
COPY grafana/provisioning /etc/grafana/provisioning

# Copy container entrypoint script
ENV EMBEDDED_PROMETHEUS=1

# Create necessary directories and configure permissions for Grafana user (UID 472)
RUN mkdir -p /prometheus /var/lib/grafana /var/log/grafana && \
    chown -R 472:0 /prometheus /etc/prometheus /etc/grafana /var/lib/grafana /var/log/grafana

USER 472

# Default ports: 3000 (Grafana Web UI), 9090 (Prometheus API / UI)
EXPOSE 3000 9090

# Health check targeting Grafana's /api/health endpoint
HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:${PORT:-3000}/api/health || exit 1

ENTRYPOINT ["/bin/bash", "/opt/portfolio/start.sh"]
