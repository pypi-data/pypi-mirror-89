"""
comment --- an explicit object for comments

The module provides a context manager `Comment` which does nothing.
"""
from contextlib import contextmanager


@contextmanager
def Comment(comment):
    """
    Context
    """
    try:
        yield comment
    finally:
        pass
