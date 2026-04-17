# Sprint 2 Phase 1 Concept - AI cowork automation and setup test Github Actions CI/CD 
- Gemini CLI and Kilo Code use git push/PR to trigger each other 
- refer to @book-ops\.scrum\5_sprint retro\SPRT1-summary.md

#the tailored CI/CD guide.

The branch [`feat/bootstrap-windows-playwright`](https://github.com/nelsonlin/book-ops/tree/feat/bootstrap-windows-playwright) has a real Python project structure with **Playwright + pytest**, a `sites/` pipeline with `taiwan_library`, `ksml`, and `zlibrary` scrapers, and existing unit tests in `tests/`.  Here's a precise GitHub Actions setup tailored to what's actually in the repo.

***

## What the Repo Uses (Key Facts)

| File/Dir | Purpose |
|---|---|
| `requirements.txt` | `playwright==1.52.0`, `rich==14.0.0`, `pytest==8.3.5` |
| `pipeline.py` | Runs book search across registered sites |
| `sites/` | Individual scrapers (taiwan_library, ksml, zlibrary) |
| `tests/` | `test_normalize.py`, `test_taiwan_library.py` (unit tests, no browser) |
| `.kilo/` | Kilo Code AI context folder |



***

## Workflow 1 — CI: Unit Tests on Every PR

The unit tests (`test_normalize.py`, `test_taiwan_library.py`) test pure Python helpers — **no browser needed**.  This is fast and safe for CI.

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, "feat/**"]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run unit tests (no browser)
        run: pytest tests/test_normalize.py tests/test_taiwan_library.py -v
```

**Why no `playwright install` here?** These tests import helper functions (`_clean_text`, `_guess_author`, etc.) and never launch a browser, so they run fast without browser binaries. 

***

## Workflow 2 — Playwright E2E Tests (with Chromium)

For full end-to-end tests that actually scrape sites, Playwright browsers must be installed. Use `ubuntu-latest` (Linux headless is cheapest/fastest).

Create `.github/workflows/e2e.yml`:

```yaml
name: E2E (Playwright)

on:
  workflow_dispatch:       # manual trigger only
  schedule:
    - cron: "0 2 * * *"  # nightly 2 AM UTC

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Install Playwright browsers
        run: playwright install chromium --with-deps

      - name: Run E2E tests
        run: pytest tests/ -v --timeout=60

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-results
          path: test-results/
```

The `--with-deps` flag installs OS-level dependencies (fonts, libs) needed by Chromium on Ubuntu. 

***

## Workflow 3 — Windows Runner (Matching Your Branch Name)

The branch is named `bootstrap-windows-playwright` — so you likely want Windows compatibility.  GitHub Actions has `windows-latest` runners:

```yaml
name: CI (Windows)

on:
  push:
    branches: ["feat/bootstrap-windows-playwright"]

jobs:
  test-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Install Playwright Chromium
        run: playwright install chromium --with-deps

      - name: Run unit tests
        run: pytest tests/test_normalize.py tests/test_taiwan_library.py -v
