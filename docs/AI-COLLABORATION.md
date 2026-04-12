# AI Collaboration & Workflow

This document defines how **Nelson**, **Gemini**, and **Kilo** work together to build Book-Ops.

## The Three-Way Partnership

### 1. Nelson (Product Owner & QA Architect)
*   **Role:** Provides "Product Logic" (e.g., format rules) and "Visual Auditing".
*   **Key Contribution:** Inspecting debug screenshots to verify that what a human sees matches what the AI extracts.
*   **Next Sprint:** Providing "Golden URL" test cases for new platforms.

### 2. Gemini CLI (Controller)
*   **Role:** Orchestrator, Researcher, and Environment Manager.
*   **Key Contribution:** Performing "Evidence-First" planning by analyzing raw HTML dumps before tasking Kilo with code changes.
*   **Next Sprint:** Implementing pipeline-level deduplication and cross-site coordination.

### 3. Kilo Code (Developer)
*   **Role:** High-speed Implementation Specialist.
*   **Key Contribution:** Writing complex regex, parallel loops (`asyncio`), and comprehensive unit tests.
*   **Next Sprint:** Refining selectors for KSML and implementing data persistence.

---

## Technical Standards (Lessons from Sprint 1)

### 1. Selector Policy
- **Semantic > Structural:** Prefer `page.locator("span").filter(has_text="Author")` over rigid CSS paths like `div > div > p:nth-child(2)`.
- **Label-Based:** Always search for the human-readable label next to a data field.

### 2. The "Defensive Wait" Rule
- Never rely on `networkidle` for Single Page Applications (SPAs).
- Always use `wait_for_selector` for a specific content block (e.g., `#book-detail`).
- Add a strategic `asyncio.sleep(2)` if templates are slow to populate after the container is visible.

### 3. Global Normalization
- **Dates:** Always return `YYYY-MM-DD`. Default to `YYYY-01-01` if month/day are missing.
- **Titles:** Strip generic platform names or site headers during extraction.

### 4. The Handoff Schema
Every task given to Kilo Code must be stored in `.ai/handoff/` and include:
- **Goal:** Clear objective.
- **Context:** Relevant files and site behavior.
- **Evidence:** Snapshots of the HTML being targeted.
- **Done Criteria:** Specific verification steps.
