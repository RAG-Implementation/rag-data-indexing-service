"""Text cleaning stage.

Light, dependency-minimal cleaning that prepares text for reliable chunking and
embedding. This is the same logic validated in `notebooks/02_clean_corpus.ipynb`,
refactored into reusable functions.
"""

from __future__ import annotations

import re
import unicodedata

import ftfy

# Compiled once at import time so repeated calls stay fast.
_RE_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")  # control chars (keep \t \n \r)
_RE_MULTI_SPACE = re.compile(r"[ \t]+")
_RE_MULTI_BLANK = re.compile(r"\n{3,}")


def fix_unicode(text: str) -> str:
    """Repair garbled unicode and normalize to a single canonical form (NFC)."""
    return unicodedata.normalize("NFC", ftfy.fix_text(text))


def remove_control_chars(text: str) -> str:
    """Remove non-printable control characters but keep newlines and tabs."""
    return _RE_CONTROL.sub("", text)


def normalize_whitespace(text: str) -> str:
    """Collapse runs of spaces/tabs and strip trailing space on each line."""
    text = _RE_MULTI_SPACE.sub(" ", text)
    return "\n".join(line.strip() for line in text.split("\n"))


def collapse_blank_lines(text: str) -> str:
    """Reduce 3 or more consecutive newlines down to a single blank line."""
    return _RE_MULTI_BLANK.sub("\n\n", text)


def clean_text(text: str) -> str:
    """Run the full cleaning pipeline on a single string.

    Order matters: fix unicode, strip control chars, normalize whitespace,
    collapse blank lines, then trim the edges.
    """
    if not text:
        return ""
    text = fix_unicode(text)
    text = remove_control_chars(text)
    text = normalize_whitespace(text)
    text = collapse_blank_lines(text)
    return text.strip()
