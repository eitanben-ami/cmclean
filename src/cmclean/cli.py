"""cmclean CLI."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from cmclean.engine import analyze


def _emit(issues, json_output=False) -> int:
    if json_output:
        data = [
            {
                "path": i.path,
                "line": i.line,
                "kind": i.kind,
                "snippet": i.snippet,
            }
            for i in issues
        ]
        print(json.dumps(data, ensure_ascii=True))
        return 1 if issues else 0
    else:
        if not issues:
            print("No questionable comments found.")
            return 0
        print(f"Found {len(issues)} issue(s):\n")
        for issue in issues:
            print(f"{issue.path}:{issue.line} [{issue.kind}]")
            print(f"  {issue.snippet}")
        print()
        return 1


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="cmclean",
        description="Lint comment debris in source trees.",
    )
    parser.add_argument("path", help="Project root to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")

    args = parser.parse_args(argv)
    target = Path(args.path).resolve()
    issues = analyze(str(target))
    return _emit(issues, json_output=args.json)


if __name__ == "__main__":
    raise SystemExit(main())
