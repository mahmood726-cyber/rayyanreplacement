# Screenr v6.2 - Future Improvements Plan

**Date:** 2026-01-31
**Current Version:** 6.2
**Status:** Accepted for publication, planning v7 features

---

## Executive Summary

Screenr v6.2 has been accepted for publication with exemplary methodological rigor. This plan outlines enhancements for future versions that would further strengthen the tool's position as the leading offline-first systematic review platform.

---

## 1. Publication Bias Enhancements

### 1.1 Trim-and-Fill Method (High Priority)
**Purpose:** Estimate number of missing studies and adjust pooled effect

**Implementation:**
```javascript
function trimAndFill(effects, ses, side = 'left') {
  // 1. Rank studies by deviation from mean
  // 2. Iteratively remove most extreme studies
  // 3. Estimate k0 (missing studies)
  // 4. Fill in imputed studies
  // 5. Re-run meta-analysis with filled data

  return {
    k0: missingStudies,
    adjustedEffect: newPooledEffect,
    adjustedCI: newCI,
    filledStudies: imputedData
  };
}
```

**Reference:** Duval & Tweedie (2000), Biometrics

**UI Addition:**
- Add "Trim-and-Fill" button to publication bias panel
- Show funnel plot with imputed studies in different color
- Display adjusted effect estimate

### 1.2 P-Curve Analysis (Medium Priority)
**Purpose:** Detect p-hacking and assess evidential value

**Implementation:**
```javascript
function pCurveAnalysis(pValues) {
  // Test if p-curve is right-skewed (evidential value)
  // vs flat (no evidential value) or left-skewed (p-hacking)

  return {
    binomialTest: pValue,
    continuousTest: zScore,
    interpretation: 'evidential' | 'inadequate' | 'phacking'
  };
}
```

**Reference:** Simonsohn, Nelson & Simmons (2014), J Exp Psych

### 1.3 Selection Models (Lower Priority)
**Purpose:** Model publication selection process

**Options:**
- Vevea-Hedges weight function models
- Copas selection model
- 3PSM (three-parameter selection model)

---

## 2. Influence Diagnostics

### 2.1 Leave-One-Out Analysis (High Priority)
**Current:** Basic implementation exists
**Enhancement:** Add visualization and automated flagging

```javascript
function leaveOneOutAnalysis(studies) {
  const results = [];
  for (let i = 0; i < studies.length; i++) {
    const subset = studies.filter((_, j) => j !== i);
    const ma = calculateMetaAnalysis(subset);
    results.push({
      omitted: studies[i].id,
      effect: ma.randomEffect,
      changePercent: calculateChange(ma.randomEffect, fullEffect)
    });
  }
  return results;
}
```

**UI Addition:**
- Interactive leave-one-out plot
- Highlight influential studies (>10% change)

### 2.2 Cook's Distance (Medium Priority)
**Purpose:** Identify studies with undue influence

```javascript
function cookDistance(studies, i) {
  // Measure change in all fitted values when study i removed
  const Di = (βfull - βomit)' * V * (βfull - βomit) / (p * MSE);
  return Di;
}
```

### 2.3 DFBETAS (Medium Priority)
**Purpose:** Standardized change in regression coefficients

```javascript
function dfbetas(studies, i) {
  // Change in coefficient when study i deleted
  // Standardized by SE
  return (β - β_(-i)) / SE(β_(-i));
}
```

### 2.4 Externally Studentized Residuals
**Purpose:** Detect outliers with heavy leverage

---

## 3. Advanced Meta-Analysis Methods

### 3.1 Network Meta-Analysis (High Priority)
**Purpose:** Compare multiple interventions simultaneously

**Components:**
1. **Treatment network graph**
   - Nodes = treatments
   - Edges = direct comparisons
   - Edge thickness = study count

2. **Consistency model**
   ```javascript
   function networkMetaAnalysis(contrasts) {
     // Build design matrix
     // Fit random-effects NMA
     // Check consistency (node-splitting)

     return {
       leagueTable: allPairwiseEffects,
       rankogram: treatmentRankings,
       sucra: surfaceUnderCurve,
       inconsistency: pValue
     };
   }
   ```

3. **UI Components:**
   - Network graph visualization (D3.js)
   - League table (heatmap)
   - Rankogram plots
   - SUCRA values

**Reference:** Salanti (2012), Statistical Methods in Medical Research

### 3.2 Multivariate Meta-Analysis (Medium Priority)
**Purpose:** Jointly analyze correlated outcomes

