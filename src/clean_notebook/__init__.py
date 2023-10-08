from __future__ import annotations

import importlib.metadata

from .clean import clean_notebook, clean_single_notebook  # noqa: F401

__version__ = importlib.metadata.version("clean_notebook")
