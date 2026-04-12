# PRODUCT.md

Book-Ops is a CLI that accepts a book title, searches multiple sites, extracts metadata, normalizes fields, and returns readable output for borrowing or sourcing decisions.

## Features
- **Deep Crawl:** Navigates from meta-search results to individual library pages for high-fidelity data.
- **Hierarchical Extraction:** Optimized "Platform -> Book -> Library" loop to reduce redundant crawls.
- **Multi-Output:** Supports rich table, JSON, and TSV formats.
- **Debug Artifacts:** Automatic HTML/PNG/Log snapshots for every search session.

## Current Stage
**Sprint 1 Completed.** Taiwan Library adapter is fully functional with parallel extraction and "Level 4" precision across HyRead, UDN, NTL, and Taiwan Cloud Bookcase.

## Target Platforms
1.  **Taiwan Library (Verified)**
2.  KSML (Backlog)
3.  Z-Library (Backlog)
