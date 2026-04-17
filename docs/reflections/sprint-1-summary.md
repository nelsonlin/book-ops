# Sprint 1 Reflection Summary: Taiwan Library Scraper

## 1. Maturity Assessment
- **Level 1 (Basic):** 100% Success. Fixed encoding and core navigation.
- **Level 2 (Functional):** 80% Success. Repeat data remains an issue for the pipeline deduplication step.
- **Level 3 (Hierarchical):** 100% Success. Platform -> Book -> Library loop is efficient.
- **Level 4 (High-Precision):** 50% Success. Several iterations were needed for SPA sites (NTL/Cloud). Precision was lost due to "lying" network idle states and fragile selectors.

## 2. Critical Learning Points (The "Nelson/Gemini" Agreement)
- **Label-Based Selectors:** Moving forward, we will prioritize `has_text` labels (e.g., "作者：") over structural CSS paths.
- **Defensive Waiting:** For SPAs, we will no longer rely on `networkidle`. We will use explicit `wait_for_selector` for key data points.
- **Evidence-First Planning:** The Controller (Gemini) must provide an analysis of raw HTML/PNG snapshots *before* tasking the Developer (Kilo) with implementation.

## 3. Sprint 2 Action Items
1. **Deduplication:** Implement a post-processing step in `pipeline.py` to handle repeated book results.
2. **"Golden URL" Testing:** Use specific high-quality and low-quality URLs to verify scraper resilience.
3. **Wait Strategy:** Standardize the `asyncio.sleep` and `wait_for_selector` patterns for slow-loading templates.
