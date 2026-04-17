# SPPP2-2: Site Stabilization & E2E Verification

This plan focuses on verifying the E2E (Playwright) tier, stabilizing the Taiwan Library scrapers, and ensuring cross-platform compatibility with full Chinese character support.

## Phase 2.1: E2E Baseline Audit (Gemini CLI)
- **Objective:** Establish the current "Baseline" failure rate and verify environment readiness.
- **Action:** 
    1. Manually trigger `e2e.yml` via `gh workflow run`.
    2. Audit the logs and Playwright artifacts (screenshots/HTML) for failures.
    3. **Chinese Support Check:** Inspect screenshots for "tofu" blocks; verify if `fonts-noto-cjk` is required on the Linux runner for proper rendering.
- **Deliverable:** Audit Handoff in `.ai/handoff/phase2-e2e-audit.md`.

## Phase 2.2: Surgical Site Fixes (Kilo Code)
- **Objective:** Fix the most critical scraper bugs and improve selector resilience.
- **Action:** 
    1. Replace `asyncio.sleep` with explicit `wait_for_selector` logic.
    2. Migrate rigid CSS selectors to **Chinese label-based filtering** (`filter(has_text="作者")`).
    3. Implement structured logging for metadata extraction failures.
- **Deliverable:** Green E2E status for 80%+ of platforms.

## Phase 2.3: Windows & UTF-8 Verification (Gemini CLI)
- **Objective:** Ensure CLI stability and visual correctness for Windows users.
- **Action:** 
    1. Create `.github/workflows/ci-windows.yml`.
    2. **Encoding Verification:** Confirm that Chinese characters in the "Rich" table do not cause crashes or rendering artifacts on `windows-latest`.
    3. Audit the CLI's `sys.stdout` UTF-8 patches in the Windows CI environment.
- **Deliverable:** Green status on Windows CI with verified Chinese output.

---

## Future Test Strategy: Linux vs. Windows Runners

| Runner | Tier | Goal | Chinese Support Strategy |
| :--- | :--- | :--- | :--- |
| **Linux** | Unit, Nightly E2E | Functional Stability | Install `fonts-noto-cjk` for Playwright rendering. |
| **Windows** | Pipeline Dry-Run | UX & Encoding | Use native system UTF-8; verify via `chcp 65001`. |
