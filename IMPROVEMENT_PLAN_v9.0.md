# Screenr v9.0+ Improvement and Validation Plan

**Date:** 2026-01-31
**Current Version:** 8.0 (716 KB, 30 citations, 18 validation tests)
**Planning Horizon:** v9.0, v10.0

---

## Part 1: Gap Analysis

### 1.1 Current Capabilities (v8.0)

| Category | Features | Status |
|----------|----------|--------|
| τ² Estimators | DL, REML, PM, SJ, HE, EB | ✓ Complete |
| Core MA | HKSJ, I² CI, H², prediction intervals | ✓ Complete |
| Meta-Regression | Single covariate, bubble plots | ✓ Basic |
| Publication Bias | Egger, Begg, T&F, PET-PEESE, Z-Curve, 3PSM | ✓ Comprehensive |
| NMA | Contrast-based, SUCRA, P-scores, inconsistency | ✓ Good |
| DTA | Bivariate pooling, SROC | ✓ Basic |
| Bayesian | Gibbs, Rhat, ESS, multiple chains | ✓ Good |
| Validation | 18 tests, 4 datasets | ✓ Good |

### 1.2 Identified Gaps

#### HIGH PRIORITY

| Gap | Impact | Complexity | Target |
|-----|--------|------------|--------|
| Multivariate meta-regression | Explains more heterogeneity | Medium | v9.0 |
| Robust variance estimation | Handles correlated effects | High | v9.0 |
| HSROC model for DTA | Alternative parameterization | Medium | v9.0 |
| CINeMA framework | NMA confidence assessment | Medium | v9.0 |
| Trace plots for Bayesian | Visual MCMC diagnostics | Low | v9.0 |
| More validation tests | Quality assurance | Medium | v9.0 |

#### MEDIUM PRIORITY

| Gap | Impact | Complexity | Target |
|-----|--------|------------|--------|
| Network meta-regression | Covariates in NMA | High | v9.0 |
| Contribution matrix | NMA transparency | Medium | v9.0 |
| Copas selection model | Sensitivity analysis | High | v10.0 |
| p-uniform* | Publication bias | Medium | v10.0 |
| Dose-response MA | Non-linear effects | High | v10.0 |
| Multivariate MA | Multiple outcomes | High | v10.0 |

#### LOWER PRIORITY

| Gap | Impact | Complexity | Target |
|-----|--------|------------|--------|
| IPD meta-analysis | Individual data | Very High | v10.0+ |
| Living SR support | Auto-updates | High | v10.0+ |
| Component NMA | Complex interventions | Very High | v10.0+ |
| Bayesian NMA | Full Bayesian network | Very High | v10.0+ |

---

## Part 2: v9.0 Roadmap

### Phase 1: Enhanced Meta-Regression (Week 1-2)

#### 1.1 Multiple Covariates
```javascript
function multipleMetaRegression(effects, ses, covariates, method = 'random') {
  // Model: θᵢ = β₀ + β₁x₁ᵢ + β₂x₂ᵢ + ... + εᵢ
  // Weighted least squares with matrix operations
  // Returns: coefficients, SEs, p-values, QM, QE, R²
}
```

**Features:**
- Up to 5 continuous/categorical covariates
- Automatic dummy coding for categorical
- Omnibus test (QM) for all moderators
- Individual coefficient tests
- Model comparison (AIC/BIC)

#### 1.2 Categorical Moderator Analysis
```javascript
function categoricalModerator(effects, ses, groups) {
  // Subgroup analysis with between-group Q test
  // Within-group heterogeneity
  // Mixed-effects model option
}
```

#### 1.3 Permutation Tests
```javascript
function permutationTest(effects, ses, covariate, nPerms = 1000) {
  // Non-parametric test for moderator significance
  // Handles non-normality and small samples
}
```

**Reference:** Higgins & Thompson (2004). Stat Med 23:1663-1682

### Phase 2: Robust Variance Estimation (Week 2-3)

