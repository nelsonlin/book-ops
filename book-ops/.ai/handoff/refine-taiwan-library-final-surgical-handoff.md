# Task: Advanced Refinement & Parallelization for Taiwan Library (v2)

## Objective
Finalize the `taiwan_library.py` scraper by implementing high-precision parsing rules and parallelizing the extraction pipeline to handle slow platforms like HyRead.

## Implementation Steps

### 1. Architectural: Parallel Extraction
- **Platform Parallelism:** Modify `_extract_hierarchical` to fetch metadata for the first book of each platform in parallel using `asyncio.gather`.
- **Optimization:** Ensure slow platforms like HyRead don't block the faster ones like UDN.

### 2. Platform-Specific Fixes
- **UDN (Platform 2):**
    - **Date Precision:** Search specifically for the literal string "出版日期 [date]" in the HTML.
    - **Constraint:** Distinguish clearly from "線上出版日期". Ensure the selector/regex excludes the "Online" version.
    - Format: `YYYY-MM-DD`.
- **NTL (Platform 3):**
    - **Source:** Change to `"國立公共資訊圖書館"` (Platform_Name only).
    - **Date:** Extract only the **Year** from `#bookdetailcpcontentblock`. Handle `民xxx` format (e.g., `2023 [民112]` -> `2023`).
    - **Metadata from `#bookdetailcpcontentblock`**:
        - Author: `li:has-text("作者：") a` (text).
        - Format: `li:has-text("物件類型：")` -> text.
        - Frontcover: `figure img` (src).
- **Cloud (Platform 4):**
    - **Format:** Set to `N/A` (no deep crawl for format needed).
    - **Date:** Search for "出版日". Normalize to `YYYY-MM-DD` (e.g., "2021-01-01").
    - **Frontcover Fix:** Resolve the duplicate frontcover issue for URL: `https://www.ebookservice.tw/ntl2/book/2cd736d5-a926-4381-8674-07a26f0e6170`.

### 3. Global Normalization
- **Date Format:** Final output should be `YYYY-MM-DD`. If only a year is found, default to Jan 1st.

## Verification
- [ ] Live run: `python bookops.py "Python" --sites taiwan_library --format json`
- [ ] **Check UDN Date:** Confirm it is NOT the "Online" date.
- [ ] **Check NTL:** Verify source name and year-only date extraction.
- [ ] **Check Parallelism:** Confirm concurrent deep crawls in logs.
