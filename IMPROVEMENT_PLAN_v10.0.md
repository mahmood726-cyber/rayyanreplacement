# Screenr v10.0 Improvement and Validation Plan

**Date:** 2026-01-31
**Current Version:** 9.0 (767 KB, 34 citations, 28 validation tests)
**Target Version:** 10.0
**Planning Horizon:** v10.0, v11.0

---

## Executive Summary

Screenr v10.0 will extend the platform with advanced meta-analytic methods including multivariate meta-analysis, dose-response modeling, the Copas selection model, and the CINeMA framework for NMA confidence assessment. The validation suite will expand to 48+ tests with new reference datasets and performance benchmarks.

---

## Part 1: Current State (v9.0)

### 1.1 Implemented Features

| Category | Features | Tests |
|----------|----------|-------|
| Core MA | 6 τ² estimators, HKSJ, I² CI, H², prediction intervals | 10 |
| Meta-Regression | Single covariate, bubble plots | 1 |
| Publication Bias | Egger, Begg, T&F, PET-PEESE, Z-Curve, 3PSM | 4 |
| NMA | Contrast-based, SUCRA, P-scores, inconsistency, meta-regression | 3 |
| DTA | Bivariate, HSROC, SROC curves | 3 |
| Bayesian | Gibbs, Rhat, ESS, multiple chains | 1 |
| RVE | Sandwich estimator, Satterthwaite df | 2 |
| Living SR | Scheduled searches, Jaro-Winkler, cumulative MA | 2 |
| Edge Cases | k=1, k=2, τ²=0 | 2 |
| **Total** | **29 methods** | **28 tests** |

### 1.2 Identified Gaps for v10.0

| Gap | Impact | Complexity | Priority |
|-----|--------|------------|----------|
| Multiple meta-regression | High | Medium | P1 |
| Multivariate MA | High | High | P1 |
| Dose-response MA | Medium | High | P2 |
| Copas selection model | Medium | Medium | P2 |
| CINeMA framework | High | Medium | P1 |
| Trace plots (Bayesian) | Medium | Low | P2 |
| Contribution matrix (NMA) | Medium | Medium | P2 |
| Performance benchmarks | Medium | Low | P1 |
| Extended validation | High | Medium | P1 |

---

## Part 2: v10.0 Feature Roadmap

### Phase 1: Multiple Meta-Regression (Week 1-2)

#### 2.1.1 Multiple Covariates

```javascript
function multipleMetaRegression(effects, ses, covariates, options = {}) {
  // Model: θᵢ = β₀ + β₁x₁ᵢ + β₂x₂ᵢ + ... + βₚxₚᵢ + εᵢ
  // Design matrix X with intercept and p covariates
  // Weighted least squares: β = (X'WX)⁻¹X'Wy
  // Random effects: W = diag(1/(σᵢ² + τ²))

  return {
    coefficients: [],      // β₀, β₁, ..., βₚ
    standardErrors: [],    // SE for each coefficient
    tValues: [],           // t-statistics
    pValues: [],           // p-values
    QM: 0,                 // Omnibus test for moderators
    QMdf: p,               // Degrees of freedom
    QMp: 0,                // p-value for QM
    QE: 0,                 // Residual heterogeneity
    QEdf: k - p - 1,       // Residual df
    QEp: 0,                // p-value for QE
    R2: 0,                 // Pseudo R² (variance explained)
    tau2: 0,               // Residual τ²
    I2res: 0,              // Residual I²
    AIC: 0,                // Model comparison
    BIC: 0,
    vif: []                // Variance inflation factors
  };
}
```

**Features:**
- Up to 5 covariates (continuous or categorical)
- Automatic dummy coding for categorical variables
- Omnibus test (QM) for all moderators
- Individual coefficient Wald tests
- Model comparison (AIC/BIC)
- Variance inflation factors for collinearity
- Permutation test option for small samples

**Reference:** Higgins JPT, Thompson SG (2004). Stat Med 23:1663-1682

#### 2.1.2 Categorical Subgroup Analysis

