/**
 * In-memory Prometheus telemetry store for the portfolio website.
 * Aggregates client-side Real User Monitoring (RUM), section dwell times,
 * interactive 3D model events, conversions, and serverless API metrics.
 */

const sections = ['hero', 'systems-in-motion', 'systems', 'projects', 'playground', 'stack', 'experience', 'philosophy', 'contact'];
const poses = ['idle', 'salute', 'victory', 'clapping'];
const materials = ['surface', 'wireframe'];
const actions = ['start', 'submit', 'success', 'error'];
export const sessionLimit = 10000;

function sectionLabel(id) {
  if (id === 'home') return 'hero';
  if (id === 'skills') return 'stack';
  return id;
}

function increment(map, key, amount = 1) {
  map.set(key, (map.get(key) || 0) + amount);
}

function category(value, allowed) {
  return allowed.includes(value) ? value : 'other';
}

export class TelemetryStore {
  constructor() {
    this.startTime = Date.now();
    this.pageviews = new Map(); // key -> count
    this.sessions = new Map(); // sessionId -> lastSeenTimestamp
    this.sectionViews = new Map(); // section -> count
    this.sectionDwell = new Map(); // section -> totalSeconds
    this.scrollDepth = new Map(); // bucket -> count
    this.poses = new Map(); // pose -> count
    this.materials = new Map(); // mode -> count
    this.clicks = new Map(); // target:type -> count
    this.formEvents = new Map(); // action -> count
    this.webVitals = {
      lcp: [],
      fcp: [],
      cls: [],
      ttfb: [],
    };
    this.httpRequests = new Map(); // endpoint:status -> count
  }

  recordPageview({ path = '/', device = 'desktop', browser = 'other', referrer = 'direct' }) {
    const key = [
      path === '/' ? '/' : 'other',
      category(device, ['desktop', 'mobile', 'tablet']),
      category(browser, ['edge', 'chrome', 'safari', 'firefox']),
      category(referrer, ['direct', 'internal', 'google', 'github', 'linkedin', 'twitter']),
    ].join('|');
    increment(this.pageviews, key);
  }

  recordHeartbeat(sessionId) {
    if (typeof sessionId !== 'string' || !/^[a-zA-Z0-9_-]{1,64}$/.test(sessionId)) return;
    this.sessions.delete(sessionId);
    this.sessions.set(sessionId, Date.now());
    if (this.sessions.size > sessionLimit) this.sessions.delete(this.sessions.keys().next().value);
  }

  getActiveVisitors(windowSeconds = 180) {
    const cutoff = Date.now() - windowSeconds * 1000;
    for (const [id, lastSeen] of this.sessions) {
      if (lastSeen >= cutoff) break;
      this.sessions.delete(id);
    }
    return this.sessions.size;
  }

  recordSectionView(id) {
    const section = sectionLabel(id);
    if (sections.includes(section)) increment(this.sectionViews, section);
  }

  recordSectionDwell(id, seconds) {
    const section = sectionLabel(id);
    if (sections.includes(section) && Number.isFinite(seconds) && seconds > 0) {
      increment(this.sectionDwell, section, Math.min(seconds, 300));
    }
  }

  recordScrollDepth(percent) {
    if ([25, 50, 75, 100].includes(percent)) increment(this.scrollDepth, percent + '%');
  }

  record3DPose(pose) {
    const label = typeof pose === 'string' && pose.toLowerCase().trim();
    if (poses.includes(label)) increment(this.poses, label);
  }

  record3DMaterial(mode) {
    const label = typeof mode === 'string' && mode.toLowerCase().trim();
    if (materials.includes(label)) increment(this.materials, label);
  }

  recordClick(target, type = 'outbound') {
    if (typeof target !== 'string' || !target) return;
    const label = category(target, ['resume', 'github', 'linkedin', 'book_chapter', 'external']);
    const clickType = category(type, ['cta', 'social', 'publication', 'external_project', 'outbound']);
    increment(this.clicks, label + '|' + clickType);
  }

