# Screenr v8.0 Improvement and Validation Plan

**Date:** 2026-01-31
**Current Version:** 7.0
**Target Version:** 8.0

---

## Part 1: Gap Analysis

### 1.1 Core Meta-Analysis Gaps

| Gap | Priority | Impact | Complexity |
|-----|----------|--------|------------|
| Meta-regression | HIGH | Explains heterogeneity | Medium |
| More τ² estimators (PM, SJ, HE, EB) | MEDIUM | Research flexibility | Low |
| Robust variance estimation | MEDIUM | Correlated effects | High |
| Multivariate MA | LOW | Multiple outcomes | High |
| Dose-response MA | LOW | Non-linear effects | High |

### 1.2 Publication Bias Gaps

| Gap | Priority | Impact | Complexity |
|-----|----------|--------|------------|
| PET-PEESE | HIGH | Better bias correction | Low |
| Limit meta-analysis | MEDIUM | Small-study effects | Low |
| 3PSM (three-parameter selection) | MEDIUM | Formal selection model | Medium |
| Copas selection model | LOW | Sensitivity analysis | High |

### 1.3 Network Meta-Analysis Gaps

| Gap | Priority | Impact | Complexity |
|-----|----------|--------|------------|
| Design-by-treatment interaction | HIGH | Global inconsistency | Medium |
| Comparison-adjusted funnel plot | HIGH | NMA publication bias | Medium |
| Network meta-regression | MEDIUM | Covariates in NMA | High |
| Component NMA | LOW | Complex interventions | High |
| CINeMA framework | MEDIUM | Confidence assessment | Medium |

### 1.4 DTA Meta-Analysis Gaps

| Gap | Priority | Impact | Complexity |
|-----|----------|--------|------------|
| HSROC model | HIGH | Alternative to bivariate | Medium |
| Full bivariate GLMM | MEDIUM | Proper correlation | High |
| DTA meta-regression | MEDIUM | Covariates | High |
| Multiple thresholds | LOW | ROC meta-analysis | High |

### 1.5 Bayesian Analysis Gaps

| Gap | Priority | Impact | Complexity |
|-----|----------|--------|------------|
| Convergence diagnostics (Rhat, ESS) | HIGH | Quality assurance | Medium |
| Multiple chains | HIGH | Better mixing | Low |
| Trace plots | MEDIUM | Visual diagnostics | Low |
| Prior sensitivity analysis | MEDIUM | Robustness | Medium |
| Informative priors | LOW | Expert knowledge | Low |

### 1.6 Other Method Gaps

| Gap | Priority | Impact | Complexity |
|-----|----------|--------|------------|
| Z-curve 2.0 | MEDIUM | Alternative to P-curve | Medium |
| Power analysis | MEDIUM | Sample size planning | Low |
| Fragility index | LOW | Result robustness | Low |
| Living SR support | MEDIUM | Auto-updates | High |

### 1.7 Validation Gaps

| Gap | Priority | Impact |
|-----|----------|--------|
| NMA validation (vs netmeta) | HIGH | Method credibility |
| DTA validation (vs mada) | HIGH | Method credibility |
| Bayesian validation (vs bayesmeta) | HIGH | Method credibility |
| More reference datasets | MEDIUM | Broader coverage |
| Edge case testing | HIGH | Robustness |
| Numerical precision tests | MEDIUM | Accuracy |

---

## Part 2: Prioritized Roadmap

### Phase 1: Critical Improvements (v7.1)

#### 1.1 Meta-Regression
**Priority:** HIGH | **Effort:** Medium | **Impact:** HIGH

```javascript
function metaRegression(studies, covariate, weights = 'random') {
  // Weighted least squares regression
  // Model: θᵢ = β₀ + β₁xᵢ + εᵢ
  // Returns: β₀, β₁, SE, p-value, R², QM, QE
}
```

**Features:**
- Single continuous or categorical covariate
- Random-effects (method of moments)
- Bubble plot visualization
- Test for moderation (QM statistic)
- Residual heterogeneity (QE, I²res)

**Validation:** Compare to metafor::rma(mods = ~covariate)

#### 1.2 PET-PEESE
**Priority:** HIGH | **Effort:** Low | **Impact:** HIGH

```javascript
function petPeese(effects, ses) {
  // PET: θ = β₀ + β₁(SE) + ε
  // PEESE: θ = β₀ + β₁(SE²) + ε
  // Conditional: Use PET if PET p > 0.05, else PEESE
  return { pet, peese, conditional, recommendation };
}
```

