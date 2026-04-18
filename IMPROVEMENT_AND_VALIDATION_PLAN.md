# Screenr v7.0 - Significant Improvements & Validation Plan

**Date:** 2026-01-31
**Target Version:** 7.0
**Status:** Planning

---

## Executive Summary

This plan outlines major enhancements and a rigorous validation framework to establish Screenr as the definitive open-source systematic review platform. The focus is on:

1. **Network Meta-Analysis** — Compare multiple treatments
2. **Diagnostic Test Accuracy** — Bivariate model and SROC curves
3. **Comprehensive Validation** — Against R packages with published test cases
4. **Performance Benchmarking** — Speed and accuracy metrics

---

## Part 1: Significant Improvements

### 1.1 Network Meta-Analysis (HIGH PRIORITY)

#### Rationale
NMA is increasingly required for health technology assessments and clinical guidelines. Currently no offline tool supports NMA.

#### Implementation Plan

**Phase 1: Data Structure**
```javascript
// Treatment network representation
class TreatmentNetwork {
  constructor() {
    this.treatments = new Map();  // treatment_id -> {name, type}
    this.comparisons = [];        // [{t1, t2, effect, se, study_id}]
    this.studies = new Map();     // study_id -> {design, comparisons[]}
  }

  addComparison(study, t1, t2, effect, se) { }
  getDirectEvidence(t1, t2) { }
  getIndirectEvidence(t1, t2) { }
  buildDesignMatrix() { }
}
```

**Phase 2: Statistical Model**
```javascript
// Contrast-based NMA (frequentist)
function networkMetaAnalysis(network, reference) {
  // 1. Build design matrix X for contrasts
  // 2. Fit multivariate random-effects model
  // 3. Estimate all pairwise contrasts
  // 4. Calculate SUCRA/P-scores

  return {
    leagueTable: allPairwiseEffects,
    sucra: treatmentRankings,
    pScores: probabilityScores,
    inconsistency: {
      global: designByTreatmentTest,
      local: nodeSplitting
    }
  };
}
```

**Phase 3: Consistency Assessment**
```javascript
// Node-splitting for local inconsistency
function nodeSplitting(network, contrast) {
  // Separate direct and indirect evidence
  // Test: direct - indirect = 0
  return {
    direct: { effect, se, ci },
    indirect: { effect, se, ci },
    difference: { effect, se, pValue }
  };
}

// Design-by-treatment interaction (global)
function designByTreatmentTest(network) {
  // Q statistic for inconsistency
  return { q, df, pValue };
}
```

**Phase 4: Visualizations**
- Network graph (D3.js force-directed)
- League table (heatmap with CI)
- Forest plot of all comparisons vs reference
- Rankogram (probability of each rank)
- SUCRA bar chart

**Validation Target:** Match R `netmeta` package output

#### Files to Create
| File | Purpose |
|------|---------|
| `nma.js` (embedded) | Core NMA algorithms |
| Network graph component | D3.js visualization |
| League table component | Interactive heatmap |

#### References
- Salanti G (2012). Stat Methods Med Res 21:301-324
- Rücker G, Schwarzer G (2015). Res Synth Methods 6:49-62
- Dias S et al. (2018). Network Meta-Analysis for Decision Making. Wiley

---

### 1.2 Diagnostic Test Accuracy Meta-Analysis (HIGH PRIORITY)

#### Rationale
DTA reviews require specialized bivariate models that account for the correlation between sensitivity and specificity.

#### Implementation Plan

**Phase 1: Data Entry**
```javascript
// 2x2 table input per study
const dtaStudy = {
  tp: truePositives,
  fp: falsePositives,
  fn: falseNegatives,
  tn: trueNegatives,
  // Derived
  sensitivity: tp / (tp + fn),
  specificity: tn / (tn + fp),
  threshold: cutoffValue  // optional
};
```

**Phase 2: Bivariate Model**
```javascript
// Reitsma bivariate model
function bivariateDTA(studies) {
  // Transform to logit scale
  const logitSe = studies.map(s => logit(s.sensitivity));
  const logitSp = studies.map(s => logit(s.specificity));

  // Fit bivariate random-effects model
  // Y ~ N(μ, Σ_within + Σ_between)

  return {
    pooledSensitivity: invLogit(muSe),
    pooledSpecificity: invLogit(muSp),
    pooledSensitivityCI: [...],
    pooledSpecificityCI: [...],
    correlation: rho,
    tau2Se: betweenStudyVarSe,
    tau2Sp: betweenStudyVarSp,
    srocCurve: generateSROC(mu, Sigma)
  };
}
```

