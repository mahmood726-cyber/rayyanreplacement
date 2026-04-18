# Screenr v10.1 → v12.0 Improvement Plan

**Document:** Strategic Roadmap for Continued Development
**Date:** 2026-01-31
**Current Version:** 10.1 (915 KB, 570 functions, 31+ validation tests)
**Target:** v12.0 - The Definitive Systematic Review Platform

---

## Executive Summary

This plan outlines 50+ improvements across 6 phases to transform Screenr from an excellent tool into the definitive systematic review platform. Priorities are based on:
1. User impact (time saved, errors prevented)
2. Methodological rigor (statistical accuracy)
3. Competitive differentiation (unique features)
4. Implementation feasibility (single HTML file constraint)

---

## Phase 1: Immediate Priorities (1-2 Weeks)

### 1.1 Multi-Registry Search Integration
**Impact:** High | **Effort:** Medium

| Registry | API/Method | Status |
|----------|------------|--------|
| WHO ICTRP | Web scraping | To implement |
| EUCTR (EU) | API available | To implement |
| ANZCTR (Australia/NZ) | API available | To implement |
| ISRCTN | API available | To implement |
| ChiCTR (China) | Limited API | To implement |

**Implementation:**
```javascript
const RegistrySearch = {
  registries: ['CT.gov', 'ICTRP', 'EUCTR', 'ANZCTR', 'ISRCTN'],
  async searchAll(condition) { /* unified search */ },
  deduplicate(results) { /* cross-registry deduplication */ }
};
```

**Deliverables:**
- [ ] WHO ICTRP search adapter
- [ ] EUCTR search adapter
- [ ] Cross-registry deduplication (NCT/EUCTR/ISRCTN ID matching)
- [ ] Unified results view with source tagging

### 1.2 PROSPERO Integration
**Impact:** High | **Effort:** Low

- [ ] PROSPERO protocol search
- [ ] Import PROSPERO registration data
- [ ] Link review to PROSPERO ID
- [ ] Export PROSPERO-compatible protocol

### 1.3 Enhanced PRISMA Generator
**Impact:** Medium | **Effort:** Low

- [ ] Editable box values before export
- [ ] Multiple PRISMA templates (PRISMA-S, PRISMA-ScR, PRISMA-DTA)
- [ ] LaTeX/TikZ export for academic papers
- [ ] Interactive HTML version with hover details

### 1.4 Search Strategy Documentation
**Impact:** Medium | **Effort:** Low

- [ ] Auto-generate Methods section text
- [ ] Search date/database documentation
- [ ] PRESS 2015 checklist compliance
- [ ] Export search log for appendix

---

## Phase 2: Statistical Methods Expansion (2-4 Weeks)

### 2.1 Individual Patient Data (IPD) Meta-Analysis
**Impact:** High | **Effort:** High

| Component | Implementation |
|-----------|----------------|
| One-stage model | Mixed-effects regression |
| Two-stage model | Study-level then pooled |
| IPD + AD combination | Riley hybrid approach |
| Subgroup interactions | Patient-level covariates |

**Reference:** Riley RD et al. (2010). Meta-analysis of individual participant data. BMJ 340:c221

### 2.2 Time-to-Event Meta-Analysis
**Impact:** High | **Effort:** Medium

- [ ] Hazard ratio pooling (log HR, SE)
- [ ] Kaplan-Meier curve digitization (from images)
- [ ] Parmar method for HR estimation
- [ ] Survival curve meta-analysis

**Reference:** Parmar MKB et al. (1998). Extracting summary statistics. Stat Med 17:2815-2834

### 2.3 Proportion Meta-Analysis
**Impact:** Medium | **Effort:** Low

- [ ] Freeman-Tukey double arcsine transformation
- [ ] Logit transformation
- [ ] Exact binomial CIs
- [ ] Prediction intervals for proportions

### 2.4 Correlation Meta-Analysis
**Impact:** Medium | **Effort:** Low

- [ ] Fisher's z transformation
- [ ] Back-transformation to r
- [ ] Heterogeneity in correlations

### 2.5 Standardized Mean Difference Variants
**Impact:** Medium | **Effort:** Low

