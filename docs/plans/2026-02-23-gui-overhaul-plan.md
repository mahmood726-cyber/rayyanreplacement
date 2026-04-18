# Screenr v11 GUI Overhaul — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform Screenr's GUI from cluttered/dated to warm-premium polish — 67 review findings across visual design, UX, and information architecture.

**Architecture:** Single-file HTML app (screenr.html, ~32K lines). All CSS lives in lines 34-2194. All HTML body in lines 2196-3700. All JS in lines 3703-32485. Edits are CSS variable changes, HTML restructure of the header/menu (lines 2204-2476), and JS additions for click-to-toggle menus + command palette.

**Tech Stack:** Vanilla HTML/CSS/JS. No build tools. No dependencies. Changes must preserve all existing JS function signatures (onclick handlers must continue to work).

**Critical constraint:** This is a single-file app — every edit must be in `C:\Users\user\Downloads\rayyanreplacement\screenr.html`. After structural HTML edits, verify div balance (`<div` count == `</div>` count). Never use literal `</script>` inside template literals — use `${'<'}/script>`.

---

## Task 1: CSS Design Tokens — Replace :root variables

**Files:**
- Modify: `screenr.html:35-76` (the `:root` block)

**Step 1: Replace the entire :root block**

Replace lines 35-76 with a new `:root` that adds type scale, spacing scale, flattened shadows, and standardized radii while keeping all existing color variables. The new block:

```css
:root {
  /* Fonts */
  --font-sans: "Space Grotesk", "Manrope", "Segoe UI", sans-serif;
  --font-display: "Fraunces", "Georgia", serif;

  /* Type Scale (6 steps — floor is 0.75rem, no rogue sizes) */
  --text-xs:   0.75rem;
  --text-sm:   0.8125rem;
  --text-base: 0.875rem;
  --text-lg:   1rem;
  --text-xl:   1.125rem;
  --text-2xl:  1.25rem;

  /* Spacing Scale (4px grid) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;

  /* Colors — unchanged palette */
  --bg-main: #f7f2ea;
  --bg-surface: #fbf8f2;
  --bg-sidebar: #111827;
  --bg-header: #1f2937;
  --bg-panel: #ffffff;
  --border-color: #e8e1d7;
  --border-dark: #2f3b52;
  --text: #1f2937;
  --text-light: #6b7280;
  --text-white: #ffffff;
  --primary: #0ea5a4;
  --primary-dark: #0b7b78;
  --primary-light: #e2f7f5;
  --success: #22c55e;
  --success-light: #e8f9ef;
  --danger: #ef4444;
  --danger-light: #fde8e8;
  --warning: #d97706;          /* was #f59e0b — darkened for WCAG AA contrast */
  --warning-light: #fff3dd;
  --info: #2563eb;
  --info-light: #e9effe;
  --purple: #7c3aed;
  --purple-light: #ede9fe;
  --include: #ddf7e7;
  --exclude: #fde2e2;
  --maybe: #fff3c4;
  --flagged: #fed7d7;
  --conflict: #efe5ff;
  --duplicate: #dff6ff;
  --low-risk: #16a34a;
  --high-risk: #ef4444;
  --some-concerns: #d97706;    /* matched to --warning */

  /* Radius (3 levels + pill) */
  --radius-sm: 6px;
  --radius: 10px;
  --radius-lg: 14px;
  --radius-pill: 999px;

  /* Shadows — dramatically flattened */
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow: 0 2px 6px rgba(15, 23, 42, 0.06);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
  --shadow-lg: 0 8px 24px rgba(15, 23, 42, 0.12);
}
```

**Step 2: Verify page still renders**

Open screenr.html in browser. All panels should appear. Colors unchanged. Shadows noticeably subtler.

---

## Task 2: Visual Cleanup — Remove gradient blobs, animations, hover lifts

**Files:**
- Modify: `screenr.html:77-112` (body styles + pseudo-elements)
- Modify: `screenr.html:296-303` (button hover)
- Modify: `screenr.html:374-383` (panel animations)
- Modify: `screenr.html:434-441,488-503` (record item animations + hover)
- Modify: `screenr.html:446-463` (filter chip hover lift)
- Modify: `screenr.html:147-153` (conic-gradient logo)
- Modify: `screenr.html:1434-1445` (keyframe animations)

**Step 1: Simplify body background — remove 3 gradients + 2 pseudo-element blobs**

Replace body background-image (lines 81-84) with just the flat color:
```css
body {
  font-family: var(--font-sans);
  background-color: var(--bg-main);
  color: var(--text);
  line-height: 1.5;     /* was 1.6 */
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}
```

Remove the body::before and body::after blocks entirely (lines 91-112).

**Step 2: Replace conic-gradient logo with solid teal square**

Replace lines 147-153:
```css
header h1::before {
  content: "";
  width: 18px;
  height: 18px;
  border-radius: 6px;
  background: var(--primary);
  box-shadow: 0 0 0 2px rgba(255,255,255,0.15);
}
```

**Step 3: Remove button hover lift, keep only background change**

Replace lines 299-303:
```css
button:hover, .btn:hover {
  background: var(--bg-surface);
  box-shadow: var(--shadow-md);
}
```
(Remove `transform: translateY(-1px)` — keep it ONLY for `button.primary:hover`)

Add to `button.primary:hover`:
```css
button.primary:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}
```

**Step 4: Remove panel entrance animations**

Replace line 376: `animation: panelIn 0.5s ease both;` → remove this line.
Remove lines 381-383 (animation delays for panels).
Remove the staggered record-item animation (line 490-491):
```css
/* Remove: animation: rise 0.35s ease both; */
/* Remove: animation-delay: calc(var(--stagger, 0) * 35ms); */
```

**Step 5: Remove record item hover lift**

Replace lines 499-503:
```css
.record-item:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
}
```
(Remove `transform: translateY(-2px)` and the heavy `0 10px 20px` shadow.)

**Step 6: Remove filter chip hover lift**