```javascript
function multivariateMA(outcomes) {
  // Account for within-study correlation
  // Borrow strength across outcomes

  return {
    pooledEffects: effectVector,
    correlationMatrix: Sigma,
    jointCI: confidenceRegion
  };
}
```

### 3.3 Cumulative Meta-Analysis (Low Priority)
**Purpose:** Show how evidence accumulated over time

```javascript
function cumulativeMA(studies) {
  // Sort by publication year
  // Run meta-analysis adding one study at a time
  // Show temporal evolution of pooled effect
}
```

---

## 4. Diagnostic Test Accuracy Meta-Analysis

### 4.1 Bivariate Model (High Priority)
**Purpose:** Proper DTA meta-analysis accounting for sensitivity/specificity correlation

```javascript
function bivariateDTA(studies) {
  // Each study contributes (logit(Se), logit(Sp))
  // Fit bivariate random-effects model
  // Generate SROC curve

  return {
    pooledSensitivity: Se,
    pooledSpecificity: Sp,
    correlation: rho,
    srocCurve: curvePoints,
    auc: areaUnderCurve
  };
}
```

**UI Components:**
- SROC plot with confidence region
- Summary operating point
- Prediction region

**Reference:** Reitsma et al. (2005), J Clin Epidemiol

### 4.2 HSROC Model (Medium Priority)
**Purpose:** Alternative parameterization for threshold effects

```javascript
function hsrocModel(studies) {
  // Hierarchical SROC model
  // Estimates accuracy and threshold parameters
}
```

**Reference:** Rutter & Gatsonis (2001), Statistics in Medicine

### 4.3 Meta-Regression for DTA (Lower Priority)
**Purpose:** Explore heterogeneity in test accuracy

---

## 5. Bayesian Methods

### 5.1 Bayesian Random-Effects Model (Medium Priority)
**Purpose:** Proper uncertainty quantification, especially with few studies

```javascript
function bayesianMA(studies, priors = {}) {
  // Prior specification for τ²
  // MCMC or analytical approximation

  const defaultPriors = {
    tau2: { type: 'halfCauchy', scale: 0.5 },
    mu: { type: 'normal', mean: 0, sd: 10 }
  };

  return {
    posteriorEffect: distribution,
    posteriorTau2: distribution,
    credibleInterval: [low, high],
    probabilityBeneficial: P(effect > 0)
  };
}
```

### 5.2 Prior Sensitivity Analysis (Lower Priority)
**Purpose:** Assess impact of prior choices

### 5.3 Bayesian Model Averaging (Lower Priority)
**Purpose:** Weight across different model specifications

---

## 6. Quality of Evidence

### 6.1 GRADE Implementation Enhancement (High Priority)
**Current:** Basic GRADE assessment exists
**Enhancement:** Automated downgrading suggestions

```javascript
function gradeAssessment(ma, studies) {
  const domains = {
    riskOfBias: assessRoB(studies),
    inconsistency: assessI2(ma.i2, ma.i2CI),
    indirectness: null, // Manual input needed
    imprecision: assessOIS(ma),  // Optimal Information Size
    publicationBias: assessFunnel(ma)
  };

  return {
    certainty: calculateCertainty(domains),
    footnotes: generateFootnotes(domains),
    summaryOfFindings: formatSoF(ma, domains)
  };
}
```

### 6.2 Optimal Information Size (OIS) Calculator
**Purpose:** Determine if sample size is adequate

```javascript
function optimalInformationSize(ma, targetRRR = 0.25) {
  // Calculate required sample size for target effect
  // Compare to actual information size
  // Flag if underpowered
}
```

---

## 7. Data Management Enhancements

### 7.1 Supplement PDF Processing (High Priority)
**Problem:** Key data often in supplementary materials
**Solution:**
- Detect supplement references in main text
- Support multiple PDF upload per study
- Link extractions to specific documents

### 7.2 Living Systematic Review Support (Medium Priority)
**Features:**
- Automated search update scheduling
- Incremental screening
- Version control for analyses
- Change tracking over time

### 7.3 Protocol Registration (Medium Priority)
**Features:**
- PROSPERO integration
- Protocol template generation
- Pre-registration tracking

---

## 8. Reporting Enhancements

### 8.1 PRISMA-NMA Statement (High Priority)
**Purpose:** Reporting checklist for network meta-analyses
**Reference:** Hutton et al. (2015), Ann Intern Med

### 8.2 GRADE Summary of Findings Table (High Priority)
**Enhancement:**
- Automated population from meta-analysis
- Export to Word/PDF
- Interactive editing

### 8.3 Abstract Generator (Medium Priority)
**Purpose:** Draft structured abstract from results