#### 2.1 Sandwich Estimator
```javascript
function robustVarianceEstimation(effects, ses, clusterVar) {
  // Handles correlated effects within studies
  // CR0, CR1, CR2 corrections
  // Small-sample adjustments (Satterthwaite df)
}
```

**Features:**
- Cluster-robust standard errors
- Multiple effect sizes per study
- Satterthwaite degrees of freedom
- Works with meta-regression

**Reference:** Hedges, Tipton & Johnson (2010). Res Synth Methods 1:39-65

#### 2.2 Working Correlation Models
```javascript
const correlationStructures = {
  independent: () => identity,
  exchangeable: (rho) => compound_symmetry,
  hierarchical: (rho_within, rho_between) => nested
};
```

### Phase 3: HSROC Model for DTA (Week 3-4)

#### 3.1 Hierarchical Summary ROC
```javascript
function hsrocModel(studies) {
  // Parameters: Θ (accuracy), Λ (threshold), β (asymmetry)
  // Alternative to bivariate Reitsma model
  // Better for threshold variation
  return {
    theta: accuracy,
    lambda: threshold,
    beta: asymmetry,
    sigma2_theta: variance_accuracy,
    sigma2_alpha: variance_threshold,
    auc: area_under_curve
  };
}
```

**Reference:** Rutter & Gatsonis (2001). Stat Med 20:2865-2884

#### 3.2 Model Comparison
```javascript
function compareDTAModels(studies) {
  const bivariate = bivariateDTA(studies);
  const hsroc = hsrocModel(studies);
  return {
    bivariate,
    hsroc,
    equivalence: checkEquivalence(bivariate, hsroc),
    recommendation: selectModel(bivariate, hsroc)
  };
}
```

### Phase 4: CINeMA Framework (Week 4-5)

#### 4.1 Confidence in Network Meta-Analysis
```javascript
function cinemaAssessment(network, nmaResult) {
  // Six domains per GRADE-NMA
  return {
    withinStudyBias: assessWithinStudyBias(network),
    reportingBias: assessReportingBias(network),
    indirectness: assessIndirectness(network),
    imprecision: assessImprecision(nmaResult),
    heterogeneity: assessHeterogeneity(nmaResult),
    incoherence: assessIncoherence(nmaResult),
    overall: calculateOverallConfidence()
  };
}
```

**Reference:** Nikolakopoulou et al. (2020). PLoS Med 17:e1003082

#### 4.2 Contribution Matrix
```javascript
function contributionMatrix(network) {
  // How much each direct comparison contributes to each network estimate
  // Identifies influential studies
  // Transparency for NMA results
}
```

**Reference:** Papakonstantinou et al. (2018). F1000Research 7:610

### Phase 5: Enhanced Bayesian Diagnostics (Week 5-6)

#### 5.1 Trace Plots
```javascript
function generateTracePlotSVG(chains, parameter) {
  // Visual inspection of MCMC convergence
  // Multiple chains overlaid
  // Burn-in period marked
}
```

#### 5.2 Additional Diagnostics
```javascript
function gewekeDiagnostic(samples) {
  // Compare first 10% vs last 50%
  // Z-test for equality of means
}

function heidelbergerWelch(samples) {
  // Stationarity test
  // Halfwidth test for precision
}

function autocorrelationPlot(samples, maxLag = 50) {
  // ACF plot
  // Identifies mixing issues
}
```

#### 5.3 Prior Sensitivity Analysis
```javascript
function priorSensitivity(studies, priorSets) {
  // Run with multiple prior specifications
  // Compare posteriors
  // Identify robust conclusions
  const priors = [
    { tau: 'halfCauchy(0.5)' },
    { tau: 'halfCauchy(1.0)' },
    { tau: 'uniform(0, 2)' },
    { tau: 'halfNormal(0.5)' }
  ];
  return priors.map(p => bayesianMetaAnalysis(studies, p));
}
```