**Reference:** Stanley & Doucouliagos (2014)

#### 1.3 Bayesian Convergence Diagnostics
**Priority:** HIGH | **Effort:** Medium | **Impact:** HIGH

```javascript
function calculateRhat(chains) {
  // Gelman-Rubin statistic
  // Between-chain variance / within-chain variance
}

function calculateESS(samples) {
  // Effective sample size
  // Accounts for autocorrelation
}

function generateTracePlot(samples) {
  // SVG trace plot for visual inspection
}
```

#### 1.4 NMA Global Inconsistency Test
**Priority:** HIGH | **Effort:** Medium | **Impact:** HIGH

```javascript
function designByTreatmentInteraction(network) {
  // Q statistic decomposition
  // Q_total = Q_heterogeneity + Q_inconsistency
  // Chi-square test for inconsistency
}
```

**Reference:** Higgins et al. (2012)

---

### Phase 2: Enhanced Methods (v7.2)

#### 2.1 HSROC Model for DTA
**Priority:** HIGH | **Effort:** Medium

```javascript
function hsrocModel(studies) {
  // Hierarchical SROC
  // Parameters: Θ (accuracy), Λ (threshold), β (shape)
  // Alternative parameterization to bivariate
}
```

**Reference:** Rutter & Gatsonis (2001)

#### 2.2 Comparison-Adjusted Funnel Plot
**Priority:** HIGH | **Effort:** Medium

```javascript
function nmaFunnelPlot(network, reference) {
  // Centered at comparison-specific pooled effect
  // Detects small-study effects in network
}
```

**Reference:** Chaimani et al. (2013)

#### 2.3 Additional τ² Estimators
**Priority:** MEDIUM | **Effort:** Low

```javascript
const tau2Estimators = {
  DL: derSimonianLaird,      // Current
  REML: remlEstimator,       // Current
  PM: pauleMandel,           // Add
  SJ: sidikJonkman,          // Add
  HE: hedgesEstimator,       // Add
  EB: empiricalBayes         // Add
};
```

#### 2.4 Z-Curve 2.0
**Priority:** MEDIUM | **Effort:** Medium

```javascript
function zCurve(zValues) {
  // Estimate replicability
  // Expected discovery rate (EDR)
  // Expected replication rate (ERR)
  // Soric's maximum false discovery rate
}
```

**Reference:** Bartoš & Schimmack (2022)

---

### Phase 3: Advanced Features (v8.0)

#### 3.1 Robust Variance Estimation
**Priority:** MEDIUM | **Effort:** High

```javascript
function robustVarianceEstimation(studies, clusterVar) {
  // Handles correlated effects within studies
  // Sandwich estimator
  // Small-sample corrections
}
```

**Reference:** Hedges, Tipton & Johnson (2010)

#### 3.2 CINeMA Framework
**Priority:** MEDIUM | **Effort:** Medium

```javascript
function cinemaAssessment(network) {
  // Confidence in Network Meta-Analysis
  // Six domains: within-study bias, reporting bias,
  // indirectness, imprecision, heterogeneity, incoherence
  return { domainRatings, overallConfidence };
}
```

**Reference:** Nikolakopoulou et al. (2020)

#### 3.3 Three-Parameter Selection Model
**Priority:** MEDIUM | **Effort:** Medium

```javascript
function threeParameterSelectionModel(effects, ses) {
  // ML estimation of:
  // μ (true effect), τ² (heterogeneity), η (selection)
  // Likelihood ratio test for selection
}
```

**Reference:** McShane et al. (2016)

#### 3.4 Living Systematic Review Support
**Priority:** MEDIUM | **Effort:** High

```javascript
const livingReviewFeatures = {
  scheduledSearch: true,      // Auto-run saved searches
  newStudyAlerts: true,       // Email/notification
  cumulativeMA: true,         // Track effect over time
  versionControl: true,       // Review history
  updateTriggers: true        // When to update
};
```

---

## Part 3: Comprehensive Validation Plan

### 3.1 Reference Datasets

| Dataset | Source | k | Use Case |
|---------|--------|---|----------|
| BCG vaccine | metafor::dat.bcg | 13 | Standard MA (current) |
| Antidepressants | Cipriani 2018 | 522 | NMA validation |
| Cochrane DTA | mada examples | varies | DTA validation |
| Smoking cessation | netmeta::smokingcessation | 24 | NMA validation |
| Senn 2013 | netmeta::Senn2013 | 26 | NMA (multi-arm) |
| Parkinson's | mada::Dementia | 10 | DTA validation |
| Amlodipine | metafor::dat.normand1999 | 9 | Bayesian validation |

