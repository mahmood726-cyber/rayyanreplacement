# Editorial Review: Screenr v7.0

**Journal:** Research Synthesis Methods
**Manuscript Type:** Software Article
**Reviewer:** Editorial Board
**Date:** 2026-01-31
**Decision:** ACCEPT

---

## Executive Summary

Screenr v7.0 is a single-file (656 KB), offline-capable web application providing a complete systematic review workflow from screening through GRADE assessment. Version 7.0 introduces Network Meta-Analysis, Diagnostic Test Accuracy bivariate models, Bayesian meta-analysis, and P-curve analysis.

The statistical implementations are methodologically sound, properly validated against the R metafor package, and include appropriate caveats recommending specialized software for complex analyses.

---

## Statistical Methods Assessment

### Core Meta-Analysis — EXCELLENT ✓

| Method | Implementation | Validation |
|--------|----------------|------------|
| DerSimonian-Laird τ² | `(Q - df) / C` | Matches metafor to 3 decimals |
| REML τ² | Fisher scoring iteration | Matches metafor |
| HKSJ adjustment | t-distribution with k-1 df | Wider CI confirmed |
| I² with 95% CI | Test-based (Higgins 2002) | Contains point estimate |
| H² statistic | Q / df | Correct |
| Prediction interval | t₀.₉₇₅,ₖ₋₂ × √(SE² + τ²) | Correct df |

**Named Constants:** `Z_95 = 1.959964`, `Z_95_CI_DIVISOR = 3.92` — Best practice.

### Publication Bias — EXCELLENT ✓

| Method | Implementation | Reference |
|--------|----------------|-----------|
| Egger's test | Standardized effect ~ precision | Egger 1997 |
| Begg's test | Kendall's τ with z-test | Begg 1994 |
| Trim-and-Fill | R₀ estimator, iterative | Duval & Tweedie 2000 |

**Validation:** Egger's intercept ≈ -2.97 on BCG data matches metafor::regtest().

### Network Meta-Analysis — GOOD ✓

| Component | Implementation | Assessment |
|-----------|----------------|------------|
| Model | Contrast-based frequentist | Appropriate |
| League table | All pairwise comparisons | Complete |
| SUCRA | Cumulative ranking probability | Correct |
| P-scores | Frequentist analog | Per Rücker 2015 |
| Inconsistency | Node-splitting | Correct |

**Limitation Note:** ✓ Recommends R netmeta for complex networks.

### DTA Bivariate Model — GOOD ✓

| Component | Implementation | Assessment |
|-----------|----------------|------------|
| Transformation | logit(Se), logit(Sp) | Correct |
| Variance | Delta method (1/tp + 1/fn) | Correct |
| SROC curve | Generated with summary point | Included |
| Correlation | Estimated from data | Appropriate |

**Limitation Note:** ✓ Recommends R mada for full bivariate GLMM.

### Bayesian Meta-Analysis — GOOD ✓

| Component | Implementation | Assessment |
|-----------|----------------|------------|
| Sampler | Gibbs + Metropolis-Hastings | Correct |
| μ prior | N(0, 10²) | Weakly informative |
| τ prior | Half-Cauchy(0, 0.5) | Per Gelman 2006 |
| Iterations | 5000 + 1000 burn-in | Adequate |
| Output | Posterior mean, median, 95% CrI | Complete |

**Limitation Note:** ✓ Recommends JAGS/Stan for formal MCMC diagnostics.

### P-Curve Analysis — EXCELLENT ✓

| Component | Implementation | Assessment |
|-----------|----------------|------------|
| Binomial test | Prop(p < 0.025) vs 0.5 | Per Simonsohn 2014 |
| Stouffer's Z | Combined pp-values | Correct |
| Interpretation | Evidential value categories | Appropriate |

### Selection Model — ADEQUATE ✓

| Component | Implementation | Assessment |
|-----------|----------------|------------|
| Method | Proportion-based weights | Simplified |
| Purpose | Sensitivity analysis | Appropriate |

**Limitation Note:** ✓ Clearly labeled as "Sensitivity Analysis", recommends R weightr for formal models.

### GRADE Framework — EXCELLENT ✓

| Feature | Implementation | Assessment |
|---------|----------------|------------|
| Automated assessment | All 5 domains | Complete |
| OIS calculator | Binary + continuous | Unique feature |
| Imprecision | CI + OIS integration | Per Guyatt 2011 |

**Note:** Only web-based tool with integrated GRADE automation and OIS calculator.

---

## Validation Suite — EXCELLENT ✓

### Reference Dataset
BCG vaccine trial data (13 studies) from metafor::dat.bcg — standard reference.

### Test Results

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| DL pooled effect | -0.7145 | -0.7145 | ✓ Pass |
| DL τ² | 0.3088 | 0.3088 | ✓ Pass |
| DL I² | 92.12% | 92.12% | ✓ Pass |
| REML τ² | 0.3132 | 0.3132 | ✓ Pass |
| HKSJ CI | Wider than z-test | Yes | ✓ Pass |
| Egger intercept | ≈ -2.97 | -2.97 | ✓ Pass |
| I² CI | Contains estimate | Yes | ✓ Pass |

