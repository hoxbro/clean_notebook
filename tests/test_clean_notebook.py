from pathlib import Path
from shutil import copy2

import pytest

from clean_notebook.clean import _clean_single_notebook


@pytest.fixture(scope="session")
def temp_path(tmp_path_factory):
    src = Path("tests/data").resolve(strict=True)
    dst = tmp_path_factory.mktemp("data")

    for file in src.glob("*.ipynb"):
        copy2(file, dst / file.name)

    return dst


@pytest.mark.parametrize("test", ["ascii", "jupyterlab", "vscode", "colab"])
def test_notebook(temp_path, test):
    dirty = temp_path / f"dirty_{test}.ipynb"
    clean = temp_path / f"clean_{test}.ipynb"

    assert dirty.read_bytes() != clean.read_bytes()

    _clean_single_notebook(dirty)

    clean_bytes = clean.read_bytes().replace(b"\r\n", b"\n")
    dirty_bytes = dirty.read_bytes().replace(b"\r\n", b"\n")
    assert clean_bytes == dirty_bytes
