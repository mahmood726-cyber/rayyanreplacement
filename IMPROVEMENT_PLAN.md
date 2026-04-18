# Screenr v10.4+ Significant Improvements Plan

## Executive Summary

Screenr v10.3 is a fully-featured systematic review platform with 32,000+ lines in a single HTML file. This plan outlines **significant architectural and feature improvements** to make it enterprise-ready while maintaining the single-file offline-first philosophy.

---

## Priority Matrix

| Priority | Category | Impact | Effort |
|----------|----------|--------|--------|
| **P0** | Performance | High | Medium |
| **P1** | Architecture | High | High |
| **P2** | Intelligence | High | Medium |
| **P3** | Collaboration | Very High | Very High |
| **P4** | Mobile UX | Medium | Medium |

---

## P0: Performance Improvements (Weeks 1-3)

### 0.1 Web Workers for Heavy Computation
**Problem:** Meta-analysis, NMA, Bayesian calculations block the UI thread.

**Solution:**
```javascript
// Create inline worker from blob
const workerCode = `
  self.onmessage = function(e) {
    const { type, data } = e.data;
    if (type === 'meta-analysis') {
      const result = calculateMetaAnalysis(data.studies);
      self.postMessage({ type: 'result', result });
    }
  };
  // Include calculation functions here
`;
const blob = new Blob([workerCode], { type: 'application/javascript' });
const worker = new Worker(URL.createObjectURL(blob));
```

**Files to modify:** `screenr.html`
- Extract calculation functions: `calculateMetaAnalysis`, `performNMA`, `runBayesianMeta`
- Create worker message protocol
- Add progress reporting via `postMessage`

**Acceptance Criteria:**
- [ ] UI remains responsive during 100+ study meta-analysis
- [ ] Progress bar shows calculation progress
- [ ] Worker gracefully handles errors

---

### 0.2 Full IndexedDB Migration
**Problem:** localStorage limited to 5-10MB; large projects fail.

**Current state:** IndexedDB exists but underutilized.

**Solution:**
```javascript
const DB_SCHEMA = {
  stores: {
    records: { keyPath: 'id', indexes: ['title', 'year', 'status'] },
    decisions: { keyPath: 'recordId' },
    extractions: { keyPath: 'recordId' },
    robAssessments: { keyPath: 'recordId' },
    auditLogs: { keyPath: 'id', indexes: ['recordId', 'timestamp'] },
    blobs: { keyPath: 'id' } // For PDF storage
  }
};
```

**Files to modify:** `screenr.html`
- Upgrade `initDB()` to create all stores
- Add `syncToIndexedDB()` for periodic persistence
- Add `loadFromIndexedDB()` with streaming for large datasets
- Add migration from localStorage

**Acceptance Criteria:**
- [ ] Support 100,000+ records
- [ ] PDF attachments stored in IndexedDB
- [ ] Graceful fallback to localStorage
- [ ] Data migration from old format

---

### 0.3 Enhanced Virtual Scrolling
**Problem:** Current virtualization only for record list; extraction table, audit logs still render all.

**Solution:** Create reusable `VirtualList` component:
```javascript
class VirtualList {
  constructor(container, options) {
    this.container = container;
    this.itemHeight = options.itemHeight || 50;
    this.buffer = options.buffer || 5;
    this.renderItem = options.renderItem;
    this.observer = new IntersectionObserver(this.onIntersect.bind(this));
  }

  setData(items) { /* ... */ }
  scrollToIndex(index) { /* ... */ }
  refresh() { /* ... */ }
}
```

**Apply to:**
- [ ] Record list (improve existing)
- [ ] Extraction data table
- [ ] Audit log timeline
- [ ] Search results
- [ ] Conflict resolution table

**Acceptance Criteria:**
- [ ] 60fps scroll with 50,000 records
- [ ] Memory usage under 200MB
- [ ] Keyboard navigation works

---

## P1: Architecture Improvements (Weeks 4-8)

### 1.1 Module System (Build-time)
**Problem:** 32,000 lines in single file is hard to maintain.

