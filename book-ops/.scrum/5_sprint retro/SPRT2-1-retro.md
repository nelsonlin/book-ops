# Sprint 2 Phase 1 Retrospective: GitHub Actions & CLI Dry-Run

## 1. Accomplishments
- **Multi-Tier CI/CD:** Implemented Fast Unit Tests (`ci.yml`), CLI Dry-Run (`validate-pipeline.yml`), and Nightly E2E (`e2e.yml`).
- **CLI Robustness:** Added `--dry-run` to `bookops.py`, enabling 10-15s validation without browser binaries.
- **Surgical Repairs:** Fixed a pre-existing `_normalize_date` bug in `taiwan_library.py` and aligned the unit test suite.
- **Automation Tools:** Created `monitor-kilo.ps1` for AI-to-AI synchronization, removing the "User as Messenger" bottleneck.

## 2. Issues Encountered
- **Technical Debt:** Unit tests for Taiwan Library were broken on start, requiring an unplanned "Phase 1.5 cleanup."
- **Environment Variance:** `pytest` required `python -m pytest` to correctly resolve local module paths in GitHub Actions.
- **Encoding:** Windows console still shows artifacts for Chinese characters when using `Rich` tables, though JSON output is clean.
- **Tooling:** `gh pr checks` had a minor JSON field mismatch ("status" vs "state") which was patched in the monitor script.

## 3. Collaboration Reflection
- **Role Alignment:** The Controller (Gemini) successfully acted as the gatekeeper for Developer (Kilo) code by setting up the CI gates.
- **Sync Protocol:** Using `.ai/handoff/` completion signals works well, but we must remain disciplined about the `gh pr create` and `monitor-kilo` steps.

## 4. Next Phase: Sprint 2.2 Goals
1.  **Orchestration:** Implement result deduplication in `pipeline.py`.
2.  **Reliability:** Refactor Taiwan Library SPA wait strategies (NTL/Cloud) to remove `asyncio.sleep`.
3.  **Maintenance:** Migrate remaining rigid CSS selectors to label-based filtering.