### 3.2 Core MA Validation Tests

```javascript
const coreMAValidation = {
  // Test 1: DerSimonian-Laird
  testDL: {
    dataset: 'bcg',
    expected: { b: -0.7145, tau2: 0.3088, i2: 92.12 },
    tolerance: { b: 0.001, tau2: 0.001, i2: 0.1 },
    reference: 'metafor::rma(method="DL")'
  },

  // Test 2: REML
  testREML: {
    dataset: 'bcg',
    expected: { b: -0.7138, tau2: 0.3132 },
    tolerance: { b: 0.001, tau2: 0.001 },
    reference: 'metafor::rma(method="REML")'
  },

  // Test 3: HKSJ adjustment
  testHKSJ: {
    dataset: 'bcg',
    expected: { ciRatio: 1.5 }, // Approximate
    check: 'HKSJ CI wider than z-test CI',
    reference: 'metafor::rma(test="knha")'
  },

  // Test 4: I² confidence interval
  testI2CI: {
    dataset: 'bcg',
    expected: { i2Low: 88, i2High: 95 }, // Approximate
    check: 'CI contains point estimate',
    reference: 'metafor::confint()'
  },

  // Test 5: Prediction interval
  testPI: {
    dataset: 'bcg',
    check: 'Uses t-distribution with k-2 df',
    reference: 'metafor::predict()'
  },

  // Test 6: Egger's test
  testEgger: {
    dataset: 'bcg',
    expected: { intercept: -2.97, pValue: 0.001 },
    tolerance: { intercept: 0.1 },
    reference: 'metafor::regtest()'
  },

  // Test 7: Trim-and-Fill
  testTrimFill: {
    dataset: 'bcg',
    check: 'Returns k0, adjusted effect, filled studies',
    reference: 'metafor::trimfill()'
  }
};
```

### 3.3 NMA Validation Tests

```javascript
const nmaValidation = {
  // Test 1: Basic network
  testBasicNMA: {
    dataset: 'smokingcessation',
    expected: {
      // vs no contact
      individualCounseling: { effect: -0.39, se: 0.17 },
      groupCounseling: { effect: -0.56, se: 0.19 },
      selfHelp: { effect: -0.15, se: 0.12 }
    },
    tolerance: { effect: 0.05, se: 0.02 },
    reference: 'netmeta::netmeta()'
  },

  // Test 2: SUCRA rankings
  testSUCRA: {
    dataset: 'smokingcessation',
    check: 'Ranking order matches netmeta',
    reference: 'netmeta::netrank()'
  },

  // Test 3: Inconsistency
  testInconsistency: {
    dataset: 'Senn2013',
    check: 'Node-splitting identifies inconsistent comparisons',
    reference: 'netmeta::netsplit()'
  },

  // Test 4: League table
  testLeagueTable: {
    dataset: 'smokingcessation',
    check: 'All pairwise effects match netmeta',
    reference: 'netmeta::netleague()'
  }
};
```

### 3.4 DTA Validation Tests

```javascript
const dtaValidation = {
  // Test 1: Pooled estimates
  testPooledDTA: {
    dataset: 'Dementia',
    expected: {
      sensitivity: 0.91,
      specificity: 0.82
    },
    tolerance: { se: 0.02, sp: 0.02 },
    reference: 'mada::reitsma()'
  },

  // Test 2: SROC curve
  testSROC: {
    check: 'AUC within 0.02 of mada',
    reference: 'mada::SROCellipse()'
  },

  // Test 3: Correlation
  testCorrelation: {
    check: 'Correlation between logit(Se) and logit(Sp)',
    reference: 'mada::reitsma()$Psi'
  }
};
```

### 3.5 Bayesian Validation Tests

```javascript
const bayesianValidation = {
  // Test 1: Posterior mean
  testPosteriorMean: {
    dataset: 'bcg',
    expected: { muMean: -0.71, tau2Mean: 0.35 },
    tolerance: { mu: 0.05, tau2: 0.05 },
    reference: 'bayesmeta::bayesmeta()'
  },

  // Test 2: Credible intervals
  testCredibleIntervals: {
    check: '95% CrI contains true value in simulation',
    coverage: 0.95,
    nSimulations: 1000
  },

  // Test 3: Prior sensitivity
  testPriorSensitivity: {
    priors: [
      { tau: 'halfCauchy(0.5)' },
      { tau: 'halfCauchy(1.0)' },
      { tau: 'uniform(0, 2)' }
    ],
    check: 'Results stable across reasonable priors'
  }
};
```

