"""Allow ``python -m cmclean`` invocation."""
from __future__ import annotations

from cmclean.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