- [ ] Hedges' g (small sample correction) ✓ (verify)
- [ ] Glass's delta (control SD only)
- [ ] Cohen's d variants
- [ ] Conversion between effect sizes (d ↔ OR ↔ r)

### 2.6 Crossover Trial Analysis
**Impact:** Medium | **Effort:** Medium

- [ ] Proper SE calculation for crossover designs
- [ ] Carryover effect testing
- [ ] Period effect adjustment

### 2.7 Cluster RCT Adjustment
**Impact:** Medium | **Effort:** Medium

- [ ] Design effect calculation
- [ ] ICC-based adjustment
- [ ] Effective sample size

---

## Phase 3: AI/ML Enhancement (4-6 Weeks)

### 3.1 GPT-Powered Abstract Screening
**Impact:** Very High | **Effort:** Medium

- [ ] Local LLM integration (Ollama/llama.cpp)
- [ ] Zero-shot classification with prompts
- [ ] Inclusion probability scoring
- [ ] Reasoning explanation for decisions
- [ ] Human-in-the-loop validation

**Implementation:**
```javascript
const AIScreener = {
  async classifyAbstract(title, abstract, criteria) {
    const prompt = `Given PICO: ${criteria}\nClassify: ${title}\n${abstract}`;
    return await localLLM.generate(prompt);
  }
};
```

### 3.2 Automated Data Extraction
**Impact:** Very High | **Effort:** High

- [ ] PDF text extraction (PDF.js)
- [ ] Table detection and parsing
- [ ] Named entity recognition for PICO elements
- [ ] Numeric outcome extraction
- [ ] Source highlighting in PDF

### 3.3 Risk of Bias Auto-Assessment
**Impact:** High | **Effort:** Medium

- [ ] RoB 2.0 signaling question suggestions
- [ ] Text highlighting for RoB evidence
- [ ] Confidence scores for each domain
- [ ] Domain-specific reasoning

### 3.4 Smart Duplicate Detection
**Impact:** Medium | **Effort:** Low

- [ ] Enhanced Jaro-Winkler with title normalization
- [ ] DOI/PMID exact matching
- [ ] Author name fuzzy matching
- [ ] Combine multiple signals (ensemble)

### 3.5 Citation Chaining
**Impact:** Medium | **Effort:** Medium

- [ ] Forward citation search (Semantic Scholar API)
- [ ] Backward reference extraction
- [ ] Citation network visualization
- [ ] "Similar articles" recommendations

---

## Phase 4: Collaboration Features (6-8 Weeks)

### 4.1 Real-Time Collaboration
**Impact:** Very High | **Effort:** High

- [ ] WebRTC peer-to-peer sync
- [ ] Conflict resolution for simultaneous edits
- [ ] User presence indicators
- [ ] Chat/comments on records

**Architecture:**
```
[User A Browser] ←→ WebRTC ←→ [User B Browser]
         ↓                           ↓
    [IndexedDB]                 [IndexedDB]
         ↓                           ↓
    [Optional Cloud Sync via WebSocket Server]
```

### 4.2 Cloud Sync (Optional)
**Impact:** High | **Effort:** Medium

- [ ] Firebase/Supabase integration (user-provided credentials)
- [ ] End-to-end encryption option
- [ ] Selective sync (include/exclude decisions only)
- [ ] Offline-first with background sync

### 4.3 Team Management
**Impact:** Medium | **Effort:** Medium

- [ ] Role-based permissions (Admin, Screener, Viewer)
- [ ] Screening assignment/workload distribution
- [ ] Progress dashboards per team member
- [ ] Activity audit log

### 4.4 Review Protocol Builder
**Impact:** Medium | **Effort:** Low

- [ ] Guided PICO/SPIDER definition
- [ ] Eligibility criteria templates
- [ ] Search strategy planning
- [ ] Export to PROSPERO format

---

## Phase 5: Advanced Reporting (8-10 Weeks)

### 5.1 Automated Results Section
**Impact:** High | **Effort:** Medium

- [ ] Template-based narrative generation
- [ ] Statistical results formatting (APA/Vancouver)
- [ ] Automatic figure/table numbering
- [ ] Citation management integration

