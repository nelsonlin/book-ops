# AGENTS.md

## Coding instructions
- Make minimal, reviewable changes
- Keep functions under ~40 lines when practical
- Preserve debug logging unless explicitly removed
- Prefer additive changes over broad rewrites
- Keep comments short and operational

## Scraper policy
- Use Playwright locator APIs first
- Try multiple selectors in ordered fallback lists
- Wait for meaningful DOM states
- Dump screenshot + HTML + metadata on important steps
- Parse repeated result rows before parsing loose links
- Normalize missing fields to safe defaults

## File ownership hints
- `sites/*.py`: website-specific interaction and extraction
- `pipeline.py`: orchestration only
- `formatters.py`: rendering only
- `models.py`: schema only
- `docs/*.md`: source of truth for architecture and workflow