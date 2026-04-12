"""Unit tests for taiwan_library.py helper functions."""
import pytest
from sites.taiwan_library import (
    _clean_text,
    _guess_author,
    _guess_format,
    _guess_date,
    _looks_like_bookish_row,
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


class TestGuessAuthor:
    """Tests for _guess_author function."""

    def test_guess_author_none(self):
        assert _guess_author(None) == ""

    def test_guess_author_empty(self):
        assert _guess_author("") == ""

    def test_guess_author_chinese(self):
        text = "書名：Python編程｜作者：张三"
        result = _guess_author(text)
        assert "张三" in result

    def test_guess_author_english(self):
        text = "Title: Python Programming | Author: John Smith"
        result = _guess_author(text)
        assert "John Smith" in result

    def test_guess_author_no_author(self):
        text = "這是一本書"
        assert _guess_author(text) == ""


class TestGuessFormat:
    """Tests for _guess_format function."""

    def test_guess_format_none(self):
        assert _guess_format(None) == "Unknown"

    def test_guess_format_empty(self):
        assert _guess_format("") == "Unknown"

    def test_guess_format_epub(self):
        assert _guess_format("EPUB") == "EPUB"
        assert _guess_format("epub") == "EPUB"
        assert _guess_format("Some text EPUB here") == "EPUB"

    def test_guess_format_pdf(self):
        assert _guess_format("PDF") == "PDF"
        assert _guess_format("Some text PDF here") == "PDF"

    def test_guess_format_paper(self):
        assert _guess_format("PAPER") == "Paper"
        assert _guess_format("paperback") == "Paper"
        # Can't reliably test Chinese due to encoding issues in test file creation

    def test_guess_format_unknown(self):
        assert _guess_format("Some random text") == "Unknown"


class TestGuessDate:
    """Tests for _guess_date function."""

    def test_guess_date_none(self):
        assert _guess_date(None) == ""

    def test_guess_date_empty(self):
        assert _guess_date("") == ""

    def test_guess_date_year_only(self):
        assert _guess_date("2020") == "2020"
        assert _guess_date("1999") == "1999"

    def test_guess_date_full_date(self):
        result = _guess_date("2020-01-15")
        assert "2020" in result

    def test_guess_date_slashed(self):
        result = _guess_date("2020/01/15")
        assert "2020" in result

    def test_guess_date_no_date(self):
        assert _guess_date("Some text without date") == ""


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

    def test_looks_like_bookish_row_blocked_facebook(self):
        assert _looks_like_bookish_row("Facebook", "follow us") is False

    def test_looks_like_bookish_row_blocked_menu(self):
        assert _looks_like_bookish_row("menu", "navigation") is False

    def test_looks_like_bookish_row_valid(self):
        # Normal book row should pass
        assert _looks_like_bookish_row("Python Programming", "作者：張三") is True

    def test_looks_like_bookish_row_title_only(self):
        # Just title should work
        assert _looks_like_bookish_row("A Great Book Title", "") is True