### 5.2 Interactive Dashboard
**Impact:** Medium | **Effort:** Medium

- [ ] Screening progress over time
- [ ] IRR trends
- [ ] Effect size evolution (cumulative MA)
- [ ] Exportable summary statistics

### 5.3 Publication-Ready Figures
**Impact:** High | **Effort:** Medium

- [ ] High-DPI forest plot export (300+ DPI)
- [ ] Customizable themes (journal-specific)
- [ ] Figure legends auto-generation
- [ ] TIFF/EPS export for journals

### 5.4 Summary of Findings Tables
**Impact:** High | **Effort:** Medium

- [ ] GRADE evidence profiles
- [ ] GRADEpro-compatible export
- [ ] Plain language summaries
- [ ] Certainty of evidence visualization

### 5.5 Appendix Generator
**Impact:** Medium | **Effort:** Low

- [ ] Search strategies for all databases
- [ ] Full list of excluded studies with reasons
- [ ] Sensitivity analysis results
- [ ] Risk of bias justifications

---

## Phase 6: Platform Extensions (10-12 Weeks)

### 6.1 Scoping Review Mode
**Impact:** Medium | **Effort:** Medium

- [ ] PRISMA-ScR compliance
- [ ] Charting table templates
- [ ] Concept mapping visualization
- [ ] Gap analysis tools

### 6.2 Rapid Review Mode
**Impact:** Medium | **Effort:** Low

- [ ] Streamlined single-screener workflow
- [ ] Abbreviated extraction forms
- [ ] Quick GRADE (simplified)
- [ ] Time-limited search strategies

### 6.3 Umbrella Review Mode
**Impact:** Medium | **Effort:** Medium

- [ ] AMSTAR 2 quality assessment
- [ ] Overlap matrix (Pieper method)
- [ ] Evidence mapping across reviews
- [ ] Corrected covered area (CCA) calculation

### 6.4 Guideline Development Support
**Impact:** Medium | **Effort:** High

- [ ] GRADE-ADOLOPMENT workflow
- [ ] Evidence-to-decision frameworks
- [ ] Recommendation formulation
- [ ] Voting/consensus tools

### 6.5 Living Review Automation
**Impact:** High | **Effort:** Medium

Current: Basic Living SR
Enhanced:
- [ ] Automated weekly searches (Service Worker)
- [ ] Email/push notifications for new evidence
- [ ] Threshold-based update triggers
- [ ] Version control for review updates
- [ ] Change log generation

---

## Phase 7: Technical Improvements

### 7.1 Performance Optimization
**Target:** Handle k=10,000 studies smoothly

- [ ] Virtual scrolling for record list
- [ ] Web Workers for heavy computation
- [ ] IndexedDB pagination
- [ ] Lazy loading for large datasets

### 7.2 Accessibility (WCAG 2.1 AA)

- [ ] Screen reader compatibility
- [ ] Keyboard navigation throughout
- [ ] High contrast mode
- [ ] Focus indicators
- [ ] ARIA labels

### 7.3 Mobile Optimization

- [ ] Responsive screening interface
- [ ] Touch-friendly buttons
- [ ] Swipe gestures (include/exclude)
- [ ] PWA with app-like experience

### 7.4 Testing Infrastructure

- [ ] Automated browser testing (Playwright)
- [ ] Statistical validation CI/CD
- [ ] Visual regression testing
- [ ] Performance benchmarking

---

## Validation Suite Expansion

### Target: 50 Validation Tests

| Category | Current | Target | New Tests |
|----------|---------|--------|-----------|
| τ² Estimators | 6 | 6 | — |
| Publication Bias | 7 | 10 | Selection models, Copas sensitivity |
| NMA | 5 | 8 | Component NMA, Threshold analysis |
| DTA | 3 | 5 | HSROC variants, Bivariate CIs |
| Bayesian | 2 | 4 | Prior sensitivity, Model comparison |
| IPD | 0 | 3 | One-stage, Two-stage, Hybrid |
| Survival | 0 | 2 | HR pooling, Curve synthesis |
| Proportions | 0 | 2 | Freeman-Tukey, Logit |
| Misc | 8 | 10 | Crossover, Cluster RCT |
| **Total** | **31** | **50** | **+19** |