```javascript
function categoricalModeratorAnalysis(effects, ses, groups, options = {}) {
  // Subgroup-specific pooled effects
  // Between-group heterogeneity (Q_between)
  // Within-group heterogeneity (Q_within per group)
  // Mixed-effects or fixed-effects subgroup model

  return {
    subgroups: [
      { name: 'Group A', k: 5, effect: 0.3, se: 0.1, ciLo: 0.1, ciHi: 0.5, tau2: 0.02, i2: 45 },
      // ...
    ],
    Qbetween: 0,           // Between-group Q
    Qbetweendf: g - 1,     // df = number of groups - 1
    Qbetweenp: 0,          // p-value
    Qwithin: 0,            // Total within-group Q
    Qwithindf: k - g,      // df
    interpretation: []
  };
}
```

**Reference:** Borenstein M et al. (2009). Introduction to Meta-Analysis, Chapter 19

### Phase 2: Multivariate Meta-Analysis (Week 2-4)

#### 2.2.1 Core Multivariate Model

```javascript
function multivariateMA(studies, outcomes, withinStudyCorr = 0.5) {
  // Multiple correlated outcomes per study
  // Model: y = Xβ + u + e
  // u ~ N(0, Σ_between), e ~ N(0, Σ_within)
  // Generalized least squares estimation

  return {
    pooledEffects: [],       // One per outcome
    varianceCovariance: [],  // Between-outcome covariance
    correlations: [],        // Between-outcome correlations
    borrowingStrength: 0,    // Efficiency gain from multivariate
    univariateComparison: [] // What univariate would give
  };
}
```

**Features:**
- 2-5 correlated outcomes per study
- User-specified or estimated within-study correlation
- Riley method for unknown correlations
- Comparison with univariate results
- Joint hypothesis tests

**Reference:** Jackson D, Riley R, White IR (2011). Stat Med 30:2481-2498

#### 2.2.2 Simplified Implementation

For browser feasibility, implement a simplified version:
- Assume common within-study correlation (user input)
- Use weighted least squares approximation
- Maximum 3 outcomes for computational efficiency

### Phase 3: Dose-Response Meta-Analysis (Week 4-5)

#### 2.3.1 Linear Dose-Response

```javascript
function linearDoseResponse(studies) {
  // Each study: { dose: [0, 10, 20], effect: [0, 0.3, 0.5], se: [...] }
  // Linear trend: effect = β × dose
  // Greenland-Longnecker method for correlated doses

  return {
    slope: 0,              // Effect per unit dose
    slopeSE: 0,
    slopeCILo: 0,
    slopeCIHi: 0,
    pTrend: 0,             // p-value for linear trend
    heterogeneity: { Q: 0, I2: 0, tau2: 0 }
  };
}
```

**Reference:** Greenland S, Longnecker MP (1992). Am J Epidemiol 135:1301-1309

#### 2.3.2 Non-Linear Dose-Response

```javascript
function nonLinearDoseResponse(studies, options = {}) {
  // Restricted cubic splines with 3-4 knots
  // Fractional polynomials as alternative
  // Test for non-linearity vs linear

  return {
    splineCoefficients: [],
    knots: [],
    predictedCurve: [],    // Points for plotting
    linearTest: { stat: 0, p: 0 },  // Test linearity
    optimalDose: null      // If applicable
  };
}
```

**Reference:** Crippa A, Orsini N (2016). BMC Med Res Methodol 16:91

### Phase 4: Copas Selection Model (Week 5-6)

#### 2.4.1 Sensitivity Analysis

```javascript
function copasSelectionModel(effects, ses, options = {}) {
  // Selection probability: P(selected) = Φ(γ₀ + γ₁/σᵢ)
  // Sensitivity analysis across γ₀, γ₁ grid
  // Contour plot of adjusted estimates

  const rhoRange = options.rhoRange || [-0.9, 0.9];
  const gammaRange = options.gammaRange || [0, 2];

  return {
    unadjusted: { effect: 0, se: 0 },
    sensitivityGrid: [
      // { rho: -0.5, gamma: 1.0, adjustedEffect: 0.3, adjustedSE: 0.12 }
    ],
    contourData: [],       // For visualization
    robustRange: { min: 0, max: 0 },  // Range of adjusted effects
    interpretation: ''
  };
}
```

