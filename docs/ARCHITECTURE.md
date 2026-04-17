# ARCHITECTURE.md

## High-Level Flow
CLI -> pipeline -> site adapters -> normalized BookResult -> output formatter

## Advanced Patterns (Established in Sprint 1)

### 1. Hierarchical Scraping
To optimize search speed, site adapters (like `taiwan_library.py`) follow a three-tier loop:
- **Platform:** Group results by the provider (e.g., HyRead, UDN).
- **Book:** Identify unique titles within a platform.
- **Library:** Group multiple library availability links under one book record.

### 2. Parallel Deep Crawling
Uses `asyncio.gather` to concurrently visit detail pages for different platforms. This prevents slow-loading sites from blocking the entire pipeline.

### 3. Metadata Auto-Fill
The "Master Metadata" (Author, Date, Frontcover) is fetched only for the first library link of a unique book and shared across all other links for that book within the same platform.

## Modules
- `bookops.py`: CLI entry point & terminal configuration.
- `pipeline.py`: Orchestrates multi-site search.
- `sites/`: Contains site-specific Playwright logic.
- `models.py`: The `BookResult` dataclass (Title, Author, Format, Date, URL, Source, Frontcover).
- `formatters.py`: Logic for rendering data to the console or files.
