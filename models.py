from dataclasses import dataclass, asdict

@dataclass
class BookResult:
    title: str
    author: str
    format: str = "Unknown"
    date: str = ""
    url: str = ""
    source: str = ""
    frontcover: str = ""

    def to_dict(self):
        return asdict(self)
