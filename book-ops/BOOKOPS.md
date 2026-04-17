# BOOKOPS.md

## Goal
Book-Ops is a Python CLI for searching multiple book websites and normalizing results.

## Priorities
1. Make `sites/taiwan_library.py` work with Playwright
2. Keep the project easy to run on Windows PowerShell
3. Support table / JSON / TSV output
4. Add deduplication after the first real adapter works

## Rules
- Keep site-specific selectors and parsing inside `sites/*.py`
- Return `BookResult` objects from every site handler
- Do not put scraping logic in `bookops.py`
- Prefer small, testable functions
- Save debug artifacts under `output/`

## Development workflow
- VS Code is the editor
- Gemini CLI runs in the integrated terminal
