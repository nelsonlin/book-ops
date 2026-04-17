▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
 > explain design decision using Multi-Tier CI/CD, what purpose of each of the three tiers
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
✦ The Multi-Tier CI/CD design was chosen to balance developer speed, operational cost, and system reliability. In a  
  Playwright project, running full browser tests on every push is too slow and expensive.

  Here is the purpose of each tier:

  Tier 1: Fast CI (Unit Tests)
   * File: .github/workflows/ci.yml
   * Target: tests/test_normalize.py, tests/test_taiwan_library.py (helpers only).
   * Purpose: To verify pure Python logic (regex, text cleaning, data models) without launching a browser.
   * Why: It runs in <15 seconds. It catches "dumb" coding mistakes (syntax errors, logic bugs) immediately,
     providing a near-instant feedback loop for the developer.

  Tier 2: Pipeline Validation (Dry-Run)
   * File: .github/workflows/validate-pipeline.yml
   * Target: python bookops.py --dry-run
   * Purpose: To verify the CLI "Wiring" and Orchestration. It ensures that the CLI entry point, the pipeline, and
     the output formatters (Table/JSON/TSV) all work together.
   * Why: It catches integration errors (e.g., a change in pipeline.py that crashes bookops.py) without needing to
     install Playwright Chromium. It ensures the "core" of the application is never broken.

  Tier 3: Nightly E2E (Playwright Integration)
   * File: .github/workflows/e2e.yml
   * Target: pytest tests/ (Full integration tests with real site scraping).
   * Purpose: To verify Site Compatibility. It checks if external websites (like Taiwan Library or Z-Library) have
     changed their HTML structure, which would break our scrapers.
   * Why: These tests are slow (2+ minutes) and expensive (requiring large browser binaries and OS dependencies). By
     running them nightly rather than on every push, we save GitHub Actions minutes while still catching
     site-breakages within 24 hours.

  Summary of Design Philosophy:
  ┌────────────┬───────────────────────────────────────┬────────────┬──────┬────────────┐
  │ Tier       │ Focus                                 │ Speed      │ Cost │ Trigger    │
  ├────────────┼───────────────────────────────────────┼────────────┼──────┼────────────┤
  │ 1. Unit    │ "Is my code logically sound?"         │ Ultra Fast │ Low  │ Every Push │
  │ 2. Dry-Run │ "Is my CLI wired correctly?"          │ Fast       │ Low  │ Every Push │
  │ 3. E2E     │ "Do the library websites still work?" │ Slow       │ High │ Nightly    │
  └────────────┴───────────────────────────────────────┴────────────┴──────┴────────────┘

  This structure creates a "Safety Net" that gets progressively deeper: we catch 90% of bugs in seconds (Tier 1 & 2)
  and the remaining 10% of external site changes overnight (Tier 3).
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
 > what tiers not be verified in this sprint and plan to do
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
✦ In this sprint, we successfully verified Tier 1 (Unit Tests) and Tier 2 (Pipeline Dry-Run). Both are currently     
  passing in GitHub Actions.

  The tier that has NOT been fully verified is Tier 3: Nightly E2E (Playwright Integration).

  Why Tier 3 is not yet verified:
   1. Environment Setup: While the e2e.yml file is created and merged, I have not yet confirmed that the
      ubuntu-latest runner can successfully install all required Linux OS dependencies (--with-deps) and font
      packages needed for Chinese character rendering.
   2. Scraper Fragility: As noted in the Sprint 2 Phase 1 Retrospective, the Taiwan Library scraper has known issues
      with SPA loading (NTL/Cloud sites). It is highly likely that a full E2E run would fail right now due to these
      pre-existing bugs.
   3. Scheduled Trigger: The workflow is currently set to run nightly at 2 AM UTC, so we haven't seen the first
      "Natural" result yet.

  ---

  The Plan for Verification (Sprint 2 Phase 2)

  I propose the following plan to verify the remaining tiers and environmental stability:

  1. Manual E2E Triage (Immediate)
  I will use the GitHub CLI to manually trigger the E2E workflow:

   1 gh workflow run e2e.yml
  I will then use gh run watch to monitor it and gh run view --log to triage any failures related to Playwright
  installation or site-scraping timeouts.

  2. Environment Verification (Linux vs. Windows)
  We have not yet verified a Windows CI Runner. While Tier 1/2 work on Linux, our users primarily use Windows.       
   * Plan: I will implement an optional ci-windows.yml to verify that the CLI's UTF-8 patches and Chinese character  
     output are stable on windows-latest runners.

  3. Scraper "Surgical" Fixes
  Once Tier 3 (E2E) identifies the specific failing sites (e.g., HyRead, UDN, or NTL):
   * Plan: I will task Kilo Code to replace the asyncio.sleep calls with explicit wait_for_selector logic, as defined
     in our "Wait Strategy" action item.

  ---

  Next Step Recommendation:
  Should I manually trigger the E2E (Playwright) workflow now to see our current "Baseline" failure rate, or would
  you like to start on the Windows Runner setup first?

## Playwright E2E Test Runner Design: Windows vs Linux

### Recommended Approach: **Use Linux as Default**

| Aspect | Linux (`ubuntu-latest`) | Windows (`windows-latest`) |
|--------|------------------------|----------------------------|
| **Speed** | Fastest, efficient sharding | Slower, higher resource usage |
| **Cost** | Cheaper GitHub minutes | More expensive |
| **Visual Tests** | Custom WebKit, Linux fonts | Native-like Chromium, DirectX |
| **Use Case** | Default CI/CD | Windows-specific app validation |

### Key Design Best Practices:

1. **Default to Linux** (`ubuntu-latest`) for most E2E test workflows due to faster execution and native browser support[^1]

2. **Use Windows selectively** - Only add Windows matrix jobs (`windows-latest`) for:
   - Windows-specific app validation
   - Cross-platform consistency testing
   - Separate screenshot baselines required[^5]

3. **Implement parallelization** with matrix strategies:
   ```yaml
   strategy:
     matrix:
       shard: [1, 2, 3, 4]
   ```

4. **Cache Playwright browsers** via `actions/cache` keyed by OS and `package-lock.json` hash[^1]

5. **Consider visual differences**: Linux/Windows browsers produce pixel deviations due to font rendering and GPU acceleration (DirectX vs none) - use separate baselines for visual tests[^5]

### Concise Recommendation:
> Run Linux for most workflows, add Windows matrix jobs selectively to catch platform gaps without inflating costs[^1][^5]

[^1]: https://www.shiplight.ai/blog/github-actions-e2e-testing
[^5]: https://github.com/microsoft/playwright/issues/10120