```

> ⚠️ `windows-latest` runners are **~2× slower and more expensive** in GitHub Actions minutes. Use them only when testing Windows-specific behavior — for most CI, `ubuntu-latest` is preferred.

***

## How to Create These via Kilo Code in VS Code

1. Open Kilo Code panel in VS Code
2. Paste this prompt:

> *"Create `.github/workflows/ci.yml` for this Python Playwright project. It should run `pytest tests/test_normalize.py tests/test_taiwan_library.py` on push to any `feat/**` branch and PRs to main. No browser install needed for these unit tests. Also create `.github/workflows/e2e.yml` that installs Playwright Chromium and runs all tests nightly via cron."*

Kilo Code will read your `.kilo/` context and generate both files directly in your workspace. 

***

## Use Case Summary

| Workflow | Trigger | Runner | Browser? |
|---|---|---|---|
| `ci.yml` — Unit tests | push / PR | ubuntu | ❌ No |
| `e2e.yml` — Full scrape | nightly + manual | ubuntu | ✅ Chromium |
| `ci-windows.yml` — Win compat | push to this branch | windows | ✅ Chromium |

Now I have the full picture. The key insight: **`bookops.py` is the actual CLI entry point** — it requires a `book_name` positional argument and has no `--dry-run` flag.  The `main.py` from my earlier suggestion doesn't exist. Here's the full design consideration and a concrete example.

***

## The Problem with `python main.py --dry-run`

Looking at the actual code, `bookops.py` is the CLI entry point — not `main.py`.  It requires a mandatory `book_name` positional argument, so calling it with no arguments **crashes** in CI. The `--dry-run` flag doesn't exist yet. This is what needs to be designed.

***

## Design Considerations for `--dry-run`

### 1. What should dry-run validate?
Dry-run in CI should verify the pipeline **wires up correctly** without making live network calls (no Playwright browser launch, no real scraping). Based on the architecture in `GEMINI.md`, the key things to validate are:

- `SITE_REGISTRY` loads all 3 sites without import errors
- `BookResult` dataclass instantiates correctly
- Formatters (`print_table`, `print_json`, `print_tsv`) work with mock data
- CLI argument parsing succeeds



### 2. Architectural boundary to respect
`GEMINI.md` explicitly states: **do not move scraping logic into `bookops.py`** — keep it in `sites/*.py`.  So `--dry-run` should live in `bookops.py` but call a dry-run mode injected into `pipeline.py`, not bypass `sites/` entirely.

### 3. Windows UTF-8 concern
`bookops.py` already patches `sys.stdout` for Windows encoding.  Dry-run output must go through the same path so CI on `windows-latest` doesn't fail on Chinese characters from mock data.

***

## Example: Adding `--dry-run` to `bookops.py`

**Step 1 — Add mock data to `pipeline.py`:**

```python
# pipeline.py  (add this function)
from models import BookResult

def run_pipeline_dry() -> list[BookResult]:
    """Returns mock BookResult objects — no browser, no network."""
    return [
        BookResult(
            title="Python 編程",
            author="張三",
            format="EPUB",
            date="2023",
            url="https://example.com/book/1",
            source="taiwan_library",
            frontcover="",
        ),
        BookResult(
            title="Clean Code",
            author="Robert C. Martin",
            format="PDF",
            date="2008",
            url="https://example.com/book/2",
            source="zlibrary",
            frontcover="",
        ),
    ]
```

**Step 2 — Add `--dry-run` flag to `bookops.py`:**

```python
# bookops.py  (updated)
import argparse, sys, io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from pipeline import run_pipeline, run_pipeline_dry
from formatters import print_table, print_json, print_tsv

def main():
    parser = argparse.ArgumentParser(description="Book-Ops CLI")
    parser.add_argument("book_name", nargs="?", default=None,
                        help="Name of the book to search")
    parser.add_argument("--format", choices=["table", "json", "tsv"],
                        default="table")
    parser.add_argument("--sites", nargs="*", default=[])
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate pipeline with mock data, no network calls")
    args = parser.parse_args()

    # dry-run: no book_name required
    if args.dry_run:
        results = run_pipeline_dry()
        print("[dry-run] Pipeline OK — mock results:")
    else:
        if not args.book_name:
            parser.error("book_name is required unless --dry-run is set")
        results = run_pipeline(args.book_name, selected_sites=args.sites)

    if args.format == "json":
        print_json(results)
    elif args.format == "tsv":
        print_tsv(results)
    else:
        print_table(results)

if __name__ == "__main__":
    main()
```

**Step 3 — Update the GitHub Actions workflow:**

```yaml
# .github/workflows/validate-pipeline.yml
name: Validate Pipeline

on:
  push:
    branches: [main, "feat/**"]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      # No `playwright install` needed — dry-run never launches a browser
      - name: Validate pipeline (dry-run)
        run: python bookops.py --dry-run --format json
```

***

## Key Design Decisions Summary

| Decision | Rationale |
|---|---|
| `nargs="?"` on `book_name` | Makes it optional only when `--dry-run` is passed  |
| Mock data lives in `pipeline.py` | Respects the boundary: scrapers stay in `sites/`, pipeline owns orchestration  |
| No `playwright install` in validate workflow | Dry-run never calls `sites/*.py` scrapers, so no browser binary needed  |
| `--format json` in CI | Machine-readable output; easier to assert in future test steps |
| Kilo Code prompt to generate this | Use **Code mode** for the implementation, per tool routing in `GEMINI.md`  |

### Kilo Code Prompt to Generate This

> *"Add a `--dry-run` flag to `bookops.py`. When passed, it should call `run_pipeline_dry()` from `pipeline.py` which returns 2 mock `BookResult` objects. `book_name` becomes optional. Do not modify any files in `sites/`. Follow the rules in GEMINI.md."*