In `.filter-chip.active` (lines 459-463), remove `transform: translateY(-1px)`.

**Step 7: Simplify modal overlay**

Replace line 1362:
```css
background: rgba(0, 0, 0, 0.25);
backdrop-filter: blur(6px);
-webkit-backdrop-filter: blur(6px);
```

**Step 8: Verify visually**

Open in browser. Page should look cleaner — flat shadows, no floating cards, no jumping on hover, no gradient blobs. Warm beige background should feel calmer.

---

## Task 3: Font Size Normalization

**Files:**
- Modify: `screenr.html` — approximately 90 CSS rules with font-size values in lines 34-2194

**Step 1: Global font-size replacements in the CSS section (lines 34-2194 ONLY)**

Apply these systematic replacements within the `<style>` block:
- `font-size: 0.6rem` → `font-size: var(--text-xs)` (0.75rem)
- `font-size: 0.65rem` → `font-size: var(--text-xs)`
- `font-size: 0.7rem` → `font-size: var(--text-sm)`
- `font-size: 0.72rem` → `font-size: var(--text-sm)`
- `font-size: 0.75rem` → `font-size: var(--text-xs)`
- `font-size: 0.78rem` → `font-size: var(--text-sm)`
- `font-size: 0.8rem` → `font-size: var(--text-sm)`
- `font-size: 0.85rem` → `font-size: var(--text-base)`
- `font-size: 0.875rem` → `font-size: var(--text-base)`
- `font-size: 0.9rem` → `font-size: var(--text-base)`
- `font-size: 0.95rem` → `font-size: var(--text-lg)`
- `font-size: 1.1rem` → `font-size: var(--text-xl)`
- `font-size: 1.2rem` → `font-size: var(--text-xl)`
- `font-size: 1.3rem` → `font-size: var(--text-2xl)`
- `font-size: 1.5rem` → `font-size: var(--text-2xl)`

**CRITICAL**: Only replace within the main `<style>` block (lines 34-2194). Do NOT replace font-size values in JS-generated inline HTML (lines 4273+) in this task — those will be addressed in JS cleanup later.

**Step 2: Verify**

Open app. Text should be slightly larger overall (floor raised from 0.6rem to 0.75rem). All labels, badges, chips should still be readable and not overflow their containers.

---

## Task 4: Border Radius + Scrollbar Normalization

**Files:**
- Modify: `screenr.html` — CSS rules with hardcoded border-radius in lines 34-2194

**Step 1: Replace rogue border-radius values in CSS**

Within lines 34-2194:
- `border-radius: 4px` → `border-radius: var(--radius-sm)` (where it appears on interactive elements)
- `border-radius: 6px` → `border-radius: var(--radius-sm)`
- `border-radius: 8px` → `border-radius: var(--radius-sm)` (where it was --radius-sm before)
- `border-radius: 12px` → `border-radius: var(--radius)`
- `border-radius: 14px` → `border-radius: var(--radius-lg)`
- `border-radius: 18px` → `border-radius: var(--radius-lg)`
- `border-radius: 20px` → `border-radius: var(--radius-pill)`
- `border-radius: 999px` → `border-radius: var(--radius-pill)`
- Keep `border-radius: 50%` as-is (circles)
- Keep `border-radius: 40%` as-is (body pseudo-elements — but those are being removed in Task 2)

**Step 2: Add Firefox scrollbar support**

After the `::-webkit-scrollbar` rules (line 1457), add:
```css
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(0,0,0,0.2) transparent;
}
```

**Step 3: Fix uppercase letter-spacing**

In `.detail-section h3` (line 577), change `letter-spacing: 0.5px` → `letter-spacing: 0.08em`.

---

## Task 5: Menu HTML Restructure (10 → 5 menus)

**Files:**
- Modify: `screenr.html:2206-2454` (the entire toolbar with 10 menu-btn divs)

**Step 1: Replace the toolbar HTML**

Replace lines 2206-2454 (the `<div class="toolbar">` through the closing `</div>` of the Help menu-btn) with the new 5-menu structure. All onclick handlers MUST use the same function names as before — we are reorganizing, not renaming.

The new toolbar HTML:

