# Handoff: UDN Async Loading Issue

## Current Status
- **Issue**: UDN (platform 2) scraping is failing in live E2E runs because the site renders dynamically. The `domcontentloaded` event triggers while the page is still in a "Loading" state (showing a spinner).
- **Evidence**: `output/taiwan_library/udn_detail_2.html` confirms the presence of the loading overlay during extraction.
- **Diagnostics**: Debug logs show `h3` count of 12 (all garbled/missing expected content) vs local `udn.html` files. 

## Technical Findings
- The extraction logic (selectors) is correct and works against static files (`udn.html`).
- The failure occurs at the integration level due to timing/race conditions in the SPA navigation.

## Recommended Fix for Kilo Code
- Implement a more robust waiting strategy for UDN that explicitly monitors the removal of the loading overlay or the presence of the detail content container.
- Consider utilizing `page.wait_for_load_state('networkidle')` or custom polling for expected metadata elements before extraction.
