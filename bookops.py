import argparse
from pipeline import run_pipeline
from formatters import print_table, print_json, print_tsv

def main():
    parser = argparse.ArgumentParser(description="Book-Ops CLI")
    parser.add_argument("book_name", help="Name of the book to search")
    parser.add_argument("--format", choices=["table", "json", "tsv"], default="table")
    parser.add_argument("--sites", nargs="*", default=[])
    args = parser.parse_args()

    results = run_pipeline(args.book_name, selected_sites=args.sites)

    if args.format == "json":
        print_json(results)
    elif args.format == "tsv":
        print_tsv(results)
    else:
        print_table(results)

if __name__ == "__main__":