```html
<div class="toolbar" role="menubar">
  <!-- FILE menu -->
  <div class="menu-btn" role="none">
    <button role="menuitem" aria-haspopup="true" aria-expanded="false" onclick="toggleMenu(this)">File</button>
    <div class="menu-dropdown" role="menu">
      <div class="menu-submenu" role="none">
        <button class="menu-item" role="menuitem" aria-haspopup="true">Import</button>
        <div class="submenu-dropdown" role="menu">
          <button class="menu-item" role="menuitem" onclick="importRIS()">Import RIS</button>
          <button class="menu-item" role="menuitem" onclick="importEndNote()">Import EndNote XML</button>
          <button class="menu-item" role="menuitem" onclick="importBibTeX()">Import BibTeX</button>
          <button class="menu-item" role="menuitem" onclick="importCSV()">Import CSV</button>
          <button class="menu-item" role="menuitem" onclick="importPubMedNBib()">Import PubMed NBib</button>
          <button class="menu-item" role="menuitem" onclick="importProvenanceCSV()">Import Provenance CSV</button>
          <div class="menu-divider" role="separator"></div>
          <button class="menu-item" role="menuitem" onclick="openPubMedSearch()">Search PubMed</button>
          <button class="menu-item" role="menuitem" onclick="openCrossRefSearch()">Search CrossRef</button>
          <button class="menu-item" role="menuitem" onclick="openOpenAlexSearch()">Search OpenAlex</button>
        </div>
      </div>
      <div class="menu-submenu" role="none">
        <button class="menu-item" role="menuitem" aria-haspopup="true">Export</button>
        <div class="submenu-dropdown" role="menu">
          <button class="menu-item" role="menuitem" onclick="exportJSON()">Export JSON</button>
          <button class="menu-item" role="menuitem" onclick="exportCSV()">Export CSV</button>
          <button class="menu-item" role="menuitem" onclick="exportRIS()">Export RIS</button>
          <button class="menu-item" role="menuitem" onclick="exportDecisions()">Export Decisions</button>
          <button class="menu-item" role="menuitem" onclick="exportExtractedData()">Export Extracted Data</button>
          <button class="menu-item" role="menuitem" onclick="exportProvenanceCsv()">Export Provenance CSV</button>
          <div class="menu-divider" role="separator"></div>
          <button class="menu-item" role="menuitem" onclick="showHighDPIExport()">High-DPI Figure Export</button>
          <button class="menu-item" role="menuitem" onclick="exportForestPlotHighDPI()">Export Forest Plot (300 DPI)</button>
          <button class="menu-item" role="menuitem" onclick="exportFunnelPlotHighDPI()">Export Funnel Plot (300 DPI)</button>
          <button class="menu-item" role="menuitem" onclick="exportAllFiguresHighDPI()">Export All Figures (ZIP)</button>
          <div class="menu-divider" role="separator"></div>
          <button class="menu-item" role="menuitem" onclick="showExportOptions()">Export to Reference Manager</button>
        </div>
      </div>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="saveProject()">Save Project</button>
      <button class="menu-item" role="menuitem" onclick="loadProject()">Load Project</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="openTruthCertModal()">TruthCert Certification</button>
      <button class="menu-item" role="menuitem" onclick="exportTruthCertDisclosure()">Export TruthCert Bundle</button>
    </div>
  </div>

  <!-- SCREENING menu -->
  <div class="menu-btn" role="none">
    <button role="menuitem" aria-haspopup="true" aria-expanded="false" onclick="toggleMenu(this)">Screening</button>
    <div class="menu-dropdown" role="menu">
      <button class="menu-item" role="menuitem" onclick="openPICOBuilder()">PICO Builder</button>
      <button class="menu-item" role="menuitem" onclick="loadRuleset()">Load Ruleset</button>
      <button class="menu-item" role="menuitem" onclick="saveRuleset()">Save Ruleset</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="runAutoScreen()">Run Auto-Screen</button>
      <button class="menu-item" role="menuitem" onclick="runDeduplication()">Run Deduplication</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="toggleBatchMode()">Batch Mode</button>
      <button class="menu-item" role="menuitem" onclick="selectAllVisible()">Select All Visible</button>
      <button class="menu-item" role="menuitem" onclick="clearBatchSelection()">Clear Selection</button>
      <button class="menu-item" role="menuitem" onclick="batchMarkAs('include')">Batch Include</button>
      <button class="menu-item" role="menuitem" onclick="batchMarkAs('exclude')">Batch Exclude</button>
      <button class="menu-item" role="menuitem" onclick="batchMarkAs('maybe')">Batch Maybe</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showStoppingAnalysis()">SAFE Stopping Analysis</button>
      <button class="menu-item" role="menuitem" onclick="showIRRAnalysis()">Inter-Rater Reliability</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showNeuralScreener()">Neural Network Prioritization</button>
      <button class="menu-item" role="menuitem" onclick="showMLPrioritization()">ML Prioritization</button>
      <button class="menu-item" role="menuitem" onclick="applyMLPrioritization()">Apply ML Ranking</button>
      <button class="menu-item" role="menuitem" onclick="trainMLModel()">Retrain ML Model</button>
    </div>
  </div>

  <!-- SYNTHESIS menu -->
  <div class="menu-btn" role="none">
    <button role="menuitem" aria-haspopup="true" aria-expanded="false" onclick="toggleMenu(this)">Synthesis</button>
    <div class="menu-dropdown" role="menu">
      <button class="menu-item" role="menuitem" onclick="showMetaAnalysis()">Pairwise Meta-Analysis</button>
      <button class="menu-item" role="menuitem" onclick="showForestPlot()">Forest Plot</button>
      <button class="menu-item" role="menuitem" onclick="showFunnelPlot()">Funnel Plot</button>
      <button class="menu-item" role="menuitem" onclick="exportMetaAnalysis()">Export MA Data</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showSensitivityAnalysis()">Sensitivity Analyses</button>
      <button class="menu-item" role="menuitem" onclick="showMetaRegression()">Meta-Regression</button>
      <button class="menu-item" role="menuitem" onclick="showMultipleMetaRegression()">Multiple Meta-Regression</button>
      <button class="menu-item" role="menuitem" onclick="showSubgroupAnalysis()">Subgroup Analysis</button>
      <button class="menu-item" role="menuitem" onclick="showGOSHAnalysis()">GOSH Outlier Analysis</button>
      <div class="menu-divider" role="separator"></div>
      <div class="menu-submenu" role="none">
        <button class="menu-item" role="menuitem" aria-haspopup="true">Network MA</button>
        <div class="submenu-dropdown" role="menu">
          <button class="menu-item" role="menuitem" onclick="showNMA()">Network Meta-Analysis</button>
          <button class="menu-item" role="menuitem" onclick="showNMARegression()">NMA Meta-Regression</button>
          <button class="menu-item" role="menuitem" onclick="showCINeMA()">CINeMA Framework</button>
          <button class="menu-item" role="menuitem" onclick="showComponentNMA()">Component NMA</button>
          <button class="menu-item" role="menuitem" onclick="showBayesianNMA()">Bayesian NMA</button>
          <button class="menu-item" role="menuitem" onclick="showThresholdNMA()">Threshold NMA</button>
        </div>
      </div>
      <div class="menu-submenu" role="none">
        <button class="menu-item" role="menuitem" aria-haspopup="true">Specialized</button>
        <div class="submenu-dropdown" role="menu">
          <button class="menu-item" role="menuitem" onclick="showDTA()">DTA Meta-Analysis</button>
          <button class="menu-item" role="menuitem" onclick="showHSROC()">HSROC Model (DTA)</button>
          <div class="menu-divider" role="separator"></div>
          <button class="menu-item" role="menuitem" onclick="showIPDMetaAnalysis()">IPD Meta-Analysis</button>
          <button class="menu-item" role="menuitem" onclick="showSurvivalMA()">Survival / Time-to-Event</button>
          <button class="menu-item" role="menuitem" onclick="showProportionMA()">Proportion Meta-Analysis</button>
          <button class="menu-item" role="menuitem" onclick="showCorrelationMA()">Correlation Meta-Analysis</button>
          <div class="menu-divider" role="separator"></div>
          <button class="menu-item" role="menuitem" onclick="showMultivariateMA()">Multivariate MA</button>
          <button class="menu-item" role="menuitem" onclick="showDoseResponse()">Dose-Response MA</button>
          <button class="menu-item" role="menuitem" onclick="showRobustVariance()">Robust Variance (RVE)</button>
          <button class="menu-item" role="menuitem" onclick="showCrossoverMA()">Crossover Trials</button>
          <button class="menu-item" role="menuitem" onclick="showClusterRCTMA()">Cluster RCT Adjustment</button>
        </div>
      </div>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showBayesianMA()">Bayesian Meta-Analysis</button>
      <button class="menu-item" role="menuitem" onclick="showBayesianDiagnostics()">Bayesian Diagnostics</button>
      <div class="menu-divider" role="separator"></div>
      <div class="menu-submenu" role="none">
        <button class="menu-item" role="menuitem" aria-haspopup="true">Publication Bias</button>
        <div class="submenu-dropdown" role="menu">
          <button class="menu-item" role="menuitem" onclick="showPCurve()">P-Curve Analysis</button>
          <button class="menu-item" role="menuitem" onclick="showZCurve()">Z-Curve 2.0</button>
          <button class="menu-item" role="menuitem" onclick="showPetPeese()">PET-PEESE</button>
          <button class="menu-item" role="menuitem" onclick="show3PSM()">3-Parameter Selection</button>
          <button class="menu-item" role="menuitem" onclick="showCopas()">Copas Selection Model</button>
        </div>
      </div>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showEffectSizeConverter()">Effect Size Converter</button>
      <button class="menu-item" role="menuitem" onclick="showStatisticalEstimators()">Statistical Estimators</button>
      <button class="menu-item" role="menuitem" onclick="showPowerCalculator()">Power Calculator</button>
      <button class="menu-item" role="menuitem" onclick="showFragilityIndex()">Fragility Index Calculator</button>
    </div>
  </div>

  <!-- REVIEW menu -->
  <div class="menu-btn" role="none">
    <button role="menuitem" aria-haspopup="true" aria-expanded="false" onclick="toggleMenu(this)">Review</button>
    <div class="menu-dropdown" role="menu">
      <button class="menu-item" role="menuitem" onclick="showProgressStats()">Progress Statistics</button>
      <button class="menu-item" role="menuitem" onclick="showPRISMA()">PRISMA Flow Diagram</button>
      <button class="menu-item" role="menuitem" onclick="showRoBSummary()">Risk of Bias Summary</button>
      <button class="menu-item" role="menuitem" onclick="showManuscriptBundle()">Manuscript Evidence Bundle</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showGRADEAssessment()">GRADE Assessment</button>
      <button class="menu-item" role="menuitem" onclick="showGRADEAutomated()">GRADE Automated Analysis</button>
      <button class="menu-item" role="menuitem" onclick="showOISCalculator()">OIS Calculator</button>
      <button class="menu-item" role="menuitem" onclick="exportSummaryOfFindings()">Summary of Findings</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showProtocolBuilder()">Protocol Builder (PROSPERO)</button>
      <button class="menu-item" role="menuitem" onclick="showCTGovSearch()">ClinicalTrials.gov Search</button>
      <button class="menu-item" role="menuitem" onclick="showMultiRegistrySearch()">Multi-Registry Search</button>
      <button class="menu-item" role="menuitem" onclick="showSearchTranslator()">Database Search Translator</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showLivingSR()">Living SR Settings</button>
      <button class="menu-item" role="menuitem" onclick="showRapidReviewMode()">Rapid Review Mode</button>
      <button class="menu-item" role="menuitem" onclick="showUmbrellaReview()">Umbrella Review Tools</button>
      <button class="menu-item" role="menuitem" onclick="showScopingReview()">Scoping Review Tools</button>
      <button class="menu-item" role="menuitem" onclick="showCitationChainer()">Citation Chaining</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showKMDigitizer()">KM Curve Digitizer</button>
      <button class="menu-item" role="menuitem" onclick="showPDFTableExtractor()">PDF Table Extractor</button>
      <button class="menu-item" role="menuitem" onclick="showPDFTextExtractor()">PDF Text Extractor</button>
      <button class="menu-item" role="menuitem" onclick="showDataEntryValidator()">Data Entry Validator</button>
    </div>
  </div>

  <!-- HELP menu -->
  <div class="menu-btn" role="none">
    <button role="menuitem" aria-haspopup="true" aria-expanded="false" onclick="toggleMenu(this)">Help</button>
    <div class="menu-dropdown" role="menu">
      <button class="menu-item" role="menuitem" onclick="showQuickStartWizard()">Quick Start Wizard</button>
      <button class="menu-item" role="menuitem" onclick="showHelpCenter()">Help Center</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="TutorialSystem.start('quickStart')">Tour: Quick Start</button>
      <button class="menu-item" role="menuitem" onclick="TutorialSystem.start('metaAnalysis')">Tour: Meta-Analysis</button>
      <button class="menu-item" role="menuitem" onclick="TutorialSystem.start('advancedMethods')">Tour: Advanced Methods</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="loadExampleDataset()">Load Example Dataset</button>
      <button class="menu-item" role="menuitem" onclick="showMethodCitations()">Method Citations (50+)</button>
      <button class="menu-item" role="menuitem" onclick="showKeyboardShortcuts()">Keyboard Shortcuts</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showValidation()">Validation Suite</button>
      <button class="menu-item" role="menuitem" onclick="showExtendedValidation()">Extended Validation</button>
      <button class="menu-item" role="menuitem" onclick="showBenchmarks()">Performance Benchmarks</button>
      <button class="menu-item" role="menuitem" onclick="showStatisticalMethods()">Statistical Methods</button>
      <div class="menu-divider" role="separator"></div>
      <button class="menu-item" role="menuitem" onclick="showCollaboration()">Peer Collaboration</button>
      <button class="menu-item" role="menuitem" onclick="showAbout()">About Screenr v11.0.0</button>
    </div>
  </div>

  <!-- Mode tabs — kept in toolbar for now, will be moved to sub-bar in Task 10 -->
  <div class="mode-tabs">
    <button class="mode-tab active" onclick="setMode('screen')">Screen</button>
    <button class="mode-tab" onclick="setMode('extract')">Extract</button>
    <button class="mode-tab" onclick="setMode('rob')">RoB</button>
    <button class="mode-tab" onclick="setMode('meta')">Meta</button>
  </div>
</div>
```

