FROM prom/prometheus:v3.2.1

# Set labels for OCI compliance
LABEL maintainer="SalesCentri DevOps <devops@salescentri.com>"
LABEL description="Prometheus Monitoring Server with pre-configured scraping and health checks"

# Copy Prometheus configuration
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Expose default Prometheus web port
EXPOSE 9090

# Enable lifecycle API (for hot-reloads) and set storage path
ENTRYPOINT [ "/bin/prometheus" ]
CMD [ \
  "--config.file=/etc/prometheus/prometheus.yml", \
  "--storage.tsdb.path=/prometheus", \
  "--web.console.libraries=/usr/share/prometheus/console_libraries", \
  "--web.console.templates=/usr/share/prometheus/consoles", \
  "--web.enable-lifecycle" \
]

# Health check using Prometheus built-in /-/healthy endpoint
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -q --spider http://localhost:9090/-/healthy || exit 1
