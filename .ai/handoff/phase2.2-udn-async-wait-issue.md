# Handoff: UDN Async Loading Issue

## Current Status
- **Issue**: UDN (platform 2) scraping is failing in live E2E runs because the site renders dynamically. The `domcontentloaded` event triggers while the page is still in a "Loading" state (showing a spinner).
- **Evidence**: `book-ops/output/taiwan_library/udn_detail_2.html` confirms the presence of the loading overlay during extraction.
- **Diagnostics**: Debug logs show `h3` count of 12 (all garbled/missing expected content) vs local `udn.html` files. 

## Technical Findings
- The extraction logic (selectors) is correct and works against static files (`udn.html`).
- The failure occurs at the integration level due to timing/race conditions in the SPA navigation.

## Recommended Fix for Kilo Code
- Implement a more robust waiting strategy for UDN that explicitly monitors the removal of the loading overlay or the presence of the detail container.
- Consider utilizing `page.wait_for_load_state('networkidle')` or custom polling for expected metadata elements before extraction.
- **Alternative Path**: Use the UDN internal API endpoint `https://reading.udn.com/udnLibService/api/product/{library}/{book_id}` to fetch metadata directly as JSON, bypassing DOM extraction issues. Refer to `tools/udn-demo.py` for API endpoint details.

---

# In-Progress Report (Updated: 2026-04-18)

## Resolution Summary

### Collaboration
- **Kilo Code (AI Agent)**: Identified root cause (Nuxt.js SPA with __NUXT__ data), implemented window.__NUXT__ extraction logic
- **Nelson (E2E Tester)**: Live tested the fix, confirmed it works for first book

### Solution Implemented
Modified `book-ops/sites/taiwan_library.py` in `_deep_crawl_for_metadata()`:

1. **Primary extraction** (lines 267-300): Extract metadata directly from `window.__NUXT__.data[0].productDetail.data`
   - Fields: title, author, publishdate, format, cover (frontcover)
   - Returns immediately on success, bypassing DOM waiting entirely

2. **Fallback** (lines 301-314): If Nuxt extraction fails, waits for loading overlay to disappear, then waits for "日期時間" text to appear before using standard DOM extraction

### Verification
- ✅ Nelson E2E live test passed for first book
- ✅ Publication date (publishdate) is reliably extracted

## Next Steps

### Immediate
1. **Confirm fix works for 2nd~all books**: Run full search with multiple UDN results to verify extraction works consistently across all books returned from search results

### Future Enhancement
2. **Scale to all UDN books**: The current implementation processes only one book per search result. Need to verify that when multiple books appear in UDN platform section, all get extracted correctly. Check `_extract_hierarchical` loop at line ~190 to ensure all book accordions are processed.

3. **Performance optimization**: Consider parallel processing of multiple UDN detail pages if not already implemented (check `_deep_crawl_for_metadata` call sites)

---

(End of handoff)