---

## Citation Additions

### New References Needed

| Method | Reference |
|--------|-----------|
| IPD Meta-Analysis | Riley et al. 2010, Stewart & Parmar 1993 |
| Survival MA | Parmar et al. 1998, Tierney et al. 2007 |
| Proportion MA | Freeman & Tukey 1950, Barendregt et al. 2013 |
| Crossover Trials | Elbourne et al. 2002 |
| Cluster RCTs | Donner & Klar 2002 |
| Component NMA | Welton et al. 2009 |
| Umbrella Reviews | Pieper et al. 2014, AMSTAR 2 |

**Target: 50+ peer-reviewed citations**

---

## Competitive Positioning

### v12.0 vs Competitors

| Feature | Screenr v12 | Rayyan | Covidence | RevMan | DistillerSR |
|---------|-------------|--------|-----------|--------|-------------|
| Price | Free | Freemium | $$$$ | Free | $$$$ |
| Offline | Yes | No | No | Yes | No |
| Single file | Yes | No | No | No | No |
| Multi-registry search | Yes | No | No | No | No |
| AI screening | Yes | Yes | Yes | No | Yes |
| Full meta-analysis | Yes | No | No | Yes | No |
| IPD meta-analysis | Yes | No | No | No | No |
| Living SR automation | Yes | No | No | No | Partial |
| Real-time collab | Yes | Yes | Yes | No | Yes |
| GRADE automation | Yes | No | Partial | Yes | Partial |
| Built-in validation | Yes | No | No | No | No |

---

## Implementation Priority Matrix

```
                    HIGH IMPACT
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │  AI Screening      │  Multi-Registry    │
    │  IPD Meta-Analysis │  Real-Time Collab  │
    │  Auto Extraction   │  PROSPERO Integ    │
    │                    │                    │
LOW ├────────────────────┼────────────────────┤ HIGH
EFFORT                   │                    EFFORT
    │                    │                    │
    │  Proportion MA     │  Cloud Sync        │
    │  PRISMA Templates  │  Umbrella Review   │
    │  Search Docs       │  Guideline Support │
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                    LOW IMPACT
```

**Recommended Order:**
1. Multi-Registry Search (High Impact, Medium Effort)
2. PROSPERO Integration (High Impact, Low Effort)
3. AI Screening (Very High Impact, Medium Effort)
4. IPD Meta-Analysis (High Impact, High Effort)
5. Real-Time Collaboration (Very High Impact, High Effort)

---

## Version Roadmap

| Version | Features | Target Date | File Size |
|---------|----------|-------------|-----------|
| v10.2 | Multi-Registry, PROSPERO, Enhanced PRISMA | +2 weeks | ~950 KB |
| v11.0 | IPD MA, Survival MA, Proportion MA | +4 weeks | ~1.0 MB |
| v11.5 | AI Screening, Auto Extraction | +6 weeks | ~1.1 MB |
| v12.0 | Real-Time Collab, Cloud Sync, Full Suite | +12 weeks | ~1.2 MB |

---

## Success Metrics

| Metric | Current | v12.0 Target |
|--------|---------|--------------|
| Statistical methods | 46 | 60+ |
| Validation tests | 31 | 50 |
| Citations | 38 | 50+ |
| Search registries | 1 | 6 |
| Export formats | 7 | 12 |
| File size | 915 KB | <1.5 MB |
| Editorial rating | 5/5 | 5/5 + Innovation Award |

---

## Conclusion

This roadmap transforms Screenr from an excellent systematic review tool into the **definitive platform** for evidence synthesis. Key differentiators:

1. **Only tool with AI + full statistics** in a single offline file
2. **Only tool with multi-registry search** integrated
3. **Only tool with IPD meta-analysis** in browser
4. **Only tool with real-time collaboration** without cloud dependency
5. **Only tool with 50+ validation tests** against R packages

The single-file, offline-first architecture remains the core constraint and competitive advantage.

---

**Next Action:** Begin Phase 1.1 (Multi-Registry Search) implementation.
