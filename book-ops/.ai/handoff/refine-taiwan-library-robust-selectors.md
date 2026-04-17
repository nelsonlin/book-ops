# Task: Robust Selector Implementation & Logic Fixes

## Objective
Address the failures in Platforms 2, 3, and 4 by switching to semantic selectors and fixing hierarchical title extraction bugs.

## Implementation Steps

### 1. Fix Platform 4 (Cloud Bookcase) Title Bug
In `_extract_hierarchical`, ensure that the book title is captured correctly from the accordion.
- **Problem:** Currently, results from Platform 4 often use the platform name as the book title.
- **Fix:** Locate the `.accordion .title` (or equivalent) text *inside* the platform's content block. If it contains "台灣雲端書庫", ignore it and look for the actual book name in the next header or the deep-crawled title.

### 2. Semantic Selectors for Platform 2 (UDN)
Stop using fragile Tailwind paths. In `_extract_detail_field`:
- **Date:** Search for the text "出版日期" or "日期" and get the sibling or parent text.
  - *Playwright hint:* `page.locator("div,span,p").filter(has_text="出版日期").first`
- **Author:** Use the existing logic but ensure it strips the "作者：" prefix completely.

### 3. Precision Selectors for Platform 3 (NTL)
Move NTL out of "Unknown" status using these verified selectors:
- **Root:** The detail page uses a `table.cptb`.
- **Title:** `table.cptb h1`
- **Frontcover:** `table.cptb figure img`
- **Format:** `table.cptb p:has-text("物件類型")`
- **Date:** `#bookdetailcpcontentblock li:has-text("出版年")` (Regex extract the 4-digit year).

### 4. General Metadata Cleaning
In `_extract_detail_field`, apply a global cleaning rule to all extracted fields:
- Strip "作者：", "出版年：", "格式：", "著", etc., using a robust regex before returning the value.

## Verification
- [ ] Live run: `python bookops.py "Python" --sites taiwan_library --format json`
- [ ] **Check UDN:** Date field should be a year (e.g., "2023") not `null`.
- [ ] **Check NTL:** Title and Frontcover should be populated.
- [ ] **Check Cloud Bookcase:** Title should be "Python..." not "台灣雲端書庫".

## Done Criteria
- [ ] No fragile Tailwind path selectors (e.g., no `nth-child` beyond 3 levels).
- [ ] Platform 3 (NTL) metadata is fully extracted.
- [ ] Platform 4 titles are specific to the book.
- [ ] Terminal output is readable (UTF-8 fix in bookops.py verified).