**Reference:** Copas JB, Shi JQ (2001). Biostatistics 2:247-262

#### 2.4.2 Contour-Enhanced Funnel Plot

```javascript
function copasContourPlot(effects, ses, copasResult) {
  // Funnel plot with Copas selection contours
  // Shows how selection affects apparent asymmetry
}
```

### Phase 5: CINeMA Framework for NMA (Week 6-7)

#### 2.5.1 Confidence Assessment

```javascript
function cinemaAssessment(network, nmaResult, robData = {}) {
  // Six domains per GRADE-NMA methodology

  return {
    domains: {
      withinStudyBias: assessWithinStudyBias(network, robData),
      reportingBias: assessReportingBias(network),
      indirectness: assessIndirectness(network),
      imprecision: assessImprecision(nmaResult),
      heterogeneity: assessHeterogeneity(nmaResult),
      incoherence: assessIncoherence(nmaResult)
    },
    comparisonRatings: [
      // { comparison: 'A vs B', ratings: {...}, overall: 'Moderate' }
    ],
    summary: generateCINeMATable()
  };
}
```

**Reference:** Nikolakopoulou A et al. (2020). PLoS Med 17:e1003082

#### 2.5.2 Contribution Matrix

```javascript
function nmaContributionMatrix(network) {
  // How much each direct comparison contributes to each network estimate
  // Based on hat matrix decomposition
  // Identifies influential comparisons

  return {
    matrix: [],            // rows: network estimates, cols: direct comparisons
    mostInfluential: [],   // Top contributors per estimate
    visualization: ''      // SVG heatmap
  };
}
```

**Reference:** Papakonstantinou T et al. (2018). F1000Research 7:610

### Phase 6: Enhanced Bayesian Diagnostics (Week 7-8)

#### 2.6.1 Trace Plots

```javascript
function generateTracePlot(chains, parameter, options = {}) {
  // Visual inspection of MCMC convergence
  // Multiple chains overlaid with different colors
  // Burn-in period clearly marked

  return {
    svg: '',               // SVG trace plot
    iterations: [],
    chainMeans: [],
    visualConvergence: true/false
  };
}
```

#### 2.6.2 Additional Diagnostics

```javascript
function gewekeDiagnostic(samples, frac1 = 0.1, frac2 = 0.5) {
  // Compare first 10% vs last 50%
  // Z-test for equality of means
  return { z: 0, p: 0, converged: true/false };
}

function heidelbergerWelch(samples) {
  // Stationarity test
  // Halfwidth test for precision
  return { stationary: true/false, halfwidthOK: true/false };
}

function autocorrelationPlot(samples, maxLag = 50) {
  // ACF plot for mixing assessment
  return { acf: [], effectiveSampleSize: 0, svg: '' };
}
```

#### 2.6.3 Prior Sensitivity

```javascript
function priorSensitivityAnalysis(studies, priorSets) {
  // Run Bayesian MA with multiple prior specifications
  // Compare posteriors to identify robust conclusions

  const defaultPriors = [
    { name: 'Weakly informative', tau: 'halfCauchy(0.5)' },
    { name: 'Moderately informative', tau: 'halfCauchy(1.0)' },
    { name: 'Vague', tau: 'uniform(0, 2)' },
    { name: 'Empirical', tau: 'halfNormal(0.5)' }
  ];

  return {
    results: [],           // One per prior
    sensitivity: 'low/moderate/high',
    robustConclusion: true/false
  };
}
```

---

## Part 3: Extended Validation Suite

### 3.1 Test Coverage Targets

| Category | v9.0 | v10.0 Target | New Tests |
|----------|------|--------------|-----------|
| Core MA | 10 | 12 | +2 |
| Multiple Meta-Regression | 1 | 5 | +4 |
| Publication Bias | 4 | 6 | +2 (Copas) |
| NMA | 3 | 6 | +3 (CINeMA, contribution) |
| DTA | 3 | 4 | +1 |
| Bayesian | 1 | 4 | +3 (diagnostics) |
| RVE | 2 | 3 | +1 |
| Multivariate | 0 | 3 | +3 |
| Dose-Response | 0 | 3 | +3 |
| Living SR | 2 | 2 | — |
| Edge Cases | 2 | 4 | +2 |
| Performance | 0 | 4 | +4 |
| **Total** | **28** | **56** | **+28** |

