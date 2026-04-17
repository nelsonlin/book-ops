# Task: Hierarchical Scraping & Deep Crawl Optimization

## Objective
Restructure `sites/taiwan_library.py` to follow the "Platform -> Book -> Library" hierarchy and optimize deep crawling with metadata auto-fill for specific platforms.

## Implementation Steps

### 1. Restructure `_extract_results_from_rows`
Instead of a flat loop over all `a` tags, implement a hierarchical search:
- **Loop 1 (Platform):** Iterate over `.content-block` elements.
  - Extract `Platform_Name` from `.items-head p`.
- **Loop 2 (Book):** Within each platform, iterate over the "M-th book" (Accordion titles).
- **Loop 3 (Library):** Within each book accordion, find all library links `[Source_Library]`.

### 2. Implement Deep Crawl with Auto-Fill
- For **Platforms 1 (HyRead), 2 (UDN), and 4 (台灣雲端書庫)**:
  - Perform a deep crawl on the **first** library link for each book.
  - Store the extracted metadata (Title, Author, Date, Format, Frontcover).
  - **Auto-Fill:** Apply this same metadata to all subsequent library links for that specific book within the same platform.
- For **Platform 3 (NTL)**: No auto-fill; parse each link as a separate entry or use existing logic.

### 3. Precision Selectors for `_extract_detail_field`
Update site-specific extraction with these new selectors:
- **HyRead (Platform 1):**
    - Title: `#center h3` (specifically within the book detail area)
    - Author: `#center p:nth-child(4)` (format: "作者：[author]著")
    - Date: `#center p:nth-child(5)` (format: "出版年：[date]")
- **UDN (Platform 2):**
    - Date: Use the specific Tailwind-based path: `main .lg\:grid-cols-\[1fr_3fr_1fr\] div:nth-child(2) p` (look for the text content).

### 4. Update Source Formatting
Set the `source` field of `BookResult` as: `"[Platform_Name]/[Source_Library]"`.

## Verification
- [ ] `pytest tests/test_taiwan_library.py` passes.
- [ ] Live run (`python bookops.py "Python" --sites taiwan_library --format json`) shows fewer deep crawls (optimized) and consistent metadata across multiple library links for the same book in Platforms 1, 2, and 4.

## Done Criteria
- [ ] Hierarchy "Platform -> Book -> Library" is implemented.
- [ ] Auto-Fill logic is active for Platforms 1, 2, and 4.
- [ ] Platform 1 and 2 use the new precision selectors from the hint MD.
- [ ] Deep crawls are performed only once per book for the specified platforms.