### 3.6 Edge Case Tests

```javascript
const edgeCaseTests = {
  // Single study
  testK1: {
    input: [{ effect: 0.5, ciLo: 0.3, ciHi: 0.8 }],
    expected: 'Graceful handling, no pooling'
  },

  // Two studies
  testK2: {
    input: 2,
    check: 'τ² estimable, HKSJ applicable with df=1'
  },

  // Zero heterogeneity
  testTau0: {
    check: 'τ²=0 handled, no prediction interval'
  },

  // Very large heterogeneity
  testLargeTau: {
    check: 'I²≈100% handled correctly'
  },

  // Negative effects
  testNegativeEffects: {
    check: 'Log-transform only for ratio measures'
  },

  // Missing data
  testMissingData: {
    check: 'Studies with missing CI excluded gracefully'
  },

  // Extreme p-values
  testExtremePValues: {
    input: [0.00001, 0.99999],
    check: 'P-curve handles boundary values'
  }
};
```

### 3.7 Numerical Precision Tests

```javascript
const precisionTests = {
  // Chi-square quantile accuracy
  testChiSquare: {
    inputs: [[0.95, 10], [0.99, 50], [0.025, 100]],
    expected: [18.307, 76.154, 74.222],
    tolerance: 0.01
  },

  // Normal quantile accuracy
  testNormalQuantile: {
    inputs: [0.975, 0.995, 0.999],
    expected: [1.96, 2.576, 3.09],
    tolerance: 0.001
  },

  // t-distribution quantile
  testTQuantile: {
    inputs: [[0.975, 5], [0.975, 30], [0.975, 100]],
    expected: [2.571, 2.042, 1.984],
    tolerance: 0.001
  },

  // Log-transform precision
  testLogTransform: {
    input: { effect: 0.001, ciLo: 0.0001, ciHi: 0.01 },
    check: 'No underflow/overflow'
  }
};
```

### 3.8 Performance Tests

```javascript
const performanceTests = {
  // Large meta-analysis
  testLargeMA: {
    k: 500,
    target: '< 1 second'
  },

  // Large NMA
  testLargeNMA: {
    treatments: 20,
    comparisons: 100,
    target: '< 3 seconds'
  },

  // Bayesian with many iterations
  testBayesianPerformance: {
    iterations: 10000,
    target: '< 10 seconds'
  },

  // UI responsiveness
  testUIResponsive: {
    check: 'No UI freeze during calculations'
  }
};
```

---

## Part 4: Implementation Priorities

### Immediate (v7.1) — 2 weeks

| Feature | Effort | Files |
|---------|--------|-------|
| Meta-regression | Medium | screenr.html |
| PET-PEESE | Low | screenr.html |
| Bayesian Rhat/ESS | Medium | screenr.html |
| NMA global inconsistency | Medium | screenr.html |
| Extended validation suite | Medium | screenr.html |

### Short-term (v7.2) — 4 weeks

| Feature | Effort | Files |
|---------|--------|-------|
| HSROC model | Medium | screenr.html |
| Comparison-adjusted funnel | Medium | screenr.html |
| Additional τ² estimators | Low | screenr.html |
| Z-curve 2.0 | Medium | screenr.html |
| NMA validation tests | Medium | screenr.html |
| DTA validation tests | Medium | screenr.html |

### Medium-term (v8.0) — 8 weeks

| Feature | Effort | Files |
|---------|--------|-------|
| Robust variance estimation | High | screenr.html |
| CINeMA framework | Medium | screenr.html |
| 3-parameter selection model | Medium | screenr.html |
| Living SR support | High | screenr.html |
| Full validation suite | High | screenr.html |

---

## Part 5: Validation Infrastructure

### 5.1 Automated Test Runner

```javascript
const ValidationRunner = {
  datasets: {
    bcg: [...],           // 13 studies
    smoking: [...],       // 24 studies
    dementia: [...],      // 10 studies
    senn2013: [...]       // 26 studies
  },

  runAll() {
    const results = [];
    results.push(...this.runCoreMATests());
    results.push(...this.runNMATests());
    results.push(...this.runDTATests());
    results.push(...this.runBayesianTests());
    results.push(...this.runEdgeCaseTests());
    results.push(...this.runPrecisionTests());
    return this.generateReport(results);
  },

  generateReport(results) {
    const passed = results.filter(r => r.passed).length;
    const total = results.length;
    return {
      summary: `${passed}/${total} tests passed`,
      details: results,
      timestamp: new Date().toISOString()
    };
  }
};
```

