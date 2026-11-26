import json
import os
import urllib.request
import urllib.error
import base64

def build_dashboard():
    dashboard = {
        "annotations": {
            "list": [
                {
                    "builtIn": 1,
                    "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                    "enable": True,
                    "hide": True,
                    "name": "Annotations & Alerts",
                    "type": "dashboard"
                }
            ]
        },
        "description": "Spatial Productivity Operating System, Knowledge Graph Coordinates & Workspace Execution Telemetry for Orbit",
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 1,
        "id": None,
        "links": [
            {
                "asDropdown": False,
                "icon": "external link",
                "includeVars": False,
                "keepTime": False,
                "tags": [],
                "targetBlank": True,
                "title": "Visit Orbit App",
                "tooltip": "Open Orbit workspace in a new tab",
                "type": "link",
                "url": "http://localhost:3000"
            },
            {
                "asDropdown": False,
                "icon": "external link",
                "includeVars": False,
                "keepTime": False,
                "tags": [],
                "targetBlank": True,
                "title": "GitHub Repository",
                "tooltip": "Open Orbit repository",
                "type": "link",
                "url": "https://github.com/HarshavardhanKurtkoti/orbit"
            }
        ],
        "liveNow": True,
        "panels": [],
        "refresh": "10s",
        "schemaVersion": 39,
        "tags": ["orbit", "spatial-os", "productivity", "knowledge-graph", "neon-db"],
        "templating": {"list": []},
        "time": {"from": "now-1h", "to": "now"},
        "timepicker": {
            "refresh_intervals": ["5s", "10s", "30s", "1m", "5m"],
            "time_options": ["5m", "15m", "1h", "6h", "12h", "24h", "7d"]
        },
        "timezone": "browser",
        "title": "Orbit — Spatial Productivity Operating System & Knowledge Graph",
        "uid": "orbit-spatial-os",
        "version": 1,
        "weekStart": ""
    }

    panels = []
    pid = 1

    # ==========================================
    # ROW 1: Live Pulse & Spatial OS KPIs
    # ==========================================
    panels.append({
        "collapsed": False,
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 0},
        "id": 100,
        "title": "⚡ Live Pulse & Spatial OS KPIs",
        "type": "row"
    })

    # Panel 1: API Operational Status
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "mappings": [
                    {"options": {"0": {"color": "#F2495C", "text": "Offline"}, "1": {"color": "#73BF69", "text": "Healthy"}}, "type": "value"}
                ],
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#F2495C", "value": None}, {"color": "#73BF69", "value": 1}]},
                "unit": "none"
            }
        },
        "gridPos": {"h": 4, "w": 3, "x": 0, "y": 1},
        "id": pid,
        "options": {"colorMode": "background", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_api_status{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "API Status", "refId": "A"}],
        "title": "Orbit API Status",
        "type": "stat"
    })
    pid += 1

    # Panel 2: Neon PostgreSQL Connectivity
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "mappings": [
                    {"options": {"0": {"color": "#F2495C", "text": "Unhealthy"}, "1": {"color": "#56A64B", "text": "Connected"}}, "type": "value"}
                ],
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#F2495C", "value": None}, {"color": "#56A64B", "value": 1}]},
                "unit": "none"
            }
        },
        "gridPos": {"h": 4, "w": 3, "x": 3, "y": 1},
        "id": pid,
        "options": {"colorMode": "background", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_database_status{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Neon DB", "refId": "A"}],
        "title": "Neon PostgreSQL",
        "type": "stat"
    })
    pid += 1

    # Panel 3: Active Workspaces
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#5794F2", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 3, "x": 6, "y": 1},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_workspaces_total{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Workspaces", "refId": "A"}],
        "title": "Active Workspaces",
        "type": "stat"
    })
    pid += 1

    # Panel 4: Total Projects
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#a7f3d0", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 3, "x": 9, "y": 1},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_projects_total{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Projects", "refId": "A"}],
        "title": "Managed Projects",
        "type": "stat"
    })
    pid += 1

    # Panel 5: Total Tasks
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#38bdf8", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 3, "x": 12, "y": 1},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_tasks_total{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Tasks", "refId": "A"}],
        "title": "Total Tasks in Pipeline",
        "type": "stat"
    })
    pid += 1

    # Panel 6: Completion Rate Gauge
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "max": 100,
                "min": 0,
                "noValue": "0",
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                        {"color": "#F2495C", "value": None},
                        {"color": "#FF9900", "value": 40},
                        {"color": "#73BF69", "value": 70}
                    ]
                },
                "unit": "percent"
            }
        },
        "gridPos": {"h": 4, "w": 3, "x": 15, "y": 1},
        "id": pid,
        "options": {"minVizHeight": 10, "minVizWidth": 10, "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "showThresholdLabels": False, "showThresholdMarkers": True},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_completion_rate_percent{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Completion %", "refId": "A"}],
        "title": "Task Completion Rate",
        "type": "gauge"
    })
    pid += 1

    # Panel 7: Spatial Graph Coordinates (Nodes)
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#B388FF", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 3, "x": 18, "y": 1},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_graph_nodes_total{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Coordinates", "refId": "A"}],
        "title": "Spatial Coordinates",
        "type": "stat"
    })
    pid += 1

    # Panel 8: Engine Uptime
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#73BF69", "value": None}]},
                "unit": "s"
            }
        },
        "gridPos": {"h": 4, "w": 3, "x": 21, "y": 1},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_uptime_seconds{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Uptime", "refId": "A"}],
        "title": "Engine Uptime",
        "type": "stat"
    })
    pid += 1

    # ==========================================
    # ROW 2: Spatial Knowledge Graph & Coordinate Telemetry
    # ==========================================
    panels.append({
        "collapsed": False,
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 5},
        "id": 200,
        "title": "🌌 Spatial Knowledge Graph & Coordinate Telemetry",
        "type": "row"
    })

    # Panel 9: Entity Distribution Donut
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {"hideFrom": {"legend": False, "tooltip": False, "viz": False}},
                "mappings": [],
                "unit": "short"
            }
        },
        "gridPos": {"h": 8, "w": 8, "x": 0, "y": 6},
        "id": pid,
        "options": {
            "displayLabels": [],
            "legend": {"displayMode": "table", "placement": "right", "showLegend": True, "values": ["value", "percent"]},
            "pieType": "donut",
            "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
            "tooltip": {"mode": "single", "sort": "none"}
        },
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_graph_nodes{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "{{entity_type}}", "refId": "A"}],
        "title": "Spatial Entity Breakdown (Goals, Projects, Tasks, Notes)",
        "type": "piechart"
    })
    pid += 1

    # Panel 10: Relational Edges Stat
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#a7f3d0", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 4, "x": 8, "y": 6},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_graph_edges_total{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Edges", "refId": "A"}],
        "title": "Relational Edge Connections",
        "type": "stat"
    })
    pid += 1

    # Panel 11: Frame Rate
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "60",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#73BF69", "value": None}]},
                "unit": "fps"
            }
        },
        "gridPos": {"h": 4, "w": 4, "x": 12, "y": 6},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_coordinate_fps{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "FPS", "refId": "A"}],
        "title": "Spatial Render FPS",
        "type": "stat"
    })
    pid += 1

    # Panel 12: Coordinate Density Timeseries
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {
                    "axisBorderShow": False,
                    "axisCenteredZero": False,
                    "axisColorMode": "text",
                    "axisLabel": "Coordinates",
                    "axisPlacement": "auto",
                    "barAlignment": 0,
                    "drawStyle": "line",
                    "fillOpacity": 15,
                    "gradientMode": "opacity",
                    "lineInterpolation": "smooth",
                    "lineWidth": 2,
                    "pointSize": 5,
                    "showPoints": "auto",
                    "spanNulls": False
                },
                "unit": "short"
            }
        },
        "gridPos": {"h": 8, "w": 8, "x": 16, "y": 6},
        "id": pid,
        "options": {"legend": {"calcs": ["lastNotNull"], "displayMode": "list", "placement": "bottom", "showLegend": True}, "tooltip": {"mode": "single", "sort": "none"}},
        "targets": [
            {"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_graph_nodes_total{job=~\"orbit_api.*\"}", "legendFormat": "Nodes Total", "refId": "A"},
            {"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_graph_edges_total{job=~\"orbit_api.*\"}", "legendFormat": "Edges Total", "refId": "B"}
        ],
        "title": "Universe Coordinate & Relational Density",
        "type": "timeseries"
    })
    pid += 1

    # Panel 13: Edge Connections Distribution (below fps & edges)
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {
                    "axisBorderShow": False,
                    "axisCenteredZero": False,
                    "drawStyle": "bars",
                    "fillOpacity": 40,
                    "gradientMode": "scheme",
                    "lineInterpolation": "linear",
                    "lineWidth": 1,
                    "showPoints": "never"
                },
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 8, "x": 8, "y": 10},
        "id": pid,
        "options": {"legend": {"displayMode": "list", "placement": "bottom", "showLegend": False}, "tooltip": {"mode": "single", "sort": "none"}},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_graph_nodes{job=~\"orbit_api.*\"}", "legendFormat": "{{entity_type}}", "refId": "A"}],
        "title": "Entity Count by Node Type",
        "type": "barchart"
    })
    pid += 1

    # ==========================================
    # ROW 3: Workspace Execution, Tasks & Milestone Velocity
    # ==========================================
    panels.append({
        "collapsed": False,
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 14},
        "id": 300,
        "title": "📋 Workspace Execution, Tasks & Milestone Velocity",
        "type": "row"
    })

    # Panel 14: Completed Tasks Stat
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#73BF69", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 4, "x": 0, "y": 15},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_tasks_status{status=\"done\",job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Resolved", "refId": "A"}],
        "title": "Completed Tasks",
        "type": "stat"
    })
    pid += 1

    # Panel 15: In Progress Tasks Stat
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#38bdf8", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 4, "x": 4, "y": 15},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_tasks_status{status=\"in_progress\",job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "In Flight", "refId": "A"}],
        "title": "In Progress Tasks",
        "type": "stat"
    })
    pid += 1

    # Panel 16: Todo Tasks Stat
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#FF9900", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 4, "x": 8, "y": 15},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_tasks_status{status=\"todo\",job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Backlog", "refId": "A"}],
        "title": "Backlog / Todo Tasks",
        "type": "stat"
    })
    pid += 1

    # Panel 17: Tasks Breakdown Bar Chart
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {"axisLabel": "Tasks", "drawStyle": "bars", "fillOpacity": 60, "gradientMode": "scheme", "lineWidth": 1},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 12, "x": 12, "y": 15},
        "id": pid,
        "options": {"legend": {"displayMode": "list", "placement": "right", "showLegend": True}, "tooltip": {"mode": "single", "sort": "none"}},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_tasks_status{job=~\"orbit_api.*\"}", "legendFormat": "{{status}}", "refId": "A"}],
        "title": "Task Status Pipeline",
        "type": "barchart"
    })
    pid += 1

    # ==========================================
    # ROW 4: Knowledge Specs & AI Architect
    # ==========================================
    panels.append({
        "collapsed": False,
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 19},
        "id": 400,
        "title": "📖 Knowledge Base, Specifications & AI Architect",
        "type": "row"
    })

    # Panel 18: Knowledge Notes Stat
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#fbbf24", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 20},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_notes_total{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Notes", "refId": "A"}],
        "title": "Knowledge Specs & Architecture Notes",
        "type": "stat"
    })
    pid += 1

    # Panel 19: AI Architect Synthesized Plans
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#a7f3d0", "value": None}]},
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 20},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_ai_generations_total{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Plans", "refId": "A"}],
        "title": "AI Architect Synthesized Plans",
        "type": "stat"
    })
    pid += 1

    # Panel 20: AI Planning Velocity Timeseries
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {
                    "axisBorderShow": False,
                    "axisCenteredZero": False,
                    "drawStyle": "line",
                    "fillOpacity": 15,
                    "gradientMode": "opacity",
                    "lineInterpolation": "smooth",
                    "lineWidth": 2,
                    "showPoints": "auto"
                },
                "unit": "short"
            }
        },
        "gridPos": {"h": 4, "w": 12, "x": 12, "y": 20},
        "id": pid,
        "options": {"legend": {"displayMode": "list", "placement": "bottom", "showLegend": True}, "tooltip": {"mode": "single", "sort": "none"}},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_ai_generations_total{job=~\"orbit_api.*\"}", "legendFormat": "Cumulative AI Plans", "refId": "A"}],
        "title": "AI Cognitive Planning Volume",
        "type": "timeseries"
    })
    pid += 1

    # ==========================================
    # ROW 5: System Infrastructure, Latency & Redis Bus
    # ==========================================
    panels.append({
        "collapsed": False,
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 24},
        "id": 500,
        "title": "🛠️ System Infrastructure, Latency & Redis Bus",
        "type": "row"
    })

    # Panel 21: Average Latency
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#73BF69", "value": None}, {"color": "#FF9900", "value": 50}, {"color": "#F2495C", "value": 100}]},
                "unit": "ms"
            }
        },
        "gridPos": {"h": 4, "w": 4, "x": 0, "y": 25},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_api_latency_ms{stat=\"avg\",job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Average Latency", "refId": "A"}],
        "title": "Average API Latency",
        "type": "stat"
    })
    pid += 1

    # Panel 22: P95 Latency
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#73BF69", "value": None}, {"color": "#FF9900", "value": 100}, {"color": "#F2495C", "value": 200}]},
                "unit": "ms"
            }
        },
        "gridPos": {"h": 4, "w": 4, "x": 4, "y": 25},
        "id": pid,
        "options": {"colorMode": "value", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_api_latency_ms{stat=\"p95\",job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "P95 Latency", "refId": "A"}],
        "title": "P95 API Latency",
        "type": "stat"
    })
    pid += 1

    # Panel 23: Redis Status
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "thresholds"},
                "mappings": [
                    {"options": {"0": {"color": "#6e807d", "text": "Disabled / Standby"}, "1": {"color": "#56A64B", "text": "Connected"}}, "type": "value"}
                ],
                "noValue": "0",
                "thresholds": {"mode": "absolute", "steps": [{"color": "#6e807d", "value": None}, {"color": "#56A64B", "value": 1}]},
                "unit": "none"
            }
        },
        "gridPos": {"h": 4, "w": 4, "x": 8, "y": 25},
        "id": pid,
        "options": {"colorMode": "background", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
        "targets": [{"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_redis_status{job=~\"orbit_api.*\"}", "instant": True, "legendFormat": "Redis Bus", "refId": "A"}],
        "title": "Redis Event Bus",
        "type": "stat"
    })
    pid += 1

    # Panel 24: Latency Profile Timeseries
    panels.append({
        "datasource": {"type": "prometheus", "uid": "Prometheus"},
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {
                    "axisBorderShow": False,
                    "axisCenteredZero": False,
                    "axisLabel": "Latency (ms)",
                    "drawStyle": "line",
                    "fillOpacity": 15,
                    "gradientMode": "opacity",
                    "lineInterpolation": "smooth",
                    "lineWidth": 2,
                    "showPoints": "auto"
                },
                "unit": "ms"
            }
        },
        "gridPos": {"h": 4, "w": 12, "x": 12, "y": 25},
        "id": pid,
        "options": {"legend": {"displayMode": "list", "placement": "bottom", "showLegend": True}, "tooltip": {"mode": "single", "sort": "none"}},
        "targets": [
            {"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_api_latency_ms{stat=\"avg\",job=~\"orbit_api.*\"}", "legendFormat": "Avg Latency", "refId": "A"},
            {"datasource": {"type": "prometheus", "uid": "Prometheus"}, "editorMode": "code", "expr": "orbit_api_latency_ms{stat=\"p95\",job=~\"orbit_api.*\"}", "legendFormat": "P95 Latency", "refId": "B"}
        ],
        "title": "API Request Latency Profile",
        "type": "timeseries"
    })
    pid += 1

    dashboard["panels"] = panels
    return dashboard