### 3.2 New Reference Datasets

| Dataset | Source | k | Outcomes | Purpose |
|---------|--------|---|----------|---------|
| Berkey98 | metafor | 5 | 2 | Multivariate MA |
| Senn2013 | netmeta | 26 | 1 | Multi-arm NMA |
| Dogliotti | meta | 29 | 1 | Multiple meta-regression |
| Colditz | metafor | 13 | 2 | RVE with multiple outcomes |
| Schizophrenia | mada | 14 | 2 | Extended HSROC |
| Alcohol | dosresmeta | 8 | 1 | Dose-response |
| Antidepressants | Cipriani | 522 | 1 | Large NMA stress test |

### 3.3 New Validation Tests

```javascript
const ValidationSuiteV10 = {
  // Multiple meta-regression
  testMultipleRegression: {
    data: 'Dogliotti',
    covariates: ['year', 'dose', 'duration'],
    check: 'Coefficients match metafor::rma(mods = ~.)',
    tolerance: 0.02
  },

  testInteractionTerm: {
    data: 'bcg_extended',
    check: 'Interaction coefficient and p-value'
  },

  testCategoricalModerator: {
    data: 'bcg_with_latitude',
    groups: ['tropical', 'temperate', 'cold'],
    check: 'Q_between matches metafor'
  },

  testVIF: {
    data: 'collinear_covariates',
    check: 'VIF correctly identifies collinearity'
  },

  // Multivariate MA
  testBivariateOutcome: {
    data: 'Berkey98',
    outcomes: ['probing_depth', 'attachment_loss'],
    check: 'Pooled effects match mvmeta'
  },

  testCorrelationEstimation: {
    data: 'Berkey98',
    check: 'Between-study correlation estimated'
  },

  // Dose-response
  testLinearTrend: {
    data: 'Alcohol',
    check: 'Slope matches dosresmeta::dosresmeta()'
  },

  testNonLinearity: {
    data: 'Alcohol',
    check: 'Non-linearity test p-value'
  },

  // Copas
  testCopasGrid: {
    data: 'bcg',
    check: 'Adjusted effect range computed'
  },

  testCopasExtreme: {
    data: 'asymmetric_funnel',
    check: 'Detects high selection sensitivity'
  },

  // CINeMA
  testCINeMARatings: {
    data: 'smokingNMA',
    check: 'Domain ratings computed for all comparisons'
  },

  testContributionMatrix: {
    data: 'smokingNMA',
    check: 'Contributions sum to 100% per estimate'
  },

  // Bayesian diagnostics
  testGeweke: {
    check: 'Z-statistic within ±2 for converged chains'
  },

  testAutocorrelation: {
    check: 'ACF computed, ESS reasonable'
  },

  testPriorSensitivity: {
    check: 'Results with different priors compared'
  },

  // Performance
  testLargeMA: {
    k: 500,
    check: 'Completes in < 3 seconds'
  },

  testLargeNMA: {
    treatments: 30,
    comparisons: 200,
    check: 'Completes in < 5 seconds'
  },

  testLargeBayesian: {
    iterations: 20000,
    chains: 4,
    check: 'Completes in < 30 seconds'
  },

  testStressMultivariate: {
    k: 100,
    outcomes: 3,
    check: 'Completes without memory issues'
  }
};
```

### 3.4 Numerical Precision Tests

```javascript
const PrecisionTests = {
  // Matrix operations
  illConditionedMatrix: {
    input: 'Near-singular covariance matrix',
    check: 'Stable inversion with warning'
  },

  // Extreme values
  verySmallVariance: {
    input: 'SE = 0.0001',
    check: 'No overflow, reasonable weights'
  },

  veryLargeEffect: {
    input: 'OR = 1000',
    check: 'Log transform stable'
  },

  // Iterative algorithms
  remlDifficult: {
    input: 'High heterogeneity dataset',
    check: 'Converges in < 100 iterations'
  },

  // Edge cases
  perfectHomogeneity: {
    input: 'All effects identical',
    check: 'τ² = 0 exactly, no division errors'
  },

  singleArmNMA: {
    input: 'Treatment with only one study',
    check: 'Appropriate uncertainty, no crash'
  }
};
```