**Step 2: Verify all functions are reachable**

Grep for every `onclick="show` and `onclick="export` in the old menus. Confirm each function appears exactly once in the new menus (no duplicates, no missing). The following were intentionally removed as duplicates:
- `showPRISMAGenerator()` (was in Registry — kept `showPRISMA()` in Review)
- `showPRISMATemplates()` (was in Statistics — consolidated into `showPRISMA()`)
- `showIRR()` (was in Reports — kept `showIRRAnalysis()` in Screening)
- Second `showMultivariateMA()` (was in Statistics — kept one in Synthesis > Specialized)
- Second `exportProvenanceCsv()` (was in TruthCert — kept in File > Export)
- Second `toggleDarkMode()` (was in Tools menu — kept toolbar button only)
- `AdditionalValidationTests.runAll()` (moved to Help > Extended Validation conceptually)

---

## Task 6: Click-to-Toggle Menu JS

**Files:**
- Modify: `screenr.html` — add JS function near the top of the main `<script>` block (after line ~4273)

**Step 1: Add the toggleMenu function and keyboard navigation**

Insert this JS right after the opening `<script>` tag at line 4273:

```javascript
// ============================================================
// CLICK-TO-TOGGLE MENUS (replaces hover-only)
// ============================================================

function toggleMenu(btn) {
  const menuBtn = btn.closest('.menu-btn');
  const dropdown = menuBtn.querySelector('.menu-dropdown');
  const isOpen = menuBtn.classList.contains('menu-open');

  // Close all other menus first
  document.querySelectorAll('.menu-btn.menu-open').forEach(m => {
    m.classList.remove('menu-open');
    m.querySelector('button[aria-expanded]').setAttribute('aria-expanded', 'false');
  });

  if (!isOpen) {
    menuBtn.classList.add('menu-open');
    btn.setAttribute('aria-expanded', 'true');
    // Focus first menu item
    const firstItem = dropdown.querySelector('.menu-item');
    if (firstItem) firstItem.focus();
  }
}

// Close menus on outside click
document.addEventListener('click', (e) => {
  if (!e.target.closest('.menu-btn')) {
    document.querySelectorAll('.menu-btn.menu-open').forEach(m => {
      m.classList.remove('menu-open');
      m.querySelector('button[aria-expanded]')?.setAttribute('aria-expanded', 'false');
    });
  }
});

// Close menus on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.menu-btn.menu-open').forEach(m => {
      m.classList.remove('menu-open');
      const trigger = m.querySelector('button[aria-expanded]');
      trigger?.setAttribute('aria-expanded', 'false');
      trigger?.focus();
    });
  }
});
```

