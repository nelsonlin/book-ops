# Handoff: Phase 2.1 - Formal Pipeline Testing

## Goal
Add a dedicated unit test for the pipeline orchestration logic to ensure the dry-run mode remains stable.

## Requirements
- Create a new test file: `tests/test_pipeline.py`.
- Implement a test case `test_run_pipeline_dry()`:
    - Call `run_pipeline_dry()` from `pipeline.py`.
    - Assert that the result is a list.
    - Assert that the length of the list is 3 (following the previous sync test).
    - Assert that the first result's title contains "Python".
- Ensure the test can be run via `python -m pytest tests/test_pipeline.py`.

## Done Criteria
- `tests/test_pipeline.py` is created and passes locally.
- GitHub Actions "CI" workflow passes after you push.

## Completion Signal
1. Push changes to your branch for PR #3.
2. **Self-Verify:** Run `.\tools\monitor-kilo.ps1 -TaskName "phase2-unit-tests" -PrNumber 3` to ensure CI is Green.
3. **Signal Done:** ONLY after the monitor succeeds, create `.ai/handoff/phase2-unit-tests-completion.md`.