**Phase 3: HSROC Model (Alternative)**
```javascript
// Hierarchical SROC model (Rutter & Gatsonis)
function hsrocModel(studies) {
  // Parameters: Λ (accuracy), Θ (threshold), β (asymmetry)
  return {
    lambda: accuracy,
    theta: thresholdEffect,
    beta: asymmetry,
    srocCurve: hsrocCurve
  };
}
```

**Phase 4: Visualizations**
- SROC plot with:
  - Individual study points (sized by N)
  - Summary operating point
  - 95% confidence region (ellipse)
  - 95% prediction region
  - SROC curve
- Coupled forest plots (Se and Sp side by side)
- Crosshairs plot

**Validation Target:** Match R `mada` package output

#### References
- Reitsma JB et al. (2005). J Clin Epidemiol 58:982-990
- Rutter CM, Gatsonis CA (2001). Stat Med 20:2865-2884
- Harbord RM et al. (2007). Biostatistics 8:239-251

---

### 1.3 Bayesian Meta-Analysis (MEDIUM PRIORITY)

#### Implementation Plan

**Phase 1: Prior Specification UI**
```javascript
const bayesianSettings = {
  effectPrior: { type: 'normal', mean: 0, sd: 10 },
  tau2Prior: { type: 'halfCauchy', scale: 0.5 },
  // Alternatives: halfNormal, uniform, inverseGamma
  nIterations: 10000,
  burnin: 1000,
  thin: 1
};
```

**Phase 2: MCMC Sampler (Gibbs)**
```javascript
function bayesianMA(studies, priors) {
  // Gibbs sampling for conjugate priors
  // Or Metropolis-Hastings for non-conjugate

  return {
    posteriorEffect: { mean, median, sd, ci95, hdi95 },
    posteriorTau2: { mean, median, sd, ci95 },
    posteriorSamples: samples,
    diagnostics: { rhat, ess, trace }
  };
}
```

**Phase 3: Prior Sensitivity**
- Compare results across different prior choices
- Visualize prior vs posterior

**Validation Target:** Match R `brms` or `bayesmeta` output

---

### 1.4 Advanced Publication Bias Methods (MEDIUM PRIORITY)

#### P-Curve Analysis
```javascript
function pCurveAnalysis(pValues) {
  // Test if p-curve is right-skewed (evidential value)
  const binomialTest = testRightSkew(pValues);
  const continuousTest = stoufferZ(pValues);

  return {
    evidentialValue: binomialTest.pValue < 0.05,
    inadequateEvidence: continuousTest.pValue > 0.05,
    pHacking: leftSkewed(pValues)
  };
}
```

#### Selection Models
```javascript
// Vevea-Hedges weight function model
function selectionModel(effects, ses, cutpoints = [0.05, 0.10]) {
  // Model publication probability as step function of p-value
  return {
    adjustedEffect: correctedPooled,
    selectionWeights: estimatedWeights,
    likelihoodRatioTest: lrt
  };
}
```

---

### 1.5 Living Systematic Review Support (MEDIUM PRIORITY)

#### Features
- Scheduled search updates (manual trigger in offline mode)
- Incremental screening queue
- Version control for analyses
- Change log / audit trail
- Alert for new studies matching criteria

```javascript
class LivingReview {
  constructor(reviewId) {
    this.versions = [];
    this.searchHistory = [];
    this.analysisSnapshots = [];
  }

  addSearchUpdate(date, newRecords) { }
  createSnapshot() { }
  compareVersions(v1, v2) { }
  generateChangeReport() { }
}
```

---

### 1.6 Individual Participant Data Support (LOWER PRIORITY)

#### Features
- IPD import (CSV with patient-level data)
- One-stage meta-analysis
- Two-stage meta-analysis
- Mixed IPD + aggregate data

---

## Part 2: Validation Framework

### 2.1 Validation Strategy

#### Levels of Validation

| Level | Description | Method |
|-------|-------------|--------|
| **Unit** | Individual functions | Jest/Mocha tests |
| **Integration** | Combined workflows | Selenium tests |
| **Statistical** | Against R packages | Published datasets |
| **Clinical** | Real-world reviews | Cochrane reproductions |

### 2.2 Reference Software

| Domain | R Package | Version | Citation |
|--------|-----------|---------|----------|
| Meta-Analysis | metafor | 4.4-0 | Viechtbauer 2010 |
| NMA | netmeta | 2.8-0 | Rücker 2020 |
| DTA | mada | 0.5.11 | Doebler 2015 |
| Bayesian | bayesmeta | 3.4 | Röver 2020 |
| IRR | irr | 0.84.1 | Gamer 2019 |

### 2.3 Test Datasets

#### Meta-Analysis Validation

**Dataset 1: Amlodipine Hypertension (metafor)**
```r
# R reference code
library(metafor)
data(dat.bcg)
res <- rma(yi, vi, data=dat.bcg, method="DL")
# Expected: b = -0.7145, se = 0.1798, tau2 = 0.3088
```

