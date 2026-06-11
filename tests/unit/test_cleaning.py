"""Tests for the text cleaning stage."""

from app.pipeline.cleaning import clean_text


def test_clean_text_removes_all_problems():
    messy = "  Hello   world\t\tthis  is\n\n\n\nspaced   out.\x07  And TGF-\u03b2.  "
    cleaned = clean_text(messy)

    assert "\t" not in cleaned, "tabs should be gone"
    assert "  " not in cleaned, "double spaces should be collapsed"
    assert "\n\n\n" not in cleaned, "3+ newlines should be collapsed"
    assert "\x07" not in cleaned, "control chars should be removed"
    assert cleaned == cleaned.strip(), "edges should be trimmed"


def test_clean_text_empty_input_returns_empty_string():
    assert clean_text("") == ""
    assert clean_text(None) == ""  # type: ignore[arg-type]


def test_clean_text_preserves_real_unicode():
    # The Greek beta should survive cleaning (only artifacts are normalized).
    assert "\u03b2" in clean_text("TGF-\u03b2 signalling")
