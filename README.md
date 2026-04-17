# book-ops

A Windows-friendly Python + Playwright starter for a multi-site book search pipeline.

## Quick start

```powershell
.\tools\setup.ps1
.\tools\run.ps1 -BookName "Atomic Habits"
.\tools\run.ps1 -BookName "原子習慣" -Format json
```

## GitHub remote

```powershell
git init
git branch -M main
git remote add origin https://github.com/nelsonlin/book-ops.git
git add .
git commit -m "Initial book-ops starter"
git push -u origin main
```

## Gemini CLI workflow

- Use Gemini CLI in VS Code integrated terminal.
- Ask it to review diffs, write tests, and suggest commit messages.
- Keep git as the source of truth for branches and commits.

## Project structure

- `bookops.py` CLI entry
- `pipeline.py` orchestration
- `models.py` result schema
- `formatters.py` output renderers
- `sites/*.py` site adapters
- `tools/*.ps1` Windows development scripts
- `.vscode/*` workspace settings
- `BOOKOPS.md` AI/dev contract

## Suggested flow

```powershell