---

## Part 4: Performance Optimization

### 4.1 Targets

| Operation | k | Current | Target |
|-----------|---|---------|--------|
| Basic MA | 100 | <0.5s | <0.3s |
| Basic MA | 500 | ~2s | <1s |
| Meta-regression (1 cov) | 100 | <1s | <0.5s |
| Meta-regression (5 cov) | 100 | N/A | <2s |
| NMA (10 treatments) | 50 | <2s | <1s |
| NMA (30 treatments) | 200 | N/A | <5s |
| Bayesian (10k iter) | 20 | ~10s | <8s |
| Multivariate (3 outcomes) | 50 | N/A | <3s |
| Dose-response (splines) | 30 | N/A | <2s |

### 4.2 Optimization Strategies

1. **Web Workers** for computationally intensive operations
2. **Lazy evaluation** for plots (generate on demand)
3. **Caching** of intermediate results
4. **Typed arrays** for matrix operations
5. **Early termination** for iterative algorithms

---

## Part 5: UI Enhancements

### 5.1 New Analysis Dialogs

| Feature | Menu Location | Description |
|---------|---------------|-------------|
| Multiple Meta-Regression | Analysis > Meta-Regression | Extended covariate interface |
| Subgroup Analysis | Analysis > Subgroup Analysis | Visual subgroup comparison |
| Multivariate MA | Analysis > Multivariate MA | Multiple outcome pooling |
| Dose-Response | Analysis > Dose-Response | Dose-effect modeling |
| Copas Model | Analysis > Publication Bias > Copas | Contour sensitivity |
| CINeMA | Analysis > NMA > CINeMA | Confidence assessment table |
| Trace Plots | Analysis > Bayesian > Diagnostics | Visual MCMC inspection |

### 5.2 Visualization Additions

| Visualization | Purpose |
|---------------|---------|
| Multi-covariate bubble plot | Meta-regression with size/color mapping |
| Subgroup forest plot | Side-by-side subgroup comparison |
| Dose-response curve | Non-linear effect visualization |
| Copas contour plot | Selection model sensitivity |
| CINeMA heatmap | NMA confidence ratings |
| Trace plot panel | MCMC chain visualization |
| ACF plot | Autocorrelation assessment |
| Contribution heatmap | NMA evidence flow |

---

## Part 6: New References for v10.0

### Multiple Meta-Regression
35. Higgins JPT, Thompson SG (2004). Controlling the risk of spurious findings from meta-regression. *Statistics in Medicine*, 23:1663-1682.

### Multivariate Meta-Analysis
36. Jackson D, Riley R, White IR (2011). Multivariate meta-analysis: Potential and promise. *Statistics in Medicine*, 30:2481-2498.
37. Riley RD et al. (2017). Multivariate meta-analysis using individual participant data. *Research Synthesis Methods*, 8:25-42.

### Dose-Response
38. Greenland S, Longnecker MP (1992). Methods for trend estimation from summarized dose-response data. *American Journal of Epidemiology*, 135:1301-1309.
39. Crippa A, Orsini N (2016). Dose-response meta-analysis of differences in means. *BMC Medical Research Methodology*, 16:91.

### Copas Selection Model
40. Copas JB, Shi JQ (2001). A sensitivity analysis for publication bias in systematic reviews. *Biostatistics*, 2:247-262.
41. Carpenter JR et al. (2009). A sensitivity analysis for publication bias in systematic reviews. *Stat Methods Med Res*, 18:407-434.

### CINeMA Framework
42. Nikolakopoulou A et al. (2020). CINeMA: An approach for assessing confidence in the results of a network meta-analysis. *PLoS Medicine*, 17:e1003082.
43. Papakonstantinou T et al. (2018). CINeMA: Software for semiautomated assessment of the confidence in the results of network meta-analysis. *Campbell Systematic Reviews*, 14:e1080.