**Solution:** Split into modules, bundle for distribution:
```
screenr/
├── src/
│   ├── index.html          # Shell with script tags
│   ├── css/
│   │   ├── variables.css
│   │   ├── components.css
│   │   ├── layouts.css
│   │   └── dark-mode.css
│   ├── js/
│   │   ├── core/
│   │   │   ├── state.js
│   │   │   ├── db.js
│   │   │   └── events.js
│   │   ├── features/
│   │   │   ├── screening.js
│   │   │   ├── extraction.js
│   │   │   ├── meta-analysis.js
│   │   │   ├── nma.js
│   │   │   ├── dta.js
│   │   │   └── bayesian.js
│   │   ├── ui/
│   │   │   ├── modals.js
│   │   │   ├── charts.js
│   │   │   └── virtual-list.js
│   │   └── utils/
│   │       ├── statistics.js
│   │       ├── export.js
│   │       └── import.js
│   └── workers/
│       └── compute-worker.js
├── build.js                 # Bundles to single file
├── package.json
└── dist/
    └── screenr.html         # Production single-file output
```

**Build script:**
```javascript
// build.js - Inline all JS/CSS into single HTML
const fs = require('fs');
const path = require('path');

function bundle() {
  let html = fs.readFileSync('src/index.html', 'utf8');

  // Inline CSS
  const cssFiles = glob.sync('src/css/*.css');
  const css = cssFiles.map(f => fs.readFileSync(f, 'utf8')).join('\n');
  html = html.replace('/* CSS_PLACEHOLDER */', css);

  // Inline JS
  const jsFiles = glob.sync('src/js/**/*.js');
  const js = jsFiles.map(f => fs.readFileSync(f, 'utf8')).join('\n');
  html = html.replace('/* JS_PLACEHOLDER */', js);

  fs.writeFileSync('dist/screenr.html', html);
}
```

**Acceptance Criteria:**
- [ ] Development uses separate files
- [ ] Build produces identical single-file output
- [ ] Source maps for debugging
- [ ] No runtime dependencies

---

### 1.2 State Management Refactor
**Problem:** Global mutable state (`records`, `decisions`, etc.) scattered throughout.

**Solution:** Centralized immutable state with events:
```javascript
const Store = {
  state: {
    records: [],
    decisions: new Map(),
    extractions: new Map(),
    ui: { selectedRecordId: null, filter: 'all', mode: 'screen' }
  },

  listeners: new Set(),

  dispatch(action, payload) {
    const newState = this.reducer(this.state, action, payload);
    if (newState !== this.state) {
      this.state = newState;
      this.persist();
      this.notify();
    }
  },

  reducer(state, action, payload) {
    switch (action) {
      case 'ADD_RECORD': return { ...state, records: [...state.records, payload] };
      case 'SET_DECISION': return { ...state, decisions: new Map(state.decisions).set(payload.id, payload.decision) };
      // ...
    }
  },

  subscribe(fn) { this.listeners.add(fn); return () => this.listeners.delete(fn); },
  notify() { this.listeners.forEach(fn => fn(this.state)); }
};
```

**Acceptance Criteria:**
- [ ] All state changes through dispatch
- [ ] Time-travel debugging possible
- [ ] Undo/redo for all operations
- [ ] State persistence automatic

---

### 1.3 Testing Infrastructure
**Problem:** No automated tests.

**Solution:**
```javascript
// tests/meta-analysis.test.js
import { describe, it, expect } from 'vitest';
import { calculateMetaAnalysis, calculateI2 } from '../src/js/features/meta-analysis.js';

describe('Meta-Analysis Calculations', () => {
  it('calculates pooled effect correctly', () => {
    const studies = [
      { effect: 0.5, se: 0.1 },
      { effect: 0.7, se: 0.15 },
      { effect: 0.3, se: 0.12 }
    ];
    const result = calculateMetaAnalysis(studies);
    expect(result.pooledEffect).toBeCloseTo(0.51, 2);
  });

  it('calculates I² correctly', () => {
    expect(calculateI2(100, 5)).toBeCloseTo(96, 0);
    expect(calculateI2(3, 5)).toBe(0); // Q < df
  });
});
```

