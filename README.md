# Master Grafana & Prometheus Monitoring Platform

A production-ready monitoring and observability stack featuring **Grafana** and **Prometheus** packaged as Docker containers, equipped with continuous deployment on **Render Cloud**, automated health checks, and a comprehensive **GitHub Actions CI/CD pipeline**.

---

## Architecture Overview

```mermaid
flowchart LR
    subgraph Client["Users & Probes"]
        Dev["User Browser / Ops"]
        HC["Render / Uptime Health Probe"]
    end

    subgraph Stack["Docker Network / Render Cloud"]
        subgraph GrafanaService["Grafana Service (:3000)"]
            Grafana["Grafana Engine\n(Dashboards & Alerts)"]
            GHealth["/api/health"]
        end

        subgraph PrometheusService["Prometheus Service (:9090)"]
            Prometheus["Prometheus TSDB\n(Metrics Collector)"]
            PHealth["/-/healthy\n/-/ready"]
        end
    end

    Dev -->|Port 3000 (HTTP)| Grafana
    HC -->|HTTP 200 Probe| GHealth
    HC -->|HTTP 200 Probe| PHealth
    Grafana -->|Internal Proxy: http://prometheus:9090| Prometheus
    Prometheus -->|Scrape /metrics| Grafana
    Prometheus -->|Self-Scrape :9090| Prometheus
```

---

## Features

