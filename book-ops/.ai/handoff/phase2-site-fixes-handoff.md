# Task: Surgical Site Fixes (Phase 2.2)

## Objective
Establish high-precision scraping rules for Taiwan Library by migrating to resilient **Semantic Selectors** and fixing remaining `null` metadata fields.

## Context
- **Baseline:** E2E tests are functional on the GitHub runner, but metadata for UDN (Date) and NTL (Full detail) still requires refinement.
- **Rules:** Follow the technical standards in `docs/AI-COLLABORATION.md`.

## Golden Evidence (Ground Truth Targets)
Kilo Code: The scraper is not considered fixed until it can successfully parse these specific snapshots with 100% accuracy:
- **UDN:** `output/investigation/udn.html` (Target: Physical "出版日期", NOT online date).
- **NTL:** `output/investigation/ntl.html` (Target: Full metadata from `#bookdetailcpcontentblock`).
- **Cloud:** `output/investigation/cloud.html` (Target: Book title from `.detail h2`).

## Implementation Steps

### 1. Robust Date Extraction (UDN & Cloud)
- **UDN:** Search specifically for the label "出版日期" (avoiding "線上出版日期"). Use the sidebar structure: `h3:has-text('出版日期') + p`.
- **Cloud:** Normalize all dates to `YYYY-MM-DD`. Default to Jan 1st if only year is found.

### 2. NTL Precision Fix
- **Dynamic Loading:** Implement a targeted wait for `#bookdetailcpcontentblock` to ensure metadata is rendered.
- **Selectors:** 
    - **Title:** `.cp_content h1, table.cptb h1`.
    - **Author:** `li:has-text("作者：") a`.
    - **Date:** `li:has-text("出版年：")` (Extract year, handle Minguo `民xxx`).

### 3. Selector Migration (Label-Based)
- Migrate all remaining rigid CSS paths (like `div:nth-child(2) > p`) to Playwright's label-based filtering (`filter(has_text="...")`).

## Done Criteria
- [ ] `pytest tests/test_taiwan_library.py` passes (30/30).
- [ ] Scraper successfully extracts data from all three **Golden Evidence** files.
- [ ] E2E tests return full metadata for all 4 platforms (HyRead, UDN, NTL, Cloud).
- [ ] No rigid `nth-child` selectors remain in `_extract_detail_field`.
