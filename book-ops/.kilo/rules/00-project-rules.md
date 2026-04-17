# Kilo Code project rules

## Working style
- For tasks affecting more than 3 files, start in Architect mode.
- For debugging, capture failing command output before proposing code changes.
- Keep changes scoped to the approved task.

## Edit boundaries
- Allowed by default: `src/`, `tests/`, `docs/`, `sites/`.
- Ask before editing: dependency manifests, CI config, migrations, generated code.
- Never edit secrets, environment files, or release artifacts.

## Quality gates
- Update tests for behavior changes.
- Update docs when interfaces or workflows change.
- Summarize touched files and required validation before ending the task.
