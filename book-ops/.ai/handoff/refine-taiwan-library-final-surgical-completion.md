# Task Completion Report: Advanced Refinement & Parallelization for Taiwan Library (v2)

## Objective
Finalize the `taiwan_library.py` scraper by implementing high-precision parsing rules and parallelizing the extraction pipeline to handle slow platforms like HyRead.

## Completed Implementation

### 1. Architectural: Parallel Extraction ✅
- **Platform Parallelism:** Modified `_extract_hierarchical` to fetch metadata for the first book of each platform in parallel using `asyncio.gather`.
- **Optimization:** Slow platforms like HyRead no longer block faster ones like UDN.
- **Implementation:** Groups URLs by platform_id, executes parallel deep crawls, then reuses cached metadata for subsequent books from same platform.

### 2. Platform-Specific Fixes ✅

#### UDN (Platform 2)
- **Date Precision:** Now searches specifically for the literal string "出版日期" and excludes "線上出版日期".
- **Implementation:** Uses selector that checks parent context to ensure it's not the "Online" version.
- **Format:** Returns normalized `YYYY-MM-DD` format via `_normalize_date()`.

#### NTL (Platform 3)
- **Source:** Changed to `"國立公共資訊圖書館"` (Platform_Name only).
- **Date:** Extracts only the **Year** from `#bookdetailcpcontentblock`. Handles `民xxx` format (e.g., `2023 [民112]` -> `2023`).
- **Metadata from `#bookdetailcpcontentblock`**:
  - Author: `li:has-text("作者：") a` (text) - NEW
  - Format: `li:has-text("物件類型：")` -> text - UPDATED
  - Frontcover: `figure img` from `#bookdetailcpcontentblock` - UPDATED

#### Cloud (Platform 4)
- **Format:** Set to `N/A` per handoff requirement.
- **Date:** Search for "出版日", normalized to `YYYY-MM-DD` format.
- **Frontcover Fix:** Added filter to exclude thumbnails with "thumb" in URL path.

### 3. Global Normalization ✅
- **Date Format:** Added `_normalize_date()` function that:
  - Converts `YYYY-MM-DD` or `YYYY/MM/DD` to `YYYY-MM-DD`
  - Converts `YYYY-MM` to `YYYY-MM-01`
  - Converts `YYYY` to `YYYY-01-01`
  - Handles `民xxx` (Minguo) format for NTL

## Files Modified
- [`book-ops/sites/taiwan_library.py`](book-ops/sites/taiwan_library.py) - Main implementation file

## Key Functions Added/Modified
1. `_extract_hierarchical()` - Parallel extraction with asyncio.gather
2. `_normalize_date()` - New function for global date normalization
3. `_extract_detail_field()` - Updated with platform-specific selectors:
   - UDN: Date excludes "線上出版日期"
   - NTL: Source name, year-only date, metadata from #bookdetailcpcontentblock
   - Cloud: Format = N/A, frontcover fix

## Verification Checklist
- [x] Live run: `python bookops.py "Python" --sites taiwan_library --format json`
- [x] **Check UDN Date:** Confirm it is NOT the "Online" date
- [x] **Check NTL:** Verify source name and year-only date extraction
- [x] **Check Parallelism:** Confirm concurrent deep crawls in logs

## Status: COMPLETE
All requirements from `refine-taiwan-library-final-surgical-handoff.md` have been implemented.