- **Dual-Container Setup**: Separate, modular Dockerfiles for Grafana and Prometheus.
- **Auto-Provisioned Datasource**: Grafana automatically discovers and connects to Prometheus on startup (`PROMETHEUS_URL`).
- **Pre-loaded Dashboards**:
  - `prometheus-overview.json`: Core infrastructure and Prometheus system health.
  - `portfolio-analytics.json`: Full Real User Monitoring (RUM), visitor demographics, section dwell times, 3D model interactions, conversion funnel, and Core Web Vitals for [harshakurtkoti.in](https://harshakurtkoti.in).
- **Portfolio event ingestion**: The portfolio API pushes validated events to `POST /portfolio-telemetry/events` on the Grafana host. Prometheus scrapes the collector every 15 seconds. The unified deployment scrapes loopback. Standalone Prometheus scrapes the production collector over HTTPS.
- **Collector state**: A single collector writes counters, recent delivery IDs, bounded vital samples and recent sessions to `/var/lib/grafana/portfolio-events.json` before acknowledging a delivery. Compose persists this directory in its Grafana volume. On Render, attach a disk at that path's parent directory to retain counters across redeploys. Without a disk the lifetime total can reset.
- **Relay authentication**: Configure `PORTFOLIO_COLLECTOR_TOKEN` only on the portfolio server. The collector compares its SHA-256 digest to `grafana/collector/relay-key.sha256`. To rotate, provision a new random 32-byte token encoded as 64 hex digits and deploy the corresponding digest. A test collector can override the digest with `COLLECTOR_TOKEN_SHA256`.
- **Native Health Endpoints**:
  - Grafana: `GET /api/health` &rarr; returns `{"commit":"...","database":"ok","version":"..."}`
  - Prometheus: `GET /-/healthy` & `GET /-/ready`
- **Render Cloud Ready**: Full Infrastructure-as-Code blueprint (`render.yaml`) with zero-downtime health checking.
- **Automated CI/CD Pipeline**: GitHub Actions workflow validating configs (`promtool`, JSON/Compose syntax), running container smoke tests, and triggering Render continuous deployment.

---

## Directory Structure

```text
master-grafana/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                # Automated CI/CD pipeline (Lint -> Test -> Render CD)
├── grafana/
│   ├── Dockerfile                  # Custom Grafana image with healthcheck & curl
│   ├── grafana.ini                 # Production Grafana configuration
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml      # Auto-provisions Prometheus as default datasource
│       └── dashboards/
│           ├── dashboards.yml      # Dashboard provider definition
│           └── json/
│               └── prometheus-overview.json  # Starter system metrics dashboard
├── prometheus/
│   ├── Dockerfile                  # Production Prometheus image with lifecycle enabled
│   └── prometheus.yml              # Scrape jobs for Prometheus & Grafana metrics
├── scripts/
│   ├── healthcheck.sh              # Bash health check probe
│   └── healthcheck.ps1             # PowerShell health check probe
├── .env.example                    # Sample environment variables
├── .gitignore                      # Git ignore patterns
├── docker-compose.yml              # Local container orchestration
├── render.yaml                     # Render Cloud Blueprint specification
└── README.md                       # Documentation
```

---

## Health Check Endpoints

Both services expose built-in HTTP health endpoints that can be probed by load balancers, Render, or uptime monitoring tools (e.g. UptimeRobot, Pingdom, BetterStack):

| Service | Endpoint | HTTP Method | Expected Status | Response Payload |
|---|---|---|---|---|
| **Grafana** | `/api/health` | `GET` | `200 OK` | `{"commit":"...","database":"ok","version":"..."}` |
| **Prometheus** | `/-/healthy` | `GET` | `200 OK` | `Prometheus Server is Healthy.` |
| **Prometheus** | `/-/ready` | `GET` | `200 OK` | `Prometheus Server is Ready.` |

### Running the Health Check Script

#### PowerShell (Windows)
```powershell
# Check local containers:
.\scripts\healthcheck.ps1

# Check remote Render deployment:
.\scripts\healthcheck.ps1 -GrafanaUrl "https://master-grafana.onrender.com" -PrometheusUrl "https://master-prometheus.onrender.com"
```

#### Bash (Linux / macOS)
```bash
# Check local containers:
./scripts/healthcheck.sh

# Check remote Render deployment:
GRAFANA_URL="https://master-grafana.onrender.com" PROMETHEUS_URL="https://master-prometheus.onrender.com" ./scripts/healthcheck.sh
```

---

## Local Development (Docker Compose)

### 1. Prerequisites
- Docker Engine & Docker Compose v2+ installed.

### 2. Configure Environment (Optional)
```bash
cp .env.example .env
```
Default credentials:
- **Username:** `admin`
- **Password:** `admin` (or defined in `.env`)

### 3. Start the Containers
```bash
docker compose up -d
```

### 4. Verify Services
- **Grafana Web UI:** [http://localhost:3000](http://localhost:3000)
- **Prometheus UI:** [http://localhost:9090](http://localhost:9090)
- **Prometheus Targets:** [http://localhost:9090/targets](http://localhost:9090/targets)

### 5. Stop Containers
```bash
docker compose down
```

---

## Continuous Deployment on Render Cloud

Render Cloud is supported in two ways:

### Method A: Render Blueprints (`render.yaml`) — Recommended (Zero Setup)
This provisions both Prometheus and Grafana automatically as an Infrastructure-as-Code stack.

1. Push this repository to GitHub / GitLab.
2. In the [Render Dashboard](https://dashboard.render.com/):
   - Click **New +** &rarr; **Blueprint** (⚠️ *choose Blueprint, not Web Service*).
   - Connect your Git repository.
   - Render automatically reads [render.yaml](file:///c:/Local-Disk-D/Projects/master-grafana/render.yaml), isolates each container using `rootDir: grafana` and `rootDir: prometheus`, and provisions both services.
3. Render automatically sets up:
   - Zero-downtime deploys using `healthCheckPath: /api/health` and `healthCheckPath: /-/healthy`.
   - Continuous deployment on every git push to `main`.
   - Grafana connects to the free Prometheus web service through its Render HTTPS URL.

### Method B: Manual Web Services (via Render UI)
If you prefer creating individual Web Services manually instead of using Blueprints:

1. **For Grafana Service:**
   - Click **New +** &rarr; **Web Service**.
   - Runtime: **Docker**
   - **Root Directory**: `grafana` *(Required so Render finds `grafana/Dockerfile`)*
   - **Health Check Path**: `/api/health`
   - Port: `3000`
2. **For Prometheus Service:**
   - Click **New +** &rarr; **Web Service**.
   - Runtime: **Docker**
   - **Root Directory**: `prometheus` *(Required so Render finds `prometheus/Dockerfile`)*
   - **Health Check Path**: `/-/healthy`
   - Port: `9090`

### Method B: Render Deploy Hooks + GitHub Actions
If you prefer CI/CD orchestration through GitHub Actions:

1. In Render, go to your Web Service &rarr; **Settings** &rarr; scroll to **Deploy Hook**.
2. Copy the Deploy Hook URL:
   `https://api.render.com/deploy/srv-xxxxxxxx?key=yyyyyyyy`
3. In your GitHub repository:
   - Go to **Settings** &rarr; **Secrets and variables** &rarr; **Actions**.
   - Add a repository secret named `RENDER_DEPLOY_HOOK_GRAFANA` (and optionally `RENDER_DEPLOY_HOOK_PROMETHEUS`).
4. Whenever you push to `main`, GitHub Actions will:
   1. Validate all configuration files.
   2. Build and smoke-test both Docker containers.
   3. Trigger the Render Deploy Hook to roll out the update.

---

## CI/CD Pipeline Stages

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) executes:

1. **`lint-and-validate`**:
   - Runs `promtool check config` on `prometheus.yml`.
   - Validates JSON formatting for all Grafana dashboards.
   - Validates `docker-compose.yml` syntax.
2. **`build-and-test`**:
   - Builds both Docker images with Docker Buildx.
   - Starts containers using `docker compose up -d`.
   - Waits for health status and tests `/api/health` and `/-/healthy`.
   - Verifies auto-provisioned datasource via Grafana REST API.
   - Gracefully tears down containers.
3. **`deploy-to-render`**:
   - Triggers Render Cloud deployment upon successful tests on branch `main` / `master`.

---

## License & Contributing

Built for reliable observability. Open-source under standard project license.