```javascript
// Screenr validation test
const bcgData = [
  { effect: -0.8893, se: 0.4614 },
  { effect: -1.5854, se: 0.3388 },
  // ... 13 studies
];
const result = calculateMetaAnalysis(bcgData);
assert(Math.abs(result.pooledEffect - (-0.7145)) < 0.001);
assert(Math.abs(result.tau2 - 0.3088) < 0.001);
```

**Dataset 2: HKSJ Adjustment Test**
```r
# R reference
res <- rma(yi, vi, data=dat.bcg, method="DL", test="knha")
# Expected: wider CI with t-distribution
```

**Dataset 3: Trim-and-Fill Test**
```r
library(metafor)
res <- rma(yi, vi, data=dat.bcg)
tf <- trimfill(res)
# Expected: k0 = X, adjusted effect = Y
```

#### Publication Bias Validation

**Dataset 4: Egger's Test**
```r
regtest(res, model="lm")
# Expected: z = X, p = Y
```

**Dataset 5: Begg's Test**
```r
ranktest(res)
# Expected: tau = X, p = Y
```

#### NMA Validation

**Dataset 6: Senn Network (netmeta)**
```r
library(netmeta)
data(Senn2013)
net <- netmeta(TE, seTE, treat1, treat2, studlab, data=Senn2013)
# Expected league table values
```

**Dataset 7: Parkinson Network**
```r
data(Franchini2012)
# Multi-arm trial handling
```

#### DTA Validation

**Dataset 8: Dementia Screening (mada)**
```r
library(mada)
data(Dementia)
fit <- reitsma(Dementia)
# Expected: pooled Se, Sp, correlation
```

**Dataset 9: AuditC (mada)**
```r
data(AuditC)
# SROC curve validation
```

### 2.4 Automated Validation Suite

```javascript
// validation_suite.js

const ValidationSuite = {
  datasets: {
    bcg: require('./data/bcg.json'),
    senn: require('./data/senn2013.json'),
    dementia: require('./data/dementia.json')
  },

  referenceResults: {
    bcg_dl: { effect: -0.7145, tau2: 0.3088, i2: 92.1 },
    bcg_reml: { effect: -0.7138, tau2: 0.3132 },
    bcg_hksj: { ciLo: -1.1965, ciHi: -0.2325 }
  },

  tolerances: {
    effect: 0.001,
    se: 0.001,
    tau2: 0.001,
    i2: 0.1,
    pValue: 0.001
  },

  runAll() {
    const results = [];
    results.push(this.testDerSimonianLaird());
    results.push(this.testREML());
    results.push(this.testHKSJ());
    results.push(this.testTrimAndFill());
    results.push(this.testEgger());
    results.push(this.testBegg());
    results.push(this.testI2CI());
    return results;
  },

  testDerSimonianLaird() {
    const data = this.prepareStudies(this.datasets.bcg);
    const result = calculateMetaAnalysis(data, { tau2Estimator: 'DL', useHKSJ: false });
    const ref = this.referenceResults.bcg_dl;

    return {
      name: 'DerSimonian-Laird',
      passed: Math.abs(result.pooledEffect - ref.effect) < this.tolerances.effect &&
              Math.abs(result.tau2 - ref.tau2) < this.tolerances.tau2,
      expected: ref,
      actual: { effect: result.pooledEffect, tau2: result.tau2, i2: result.i2 }
    };
  },

  // ... more tests
};
```

### 2.5 Validation Report Template

```markdown
# Screenr v7.0 Validation Report

## Summary
- Tests Run: 50
- Passed: 48
- Failed: 2
- Accuracy: 96%

## Meta-Analysis Validation

### DerSimonian-Laird
| Metric | Expected (metafor) | Actual (Screenr) | Difference | Status |
|--------|-------------------|------------------|------------|--------|
| Effect | -0.7145 | -0.7145 | 0.0000 | ✓ PASS |
| SE | 0.1798 | 0.1798 | 0.0000 | ✓ PASS |
| τ² | 0.3088 | 0.3088 | 0.0000 | ✓ PASS |
| I² | 92.1% | 92.1% | 0.0% | ✓ PASS |

### REML Estimator
...

### HKSJ Adjustment
...

## Publication Bias Validation
...

## NMA Validation
...

## DTA Validation
...

## Conclusion
Screenr v7.0 produces results consistent with R reference packages
within acceptable numerical tolerances (±0.001 for effects, ±0.1% for I²).
```

---

## Part 3: Implementation Roadmap

### Phase 1: Core NMA (8 weeks)

