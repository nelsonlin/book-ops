import argparse
import sys
import io

# Ensure UTF-8 output for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from pipeline import run_pipeline, run_pipeline_dry
from formatters import print_table, print_json, print_tsv

def main():
    parser = argparse.ArgumentParser(description="Book-Ops CLI")
    parser.add_argument("book_name", nargs="?", help="Name of the book to search (optional for --dry-run)")
    parser.add_argument("--format", choices=["table", "json", "tsv"], default="table")
    parser.add_argument("--sites", nargs="*", default=[])
    parser.add_argument("--dry-run", action="store_true", help="Run with mock data, no browser or network calls")
    args = parser.parse_args()

    if args.dry_run:
        results = run_pipeline_dry()
        print("[dry-run] Pipeline OK — mock results:")
    else:
        if not args.book_name:
            parser.error("book_name is required unless --dry-run is used")
        results = run_pipeline(args.book_name, selected_sites=args.sites)

    if args.format == "json":
        print_json(results)
    elif args.format == "tsv":
        print_tsv(results)
    else:
        print_table(results)

if __name__ == "__main__":
    main()
