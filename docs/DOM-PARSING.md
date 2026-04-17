# DOM-PARSING.md

## Rules
- Prefer Playwright locators over XPath
- Prefer accessible/user-facing selectors first
- Wait on result containers or meaningful content
- Dump HTML and screenshot before and after search
- Parse row containers first, links second
- Skip navigation/footer noise with explicit filters
- Store debug files under `output/<site>/`

## Workflow
1. Run scraper visibly
2. Inspect `02_after_search.html`
3. Identify repeating result row
4. Extract title, author, format, date, url from row children
5. Add or refine helper tests