from models import BookResult

def search(book_name: str):
    return [BookResult(
        title=book_name,
        author="Unknown",
        format="Unknown",
        date="",
        url="https://z-library.sk/",
        source="zlibrary"
    )]