| Week | Task | Deliverable |
|------|------|-------------|
| 1-2 | Data structures | TreatmentNetwork class |
| 3-4 | Contrast-based model | Basic NMA function |
| 5 | Inconsistency tests | Node-splitting, Q-test |
| 6 | SUCRA/P-scores | Ranking functions |
| 7 | Visualizations | Network graph, league table |
| 8 | Validation | netmeta comparison |

### Phase 2: DTA Module (6 weeks)

| Week | Task | Deliverable |
|------|------|-------------|
| 1-2 | Bivariate model | reitsma() equivalent |
| 3 | HSROC model | Alternative parameterization |
| 4 | SROC visualization | Interactive plot |
| 5 | Meta-regression | Covariates for threshold |
| 6 | Validation | mada comparison |

### Phase 3: Validation Suite (4 weeks)

| Week | Task | Deliverable |
|------|------|-------------|
| 1 | Test datasets | 10 reference datasets |
| 2 | Automated tests | ValidationSuite class |
| 3 | Report generation | Markdown/HTML reports |
| 4 | CI integration | GitHub Actions workflow |

### Phase 4: Advanced Features (6 weeks)

| Week | Task | Deliverable |
|------|------|-------------|
| 1-2 | Bayesian MA | MCMC sampler |
| 3 | P-curve analysis | Evidential value tests |
| 4 | Selection models | Vevea-Hedges |
| 5-6 | Living SR support | Version control, snapshots |

---

## Part 4: Quality Assurance

### 4.1 Testing Requirements

| Test Type | Count | Coverage |
|-----------|-------|----------|
| Unit tests | 100+ | All statistical functions |
| Integration tests | 50+ | Full workflows |
| Validation tests | 30+ | R package comparison |
| Edge case tests | 20+ | Boundary conditions |

### 4.2 Performance Benchmarks

| Operation | Target | Measure |
|-----------|--------|---------|
| MA (10 studies) | <100ms | Time to result |
| MA (100 studies) | <500ms | Time to result |
| NMA (20 treatments) | <2s | Time to result |
| DTA (50 studies) | <1s | Time to result |
| Forest plot render | <200ms | DOM update |

### 4.3 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | Required |
| Firefox | 88+ | Required |
| Safari | 14+ | Required |
| Edge | 90+ | Required |

### 4.4 File Size Budget

| Component | Current | Target |
|-----------|---------|--------|
| Core HTML | 560KB | <800KB |
| With NMA | - | <900KB |
| With DTA | - | <950KB |
| Full v7.0 | - | <1MB |

---

## Part 5: Success Metrics

### 5.1 Accuracy Targets

| Method | Target | Validation |
|--------|--------|------------|
| Pairwise MA | ±0.001 vs metafor | 100% tests pass |
| NMA | ±0.01 vs netmeta | 95% tests pass |
| DTA | ±0.01 vs mada | 95% tests pass |
| Publication bias | ±0.001 vs metafor | 100% tests pass |

### 5.2 Feature Completeness

| Feature | v6.3 | v7.0 Target |
|---------|------|-------------|
| Pairwise MA | ✓ | ✓ |
| NMA | ✗ | ✓ |
| DTA bivariate | ✗ | ✓ |
| Bayesian | ✗ | ✓ |
| P-curve | ✗ | ✓ |
| Selection models | ✗ | ✓ |
| Living SR | ✗ | Partial |

### 5.3 Documentation

| Document | Status | Target |
|----------|--------|--------|
| User manual | Partial | Complete |
| Statistical appendix | Partial | Complete |
| Validation report | None | Full report |
| API reference | None | JSDoc |

---

## Part 6: Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| NMA complexity | High | Start with simple contrast model |
| Bivariate optimization | High | Use robust starting values |
| File size bloat | Medium | Lazy loading, minification |
| Browser performance | Medium | Web Workers for heavy computation |
| Numerical precision | Medium | Use established algorithms |

---

## Appendix: Reference Datasets

### A1: BCG Vaccine Trial Data (metafor)
```json
{
  "name": "BCG Vaccine Trials",
  "source": "dat.bcg from metafor",
  "studies": 13,
  "outcome": "Log Risk Ratio",
  "reference": "Colditz et al. (1994)"
}
```

### A2: Senn 2013 Diabetes Network (netmeta)
```json
{
  "name": "Senn Diabetes Network",
  "source": "Senn2013 from netmeta",
  "treatments": 10,
  "comparisons": 26,
  "reference": "Senn et al. (2013)"
}
```

### A3: Dementia Screening DTA (mada)
```json
{
  "name": "Dementia Screening Tests",
  "source": "Dementia from mada",
  "studies": 10,
  "outcome": "Sensitivity/Specificity",
  "reference": "Mitchell (2009)"
}
```

---

**Document Author:** Claude (AI Assistant)
**Last Updated:** 2026-01-31
**Next Review:** After Phase 1 completion
