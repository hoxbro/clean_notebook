from __future__ import annotations

from .clean import clean_notebook, clean_single_notebook

try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"

__all__ = ("__version__", "clean_notebook", "clean_single_notebook")