### Phase 6: Extended Validation (Week 6-7)

#### 6.1 Additional Test Cases

```javascript
const ExtendedValidationV9 = {
  // Existing tests (18)
  ...ExtendedValidationSuite,

  // New meta-regression tests
  testMultipleRegression: {
    dataset: 'bcg_with_covariates',
    check: 'Multiple coefficients, R²',
    reference: 'metafor::rma(mods = ~x1 + x2)'
  },

  // Robust variance tests
  testRobustSE: {
    dataset: 'correlated_effects',
    check: 'Cluster-robust SEs',
    reference: 'robumeta::robu()'
  },

  // HSROC tests
  testHSROC: {
    dataset: 'Dementia',
    check: 'Theta, Lambda, Beta parameters',
    reference: 'mada::madauni()'
  },

  // Additional Bayesian tests
  testGeweke: {
    check: 'Z-statistic within ±2',
    reference: 'coda::geweke.diag()'
  },

  // Edge cases
  testHighlyCorrelated: {
    input: 'effects with r=0.8',
    check: 'RVE handles correctly'
  },

  testSparseNetwork: {
    input: 'network with disconnected nodes',
    check: 'Graceful warning'
  },

  testExtremeHeterogeneity: {
    input: 'I² > 99%',
    check: 'Stable estimates'
  }
};
```

#### 6.2 Performance Benchmarks

```javascript
const PerformanceBenchmarks = {
  largeMA: {
    k: 1000,
    target: '< 2 seconds',
    test: () => timeExecution(calculateMetaAnalysis, largeDataset)
  },

  largeNMA: {
    treatments: 50,
    comparisons: 500,
    target: '< 5 seconds'
  },

  bayesianLong: {
    iterations: 50000,
    chains: 4,
    target: '< 30 seconds'
  },

  metaRegression: {
    k: 500,
    covariates: 5,
    target: '< 3 seconds'
  }
};
```

#### 6.3 Cross-Package Validation

| Test | metafor | meta | netmeta | mada | bayesmeta |
|------|---------|------|---------|------|-----------|
| DL τ² | ✓ | ✓ | - | - | - |
| REML τ² | ✓ | ✓ | - | - | - |
| Meta-regression | ✓ | ✓ | - | - | - |
| NMA effects | - | - | ✓ | - | - |
| DTA pooled | - | - | - | ✓ | - |
| Bayesian posterior | - | - | - | - | ✓ |

---

## Part 3: v10.0 Roadmap (Future)

### 3.1 Multivariate Meta-Analysis

```javascript
function multivariateMA(studies, outcomes, correlations) {
  // Multiple correlated outcomes per study
  // Generalized least squares
  // Borrowing strength across outcomes
}
```

**Reference:** Jackson et al. (2011). Stat Med 30:2481-2498

### 3.2 Dose-Response Meta-Analysis

```javascript
function doseResponseMA(studies, doses, effects) {
  // Restricted cubic splines
  // Non-linear relationships
  // Reference dose comparison
}
```

**Reference:** Crippa & Orsini (2016). BMC Med Res Methodol 16:91

### 3.3 Network Meta-Regression

```javascript
function networkMetaRegression(network, covariate) {
  // Covariate adjustment in NMA
  // Interaction with treatment effect
  // Handles effect modification
}
```

### 3.4 Copas Selection Model

```javascript
function copasSelectionModel(effects, ses, rho_range) {
  // Sensitivity analysis across selection correlation
  // Contour plot of adjusted estimates
}
```

**Reference:** Copas & Shi (2001). Biostatistics 2:247-262

### 3.5 Living Systematic Review

```javascript
const LivingSRFeatures = {
  scheduledSearch: {
    frequency: 'weekly|monthly',
    databases: ['PubMed', 'CENTRAL'],
    savedQuery: true
  },
  alerts: {
    newStudies: true,
    effectChange: { threshold: 0.1 },
    conclusionChange: true
  },
  cumulativeTracking: {
    effectOverTime: true,
    heterogeneityOverTime: true,
    trendAnalysis: true
  },
  versionControl: {
    snapshots: true,
    diffView: true,
    rollback: true
  }
};
```

