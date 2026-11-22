<#
.SYNOPSIS
    Health Probe Script for Grafana & Prometheus (PowerShell)
.EXAMPLE
    .\scripts\healthcheck.ps1
    .\scripts\healthcheck.ps1 -GrafanaUrl "https://master-grafana.onrender.com" -PrometheusUrl "https://master-prometheus.onrender.com"
#>
param (
    [string]$GrafanaUrl = "http://localhost:3000",
    [string]$PrometheusUrl = "http://localhost:9090"
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Probing Master Grafana & Prometheus     " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Grafana Target:    $GrafanaUrl"
Write-Host "Prometheus Target: $PrometheusUrl"
Write-Host "------------------------------------------"

$allHealthy = $true

# 1. Prometheus Healthy
try {
    $resProm = Invoke-WebRequest -Uri "$PrometheusUrl/-/healthy" -UseBasicParsing -TimeoutSec 5
    if ($resProm.StatusCode -eq 200) {
        Write-Host "[+] Prometheus Health: OK (HTTP 200: $($resProm.Content.Trim()))" -ForegroundColor Green
    } else {
        Write-Host "[-] Prometheus Health: FAILED (HTTP $($resProm.StatusCode))" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "[-] Prometheus Health: FAILED ($($_.Exception.Message))" -ForegroundColor Red
    $allHealthy = $false
}

# 2. Prometheus Ready
try {
    $resPromReady = Invoke-WebRequest -Uri "$PrometheusUrl/-/ready" -UseBasicParsing -TimeoutSec 5
    if ($resPromReady.StatusCode -eq 200) {
        Write-Host "[+] Prometheus Readiness: OK (HTTP 200: $($resPromReady.Content.Trim()))" -ForegroundColor Green
    } else {
        Write-Host "[-] Prometheus Readiness: FAILED (HTTP $($resPromReady.StatusCode))" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "[-] Prometheus Readiness: FAILED ($($_.Exception.Message))" -ForegroundColor Red
    $allHealthy = $false
}

# 3. Grafana Health
try {
    $resGrafana = Invoke-RestMethod -Uri "$GrafanaUrl/api/health" -Method Get -TimeoutSec 5
    if ($resGrafana.database -eq "ok") {
        Write-Host "[+] Grafana Health: OK (HTTP 200)" -ForegroundColor Green
        Write-Host "    Version: $($resGrafana.version), Database: $($resGrafana.database)" -ForegroundColor Gray
    } else {
        Write-Host "[-] Grafana Health: UNHEALTHY" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "[-] Grafana Health: FAILED ($($_.Exception.Message))" -ForegroundColor Red
    $allHealthy = $false
}

Write-Host "------------------------------------------"
if ($allHealthy) {
    Write-Host "All monitoring services are HEALTHY and OPERATIONAL!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "One or more monitoring services are UNHEALTHY or UNREACHABLE." -ForegroundColor Red
    exit 1
}
