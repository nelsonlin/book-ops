from sites import taiwan_library, ksml, zlibrary
from models import BookResult

SITE_REGISTRY = {
    "taiwan_library": taiwan_library,
    "ksml": ksml,
    "zlibrary": zlibrary,
}


def run_pipeline_dry():
    """Run a dry-run of the pipeline with mock data, no browser or network calls."""
    return [
        BookResult(
            title="Python 編程: 從入門到實踐",
            author="張三",
            format="PDF",
            date="2024",
            url="https://example.com/book/1",
            source="dry-run",
        ),
        BookResult(
            title="Machine Learning Fundamentals",
            author="李四",
            format="EPUB",
            date="2023",
            url="https://example.com/book/2",
            source="dry-run",
        ),
    ]

def run_pipeline(book_name: str, selected_sites=None):
    results = []
    site_names = selected_sites or list(SITE_REGISTRY.keys())

    for site_name in site_names:
        site = SITE_REGISTRY.get(site_name)
        if not site:
            print(f"Unknown site: {site_name}")
            continue

        try:
            site_results = site.search(book_name)
            results.extend(site_results)
        except Exception as e:
            print(f"Error searching {site_name}: {e}")

    return results
