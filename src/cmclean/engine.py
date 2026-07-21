"""Comment-structure analysis engine."""
from __future__ import annotations

import re
from pathlib import Path

from cmclean.models import CommentIssue


# Matches common comment prefixes in source code.
_COMMENT_RE = re.compile(r"^\s*(?:#|//|/\*|\*|<!--|--|;|%)")
_BLOCK_RE = re.compile(r"/\*.*?\*/")

# Patterns for interesting debris.
_PATTERNS = {
    "todo": re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.IGNORECASE),
    "author": re.compile(r"@(author|created by|written by)\b", re.IGNORECASE),
    "emergency": re.compile(r"@#\$%.{0,20}", re.IGNORECASE),
    "long_comment": re.compile(r".{241,}"),
    "blame": re.compile(r"@(blame|debugger|temp|workaround)\b", re.IGNORECASE),
}

_KIND_LABEL = {
    "todo": "TODO-like debris",
    "author": "Author plaque",
    "emergency": "Suspicious debris",
    "long_comment": "Excessively long comment",
    "blame": "Blocker-style remark",
}


def _iter_source_files(root: Path) -> list[Path]:
    allowed = {".py", ".js", ".ts", ".tsx", ".md", ".yaml", ".yml", ".json", ".toml"}
    out = []
    for entry in root.rglob("*"):
        if entry.is_file() and entry.suffix.lower() in allowed:
            out.append(entry)
    return sorted(out)


def _text_for(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    # For block-style files, do not expand multiline comments to avoid false hot-blob detection.
    # We still analyze line-by-line for single-line markers.
    if path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".toml"}:
        text = re.sub(r"/\*.*?\*/", "/* ... */", text, flags=re.DOTALL)
    return text


def _is_comment_line(line: str, path: Path) -> bool:
    if path.suffix.lower() in {".js", ".ts", ".tsx"}:
        if line.lstrip().startswith("//"):
            return True
        if "/*" in line:
            return True
        if line.strip().startswith("*"):
            return True
    if path.suffix.lower() in {".md"}:
        stripped = line.lstrip()
        if stripped.startswith("<!--"):
            return True
        if stripped.startswith("--"):
            return True
    if _COMMENT_RE.match(line):
        return True
    # SQL/YAML/Markdown inline comments are tricky; keep strict.
    return False


def analyze(root: str, *, max_long: int = 240) -> list[CommentIssue]:
    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(root)

    issues: list[CommentIssue] = []
    files = _iter_source_files(root_path)

    for path in files:
        rel = str(path.relative_to(root_path))
        text = _text_for(path)

        for lineno, raw_line in enumerate(text.splitlines(), start=1):
            if not _is_comment_line(raw_line, path):
                continue

            snippet = raw_line.strip()

            for kind, pattern in _PATTERNS.items():
                if kind == "long_comment" and len(raw_line) <= max_long:
                    continue
                if pattern.search(raw_line):
                    issues.append(
                        CommentIssue(
                            path=rel,
                            line=lineno,
                            kind=_KIND_LABEL.get(kind, kind),
                            snippet=snippet,
                        )
                    )
                    break

    return sorted(issues, key=lambda x: (x.path, x.line))
