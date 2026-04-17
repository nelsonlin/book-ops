import pytest
from sites.taiwan_library import search

@pytest.mark.e2e
def test_taiwan_library_search_real():
    """Real E2E search to verify site availability and font rendering."""
    results = search("Python")
    assert len(results) > 0
    # Verify we got a real title
    assert results[0].title != "Unknown"
    assert results[0].source != ""
    print(f"\n[E2E] Found {len(results)} results from Taiwan Library")
    for r in results[:3]:
        print(f"  - {r.title} ({r.source})")