**Test categories:**
- [ ] Unit tests for statistical functions (Vitest)
- [ ] Integration tests for UI workflows (Playwright)
- [ ] Validation tests (existing 46 tests, expand to 100+)
- [ ] Performance benchmarks

**Acceptance Criteria:**
- [ ] 80% code coverage
- [ ] CI runs on every commit
- [ ] Benchmarks tracked over time

---

## P2: Intelligence Improvements (Weeks 6-10)

### 2.1 Enhanced Duplicate Detection
**Problem:** Current detection is basic (exact title, simple Levenshtein).

**Solution:** Multi-signal semantic detection:
```javascript
class DuplicateDetector {
  constructor() {
    this.titleIndex = new Map();     // Normalized title → record IDs
    this.doiIndex = new Map();       // DOI → record ID
    this.pmidIndex = new Map();      // PMID → record ID
    this.authorYearIndex = new Map(); // "Smith2020" → record IDs
  }

  findDuplicates(record) {
    const candidates = new Set();

    // Exact matches (fast)
    if (record.doi && this.doiIndex.has(record.doi)) {
      return [{ id: this.doiIndex.get(record.doi), confidence: 1.0, method: 'DOI' }];
    }

    // Fuzzy title matching
    const normalizedTitle = this.normalize(record.title);
    const titleCandidates = this.findSimilarTitles(normalizedTitle);

    // Author-year matching
    const authorYear = this.extractAuthorYear(record);
    const authorCandidates = this.authorYearIndex.get(authorYear) || [];

    // Score candidates
    return this.scoreCandidates([...titleCandidates, ...authorCandidates], record);
  }

  findSimilarTitles(title) {
    // Use trigram similarity for fuzzy matching
    const trigrams = this.getTrigrams(title);
    // ... matching logic
  }

  scoreCandidates(candidates, record) {
    return candidates.map(c => ({
      id: c.id,
      confidence: this.calculateConfidence(c, record),
      method: c.method,
      signals: c.signals
    })).filter(c => c.confidence >= 0.7);
  }
}
```

**Features:**
- [ ] DOI/PMID exact matching
- [ ] Trigram-based fuzzy title matching
- [ ] Author-year clustering
- [ ] Visual diff view for suspected duplicates
- [ ] Batch resolution UI
- [ ] Confidence scoring

**Acceptance Criteria:**
- [ ] 95% precision (flagged items are real duplicates)
- [ ] 90% recall (catches most duplicates)
- [ ] < 100ms for 10,000 records

---

### 2.2 Smart Screening Suggestions
**Problem:** Active learning exists but could be more proactive.

**Solution:** Real-time relevance scoring:
```javascript
class ScreeningSuggestions {
  constructor() {
    this.model = null;
    this.featureExtractor = new TFIDFExtractor();
  }

  async train(records, decisions) {
    const positives = records.filter(r => decisions.get(r.id)?.status === 'include');
    const negatives = records.filter(r => decisions.get(r.id)?.status === 'exclude');

    if (positives.length < 5 || negatives.length < 5) return;

    const features = records.map(r => this.featureExtractor.extract(r));
    const labels = records.map(r => decisions.get(r.id)?.status === 'include' ? 1 : 0);

    this.model = new LogisticRegression();
    await this.model.train(features, labels);
  }

  predict(record) {
    if (!this.model) return null;
    const features = this.featureExtractor.extract(record);
    return this.model.predict(features);
  }

  suggestNextBatch(records, batchSize = 10) {
    // Uncertainty sampling: pick records model is least confident about
    const scored = records
      .filter(r => !decisions.has(r.id))
      .map(r => ({ record: r, confidence: this.predict(r) }))
      .sort((a, b) => Math.abs(0.5 - a.confidence) - Math.abs(0.5 - b.confidence));

    return scored.slice(0, batchSize);
  }
}
```

