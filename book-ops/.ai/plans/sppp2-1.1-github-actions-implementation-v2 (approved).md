# Implementation Plan: GitHub Actions CI/CD & CLI Dry-Run (v2)

This plan implements the concepts from `SPPP2-1.1-GitHub Actions CI_CD.md` while adhering to the roles defined in `docs/AI-COLLABORATION.md`.

## Objectives
- Add `--dry-run` to `bookops.py` for pipeline validation without browsers.
- Implement `run_pipeline_dry()` in `pipeline.py`.
- Create GitHub Action workflows for CI (Unit Tests), E2E (Playwright), and Pipeline Validation (Dry-Run).
- Use GitHub CLI (`gh`) and `.venv` for local and remote verification.

## Phase 1: Foundation (CLI & Pipeline Dry-Run)
*   **Gemini CLI Role (Orchestrator):** Create a detailed handoff in `.ai/handoff/phase1-dry-run-handoff.md`. Define "Done Criteria" including mock data requirements.
*   **Kilo Code Role (Implementation):** Update `pipeline.py` and `bookops.py` to include the `--dry-run` logic and mock data.
*   **Local Verification (Gemini CLI):** 
    1. Activate `.venv`: `.venv\Scripts\activate` (Windows).
    2. Run `python bookops.py --dry-run` and verify mock results.
    3. Run `pytest tests/test_normalize.py tests/test_taiwan_library.py`.

## Phase 2: Essential CI (Unit Tests & Pipeline Validation)
*   **Gemini CLI Role (Implementation):** Create `.github/workflows/ci.yml` and `validate-pipeline.yml`.
*   **Remote Verification (Gemini CLI):** Use `gh run list --workflow ci.yml` and `gh run list --workflow validate-pipeline.yml` to monitor execution after Kilo pushes the PR.

## Phase 3: Advanced CI (E2E & Environmental Testing)
*   **Gemini CLI Role (Implementation):** Create `.github/workflows/e2e.yml`.
*   **Remote Verification (Gemini CLI):** 
    1. Manually trigger via `gh workflow run e2e.yml`.
    2. Monitor status via `gh run watch`.
    3. If failed, use `gh run view --log` to triage.

---

## AI-to-AI Synchronization Protocol
To ensure Gemini CLI knows when Kilo Code has completed a task:

1.  **Handoff:** Gemini CLI writes a task to `.ai/handoff/`.
2.  **Execution:** Kilo Code implements the change.
3.  **Completion Signal:** Kilo Code MUST create a `*-completion.md` file in `.ai/handoff/` AND open a GitHub PR using `gh pr create`.
4.  **Verification Trigger:** Nelson or Kilo Code (via PR comment) prompts Gemini CLI: *"Review Kilo's PR and CI status for [Phase X]."*
5.  **Review & Audit:** Gemini CLI uses `gh pr view`, `gh pr diff`, and `gh run list` to confirm completion and CI success before signaling "Done" to Nelson.

---

**Next Step:** Please approve this updated plan (v2). Once approved, I will initiate **Phase 1** by creating the handoff for Kilo Code.