```javascript
function generateAbstract(review) {
  return {
    background: review.background,
    methods: formatMethods(review.methods),
    results: formatResults(review.metaAnalysis),
    conclusions: generateConclusion(review)
  };
}
```

---

## 9. Machine Learning Enhancements

### 9.1 Deep Learning Prioritization (Medium Priority)
**Current:** TF-IDF + Logistic Regression
**Enhancement:** Add transformer-based model option

```javascript
function trainBERTClassifier(labeledRecords) {
  // Use pre-trained biomedical BERT
  // Fine-tune on labeled screening decisions
  // Export model weights for offline use
}
```

**Challenge:** Model size (~400MB) conflicts with single-file architecture
**Solution:** Optional WebAssembly model or WebGPU inference

### 9.2 Citation Screening (Lower Priority)
**Purpose:** Screen by analyzing citation network
- Seed set expansion
- Snowballing automation

### 9.3 Duplicate Detection Improvement (Medium Priority)
**Current:** Fuzzy title matching
**Enhancement:**
- DOI matching
- Author name normalization
- Probabilistic record linkage

---

## 10. Collaboration Features

### 10.1 Real-Time Collaboration (Medium Priority)
**Challenge:** Offline-first architecture
**Solution:** WebRTC peer-to-peer sync when both users online

### 10.2 Conflict Resolution Enhancement (High Priority)
**Current:** Basic adjudication workflow
**Enhancement:**
- Discussion threads on conflicts
- Decision audit trail
- Batch conflict resolution

### 10.3 Role-Based Access Control (Lower Priority)
**Purpose:** Manage large team reviews

---

## Implementation Priority Matrix

| Feature | Impact | Effort | Priority | Target Version |
|---------|--------|--------|----------|----------------|
| Trim-and-Fill | High | Low | **P1** | v6.3 |
| Leave-One-Out Visualization | High | Low | **P1** | v6.3 |
| GRADE Enhancement | High | Medium | **P1** | v6.3 |
| Network Meta-Analysis | Very High | High | **P2** | v7.0 |
| Bivariate DTA | High | High | **P2** | v7.0 |
| Bayesian MA | Medium | High | **P3** | v7.x |
| Living SR Support | Medium | Medium | **P3** | v7.x |
| Deep Learning | Medium | Very High | **P4** | v8.0 |

---

## Roadmap

### v6.3 (Target: Q2 2026)
- [ ] Trim-and-Fill method
- [ ] Enhanced leave-one-out analysis with visualization
- [ ] Cook's distance and DFBETAS
- [ ] GRADE automated downgrading
- [ ] OIS calculator
- [ ] Improved conflict resolution

### v7.0 (Target: Q4 2026)
- [ ] Network meta-analysis module
- [ ] Bivariate DTA meta-analysis
- [ ] SROC plot generation
- [ ] PRISMA-NMA checklist
- [ ] League table visualization
- [ ] Cumulative meta-analysis

### v7.x (2027)
- [ ] Bayesian random-effects option
- [ ] Living systematic review features
- [ ] P-curve analysis
- [ ] Selection models
- [ ] Protocol registration integration

### v8.0 (Future)
- [ ] Deep learning prioritization option
- [ ] Real-time collaboration
- [ ] Multi-language NLP for screening

---

## Technical Considerations

### File Size Management
Current: ~554KB single HTML file
Target: Keep under 1MB for usability

**Strategies:**
- Lazy-load advanced modules
- Use WebWorkers for heavy computation
- Optional external model files for ML

### Browser Compatibility
Maintain support for:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Testing Strategy
- Expand Selenium suite to 50+ tests
- Add unit tests for statistical functions
- Validate against R packages (metafor, netmeta, mada)

---

## Success Metrics

| Metric | Current | v7 Target |
|--------|---------|-----------|
| Selenium tests | 35 | 60 |
| Statistical functions | ~50 | ~100 |
| Reference citations | 13 | 25 |
| R package validation | metafor | + netmeta, mada |
| File size | 554KB | <1MB |

---

## Conclusion

Screenr v6.2 has established a strong foundation with rigorous meta-analysis capabilities. The planned enhancements focus on:

1. **Short-term (v6.3):** Publication bias methods and influence diagnostics
2. **Medium-term (v7.0):** Network meta-analysis and DTA support
3. **Long-term (v8.0):** Advanced ML and collaboration features

The offline-first, single-file architecture should be preserved as a key differentiator while carefully adding advanced features that maintain usability.

---

**Document Author:** Claude (AI Assistant)
**Last Updated:** 2026-01-31
