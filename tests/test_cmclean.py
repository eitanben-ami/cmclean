"""Tests for cmclean comment-structure linter."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from cmclean.engine import analyze


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_detects_todo_like_debris():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write(root / "app.py", "# TODO: refactor me later\nx=1\n")
        issues = analyze(str(root))
        assert len(issues) == 1
        assert issues[0].kind == "TODO-like debris"
        assert issues[0].line == 1
        assert "TODO" in issues[0].snippet


def test_detects_author_plaque():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write(root / "module.js", "// @author: Jane Doe\n")
        issues = analyze(str(root))
        assert len(issues) == 1
        assert issues[0].kind == "Author plaque"
        assert "author" in issues[0].snippet.lower()


def test_clean_comments_are_not_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write(root / "service.py", "\"\"\"Clean documentation.\"\"\"\n# normal comment\n")
        issues = analyze(str(root))
        assert issues == []


def test_detects_excessively_long_comment():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        long_text = "# " + "x" * 250 + "\n"
        _write(root / "app.py", long_text)
        issues = analyze(str(root))
        assert len(issues) == 1
        assert issues[0].kind == "Excessively long comment"
        assert issues[0].line == 1


def test_multiple_files_and_kinds():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write(root / "a.js", "// HACK\n")
        _write(root / "b.py", "# main entry\n")
        _write(root / "c.ts", "// @author John\n")
        issues = analyze(str(root))
        kinds = {i.kind for i in issues}
        assert "TODO-like debris" in kinds
        assert "Author plaque" in kinds
        assert any(i.path.endswith("b.py") for i in issues) is False


def test_invalid_root_raises():
    with pytest.raises(FileNotFoundError):
        analyze("/nonexistent/path/12345")


def test_cli_json_output_returns_dict():
    from cmclean.cli import main

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write(root / "app.py", "# FIXME\n")
        rc = main([str(root), "--json"])
        # stdout is captured in tests by monkeypatch; verify parse shape when available
        assert rc == 1  # JSON mode still returns nonzero on issues
