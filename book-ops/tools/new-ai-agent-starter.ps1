param(
    [string]$ProjectRoot = "."
)

$ErrorActionPreference = 'Stop'

$root = (Resolve-Path $ProjectRoot).Path

$dirs = @(
    ".kilo",
    ".kilo/rules",
    ".ai",
    ".ai/prompts",
    ".ai/plans",
    ".ai/handoff",
    "docs",
    "docs/adr",
    "src",
    "tests",
    "scripts"
)

foreach ($dir in $dirs) {
    $path = Join-Path $root $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

$geminiMd = @'
# Project instructions for Gemini CLI

## Project summary
This repository contains <project summary>.

## Important paths
- `src/`: production source code
- `tests/`: automated tests
- `scripts/`: developer automation
- `docs/adr/`: approved architecture decisions
- `.ai/prompts/`: reusable prompts for Gemini CLI and Kilo Code
- `.ai/plans/`: temporary implementation plans
- `.ai/handoff/`: task handoff notes between tools

## Commands
- Install: `<install command>`
- Format: `<format command>`
- Lint: `<lint command>`
- Unit test: `<unit test command>`
- Integration test: `<integration test command>`
- Build: `<build command>`

## Rules
- Read this file before changing anything.
- Prefer minimal patches.
- Do not edit generated files unless explicitly instructed.
- Draft major technical decisions in `.ai/plans/` or `.ai/handoff/` first, then promote approved content to `docs/adr/`.
- After code changes, report changed files, commands run, and residual risks.

## Tool routing
- Planning and impact analysis: Kilo Code Architect mode.
- Focused implementation in approved scope: Kilo Code Code mode.
- Build, test, lint, Git inspection, release checks: Gemini CLI.
- Failure triage after command output: Kilo Code Debug mode.
'@

$kiloJsonc = @'
{
  // Project-level Kilo Code rules.
  "instructions": [
    ".kilo/rules/00-project-rules.md",
    ".kilo/rules/10-coding-standards.md",
    ".kilo/rules/20-testing-rules.md"
  ]
}
'@

$projectRules = @'
# Kilo Code project rules

## Working style
- For tasks affecting more than 3 files, start in Architect mode.
- For debugging, capture failing command output before proposing code changes.
- Keep changes scoped to the approved task.

## Edit boundaries
- Allowed by default: `src/`, `tests/`, `docs/`.
- Ask before editing: dependency manifests, CI config, migrations, generated code.
- Never edit secrets, environment files, or release artifacts.

## Quality gates
- Update tests for behavior changes.
- Update docs when interfaces or workflows change.
- Summarize touched files and required validation before ending the task.
'@

$codingRules = @'
# Coding standards

- Prefer the smallest correct change set.
- Keep public interfaces stable unless the task explicitly approves interface changes.
- Avoid broad refactors during bug fixes.
- Preserve existing naming and module structure unless there is a clear reason to change it.
- Add comments only where intent is not obvious from the code.
'@

$testingRules = @'
# Testing rules

- Run the smallest meaningful test scope first.
- Add or update tests when behavior changes.
- If tests are skipped, explain why.
- Report exact commands needed for local verification.
'@

$kiloArchitect = @'
Task: <short feature or change>

Context:
- Repo area: <path>
- Business or technical goal: <goal>
- Constraints: <latency/safety/security/compliance/team rules>
- Related files: <file list>
- Existing issue or bug: <optional>

Mode instructions:
- Do not edit code yet.
- Produce a step-by-step implementation plan.
- Identify impacted modules, interfaces, tests, and docs.
- Call out risks, assumptions, and rollback plan.
- If requirements are unclear, list exact clarification questions.

Output format:
1. Scope
2. Impacted files
3. Implementation steps
4. Test plan
5. Risks
6. Recommended handoff to Kilo Code Code mode or Gemini CLI
'@

$kiloCode = @'
Task: <implementation task>

Context:
- Approved plan: <path to .ai/plans/... or summary>
- Allowed edit scope: <paths>
- Must not edit: <paths>
- Coding constraints: <style/perf/security/error handling>
- Done criteria: <tests, behavior, docs>

Mode instructions:
- Make the smallest correct change set.
- Keep public interfaces stable unless explicitly approved.
- Update tests and docs that are directly affected.
- Stop and report if new files or interface changes are needed outside scope.

Output format:
1. Files changed
2. What changed
3. Tests to run
4. Follow-up risks
'@

$kiloDebug = @'
Task: Diagnose and fix failure

Failure evidence:
- Command: <command>
- Error output: <paste stack trace or summary>
- Frequency: <always/intermittent>
- Environment: <OS, runtime, toolchain>

Mode instructions:
- Identify likely root causes first.
- Rank them by probability.
- Propose the minimum fix.
- Specify how to reproduce and how to verify the fix.
- Avoid broad refactors unless the evidence requires them.

Output format:
1. Probable root cause
2. Evidence
3. Proposed fix
4. Verification steps
5. Residual risk
'@

$geminiRepoScan = @'
You are working in the current repository root.

Goal:
- Summarize the repo structure and identify the files most relevant to: <task>

Instructions:
- Read GEMINI.md first.
- Inspect only the directories relevant to the task.
- Report architecture, entry points, build/test commands, and likely edit locations.
- Do not modify files.

Output:
- Repo summary
- Relevant files
- Suggested next commands
- Risks or unknowns
'@

$geminiTestRunner = @'
Goal: Validate the current branch after the latest code changes.

Instructions:
- Read GEMINI.md first.
- Run the smallest meaningful verification sequence: format check, lint, unit tests, then integration tests if configured.
- Summarize failing commands with the first actionable error.
- Do not edit files unless explicitly asked.

Output:
1. Commands run
2. Pass/fail summary
3. First actionable failure
4. Suggested next step for Kilo Code Debug mode or Kilo Code Code mode
'@

$geminiRefactorReview = @'
Goal: Review the current diff for correctness and hidden risk.

Instructions:
- Read GEMINI.md first.
- Inspect git diff only.
- Look for API breakage, missed tests, duplicated logic, unsafe file operations, and documentation drift.
- Do not rewrite code unless explicitly asked.

Output:
1. High-risk findings
2. Medium-risk findings
3. Missing tests or docs
4. Ship/no-ship recommendation with reason
'@

$files = @{
    'GEMINI.md' = $geminiMd
    'kilo.jsonc' = $kiloJsonc
    '.kilo/rules/00-project-rules.md' = $projectRules
    '.kilo/rules/10-coding-standards.md' = $codingRules
    '.kilo/rules/20-testing-rules.md' = $testingRules
    '.ai/prompts/kilo-architect.md' = $kiloArchitect
    '.ai/prompts/kilo-code.md' = $kiloCode
    '.ai/prompts/kilo-debug.md' = $kiloDebug
    '.ai/prompts/gemini-repo-scan.md' = $geminiRepoScan
    '.ai/prompts/gemini-test-runner.md' = $geminiTestRunner
    '.ai/prompts/gemini-refactor-review.md' = $geminiRefactorReview
}

foreach ($relative in $files.Keys) {
    $path = Join-Path $root $relative
    $parent = Split-Path $path -Parent
    if (-not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Set-Content -Path $path -Value $files[$relative] -Encoding utf8
}

Write-Host "AI starter files created under: $root"
Write-Host "Next steps:"
Write-Host "1. Fill in commands in GEMINI.md"
Write-Host "2. Adjust kilo.jsonc instruction list if you add more rule files"
Write-Host "3. Open VS Code in this repo and start with Kilo Architect mode for the first real task"
