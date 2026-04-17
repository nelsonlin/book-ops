# Task: Selector Refinement for taiwan_library.py

## Context
- **Status:** The scraper's "brain" (parsing logic) and encoding issues are fixed, but the "eyes" (selectors) are failing.
- **Problem:** The live search for "Python" returned 0 rows for the current `RESULT_ROW_SELECTORS`. It fell back to generic link parsing which only found site navigation links (e.g., "臺北市立圖書館").
- **Evidence:** 
    - `book-ops/output/taiwan_library/02_after_search.html`: Contains the actual HTML of the results page.
    - `book-ops/output/taiwan_library/02_after_search.png`: Shows the visual state of the results.

## Implementation Steps
1.  **Analyze Artifacts:** Inspect `02_after_search.html`. Identify the container element for the search results and the specific selector for each result row.
2.  **Update Selectors:** In `sites/taiwan_library.py`, update `RESULT_ROW_SELECTORS` with the correct CSS/Playwright selectors found in Step 1.
3.  **Refine Field Extraction:** If the rows are found but fields (Title, Author, Date) are still "Unknown", update `_extract_results_from_rows` to use specific sub-selectors within each row instead of relying solely on regex heuristics on the full row text.
4.  **Verification:** Ensure no regressions in the unit tests you previously created.

## Done Criteria
- [ ] `RESULT_ROW_SELECTORS` includes a working selector for the actual book entries.
- [ ] A live run (`python bookops.py "Python" --sites taiwan_library`) returns real book results (Title/Author) instead of just library names.
- [ ] The scraper no longer falls back to "link parsing" when results are clearly present in the HTML.

## Handoff Notes
The target site appears to be a meta-search tool. Look for where the results from individual libraries (Taipei, New Taipei, etc.) are injected. You might need to wait for a specific element or use a more specific table/div selector.
