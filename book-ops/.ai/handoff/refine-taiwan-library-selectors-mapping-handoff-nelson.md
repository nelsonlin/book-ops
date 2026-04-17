# Task: Update BookResult Model and Detail Selectors

## Objective
Update the `BookResult` model to support cover images and refine `taiwan_library.py` with site-specific selectors for major library platforms.

## Implementation Steps

### 1. Update `models.py`
- Add `frontcover: str = ""` to the `BookResult` dataclass.
- Ensure `to_dict()` still works as expected.

### 2. Refine `sites/taiwan_library.py`
Based on `refine-taiwan-library-update-selector-hint.md`, implement site-specific logic in `_extract_detail_field`:

- **HyRead:**
    - Title: `.book-detail h3`
    - Author: `p.note:has-text("作者：")`
    - Date: `p.note:has-text("出版年：")`
    - Format: `p.note:has-text("格式：")`
    - Frontcover: `.book-cover img` (src)

- **UDN:**
    - Title: `h1.text-lg`
    - Author: `a[href*="search?keyword="]` (text)
    - Frontcover: `img[alt="cover"]` (src)
    - Date/Format: Extract from the info block where possible.

- **國立公共資訊圖書館 (NTL):**
    - Title: `h1`
    - Frontcover: `.cptb figure img` (src)
    - Format: `p:has-text("物件類型：")`
    - Date: `#bookdetailcpcontentblock li:has-text("出版年：")`

- **台灣雲端書庫 (EbookService):**
    - Title: `h2`
    - Frontcover: `.cover img` (src)
    - Author: `td:has-text("作者") + td`
    - Date: `td:has-text("出版日期") + td`

### 3. Update Handoff in `_extract_results_from_rows`
- Ensure the `frontcover` extracted from `_extract_detail_field(page, "frontcover")` is passed to the `BookResult` constructor.

## Verification
- [ ] `pytest tests/test_taiwan_library.py` passes (update tests for new field if needed).
- [ ] Live run (`python bookops.py "Python" --sites taiwan_library --format json`) shows the new `frontcover` field populated for results from these sites.

## Done Criteria
- [ ] `BookResult` has `frontcover` field.
- [ ] Detail pages for HyRead, UDN, NTL, and EbookService are parsed according to the provided HTML mappings.
- [ ] Scraper handles these four platforms specifically within the `_extract_detail_field` logic.
