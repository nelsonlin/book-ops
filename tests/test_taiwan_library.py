"""Unit tests for taiwan_library.py helper functions."""
import pytest
from sites.taiwan_library import (
    _clean_text,
    _looks_like_bookish_row,
    _normalize_date,
    _clean_metadata,
)


class TestCleanText:
    """Tests for _clean_text function."""

    def test_clean_text_none(self):
        assert _clean_text(None) == ""

    def test_clean_text_empty(self):
        assert _clean_text("") == ""

    def test_clean_text_whitespace(self):
        assert _clean_text("  hello  world  ") == "hello world"

    def test_clean_text_newlines(self):
        assert _clean_text("hello\n\nworld") == "hello world"

    def test_clean_text_tabs(self):
        assert _clean_text("hello\tworld") == "hello world"


class TestNormalizeDate:
    """Tests for _normalize_date function."""

    def test_normalize_date_none(self):
        assert _normalize_date(None) == ""

    def test_normalize_date_empty(self):
        assert _normalize_date("") == ""

    def test_normalize_date_year_only(self):
        assert _normalize_date("2020") == "2020-01-01"
        assert _normalize_date("1999") == "1999-01-01"

    def test_normalize_date_full_date(self):
        result = _normalize_date("2020-01-15")
        assert result == "2020-01-15"

    def test_normalize_date_slashed(self):
        result = _normalize_date("2020/01/15")
        assert result == "2020-01-15"

    def test_normalize_date_no_date(self):
        assert _normalize_date("Some text without date") == ""


class TestCleanMetadata:
    """Tests for _clean_metadata function."""

    def test_clean_metadata_none(self):
        assert _clean_metadata(None) == ""

    def test_clean_metadata_empty(self):
        assert _clean_metadata("") == ""

    def test_clean_metadata_labels(self):
        assert _clean_metadata("作者: 張三") == "張三"
        assert _clean_metadata("出版年: 2024") == "2024"

    def test_clean_metadata_suffixes(self):
        assert _clean_metadata("張三 著") == "張三"
        assert _clean_metadata("李四 編") == "李四"


class TestLooksLikeBookishRow:
    """Tests for _looks_like_bookish_row function."""

    def test_looks_like_bookish_row_empty(self):
        assert _looks_like_bookish_row("", "") is False
        assert _looks_like_bookish_row("", "a") is False

    def test_looks_like_bookish_row_short(self):
        # Combined length must be >= 2
        assert _looks_like_bookish_row("a", "") is False

    def test_looks_like_bookish_row_blocked_home(self):
        # Should block navigation/home terms
        assert _looks_like_bookish_row("首頁", "Home page") is False
        assert _looks_like_bookish_row("home", "link") is False

    def test_looks_like_bookish_row_blocked_login(self):
        assert _looks_like_bookish_row("登入", "login link") is False
        assert _looks_like_bookish_row("login", "click here") is False

    def test_looks_like_bookish_row_valid(self):
        # Normal book row should pass
        assert _looks_like_bookish_row("Python Programming", "作者：張三") is True
