# Project instructions for Gemini CLI

## Project summary
Book-Ops is a Python CLI for searching multiple book/library websites and normalizing book metadata. It uses Playwright for site automation and returns normalized `BookResult` objects.

## Important paths
- `sites/`: site-specific scraper and adapter logic (scrapers stay here)
- `tests/`: unit and integration tests
- `tools/`: developer automation and setup scripts
- `docs/adr/`: approved architecture decisions
- `.ai/prompts/`: reusable prompts for Gemini CLI and Kilo Code
- `.ai/plans/`: temporary implementation plans
- `.ai/handoff/`: task handoff notes between tools
- `bookops.py`: CLI entry point
- `models.py`: core data schemas (`BookResult`)

## Commands
- Install: `pip install -r requirements.txt; playwright install chromium`
- Run: `python bookops.py "<book_name>"`
- Unit test: `pytest tests/test_normalize.py`
- Integration test: `pytest` (runs all tests)
- Format: `python -m black .` (requires black)
- Lint: `python -m ruff check .` (requires ruff)

## Rules
- **Core Principle:** Favor debuggable code over clever code.
- **Architectural Boundary:** Do not move scraping logic into `bookops.py`; keep it inside `sites/*.py`.
- **Development Workflow:**
  - Read this file before changing anything.
  - Save debug artifacts (screenshots/HTML) to `output/<site>/`.
  - When changing selectors, inspect dumped HTML first.
  - Prefer Playwright locators and visible waits over arbitrary sleep.
- **Tooling:**
  - Draft major technical decisions in `.ai/plans/` or `.ai/handoff/` first, then promote approved content to `docs/adr/`.
  - After code changes, report changed files, commands run, and residual risks.

## Tool routing
- Planning and impact analysis: Kilo Code Architect mode.
- Focused implementation in approved scope: Kilo Code Code mode.
- Build, test, lint, Git inspection, release checks: Gemini CLI.
- Failure triage after command output: Kilo Code Debug mode.
