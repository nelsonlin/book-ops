# WORKFLOWS.md

## Gemini CLI workflow
- Open repo root
- Ask Gemini to use `GEMINI.md` and relevant docs
- Provide `output/taiwan_library/*.html` as explicit context
- Request selector refinement or parsing improvements

## Kilo Code workflow
- Use `AGENTS.md`
- Work file-by-file
- Prefer edits to helper functions instead of whole-file rewrites

## Recommended prompts
- "Refine row selector using output/taiwan_library/02_after_search.html"
- "Add tests for parsing helpers in sites/taiwan_library.py"
- "Reduce false positives in _looks_like_bookish_row"