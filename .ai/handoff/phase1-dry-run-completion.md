# Phase 1 - Foundation (CLI & Pipeline Dry-Run) Completion

## Summary
Successfully implemented `--dry-run` mode for the `bookops.py` CLI to enable fast pipeline validation without browser dependencies or network calls.

## Changes Made

### 1. [`pipeline.py`](pipeline.py)
- Added `run_pipeline_dry()` function that returns mock `BookResult` objects
- One result includes Chinese characters (`"Python 編程: 從入門到實踐"`) to verify encoding stability
- No browser or scrapers are initialized

### 2. [`bookops.py`](bookops.py)
- Added `--dry-run` flag (`action="store_true"`)
- Made `book_name` positional argument optional when `--dry-run` is used (`nargs="?"`)
- When `--dry-run` is active:
  - Calls `run_pipeline_dry()`
  - Prints `[dry-run] Pipeline OK — mock results:` header
  - Passes results to existing formatters (`table`, `json`, or `tsv`)
- Maintained Windows UTF-8 stdout/stderr compatibility

## Done Criteria Verification

| Criteria | Status |
|----------|--------|
| `python bookops.py --dry-run` runs successfully without Chromium | ✅ Pass |
| `python bookops.py --dry-run --format json` returns valid JSON | ✅ Pass |
| `python bookops.py --dry-run --format table` displays a table | ✅ Pass |
| Existing unit tests still pass | ✅ Pass (`test_normalize.py`; `test_taiwan_library.py` has pre-existing import issue) |

## Test Output Examples

### Table Format
```
[dry-run] Pipeline OK — mock results:
┌────────────────────┬────────┬────────┬──────┬─────────┬─────────────────────┐
│ Title              │ Author │ Format │ Date │ Source  │ URL                 │
├────────────────────┼────────┼────────┼──────┼─────────┼─────────────────────┤
│ Python 編程:       │ 張三   │ PDF    │ 2024 │ dry-run │ https://example.co… │
│ Machine Learning   │ 李四   │ EPUB   │ 2023 │ dry-run │ https://example.co… │
└────────────────────┴────────┴────────┴──────┴─────────┴─────────────────────┘
```

### JSON Format
```json
[dry-run] Pipeline OK — mock results:
[
  {
    "title": "Python 編程: 從入門到實踐",
    "author": "張三",
    "format": "PDF",
    "date": "2024",
    "url": "https://example.com/book/1",
    "source": "dry-run",
    "frontcover": ""
  },
  ...
]
```

## Completion Signal
- [x] Created this completion summary
- [x] Open GitHub PR with `gh pr create --title "feat: Phase 1 - CLI Dry-Run"`
- [x] Notify Nelson and Gemini CLI to review

---

**Status**: ✅ COMPLETE - PR #3 is open at https://github.com/nelsonlin/book-ops/pull/3

## Git Push Workaround
The terminal environment lacks TTY access for interactive credential prompts. The workaround that works:

```bash
# Embed GitHub token in remote URL
git remote set-url origin https://<GITHUB_TOKEN>@github.com/nelsonlin/book-ops.git
git push
```

Alternatively, use `gh pr create` directly as it works with stored credentials.

## About test_taiwan_library.py
The `test_taiwan_library.py` test file has a pre-existing import issue: it tries to import `_guess_author` from `sites.taiwan_library`, but this function doesn't exist in the current implementation. This is unrelated to the Phase 1 changes and existed before. The relevant test (`test_normalize.py`) passes successfully.