---

## Part 4: Validation Plan

### 4.1 Test Coverage Targets

| Category | v8.0 | v9.0 Target | v10.0 Target |
|----------|------|-------------|--------------|
| Core MA | 10 | 12 | 15 |
| Meta-Regression | 0 | 5 | 8 |
| Publication Bias | 1 | 3 | 5 |
| NMA | 2 | 5 | 8 |
| DTA | 1 | 4 | 6 |
| Bayesian | 1 | 4 | 6 |
| RVE | 0 | 3 | 5 |
| Edge Cases | 3 | 8 | 12 |
| Performance | 0 | 4 | 6 |
| **Total** | **18** | **48** | **71** |

### 4.2 Reference Datasets to Add

| Dataset | Source | k | Purpose |
|---------|--------|---|---------|
| Berkey98 | metafor | 5 | Multivariate MA |
| Senn2013 | netmeta | 26 | Multi-arm NMA |
| Dogliotti | meta | 29 | Meta-regression |
| Colditz | metafor | 13 | RVE (multiple outcomes) |
| Schizophrenia | mada | 14 | HSROC |
| Antidepressants | Cipriani | 522 | Large NMA |

### 4.3 Numerical Precision Tests

```javascript
const PrecisionTests = {
  // Matrix operations
  matrixInversion: {
    condition: 'ill-conditioned matrix',
    check: 'stable inversion'
  },

  // Extreme values
  verySmallVariance: {
    input: 'SE = 0.0001',
    check: 'no overflow'
  },

  veryLargeEffect: {
    input: 'OR = 1000',
    check: 'log transform stable'
  },

  // Iterative algorithms
  remlConvergence: {
    input: 'difficult dataset',
    check: 'converges in < 100 iterations'
  },

  // Distribution functions
  chiSquareTails: {
    input: 'p = 0.00001, df = 100',
    check: 'accurate quantile'
  }
};
```

### 4.4 Validation Against Published Results

| Paper | Dataset | Statistic | Published | Target |
|-------|---------|-----------|-----------|--------|
| Higgins 2003 | Multiple | I² | Various | Match |
| IntHout 2014 | Migraine | HKSJ CI | Reported | Match |
| Stanley 2014 | Economics | PET-PEESE | Table 2 | Match |
| Bartoš 2022 | Psychology | Z-Curve | Figure 3 | Match |
| Nikolakopoulou 2020 | Network | CINeMA | Example | Match |

---

## Part 5: Implementation Priorities

### Immediate (v9.0 Alpha) — 3 weeks

| Feature | Effort | Impact |
|---------|--------|--------|
| Multiple meta-regression | Medium | High |
| Permutation tests | Low | Medium |
| Trace plots | Low | Medium |
| HSROC model | Medium | High |
| 15 new validation tests | Medium | High |

### Short-term (v9.0 Beta) — 3 weeks

| Feature | Effort | Impact |
|---------|--------|--------|
| Robust variance estimation | High | High |
| CINeMA framework | Medium | High |
| Contribution matrix | Medium | Medium |
| Prior sensitivity | Low | Medium |
| Performance benchmarks | Medium | Medium |

### Medium-term (v9.0 Release) — 2 weeks

| Feature | Effort | Impact |
|---------|--------|--------|
| Network meta-regression | High | Medium |
| Cross-package validation | Medium | High |
| Documentation update | Medium | High |
| Editorial review | Low | High |

---

## Part 6: Quality Metrics

### 6.1 Statistical Accuracy

| Metric | Target |
|--------|--------|
| Effect estimates | Within 0.1% of R packages |
| Standard errors | Within 0.5% |
| P-values | Within 0.001 |
| Confidence intervals | Correct coverage (95%) |