def main():
    dashboard = build_dashboard()
    
    # 1. Save to master-grafana folder
    folder_dir = r"c:\Local-Disk-D\Projects\master-grafana\grafana\provisioning\dashboards\json\folders\Orbit"
    os.makedirs(folder_dir, exist_ok=True)
    out_path = os.path.join(folder_dir, "orbit-spatial-os.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2)
    print(f"Saved dashboard to master-grafana: {out_path}")

    # 2. Save project copy in orbit
    orbit_dashboards_dir = r"c:\Local-Disk-D\Projects\orbit\dashboards"
    os.makedirs(orbit_dashboards_dir, exist_ok=True)
    orbit_out_path = os.path.join(orbit_dashboards_dir, "orbit-spatial-os.json")
    with open(orbit_out_path, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2)
    print(f"Saved dashboard copy to orbit: {orbit_out_path}")

    # 3. Post to local Grafana container if running
    try:
        url = "http://localhost:3000/api/dashboards/db"
        # First ensure folder 'Orbit' exists
        folder_url = "http://localhost:3000/api/folders"
        folder_req = urllib.request.Request(
            folder_url,
            data=json.dumps({"title": "Orbit", "uid": "orbit-folder"}).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Basic " + base64.b64encode(b"harsha:harsha").decode("ascii")
            }
        )
        try:
            with urllib.request.urlopen(folder_req) as resp:
                folder_data = json.loads(resp.read().decode())
                folder_id = folder_data.get("id")
                print(f"Created/Found Grafana folder 'Orbit' with id: {folder_id}")
        except urllib.error.HTTPError as e:
            if e.code == 409 or e.code == 400: # folder might already exist
                # lookup folder
                get_folder_req = urllib.request.Request(
                    "http://localhost:3000/api/folders/orbit-folder",
                    headers={"Authorization": "Basic " + base64.b64encode(b"harsha:harsha").decode("ascii")}
                )
                try:
                    with urllib.request.urlopen(get_folder_req) as gresp:
                        gdata = json.loads(gresp.read().decode())
                        folder_id = gdata.get("id")
                except Exception:
                    folder_id = None
            else:
                folder_id = None

        payload = {
            "dashboard": dashboard,
            "overwrite": True
        }
        if folder_id:
            payload["folderId"] = folder_id

        dash_req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Basic " + base64.b64encode(b"harsha:harsha").decode("ascii")
            }
        )
        with urllib.request.urlopen(dash_req) as resp:
            resp_data = json.loads(resp.read().decode())
            print(f"Uploaded dashboard to local Grafana: status={resp_data.get('status')}, url={resp_data.get('url')}")
    except Exception as e:
        print(f"Local Grafana upload notice: {e}")

if __name__ == "__main__":
    main()