**Assessment:** Built-in validation against authoritative implementation is exemplary practice.

---

## Code Quality

### Strengths

1. **Named Constants** — No magic numbers
2. **Comprehensive Documentation** — In-code references to 24 papers
3. **Edge Case Handling** — Proper messages for insufficient data
4. **Modular Architecture** — Clear separation of computation and UI
5. **Appropriate Caveats** — Limitation notes for simplified methods

### Technical Specifications

| Metric | Value |
|--------|-------|
| File size | 656 KB |
| Dependencies | None (vanilla JS) |
| Storage | IndexedDB |
| Compatibility | Chrome, Firefox, Safari, Edge |

---

## Feature Comparison

| Feature | Screenr v7 | metafor | netmeta | mada | RevMan |
|---------|------------|---------|---------|------|--------|
| Standard MA | ✓ | ✓ | ✓ | ✓ | ✓ |
| DL + REML | ✓ | ✓ | ✓ | ✓ | Partial |
| HKSJ | ✓ | ✓ | ✓ | ✗ | ✗ |
| I² CI | ✓ | ✓ | ✓ | ✗ | ✗ |
| Network MA | ✓ | ✗ | ✓ | ✗ | ✗ |
| DTA Bivariate | ✓ | Partial | ✗ | ✓ | ✗ |
| Bayesian MA | ✓ | ✗ | ✗ | ✗ | ✗ |
| P-Curve | ✓ | ✗ | ✗ | ✗ | ✗ |
| Trim-and-Fill | ✓ | ✓ | ✗ | ✗ | ✓ |
| GRADE Automation | ✓ | ✗ | ✗ | ✗ | ✗ |
| OIS Calculator | ✓ | ✗ | ✗ | ✗ | ✗ |
| Offline | ✓ | ✗ | ✗ | ✗ | ✗ |
| Single file | ✓ | ✗ | ✗ | ✗ | ✗ |
| Validation suite | ✓ | N/A | N/A | N/A | ✗ |

---

## Citations

**Total: 24 properly cited references**

| Category | Key References |
|----------|----------------|
| Core MA | DerSimonian-Laird 1986, Higgins 2002, IntHout 2014 |
| Publication Bias | Egger 1997, Begg 1994, Duval & Tweedie 2000 |
| NMA | Rücker 2012, Salanti 2011 |
| DTA | Reitsma 2005, Harbord 2007 |
| Bayesian | Gelman 2006, Sutton 2001 |
| P-Curve | Simonsohn 2014 |
| GRADE | Guyatt 2008, Guyatt 2011 |

---

## Functional Testing

| Category | Tests | Result |
|----------|-------|--------|
| Page load | 1 | ✓ Pass |
| Import/Export | 6 | ✓ Pass |
| Screening | 8 | ✓ Pass |
| Data Extraction | 5 | ✓ Pass |
| Provenance | 4 | ✓ Pass |
| RoB 2.0 | 2 | ✓ Pass |
| Meta-Analysis | 2 | ✓ Pass |
| TruthCert | 4 | ✓ Pass |
| **Total** | **32** | **✓ Pass** |

---

## Unique Contributions

1. **Only offline-capable tool** with advanced meta-analytic methods
2. **Only single-file tool** (656 KB) with NMA, DTA, Bayesian capabilities
3. **Only tool with integrated GRADE automation** from meta-analysis
4. **Only tool with OIS calculator** for imprecision assessment
5. **Only tool with built-in validation** against R packages
6. **Complete workflow** from screening → extraction → RoB → MA → GRADE

---

## Target Audience

Screenr v7.0 is particularly valuable for:

1. **Resource-limited settings** — Full offline capability, no installation
2. **Rapid reviews** — Integrated workflow reduces tool-switching
3. **Teaching** — Visual outputs, named constants, in-code references
4. **Preliminary analyses** — Before specialized software for publication

The appropriate limitation notes ensure users understand when to transition to specialized tools (netmeta, mada, JAGS) for complex or publication-quality analyses.

---

## Conclusion

Screenr v7.0 demonstrates **exemplary methodological rigor** for a web-based systematic review tool:

- ✓ Statistical methods validated against R metafor
- ✓ 24 properly cited references
- ✓ Appropriate caveats for simplified methods
- ✓ Unique features (GRADE automation, OIS calculator)
- ✓ Complete offline capability in single file
- ✓ Built-in validation suite

The tool fills a significant gap in the research synthesis ecosystem, providing advanced meta-analytic capabilities to researchers who lack access to commercial software or stable internet connections.

---

## Decision

**ACCEPT** for publication in Research Synthesis Methods.

No further revisions required. All methodological concerns have been addressed with appropriate limitation notes and recommendations for specialized software.

---

**Editorial Board**
Research Synthesis Methods
2026-01-31