**Step 2: Update CSS to use click-to-toggle instead of hover**

Replace line 193-194:
```css
/* Old hover-only:
.menu-btn:hover .menu-dropdown,
.menu-dropdown:hover { display: block; }
*/

/* New click-to-toggle: */
.menu-btn.menu-open > .menu-dropdown { display: block; }
.menu-submenu:hover > .submenu-dropdown,
.menu-submenu:focus-within > .submenu-dropdown { display: block; }
```

The submenus within an open dropdown still use hover (acceptable since the parent is already open via click). Added `focus-within` for keyboard accessibility.

**Step 3: Verify**

Click each of the 5 menu buttons. Dropdown should open on click and close on outside click or Escape. Submenus should open on hover within open dropdown.

---

## Task 7: Command Palette (Cmd+K)

**Files:**
- Modify: `screenr.html` — add HTML before `</body>` and JS in the script block

**Step 1: Add command palette HTML**

Before the closing `</body>` tag (but inside the app), add:

```html
<!-- Command Palette -->
<div class="modal-overlay" id="commandPalette" role="dialog" aria-modal="true" aria-label="Command palette">
  <div class="modal" style="max-width: 560px; margin-top: 80px; align-self: flex-start;">
    <div style="padding: var(--space-3) var(--space-4);">
      <input type="text" id="cmdInput" placeholder="Type a command..." style="width: 100%; padding: var(--space-3); border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: var(--text-base); background: var(--bg-panel);" autocomplete="off">
    </div>
    <div id="cmdResults" style="max-height: 360px; overflow-y: auto; padding: var(--space-2);"></div>
  </div>
</div>
```

**Step 2: Add command palette JS**

