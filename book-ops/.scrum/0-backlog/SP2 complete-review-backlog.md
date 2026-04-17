Based on the Sprint 1 Summary and my review of the current sites/taiwan_library.py code, here are the remaining "Taiwan
  Library" bugs and improvement items that are still on the waitlist:

  1. The "SPA Loading" Problem (Reliability)
   - The Issue: For Single Page Application (SPA) platforms like NTL (National Taiwan Library) and Taiwan Cloud Library,
     the scraper currently relies on networkidle and hardcoded asyncio.sleep(3). 
   - The Risk: This is slow and fragile. If the server is slow, the scraper fails; if the server is fast, it wastes time.
   - The Fix needed: Replace arbitrary sleeps with explicit page.wait_for_selector() for specific data blocks (e.g.,
     #bookdetailcpcontentblock).

  2. Result Deduplication (Accuracy)
   - The Issue: The scraper often returns the same book multiple times if it appears in different sections or library      
     branches.
   - The Fix needed: While I've added a basic _dedupe_results in the scraper, the Sprint 1 Reflection notes that a more    
     robust post-processing step is needed in pipeline.py to handle cross-site deduplication.

  3. Fragile CSS Selectors (Maintenance)
   - The Issue: Many selectors in _extract_detail_field still use rigid CSS paths (e.g., #center p:nth-child(4)).
   - The Risk: If the library website changes its layout even slightly (e.g., adds a new paragraph), the scraper will stop
     finding the Author or Date.
   - The Fix needed: Migrate these to Label-Based Selectors using Playwright's .filter(has_text="作者") logic, as agreed
     upon in the AI Collaboration standards.

  4. Broad Error Silencing (Debuggability)
   - The Issue: The _deep_crawl_for_metadata function currently uses a global except Exception: pass.
   - The Risk: If a site changes and the scraper fails, it will simply return "Unknown" for everything without telling us  
     why it failed.
   - The Fix needed: Implement structured logging for metadata extraction failures so we can triage specific site changes. 

  5. Platform-Specific "Hints" (Architecture)
   - The Issue: The code uses numeric "hints" (platform_hint == 3) which are hard to read and maintain.
   - The Fix needed: Refactor the platform detection to use a more descriptive mapping or an Enum to make the logic
     clearer.

  Next Step Recommendation:
  Once we merge the CI/CD pipeline (PR #3), we can use the new E2E Nightly Workflow to identify which of these platforms
  are currently failing and prioritize fixing their Wait Strategies and Selectors.