**Features:**
- [ ] Real-time relevance prediction
- [ ] Uncertainty sampling for efficient screening
- [ ] Visual confidence indicators in record list
- [ ] "High priority" queue for likely includes
- [ ] Estimated stopping point

**Acceptance Criteria:**
- [ ] 50% reduction in screening time
- [ ] Model trains in < 1 second
- [ ] Predictions update live

---

### 2.3 Citation Network Analysis
**Problem:** No way to find related studies via citations.

**Solution:**
```javascript
class CitationNetwork {
  constructor() {
    this.graph = new Map(); // recordId → { citing: Set, citedBy: Set }
  }

  async fetchCitations(record) {
    // Try OpenAlex first (free, comprehensive)
    if (record.doi) {
      const response = await fetch(`https://api.openalex.org/works/doi:${record.doi}`);
      const data = await response.json();
      return {
        citing: data.referenced_works || [],
        citedBy: data.cited_by_count || 0
      };
    }
  }

  findRelatedStudies(recordId, depth = 1) {
    const related = new Set();
    const queue = [{ id: recordId, depth: 0 }];

    while (queue.length > 0) {
      const { id, depth: d } = queue.shift();
      if (d > depth) continue;

      const node = this.graph.get(id);
      if (!node) continue;

      [...node.citing, ...node.citedBy].forEach(relatedId => {
        if (!related.has(relatedId)) {
          related.add(relatedId);
          queue.push({ id: relatedId, depth: d + 1 });
        }
      });
    }

    return related;
  }

  visualize() {
    // Generate force-directed graph SVG
  }
}
```

**Features:**
- [ ] Automatic citation fetching via OpenAlex
- [ ] Citation graph visualization
- [ ] "Find related studies" button
- [ ] Snowball search support
- [ ] Citation metrics display

---

## P3: Real-Time Collaboration (Months 3-6)

### 3.1 Architecture Options

**Option A: Firebase Realtime Database (Recommended for MVP)**
```javascript
// Simple, no backend needed
import { initializeApp } from 'firebase/app';
import { getDatabase, ref, onValue, set } from 'firebase/database';

const db = getDatabase(app);

// Real-time sync
onValue(ref(db, `projects/${projectId}/records`), (snapshot) => {
  Store.dispatch('SET_RECORDS', snapshot.val());
});

// Write with conflict resolution
async function saveDecision(recordId, decision) {
  const path = `projects/${projectId}/decisions/${recordId}`;
  await set(ref(db, path), {
    ...decision,
    updatedBy: currentUser.id,
    updatedAt: Date.now()
  });
}
```

**Option B: Supabase (More control, SQL)**
```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(URL, KEY);

// Real-time subscriptions
supabase
  .channel('decisions')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'decisions' },
    payload => Store.dispatch('SYNC_DECISION', payload.new))
  .subscribe();
```

**Option C: Custom WebSocket Server (Full control)**
```javascript
// Server (Node.js)
const wss = new WebSocketServer({ port: 8080 });
const rooms = new Map(); // projectId → Set<ws>

wss.on('connection', (ws, req) => {
  const projectId = req.url.split('/')[1];
  if (!rooms.has(projectId)) rooms.set(projectId, new Set());
  rooms.get(projectId).add(ws);

  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    // Broadcast to all in room
    rooms.get(projectId).forEach(client => {
      if (client !== ws) client.send(data);
    });
  });
});
```

### 3.2 CRDT for Conflict-Free Merging
```javascript
// Use Yjs for CRDT
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

const ydoc = new Y.Doc();
const provider = new WebsocketProvider('wss://server.com', projectId, ydoc);

// Shared types
const yrecords = ydoc.getArray('records');
const ydecisions = ydoc.getMap('decisions');