  recordFormEvent(action) {
    if (actions.includes(action)) increment(this.formEvents, action);
  }

  recordWebVital(metric, value) {
    if (typeof metric !== 'string' || !Object.hasOwn(this.webVitals, metric) ||
        !Number.isFinite(value) || value < 0 || value > Number.MAX_SAFE_INTEGER) return;
    const samples = this.webVitals[metric];
    samples.push(value);
    if (samples.length > 100) samples.shift();
  }

  recordHttpRequest(endpoint, status) {
    if (!['/api/metrics', '/api/contact', '/api/status', '/api/telemetry'].includes(endpoint) ||
        !Number.isInteger(status) || status < 100 || status > 599) return;
    increment(this.httpRequests, endpoint + '|' + status);
  }

  toPrometheusFormat(activeVisitors = this.getActiveVisitors()) {
    const lines = [];
    const uptimeSec = Math.floor((Date.now() - this.startTime) / 1000);

    lines.push('# HELP portfolio_uptime_seconds Total seconds the portfolio telemetry engine has been active');
    lines.push('# TYPE portfolio_uptime_seconds counter');
    lines.push(`portfolio_uptime_seconds ${uptimeSec}`);

    lines.push('# HELP portfolio_active_visitors Number of currently active visitors (in last 3 minutes)');
    lines.push('# TYPE portfolio_active_visitors gauge');
    lines.push(`portfolio_active_visitors ${activeVisitors}`);

    // Pageviews
    lines.push('# HELP portfolio_pageviews_total Total website page views partitioned by path, device, browser, and referrer');
    lines.push('# TYPE portfolio_pageviews_total counter');
    if (this.pageviews.size === 0) {
      lines.push('portfolio_pageviews_total{path="/",device="desktop",browser="chrome",referrer="direct"} 0');
    } else {
      for (const [key, val] of this.pageviews.entries()) {
        const [path, device, browser, referrer] = key.split('|');
        lines.push(`portfolio_pageviews_total{path="${path}",device="${device}",browser="${browser}",referrer="${referrer}"} ${val}`);
      }
    }

    // A stable series includes the first visit in a previously unseen device/browser group.
    lines.push('# HELP portfolio_page_loads_total Total website page loads across all dimensions');
    lines.push('# TYPE portfolio_page_loads_total counter');
    lines.push(`portfolio_page_loads_total ${[...this.pageviews.values()].reduce((total, n) => total + n, 0)}`);

    // Section views
    lines.push('# HELP portfolio_section_views_total Total times a section was viewed by visitors');
    lines.push('# TYPE portfolio_section_views_total counter');
    for (const sec of sections) {
      const count = this.sectionViews.get(sec) || 0;
      lines.push(`portfolio_section_views_total{section="${sec}"} ${count}`);
    }

    // Section dwell time
    lines.push('# HELP portfolio_section_dwell_seconds_total Cumulative seconds users actively dwelled in each section');
    lines.push('# TYPE portfolio_section_dwell_seconds_total counter');
    for (const sec of sections) {
      const dwell = Math.round(this.sectionDwell.get(sec) || 0);
      lines.push(`portfolio_section_dwell_seconds_total{section="${sec}"} ${dwell}`);
    }

    // Scroll depth
    lines.push('# HELP portfolio_scroll_depth_milestones_total Distribution of maximum vertical scroll depths reached');
    lines.push('# TYPE portfolio_scroll_depth_milestones_total counter');
    for (const bucket of ['25%', '50%', '75%', '100%']) {
      lines.push(`portfolio_scroll_depth_milestones_total{depth="${bucket}"} ${this.scrollDepth.get(bucket) || 0}`);
    }

    // 3D Avatar Poses
    lines.push('# HELP portfolio_3d_pose_triggers_total Total triggers for each 3D developer pose');
    lines.push('# TYPE portfolio_3d_pose_triggers_total counter');
    for (const pose of poses) {
      lines.push(`portfolio_3d_pose_triggers_total{pose="${pose}"} ${this.poses.get(pose) || 0}`);
    }

    // 3D Material / Finish toggles
    lines.push('# HELP portfolio_3d_material_toggles_total Total toggles for 3D finishes (Surface vs Wireframe)');
    lines.push('# TYPE portfolio_3d_material_toggles_total counter');
    for (const mode of materials) {
      lines.push(`portfolio_3d_material_toggles_total{mode="${mode}"} ${this.materials.get(mode) || 0}`);
    }

    // Clicks & Conversions
    lines.push('# HELP portfolio_clicks_total User conversion and outbound CTA clicks');
    lines.push('# TYPE portfolio_clicks_total counter');
    if (!this.clicks.has('resume|cta')) {
      lines.push('portfolio_clicks_total{target="resume",type="cta"} 0');
    }
    for (const [key, val] of this.clicks.entries()) {
      const [target, type] = key.split('|');
      lines.push(`portfolio_clicks_total{target="${target}",type="${type}"} ${val}`);
    }

    // Contact Form
    lines.push('# HELP portfolio_form_events_total Contact form interaction and dispatch events');
    lines.push('# TYPE portfolio_form_events_total counter');
    for (const action of actions) {
      lines.push(`portfolio_form_events_total{action="${action}"} ${this.formEvents.get(action) || 0}`);
    }

    // Web Vitals (Averages)
    lines.push('# HELP portfolio_web_vitals_lcp_seconds Largest Contentful Paint (LCP) in seconds');
    lines.push('# TYPE portfolio_web_vitals_lcp_seconds gauge');
    const lcpVals = this.webVitals.lcp;
    const avgLcp = lcpVals.length ? (lcpVals.reduce((a, b) => a + b, 0) / lcpVals.length).toFixed(3) : 'NaN';
    lines.push(`portfolio_web_vitals_lcp_seconds ${avgLcp}`);

    lines.push('# HELP portfolio_web_vitals_fcp_seconds First Contentful Paint (FCP) in seconds');
    lines.push('# TYPE portfolio_web_vitals_fcp_seconds gauge');
    const fcpVals = this.webVitals.fcp;
    const avgFcp = fcpVals.length ? (fcpVals.reduce((a, b) => a + b, 0) / fcpVals.length).toFixed(3) : 'NaN';
    lines.push(`portfolio_web_vitals_fcp_seconds ${avgFcp}`);

    lines.push('# HELP portfolio_web_vitals_cls Cumulative Layout Shift (CLS) score');
    lines.push('# TYPE portfolio_web_vitals_cls gauge');
    const clsVals = this.webVitals.cls;
    const avgCls = clsVals.length ? (clsVals.reduce((a, b) => a + b, 0) / clsVals.length).toFixed(4) : 'NaN';
    lines.push(`portfolio_web_vitals_cls ${avgCls}`);

    lines.push('# HELP portfolio_web_vitals_ttfb_seconds Time To First Byte (TTFB) in seconds');
    lines.push('# TYPE portfolio_web_vitals_ttfb_seconds gauge');
    const ttfbVals = this.webVitals.ttfb;
    const avgTtfb = ttfbVals.length ? (ttfbVals.reduce((a, b) => a + b, 0) / ttfbVals.length).toFixed(3) : 'NaN';
    lines.push(`portfolio_web_vitals_ttfb_seconds ${avgTtfb}`);

    // HTTP Metrics
    lines.push('# HELP portfolio_http_requests_total Total internal API requests served');
    lines.push('# TYPE portfolio_http_requests_total counter');
    if (this.httpRequests.size === 0) {
      lines.push('portfolio_http_requests_total{endpoint="/api/contact",status="200"} 0');
    } else {
      for (const [key, val] of this.httpRequests.entries()) {
        const [endpoint, status] = key.split('|');
        lines.push(`portfolio_http_requests_total{endpoint="${endpoint}",status="${status}"} ${val}`);
      }
    }

    return lines.join('\n') + '\n';
  }
}
