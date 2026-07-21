"""Data model for a detected comment issue."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommentIssue:
    path: str
    line: int
    kind: str
    snippet: str