// Observe changes
ydecisions.observe(event => {
  event.changes.keys.forEach((change, key) => {
    Store.dispatch('SYNC_DECISION', { id: key, decision: ydecisions.get(key) });
  });
});
```

### 3.3 Collaboration UI
- [ ] User presence indicators (avatars on records being viewed)
- [ ] Real-time cursor positions
- [ ] Activity feed ("John included record #42")
- [ ] Conflict resolution UI
- [ ] Team management (invite, roles)
- [ ] Comments/annotations per record

**Acceptance Criteria:**
- [ ] < 100ms sync latency
- [ ] Works offline (queues changes)
- [ ] Handles 10+ concurrent users
- [ ] No data loss on conflicts

---

## P4: Mobile UX Improvements (Weeks 8-10)

### 4.1 Responsive Layout Redesign
```css
/* Mobile-first approach */
@media (max-width: 768px) {
  .app {
    display: flex;
    flex-direction: column;
  }

  .panel {
    position: fixed;
    inset: 0;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 100;
  }

  .panel.active {
    transform: translateX(0);
  }

  .mobile-nav {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: var(--bg-header);
    z-index: 101;
  }
}
```

### 4.2 Touch Gestures
```javascript
class SwipeHandler {
  constructor(element, options) {
    this.element = element;
    this.threshold = options.threshold || 50;
    this.onSwipeLeft = options.onSwipeLeft;
    this.onSwipeRight = options.onSwipeRight;

    element.addEventListener('touchstart', this.onTouchStart.bind(this));
    element.addEventListener('touchend', this.onTouchEnd.bind(this));
  }

  onTouchStart(e) {
    this.startX = e.touches[0].clientX;
  }

  onTouchEnd(e) {
    const diff = e.changedTouches[0].clientX - this.startX;
    if (Math.abs(diff) > this.threshold) {
      if (diff > 0) this.onSwipeRight?.();
      else this.onSwipeLeft?.();
    }
  }
}

// Usage: swipe to include/exclude
new SwipeHandler(recordCard, {
  onSwipeRight: () => makeDecision('include'),
  onSwipeLeft: () => makeDecision('exclude')
});
```

### 4.3 Mobile Features
- [ ] Bottom sheet for record details
- [ ] Swipe gestures for decisions
- [ ] Pull-to-refresh
- [ ] Haptic feedback
- [ ] Offline indicator
- [ ] PWA support (manifest, service worker)

---

## Implementation Roadmap

| Phase | Weeks | Focus | Deliverables |
|-------|-------|-------|--------------|
| **1** | 1-3 | Performance | Web Workers, IndexedDB, Virtual Scrolling |
| **2** | 4-6 | Architecture | Module system, State management |
| **3** | 6-8 | Testing | Unit tests, Integration tests, CI |
| **4** | 8-10 | Intelligence | Duplicate detection, Smart suggestions |
| **5** | 10-12 | Mobile | Responsive redesign, Touch gestures, PWA |
| **6** | 12-20 | Collaboration | Backend choice, CRDT, Real-time UI |

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Max records without lag | ~5,000 | 100,000+ |
| Meta-analysis (100 studies) | UI blocks ~2s | Background, 0ms block |
| Memory usage (10k records) | ~300MB | ~100MB |
| Lighthouse Performance | ~70 | 95+ |
| Lighthouse Accessibility | ~90 | 100 |
| Mobile usability score | ~60 | 95+ |
| Test coverage | 0% | 80%+ |
| Time to first screen | ~2s | < 500ms |

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Single-file philosophy broken | High | Build system preserves single-file output |
| Collaboration adds complexity | Medium | Start with Firebase (simple), migrate later |
| Breaking changes | High | Semantic versioning, migration scripts |
| Performance regression | Medium | Automated benchmarks in CI |

---

## Next Steps

1. **Immediate (This Week):**
   - Set up build system skeleton
   - Create Web Worker prototype for meta-analysis

2. **Short-term (Weeks 2-4):**
   - Implement full IndexedDB migration
   - Add Vitest for unit testing

3. **Medium-term (Months 2-3):**
   - Complete modularization
   - Implement enhanced duplicate detection
   - Mobile responsive redesign

4. **Long-term (Months 4-6):**
   - Choose and implement collaboration backend
   - Beta test with real teams
