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
