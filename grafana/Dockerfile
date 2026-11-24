FROM grafana/grafana:11.5.2

LABEL maintainer="SalesCentri DevOps <devops@salescentri.com>"
LABEL description="Custom Grafana Dashboard with auto-provisioned Prometheus datasource & health checks"

USER root

# Install curl for robust health checking
RUN apk add --no-cache curl nodejs nginx
COPY collector /opt/portfolio

# Copy custom configuration and provisioning rules
COPY grafana.ini /etc/grafana/grafana.ini
COPY provisioning /etc/grafana/provisioning

# Ensure correct permissions for grafana user (UID 472)
RUN chown -R 472:0 /etc/grafana /var/lib/grafana

USER 472

ENV PROMETHEUS_URL=http://prometheus:9090

EXPOSE 3000

# Built-in Grafana health endpoint is /api/health
HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

ENTRYPOINT ["/bin/bash", "/opt/portfolio/start.sh"]
