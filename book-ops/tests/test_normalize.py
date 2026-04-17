from models import BookResult

def test_book_result_to_dict():
    item = BookResult(title="A", author="B", source="test")
    data = item.to_dict()
    assert data["title"] == "A"
    assert data["author"] == "B"
    assert data["source"] == "test"
