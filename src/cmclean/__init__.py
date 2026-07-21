"""cmclean: comment-structure linter."""

from cmclean.models import CommentIssue
from cmclean.engine import analyze

__all__ = ["CommentIssue", "analyze"]
