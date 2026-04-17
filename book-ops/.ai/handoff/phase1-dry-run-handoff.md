# Handoff: Phase 1 - Foundation (CLI & Pipeline Dry-Run)

## Goal
Implement a `--dry-run` mode for the `bookops.py` CLI to allow for fast pipeline validation without browser dependencies or network calls.

## Context
- **`bookops.py`**: CLI entry point.
- **`pipeline.py`**: Orchestrates book search across sites.
- **`models.py`**: Contains the `BookResult` dataclass.
- **`GEMINI.md`**: Mandates keeping scraping logic in `sites/*.py` and away from the core CLI.

## Requirements

### 1. `pipeline.py`
Add a function `run_pipeline_dry()` that:
- Returns a list of at least two mock `BookResult` objects.
- One result should include Chinese characters (e.g., `title="Python 編程"`) to verify encoding stability.
- No browser or scrapers should be initialized.

### 2. `bookops.py`
Update the CLI to:
- Add a `--dry-run` flag (`action="store_true"`).
- Update the `book_name` positional argument to be optional *only* when `--dry-run` is present (`nargs="?"`).
- If `--dry-run` is active:
    - Call `run_pipeline_dry()`.
    - Print a `[dry-run] Pipeline OK — mock results:` header.
    - Pass the results to the existing formatters (`table`, `json`, or `tsv`).
- Ensure compatibility with existing Windows UTF-8 stdout/stderr patches.

## Done Criteria
- `python bookops.py --dry-run` runs successfully without Chromium installed.
- `python bookops.py --dry-run --format json` returns valid JSON with mock data.
- `python bookops.py --dry-run --format table` displays a table with mock data.
- Existing unit tests (`pytest tests/test_normalize.py tests/test_taiwan_library.py`) still pass.

## Completion Signal
1. Create `.ai/handoff/phase1-dry-run-completion.md` summarizing changes.
2. Open a GitHub PR with `gh pr create --title "feat: Phase 1 - CLI Dry-Run"`.
3. Notify Nelson and Gemini CLI to review.
