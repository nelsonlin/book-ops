# Task: Refine taiwan_library.py Scraper

## Context
- **Approved Plan:** `docs/adr/refine-taiwan-library.md` (or see below)
- **Allowed Edit Scope:** `sites/taiwan_library.py`, `tests/test_taiwan_library.py`
- **Must Not Edit:** `models.py`, `bookops.py`
- **Goal:** Fix encoding issues, improve selectors, and add unit tests for parsing helpers.

## Implementation Steps
1.  **Fix Encoding:** In `sites/taiwan_library.py`, replace the garbled strings in `NO_RESULT_PATTERNS` and `_guess_author` (e.g., `?亦鞈?`, `雿`) with correct Unicode characters or robust regex.
2.  **Add Logging:** Enhance `_extract_results_from_rows` with `await _log(...)` calls that print the raw text of rows when parsing fails.
3.  **Improve Heuristics:** Refine `_guess_title_from_text` and `_guess_date` to be more resilient to the site's layout.
4.  **Create Tests:** Add `tests/test_taiwan_library.py` with unit tests for:
    - `_clean_text`
    - `_guess_author`
    - `_guess_format`
    - `_guess_date`
    - `_looks_like_bookish_row`

## Done Criteria
- [ ] Garbled text is replaced with readable/correct patterns.
- [ ] `tests/test_taiwan_library.py` exists and passes.
- [ ] No changes to the `BookResult` model or CLI entry point.

## Plan Summary
The current scraper has encoding issues in its heuristics. We need to move away from garbled character matches and use better regex or actual Chinese characters. We also need unit tests to verify these small helper functions without running a full Playwright session every time.
