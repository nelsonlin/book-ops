# Task: Multi-Step Selector Refinement & Deep Crawl for taiwan_library.py

## Context
- **Project Goal:** `taiwan_library.py` should search the meta-search engine and then follow links to individual library results to get full details.
- **Problem:** The meta-search page (`taiwanlibrarysearch.herokuapp.com`) is a React app. Results are grouped in `content-block` containers by source (e.g., "HyRead", "台灣雲端書庫").
- **Requirement:** 
    1.  Extract the list of book result links from the meta-search page.
    2.  **Navigate to each link** to extract detailed metadata (Title, Author, Format, Date).
    3.  Return a list of `BookResult` objects.

## Implementation Steps
1.  **Analyze Results Page:** Inspect `output/taiwan_library/02_after_search.html`. Look for the `.content-block` and `.items-body-content` structures.
2.  **Refine Initial Selectors:** 
    - Update `RESULT_ROW_SELECTORS` to target the actual result items in the React app (e.g., `.items-body-content a`).
3.  **Implement Deep Crawl:**
    - In `_extract_results_from_rows`, instead of just parsing the link text, use the `page` (or a new `context.new_page()`) to visit the `href` of each result.
    - **Optimization:** To keep it fast, you can visit the first 3-5 links or implement a small loop.
    - **Parsing:** Once on the library's detail page (e.g., a HyRead or Udn page), use generic or site-specific selectors to find the book's metadata.
4.  **Update Heuristics:** The `_guess_*` functions should be used as fallbacks if the detail page parsing fails.

## Done Criteria
- [ ] Scraper successfully identifies result links within the `.content-block` sections.
- [ ] Scraper navigates to at least one library detail page and extracts information.
- [ ] Final output contains real book metadata (e.g., "Python 程式設計") instead of just library names.
- [ ] All 30 unit tests in `tests/test_taiwan_library.py` still pass.

## Technical Hint
The meta-search page uses Semantic UI. Results are often inside `div.items-body-content`. The links (`<a>`) inside these divs are the targets for the deep crawl.