```javascript
// ============================================================
// COMMAND PALETTE (Ctrl+K / Cmd+K)
// ============================================================

const COMMAND_REGISTRY = [
  // File
  { label: 'Import RIS', action: importRIS, category: 'File' },
  { label: 'Import EndNote XML', action: importEndNote, category: 'File' },
  { label: 'Import BibTeX', action: importBibTeX, category: 'File' },
  { label: 'Import CSV', action: importCSV, category: 'File' },
  { label: 'Import PubMed NBib', action: importPubMedNBib, category: 'File' },
  { label: 'Export JSON', action: exportJSON, category: 'File' },
  { label: 'Export CSV', action: exportCSV, category: 'File' },
  { label: 'Export RIS', action: exportRIS, category: 'File' },
  { label: 'Save Project', action: saveProject, category: 'File' },
  { label: 'Load Project', action: loadProject, category: 'File' },
  // Screening
  { label: 'PICO Builder', action: openPICOBuilder, category: 'Screening' },
  { label: 'Run Auto-Screen', action: runAutoScreen, category: 'Screening' },
  { label: 'Run Deduplication', action: runDeduplication, category: 'Screening' },
  { label: 'SAFE Stopping Analysis', action: showStoppingAnalysis, category: 'Screening' },
  { label: 'Inter-Rater Reliability', action: showIRRAnalysis, category: 'Screening' },
  { label: 'ML Prioritization', action: showMLPrioritization, category: 'Screening' },
  { label: 'Toggle Batch Mode', action: toggleBatchMode, category: 'Screening' },
  // Synthesis
  { label: 'Pairwise Meta-Analysis', action: showMetaAnalysis, category: 'Synthesis' },
  { label: 'Forest Plot', action: showForestPlot, category: 'Synthesis' },
  { label: 'Funnel Plot', action: showFunnelPlot, category: 'Synthesis' },
  { label: 'Sensitivity Analyses', action: showSensitivityAnalysis, category: 'Synthesis' },
  { label: 'Meta-Regression', action: showMetaRegression, category: 'Synthesis' },
  { label: 'Multiple Meta-Regression', action: showMultipleMetaRegression, category: 'Synthesis' },
  { label: 'Subgroup Analysis', action: showSubgroupAnalysis, category: 'Synthesis' },
  { label: 'GOSH Outlier Analysis', action: showGOSHAnalysis, category: 'Synthesis' },
  { label: 'Network Meta-Analysis', action: showNMA, category: 'Synthesis' },
  { label: 'NMA Meta-Regression', action: showNMARegression, category: 'Synthesis' },
  { label: 'CINeMA Framework', action: showCINeMA, category: 'Synthesis' },
  { label: 'DTA Meta-Analysis', action: showDTA, category: 'Synthesis' },
  { label: 'HSROC Model', action: showHSROC, category: 'Synthesis' },
  { label: 'IPD Meta-Analysis', action: showIPDMetaAnalysis, category: 'Synthesis' },
  { label: 'Survival / Time-to-Event MA', action: showSurvivalMA, category: 'Synthesis' },
  { label: 'Proportion Meta-Analysis', action: showProportionMA, category: 'Synthesis' },
  { label: 'Multivariate MA', action: showMultivariateMA, category: 'Synthesis' },
  { label: 'Dose-Response MA', action: showDoseResponse, category: 'Synthesis' },
  { label: 'Robust Variance (RVE)', action: showRobustVariance, category: 'Synthesis' },
  { label: 'Correlation Meta-Analysis', action: showCorrelationMA, category: 'Synthesis' },
  { label: 'Crossover Trials', action: showCrossoverMA, category: 'Synthesis' },
  { label: 'Cluster RCT Adjustment', action: showClusterRCTMA, category: 'Synthesis' },
  { label: 'Bayesian Meta-Analysis', action: showBayesianMA, category: 'Synthesis' },
  { label: 'P-Curve Analysis', action: showPCurve, category: 'Synthesis' },
  { label: 'Z-Curve 2.0', action: showZCurve, category: 'Synthesis' },
  { label: 'PET-PEESE', action: showPetPeese, category: 'Synthesis' },
  { label: '3-Parameter Selection Model', action: show3PSM, category: 'Synthesis' },
  { label: 'Copas Selection Model', action: showCopas, category: 'Synthesis' },
  { label: 'Effect Size Converter', action: showEffectSizeConverter, category: 'Synthesis' },
  { label: 'Power Calculator', action: showPowerCalculator, category: 'Synthesis' },
  { label: 'Fragility Index Calculator', action: showFragilityIndex, category: 'Synthesis' },
  // Review
  { label: 'Progress Statistics', action: showProgressStats, category: 'Review' },
  { label: 'PRISMA Flow Diagram', action: showPRISMA, category: 'Review' },
  { label: 'Risk of Bias Summary', action: showRoBSummary, category: 'Review' },
  { label: 'GRADE Assessment', action: showGRADEAssessment, category: 'Review' },
  { label: 'OIS Calculator', action: showOISCalculator, category: 'Review' },
  { label: 'Summary of Findings', action: exportSummaryOfFindings, category: 'Review' },
  { label: 'Protocol Builder', action: showProtocolBuilder, category: 'Review' },
  { label: 'ClinicalTrials.gov Search', action: showCTGovSearch, category: 'Review' },
  { label: 'Living SR Settings', action: showLivingSR, category: 'Review' },
  { label: 'Umbrella Review Tools', action: showUmbrellaReview, category: 'Review' },
  { label: 'Scoping Review Tools', action: showScopingReview, category: 'Review' },
  // Help
  { label: 'Quick Start Wizard', action: showQuickStartWizard, category: 'Help' },
  { label: 'Help Center', action: showHelpCenter, category: 'Help' },
  { label: 'Load Example Dataset', action: loadExampleDataset, category: 'Help' },
  { label: 'Keyboard Shortcuts', action: showKeyboardShortcuts, category: 'Help' },
  { label: 'Validation Suite', action: showValidation, category: 'Help' },
  // Settings
  { label: 'Toggle Dark Mode', action: toggleDarkMode, category: 'Settings' },
];

function openCommandPalette() {
  const overlay = document.getElementById('commandPalette');
  overlay.classList.add('active');
  const input = document.getElementById('cmdInput');
  input.value = '';
  input.focus();
  renderCommandResults('');
}

function closeCommandPalette() {
  document.getElementById('commandPalette').classList.remove('active');
}

function renderCommandResults(query) {
  const container = document.getElementById('cmdResults');
  const q = query.toLowerCase().trim();
  const filtered = q
    ? COMMAND_REGISTRY.filter(c => c.label.toLowerCase().includes(q) || c.category.toLowerCase().includes(q))
    : COMMAND_REGISTRY.slice(0, 12);

  if (filtered.length === 0) {
    container.innerHTML = '<div style="padding: var(--space-4); text-align: center; color: var(--text-light); font-size: var(--text-sm);">No commands found</div>';
    return;
  }

  let lastCat = '';
  container.innerHTML = filtered.map((c, i) => {
    const catHeader = c.category !== lastCat
      ? `<div style="padding: var(--space-1) var(--space-3); font-size: var(--text-xs); font-weight: 600; color: var(--text-light); text-transform: uppercase; letter-spacing: 0.08em;">${c.category}</div>`
      : '';
    lastCat = c.category;
    return catHeader + `<button class="cmd-item${i === 0 ? ' cmd-active' : ''}" data-idx="${i}" onclick="executeCommand(${COMMAND_REGISTRY.indexOf(c)})" style="display: block; width: 100%; text-align: left; padding: var(--space-2) var(--space-3); border: none; background: ${i === 0 ? 'var(--primary-light)' : 'transparent'}; border-radius: var(--radius-sm); font-size: var(--text-base); cursor: pointer; color: var(--text);">${c.label}</button>`;
  }).join('');
}

function executeCommand(idx) {
  closeCommandPalette();
  const cmd = COMMAND_REGISTRY[idx];
  if (cmd && typeof cmd.action === 'function') {
    cmd.action();
  }
}

// Keyboard handler
document.addEventListener('keydown', (e) => {
  // Ctrl+K or Cmd+K to open
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    const overlay = document.getElementById('commandPalette');
    if (overlay.classList.contains('active')) {
      closeCommandPalette();
    } else {
      openCommandPalette();
    }
  }
});

// Input handler for command palette
document.addEventListener('DOMContentLoaded', () => {
  const cmdInput = document.getElementById('cmdInput');
  if (cmdInput) {
    cmdInput.addEventListener('input', (e) => renderCommandResults(e.target.value));
    cmdInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeCommandPalette();
      if (e.key === 'Enter') {
        const active = document.querySelector('.cmd-active');
        if (active) active.click();
      }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        const items = [...document.querySelectorAll('.cmd-item')];
        const curr = items.findIndex(i => i.classList.contains('cmd-active'));
        const next = e.key === 'ArrowDown' ? Math.min(curr + 1, items.length - 1) : Math.max(curr - 1, 0);
        items.forEach(i => { i.classList.remove('cmd-active'); i.style.background = 'transparent'; });
        items[next].classList.add('cmd-active');
        items[next].style.background = 'var(--primary-light)';
        items[next].scrollIntoView({ block: 'nearest' });
      }
    });
  }
});

// Close on overlay click
document.getElementById('commandPalette')?.addEventListener('click', (e) => {
  if (e.target.id === 'commandPalette') closeCommandPalette();
});
```