### 6.2 Performance

| Metric | Target |
|--------|--------|
| k=100 meta-analysis | < 1 second |
| k=500 meta-analysis | < 3 seconds |
| 20-treatment NMA | < 5 seconds |
| 10,000 iteration Bayesian | < 15 seconds |
| UI responsiveness | No freezing |

### 6.3 Code Quality

| Metric | Target |
|--------|--------|
| Test coverage | 100% of statistical functions |
| Documentation | Every method cited |
| Edge case handling | All graceful |
| File size | < 1 MB |

---

## Part 7: New References for v9.0

### Robust Variance Estimation
31. Hedges, L.V., Tipton, E. & Johnson, M.C. (2010). Robust variance estimation in meta-regression with dependent effect size estimates. *Research Synthesis Methods*, 1:39-65.
32. Tipton, E. (2015). Small sample adjustments for robust variance estimation with meta-regression. *Psychological Methods*, 20:375-393.

### HSROC Model
33. Rutter, C.M. & Gatsonis, C.A. (2001). A hierarchical regression approach to meta-analysis of diagnostic test accuracy evaluations. *Statistics in Medicine*, 20:2865-2884.
34. Harbord, R.M. & Whiting, P. (2009). metandi: Meta-analysis of diagnostic accuracy using hierarchical logistic regression. *Stata Journal*, 9:211-229.

### CINeMA Framework
35. Nikolakopoulou, A., Higgins, J.P.T., Papakonstantinou, T. et al. (2020). CINeMA: An approach for assessing confidence in the results of a network meta-analysis. *PLoS Medicine*, 17:e1003082.
36. Papakonstantinou, T., Nikolakopoulou, A., Higgins, J.P.T. et al. (2018). CINeMA: Software for semiautomated assessment of the confidence in the results of network meta-analysis. *Campbell Systematic Reviews*, 14:e1080.

### Multivariate Meta-Analysis
37. Jackson, D., Riley, R. & White, I.R. (2011). Multivariate meta-analysis: Potential and promise. *Statistics in Medicine*, 30:2481-2498.

### Dose-Response
38. Crippa, A. & Orsini, N. (2016). Dose-response meta-analysis of differences in means. *BMC Medical Research Methodology*, 16:91.

---

## Part 8: Success Criteria

### v9.0 Release Criteria

| Criterion | Requirement |
|-----------|-------------|
| Validation tests | 48/48 pass |
| Performance | All benchmarks met |
| Documentation | 38 citations |
| File size | < 850 KB |
| Browser testing | Chrome, Firefox, Safari, Edge |
| Editorial review | Accept recommendation |

### Feature Completeness

| Feature | v8.0 | v9.0 | Gain |
|---------|------|------|------|
| τ² estimators | 6 | 6 | — |
| Publication bias methods | 6 | 7 | +1 (Copas sensitivity) |
| NMA features | 5 | 8 | +3 |
| DTA features | 3 | 5 | +2 |
| Bayesian diagnostics | 3 | 6 | +3 |
| Meta-regression | Basic | Full | Major |
| Validation tests | 18 | 48 | +30 |

---

## Summary

### v9.0 Focus Areas
1. **Multiple meta-regression** — Most requested enhancement
2. **Robust variance estimation** — Handles real-world correlated data
3. **HSROC model** — Complete DTA capability
4. **CINeMA framework** — NMA confidence assessment
5. **Enhanced Bayesian diagnostics** — Visual convergence tools
6. **Comprehensive validation** — 48 tests, multiple packages

### Key Differentiators to Maintain
- Single-file, offline-first architecture
- Built-in validation against R packages
- Appropriate limitation notes
- Publication-ready documentation
- Zero dependencies

### Risk Mitigation
- Incremental feature addition with testing
- Maintain backward compatibility
- Performance monitoring
- File size limits

---

**Document prepared for Screenr v9.0 development**
**2026-01-31**
