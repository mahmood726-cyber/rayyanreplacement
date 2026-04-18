# Screenr v11 GUI Overhaul — "Warm Premium" Design

**Date**: 2026-02-23
**Status**: Approved
**Scope**: Full overhaul — visual tokens, menu restructure, accessibility, dark mode

## Context

Multi-persona review (3 reviewers: UX, Visual Design, Information Architecture) identified **67 findings** (13 P0, 26 P1, 28 P2). The current GUI has:
- 10 top-level menus with 124 items and 3 levels of hover-only nesting
- 17 rogue font sizes, 11 rogue border-radius values, no spacing tokens
- Overpowered shadows and translateY micro-animations on everything
- Decorative gradient blobs on body
- Broken dark mode (shallow variable swap, hardcoded whites)
- `role="application"` on app wrapper (kills screen reader navigation)
- Duplicate menu entries (PRISMA in 3 places, IRR in 2, Multivariate MA duplicated)

## Design Direction

**Warm premium**: Keep the beige (#f7f2ea) + teal (#0ea5a4) personality. Bring to Notion-level polish: clean type scale, flat shadows, no visual noise, accessible menus, working dark mode.

## 1. Design Tokens

### Type Scale (6 steps, replace 17 rogue values)
```css
--text-xs:   0.75rem;   /* 12px — badges, timestamps */
--text-sm:   0.8125rem; /* 13px — labels, metadata, chips */
--text-base: 0.875rem;  /* 14px — body text, list items */
--text-lg:   1rem;      /* 16px — section headers */
--text-xl:   1.125rem;  /* 18px — panel titles */
--text-2xl:  1.25rem;   /* 20px — modal titles */
```

### Spacing Scale (4px grid)
```css
--space-1: 4px;  --space-2: 8px;  --space-3: 12px;
--space-4: 16px; --space-5: 20px; --space-6: 24px; --space-8: 32px;
```

### Shadow Scale (flattened)
```css
--shadow-sm: 0 1px 2px rgba(15,23,42,0.04);
--shadow:    0 2px 6px rgba(15,23,42,0.06);
--shadow-md: 0 4px 12px rgba(15,23,42,0.08);
--shadow-lg: 0 8px 24px rgba(15,23,42,0.12);
```

### Border Radius (3 + pill)
```css
--radius-sm: 6px;  --radius: 10px;  --radius-lg: 14px;  --radius-pill: 999px;
```

## 2. Menu Restructure (10 → 5)

```
FILE          SCREENING       SYNTHESIS       REVIEW          HELP
Import ▸      PICO Builder    Pairwise MA     Progress Stats  Quick Start
Export ▸      Rulesets ▸      Forest/Funnel   PRISMA (unified) Help Center
Save/Load     Auto-Screen     Sensitivity     RoB Summary     Tours ▸
Certification Deduplication   Regression ▸    GRADE ▸         Example Data
              Batch Ops ▸     Subgroup/GOSH   Protocol        Citations
              ML Priority ▸   NMA ▸           Manuscript      Shortcuts
              SAFE Stopping   Specialized ▸   Living SR       About
              IRR (unified)   Pub Bias ▸      Umbrella/Scoping
                              Bayesian ▸      Citation Chain
                              Effect Tools ▸  Collaboration
```

- Max 2 levels of nesting
- Click-to-toggle with aria-expanded + keyboard navigation
- Cmd+K command palette for all features
- Context dimming by mode

## 3. Visual Cleanup

- Remove body gradient blobs (::before, ::after)
- Remove translateY hover on record items and chips
- Remove staggered panel/record animations
- Replace conic-gradient logo with solid teal square
- Fix all rogue colors (#667eea, #38bdf8, #1565c0) to design system
- Body line-height: 1.6 → 1.5
- Modal overlay: blur backdrop instead of heavy opacity

## 4. Accessibility

- Remove role="application" from app wrapper
- Add role="menubar/menu/menuitem" + aria-expanded to menus
- Click-to-toggle JS for all dropdowns
- Fix warning color contrast (#f59e0b → #d97706 on white)
- Firefox scrollbar styling
- Standardize focus rings (2px solid, 2px offset)

## 5. Dark Mode Fix

- Remap all 6 -light tint variables
- Override hardcoded whites (forest-plot, decision-bar, wizard)
- Fix collapsible h3, toast backgrounds
- Test all status colors against dark bg

## 6. Layout Refinements

- Left panel: 320px → 300px, collapse provenance filters
- Right panel: 400px → 420px min
- Mode tabs: move to sub-bar below header, larger with colored underlines
- Decision bar: always visible (disabled when no record)
- Header progress: 3px → 6px + percentage label
- Font floor: nothing below 0.75rem

## Implementation Phases

1. **CSS Tokens + Visual Cleanup** — new variables, flatten shadows, remove blobs/animations
2. **Menu HTML Restructure** — 10→5 menus, remove duplicates, click-to-toggle JS
3. **Command Palette** — Cmd+K fuzzy search overlay
4. **Accessibility** — ARIA roles, keyboard nav, color contrast, focus rings
5. **Dark Mode** — complete remap with all overrides
6. **Layout** — panel sizes, mode tabs, decision bar, progress bar