### 5.2 Reference Data Format

```javascript
// datasets/bcg.json
{
  "name": "BCG Vaccine Trials",
  "source": "metafor::dat.bcg",
  "citation": "Colditz et al. (1994)",
  "k": 13,
  "studies": [
    { "yi": -0.8893, "vi": 0.2129, "year": 1948 },
    { "yi": -1.5854, "vi": 0.1148, "year": 1949 },
    // ...
  ],
  "expected": {
    "DL": { "b": -0.7145, "tau2": 0.3088, "i2": 92.12 },
    "REML": { "b": -0.7138, "tau2": 0.3132 },
    "egger": { "intercept": -2.97, "pValue": 0.001 }
  }
}
```

### 5.3 CI/CD Integration

```yaml
# .github/workflows/validate.yml
name: Statistical Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run validation suite
        run: node validate.js
      - name: Check all tests pass
        run: |
          if grep -q '"passed": false' results.json; then
            exit 1
          fi
```

---

## Part 6: Success Metrics

### 6.1 Validation Targets

| Category | Current | Target |
|----------|---------|--------|
| Core MA tests | 7/7 | 15/15 |
| NMA tests | 0 | 8/8 |
| DTA tests | 0 | 6/6 |
| Bayesian tests | 0 | 5/5 |
| Edge case tests | 0 | 10/10 |
| Precision tests | 0 | 8/8 |
| **Total** | **7** | **52** |

### 6.2 Feature Targets

| Category | Current | v7.1 | v7.2 | v8.0 |
|----------|---------|------|------|------|
| τ² estimators | 2 | 2 | 6 | 6 |
| Pub bias methods | 3 | 5 | 5 | 6 |
| NMA features | 4 | 5 | 6 | 7 |
| DTA features | 3 | 3 | 5 | 5 |
| Bayesian features | 4 | 6 | 6 | 7 |
| Validation tests | 7 | 20 | 35 | 52 |

### 6.3 Quality Targets

| Metric | Target |
|--------|--------|
| Numerical accuracy | Within 0.1% of R packages |
| Test coverage | 100% of statistical functions |
| Edge case handling | All graceful, no crashes |
| Performance | <3s for k=100 studies |
| Documentation | Every method cited |

---

## Part 7: References for New Methods

### Meta-Regression
1. Thompson SG, Higgins JPT (2002). How should meta-regression analyses be undertaken and interpreted? *Stat Med* 21:1559-1573.

### PET-PEESE
2. Stanley TD, Doucouliagos H (2014). Meta-regression approximations to reduce publication selection bias. *Res Synth Methods* 5:60-78.

### Z-Curve
3. Bartoš F, Schimmack U (2022). Z-curve 2.0: Estimating replication rates and discovery rates. *Meta-Psychology* 6.

### HSROC
4. Rutter CM, Gatsonis CA (2001). A hierarchical regression approach to meta-analysis of diagnostic test accuracy. *Stat Med* 20:2865-2884.

### Robust Variance
5. Hedges LV, Tipton E, Johnson MC (2010). Robust variance estimation in meta-regression. *Res Synth Methods* 1:39-65.

### CINeMA
6. Nikolakopoulou A, et al. (2020). CINeMA: An approach for assessing confidence in the results of a network meta-analysis. *PLoS Med* 17:e1003082.

### 3PSM
7. McShane BB, Böckenholt U, Hansen KT (2016). Adjusting for publication bias in meta-analysis. *Perspect Psychol Sci* 11:730-749.

---

## Summary

### Critical Path (v7.1)
1. Meta-regression ← Most requested missing feature
2. PET-PEESE ← Better publication bias correction
3. Bayesian diagnostics ← Required for credibility
4. NMA global inconsistency ← Essential for NMA validity
5. Extended validation ← NMA + DTA + Bayesian tests

### Key Differentiators to Maintain
- Offline-first, single-file architecture
- Built-in validation against R packages
- Appropriate limitation notes
- Complete SR workflow integration

### Risk Mitigation
- Add features incrementally with validation
- Maintain backward compatibility
- Keep file size reasonable (<1MB)
- Test on multiple browsers

---

**Document prepared for Screenr development roadmap**
**2026-01-31**