**Step 3: Verify**

Press Ctrl+K. Palette should open. Type "forest" — should show Forest Plot. Press Enter — should call showForestPlot(). Press Escape — should close.

---

## Task 8: Accessibility — ARIA, focus rings, role fixes

**Files:**
- Modify: `screenr.html:2203` (remove role="application")
- Modify: `screenr.html` CSS focus ring rules

**Step 1: Remove role="application"**

Change line 2203 from:
```html
<div class="app" role="application" aria-label="Screenr Systematic Review Tool">
```
to:
```html
<div class="app" aria-label="Screenr Systematic Review Tool">
```

**Step 2: Standardize focus rings**

Remove the duplicate 2px focus rule (lines 304-306) since the 3px rule at lines 1490-1504 is better. Replace lines 1490-1504 with:
```css
button:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
.record-item:focus-visible,
.filter-chip:focus-visible,
.tab:focus-visible,
.mode-tab:focus-visible,
.menu-item:focus-visible,
.rob-btn:focus-visible,
.sq-btn:focus-visible,
.qa-opt:focus-visible,
.cmd-item:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

---

## Task 9: Dark Mode — Complete Remap

**Files:**
- Modify: `screenr.html:1791-1857` (dark mode rules)

**Step 1: Expand the dark mode block**

Replace lines 1791-1857 with a comprehensive dark mode:

```css
body.dark-mode {
  --bg-main: #0f172a;
  --bg-surface: #1e293b;
  --bg-panel: #1e293b;
  --border-color: #334155;
  --text: #e2e8f0;
  --text-light: #94a3b8;
  --text-white: #f8fafc;
  --shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.5);
  /* Remap -light tints for dark backgrounds */
  --primary-light: rgba(14, 165, 164, 0.15);
  --success-light: rgba(34, 197, 94, 0.15);
  --danger-light: rgba(239, 68, 68, 0.15);
  --warning-light: rgba(217, 119, 6, 0.15);
  --info-light: rgba(37, 99, 235, 0.15);
  --purple-light: rgba(124, 58, 237, 0.15);
  /* Status backgrounds */
  --include: #166534;
  --exclude: #7f1d1d;
  --maybe: #78350f;
  --duplicate: #1e3a5f;
  --conflict: #4c1d95;
  --flagged: #7f1d1d;
}
body.dark-mode .panel-header {
  background: var(--bg-surface);
}
body.dark-mode .panel-content {
  background: var(--bg-main);
}
body.dark-mode input,
body.dark-mode select,
body.dark-mode textarea {
  background: var(--bg-surface);
  border-color: var(--border-color);
  color: var(--text);
}
body.dark-mode button:not(.primary):not(.success):not(.danger):not(.warning):not(.info) {
  background: var(--bg-surface);
  border-color: var(--border-color);
  color: var(--text);
}
body.dark-mode .record-item {
  background: var(--bg-surface);
  border-color: var(--border-color);
}
body.dark-mode .record-item.selected {
  background: rgba(14, 165, 164, 0.2);
}
body.dark-mode .filter-chip {
  border-color: var(--border-color);
}
body.dark-mode .modal {
  background: var(--bg-surface);
  border-color: var(--border-color);
}
body.dark-mode .modal-header,
body.dark-mode .modal-footer {
  background: var(--bg-main);
  border-color: var(--border-color);
}
body.dark-mode .modal-body {
  background: var(--bg-surface);
}
body.dark-mode .meta-table th {
  background: var(--bg-main);
}
body.dark-mode .meta-table td {
  border-color: var(--border-color);
}
body.dark-mode kbd {
  background: var(--bg-main) !important;
  color: var(--text);
}
body.dark-mode .forest-plot {
  background: var(--bg-panel);
}
body.dark-mode .decision-bar {
  background: var(--bg-surface);
  border-color: var(--border-color);
}
body.dark-mode .toast {
  background: var(--bg-surface);
  border-color: var(--border-color);
  color: var(--text);
}
body.dark-mode .detail-section.collapsible h3 {
  background: rgba(255, 255, 255, 0.04);
}
body.dark-mode .extract-section {
  background: var(--bg-surface);
}
body.dark-mode .rob-domain {
  background: var(--bg-surface);
}
body.dark-mode .qa-item {
  background: var(--bg-surface);
}
body.dark-mode .stat-card {
  background: var(--bg-surface);
}
body.dark-mode .search-box input {
  background: var(--bg-main);
}
```

**Step 2: Verify**

Toggle dark mode. All panels, modals, chips, toasts should have dark backgrounds with readable text. No bright white rectangles anywhere.

---

## Task 10: Layout — Mode tabs sub-bar, decision bar, panel sizing, progress bar

**Files:**
- Modify: `screenr.html` CSS (panel grid)
- Modify: `screenr.html` HTML (move mode tabs, fix decision bar)

**Step 1: Update main grid**

Change the main grid definition (line 275):
```css
main {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr) 420px;
  gap: var(--space-3);
  padding: var(--space-3);
  overflow: hidden;
}
```

**Step 2: Add mode tabs sub-bar CSS**

Add after the header styles:
```css
.mode-sub-bar {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-5);
  background: var(--bg-panel);
  border-bottom: 1px solid var(--border-color);
  z-index: 99;
}
.mode-sub-bar .mode-tab {
  padding: var(--space-2) var(--space-4);
  border: none;
  background: transparent;
  color: var(--text-light);
  font-size: var(--text-base);
  font-weight: 600;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  border-bottom: 2px solid transparent;
}
.mode-sub-bar .mode-tab.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
  background: var(--primary-light);
}
.mode-sub-bar .mode-tab:hover:not(.active) {
  background: var(--bg-surface);
  color: var(--text);
}
.mode-sub-bar .cmd-hint {
  margin-left: auto;
  font-size: var(--text-xs);
  color: var(--text-light);
}
.mode-sub-bar .cmd-hint kbd {
  padding: 2px 6px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-family: monospace;
  font-size: var(--text-xs);
}
```

**Step 3: Move mode tabs from header to sub-bar in HTML**

Remove the mode-tabs div from inside the toolbar. Add a new element between `</header>` and `<main>`:

```html
<div class="mode-sub-bar">
  <button class="mode-tab active" onclick="setMode('screen')">Screen</button>
  <button class="mode-tab" onclick="setMode('extract')">Extract</button>
  <button class="mode-tab" onclick="setMode('rob')">RoB</button>
  <button class="mode-tab" onclick="setMode('meta')">Meta</button>
  <span class="cmd-hint"><kbd>Ctrl</kbd>+<kbd>K</kbd> Command Palette</span>
