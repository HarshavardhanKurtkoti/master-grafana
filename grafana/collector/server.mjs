import { createServer } from 'node:http';
import { createHash, timingSafeEqual } from 'node:crypto';
import { existsSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { TelemetryStore } from './store.mjs';
import { record } from './record.mjs';

const stateFile = process.env.COLLECTOR_STATE_FILE || '/var/lib/grafana/portfolio-events.json';
const verifier = Buffer.from(process.env.COLLECTOR_TOKEN_SHA256 ||
  readFileSync(new URL('./relay-key.sha256', import.meta.url), 'utf8').trim(), 'hex');
if (verifier.length !== 32) throw new Error('Invalid collector token verifier');
const started = Date.now();
const mapNames = Object.entries(new TelemetryStore()).filter(([, value]) => value instanceof Map).map(([name]) => name);

function restore(saved) {
  const store = new TelemetryStore();
  store.startTime = started;
  if (saved) {
    for (const name of mapNames) store[name] = new Map(saved[name]);
    store.webVitals = structuredClone(saved.webVitals);
  }
  return store;
}

function snapshot(store, receipts) {
  const saved = { webVitals: store.webVitals, receipts };
  for (const name of mapNames) saved[name] = [...store[name]];
  return saved;
}

let saved = existsSync(stateFile) ? JSON.parse(readFileSync(stateFile, 'utf8')) : null;
let current = restore(saved);

// Serialize each small batch completely before yielding to another request. Publishing
// after the atomic rename keeps a failed disk write from advancing visible counters.
function commit(id, events) {
  const now = Date.now();
  const receipts = (saved?.receipts || []).filter(([, seen]) => seen > now - 120_000);
  if (receipts.some(([previous]) => previous === id)) return;
  const next = restore(saved);
  next.getActiveVisitors();
  for (const event of events) record(next, event);
  receipts.push([id, now]);
  const state = snapshot(next, receipts);
  writeFileSync(stateFile + '.tmp', JSON.stringify(state), { mode: 0o600 });
  renameSync(stateFile + '.tmp', stateFile);
  saved = state;
  current = next;
}

createServer(async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'GET' && req.url === '/portfolio-telemetry/metrics') {
    res.setHeader('Content-Type', 'text/plain; version=0.0.4; charset=utf-8');
    return res.end(current.toPrometheusFormat());
  }
  if (req.method !== 'POST' || req.url !== '/portfolio-telemetry/events') return res.writeHead(404).end();
  const token = /^Bearer ([a-f0-9]{64})$/.exec(req.headers.authorization || '')?.[1];
  if (!token || !timingSafeEqual(verifier, createHash('sha256').update(token).digest())) {
    return res.writeHead(401).end();
  }
  const id = req.headers['x-delivery-id'];
  if (typeof id !== 'string' || !/^[a-f0-9-]{36}$/.test(id)) return res.writeHead(400).end();
  let events;
  try {
    const chunks = [];
    let size = 0;
    for await (const chunk of req) {
      size += chunk.length;
      if (size > 32 * 1024) return res.writeHead(413).end();
      chunks.push(chunk);
    }
    events = JSON.parse(Buffer.concat(chunks).toString());
    if (!Array.isArray(events) || events.length > 50 || !events.every(e => typeof e?.type === 'string')) {
      return res.writeHead(400).end();
    }
  } catch {
    return res.writeHead(400).end();
  }
  try {
    if (events.length) commit(id, events);
    res.writeHead(204).end();
  } catch (error) {
    console.error('Portfolio event commit failed', error.code || error.name);
    res.writeHead(503).end();
  }
}).listen(Number(process.env.COLLECTOR_PORT || 13001), '127.0.0.1');
