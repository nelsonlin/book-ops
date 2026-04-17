# Implementation Plan: GitHub Actions CI/CD & CLI Dry-Run

This plan implements the concepts from `SPPP2-1.1-GitHub Actions CI_CD.md`. It introduces a dry-run mode for the CLI to enable fast pipeline validation in CI and sets up the necessary GitHub Actions workflows.

## Objectives
- Add `--dry-run` to `bookops.py` for pipeline validation without browsers.
- Implement `run_pipeline_dry()` in `pipeline.py`.
- Create GitHub Action workflows for CI (Unit Tests), E2E (Playwright), and Pipeline Validation (Dry-Run).

## Proposed Changes

### 1. `pipeline.py`
- **Action:** Add `run_pipeline_dry()` function.
- **Details:** This function will return a list of mock `BookResult` objects. This allows testing the CLI and formatting logic without triggering any scrapers or browser launches.

### 2. `bookops.py`
- **Action:** Update argument parsing and execution flow.
- **Details:**
    - Add `--dry-run` flag.
    - Make `book_name` optional if `--dry-run` is present.
    - Call `run_pipeline_dry()` when in dry-run mode.
    - Ensure output encoding patches are maintained.

### 3. GitHub Actions Workflows (`.github/workflows/`)
- **`ci.yml`**: Runs unit tests (`tests/test_normalize.py`, `tests/test_taiwan_library.py`) on every push/PR to `main` and `feat/**`.
- **`e2e.yml`**: Runs all tests including Playwright E2E nightly and on manual trigger.
- **`validate-pipeline.yml`**: Runs `python bookops.py --dry-run` on every push to verify CLI/Pipeline integration.

## Verification Plan
1. **Local Validation:**
   - Run `python bookops.py --dry-run` and verify mock results are printed in all formats (table, json, tsv).
   - Run existing unit tests: `pytest tests/test_normalize.py tests/test_taiwan_library.py`.
2. **CI Validation:**
   - Push changes to a feature branch.
   - Verify `CI` and `Validate Pipeline` workflows pass in GitHub Actions.
   - Manually trigger `E2E (Playwright)` workflow.

## Risks & Mitigations
- **Windows Encoding:** Mock data with Chinese characters might fail on Windows CI if not handled. **Mitigation:** `bookops.py` already has UTF-8 patches for `stdout/stderr`.
- **Playwright Dependencies:** Linux runners need `--with-deps`. **Mitigation:** Included in `e2e.yml`.

## Tooling Recommendation
- Use **Kilo Code (Code mode)** for the `pipeline.py` and `bookops.py` changes as they involve logic implementation.
- Use **Gemini CLI** for creating the `.github/workflows/` files and verifying the setup.
