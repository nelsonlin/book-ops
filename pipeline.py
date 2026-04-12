from sites import taiwan_library, ksml, zlibrary

SITE_REGISTRY = {
    "taiwan_library": taiwan_library,
    "ksml": ksml,
    "zlibrary": zlibrary,
}

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
