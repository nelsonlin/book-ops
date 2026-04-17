import json
from rich.console import Console
from rich.table import Table

console = Console()

def _to_row(item):
    return item.to_dict() if hasattr(item, "to_dict") else item

def print_table(results):
    table = Table(title="Book-Ops Results")
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Format")
    table.add_column("Date")
    table.add_column("Source")
    table.add_column("URL")

    for item in results:
        row = _to_row(item)
        table.add_row(
            str(row.get("title", "")),
            str(row.get("author", "")),
            str(row.get("format", "")),
            str(row.get("date", "")),
            str(row.get("source", "")),
            str(row.get("url", "")),
        )

    console.print(table)

def print_json(results):
    data = [_to_row(r) for r in results]
    print(json.dumps(data, ensure_ascii=False, indent=2))

def print_tsv(results):
    print("title\tauthor\tformat\tdate\tsource\turl")
    for item in results:
        row = _to_row(item)
        print("\t".join(str(v) for v in row.values()))