### Bayesian Diagnostics
44. Geweke J (1992). Evaluating the accuracy of sampling-based approaches to calculating posterior moments. *Bayesian Statistics*, 4:169-193.
45. Heidelberger P, Welch PD (1983). Simulation run length control in the presence of an initial transient. *Operations Research*, 31:1109-1144.

---

## Part 7: Implementation Schedule

### Week 1-2: Multiple Meta-Regression
- [ ] Implement multipleMetaRegression() function
- [ ] Add categorical moderator analysis
- [ ] Create multi-covariate UI dialog
- [ ] Add 4 validation tests
- [ ] Update documentation

### Week 3-4: Multivariate MA
- [ ] Implement multivariateMA() function
- [ ] Add Berkey98 dataset
- [ ] Create multivariate UI dialog
- [ ] Add 3 validation tests
- [ ] Update documentation

### Week 5-6: Dose-Response & Copas
- [ ] Implement linearDoseResponse()
- [ ] Implement nonLinearDoseResponse() (simplified)
- [ ] Implement copasSelectionModel()
- [ ] Add Alcohol dataset
- [ ] Create UI dialogs
- [ ] Add 5 validation tests

### Week 7-8: CINeMA & Bayesian
- [ ] Implement cinemaAssessment()
- [ ] Implement contributionMatrix()
- [ ] Add trace plots
- [ ] Add Geweke, ACF diagnostics
- [ ] Add prior sensitivity analysis
- [ ] Add 6 validation tests

### Week 9: Performance & Polish
- [ ] Implement Web Workers for heavy computations
- [ ] Add performance benchmarks
- [ ] Optimize matrix operations
- [ ] Add 4 performance tests
- [ ] Final UI polish

### Week 10: Integration & Testing
- [ ] Full integration testing
- [ ] Cross-browser testing
- [ ] Documentation update
- [ ] Editorial review preparation
- [ ] Final validation (56 tests target)

---

## Part 8: Success Criteria

### v10.0 Release Criteria

| Criterion | Requirement |
|-----------|-------------|
| Validation tests | 56/56 pass |
| Performance | All benchmarks met |
| Documentation | 45 citations |
| File size | < 900 KB |
| Browser testing | Chrome, Firefox, Safari, Edge |
| Editorial review | Accept recommendation |

### Feature Completeness

| Feature | v9.0 | v10.0 | Gain |
|---------|------|-------|------|
| Meta-regression covariates | 1 | 5 | +4 |
| Publication bias methods | 6 | 7 | +1 (Copas) |
| NMA features | 5 | 8 | +3 (CINeMA, contribution) |
| DTA features | 3 | 3 | — |
| Bayesian diagnostics | 3 | 7 | +4 |
| Multivariate | 0 | 1 | +1 |
| Dose-response | 0 | 2 | +2 |
| Validation tests | 28 | 56 | +28 |
| Citations | 34 | 45 | +11 |

---

## Part 9: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Multivariate too complex | Medium | High | Simplify to 2-outcome case |
| Dose-response numerical issues | Medium | Medium | Use robust spline library |
| Performance degradation | Low | High | Profile and optimize early |
| File size exceeds 1MB | Medium | Medium | Code minification if needed |
| CINeMA subjectivity | Low | Low | Clear documentation of criteria |

---

## Summary

### v10.0 Key Additions

1. **Multiple meta-regression** — Up to 5 covariates with interaction terms
2. **Multivariate meta-analysis** — Correlated outcomes pooling
3. **Dose-response modeling** — Linear and non-linear trends
4. **Copas selection model** — Publication bias sensitivity analysis
5. **CINeMA framework** — NMA confidence assessment
6. **Enhanced Bayesian** — Trace plots, Geweke, ACF, prior sensitivity
7. **56 validation tests** — Doubled from v9.0
8. **Performance benchmarks** — Verified scalability

### Maintained Strengths

- Single-file, offline-first architecture
- Zero dependencies
- Built-in validation against R packages
- Appropriate limitation notes
- Publication-ready documentation

---

**Document prepared for Screenr v10.0 development**
**2026-01-31**