</div>
```

Update the `.app` grid to accommodate:
```css
.app {
  display: grid;
  grid-template-rows: auto auto 1fr;
  min-height: 100vh;
  height: 100vh;
  position: relative;
  z-index: 1;
}
```

**Step 4: Make decision bar always visible**

Change line 2545 from `style="display: none;"` to `style=""`. Add CSS:
```css
.decision-bar.disabled button {
  opacity: 0.4;
  pointer-events: none;
}
```

Update JS: instead of `decisionBar.style.display = 'none'`, toggle the `.disabled` class.

**Step 5: Improve header progress bar**

Change `.header-progress` CSS:
```css
.header-progress {
  height: 6px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-pill);
  overflow: hidden;
  width: 120px;
}
```

**Step 6: Verify**

- Mode tabs should appear in a clean sub-bar below the header
- Decision bar should be visible but grayed out when no record is selected
- Progress bar should be thicker and more visible
- 3-panel layout should have slightly narrower left (300px) and wider right (420px)

---

## Task 11: Final Verification

**Step 1: Div balance check**

Count `<div` (excluding JS regex patterns) vs `</div>` — must match.

**Step 2: Script integrity check**

Search for literal `</script>` inside template literals — must not exist. Use `${'<'}/script>` pattern.

**Step 3: Function reachability check**

Every function that was previously in an onclick must still be callable from either:
- The new 5-menu structure, OR
- The command palette (COMMAND_REGISTRY)

**Step 4: Cross-browser quick test**

Open in Chrome and Edge. Verify:
- All 5 menus open/close on click
- Cmd+K opens command palette
- Dark mode toggle works and looks correct
- Record items don't jump on hover
- Shadows are subtle, not heavy
- No gradient blobs visible

---

## Summary of Changes

| Category | Before | After |
|----------|--------|-------|
| Top-level menus | 10 | 5 |
| Total menu items | 124 | ~85 (duplicates removed) |
| Max nesting depth | 3 | 2 |
| Menu activation | Hover-only | Click-to-toggle |
| Font sizes used | 17 | 6 tokens |
| Shadow levels | 3 (heavy) | 4 (flat) |
| Body bg elements | 5 gradients | 1 solid color |
| Hover animations | translateY everywhere | Background-only |
| Dark mode overrides | 11 variables | 24 variables + 15 components |
| Command palette | None | Ctrl+K fuzzy search |
| role="application" | On entire app | Removed |
| ARIA menu roles | None | Full menubar pattern |
