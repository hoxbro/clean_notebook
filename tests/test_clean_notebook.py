import json

import pytest
from clean_notebook.clean_notebook import _clean_single_notebook


@pytest.mark.parametrize("test", ["ascii"])
def test_notebook(test):
    dirtyfile = f"tests/data/dirty_{test}.ipynb"
    cleanfile = f"tests/data/clean_{test}.ipynb"

    dirty = _clean_single_notebook(dirtyfile, dryrun=True)

    with open(cleanfile) as f:
        clean = json.load(f)

    assert dirty == clean
