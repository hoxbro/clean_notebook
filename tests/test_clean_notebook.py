from __future__ import annotations

from pathlib import Path
from shutil import copy2, rmtree
from typing import TYPE_CHECKING, Iterator

import pytest

from clean_notebook.clean import _clean_single_notebook, find_line_ending

if TYPE_CHECKING:
    from _pytest.tmpdir import TempPathFactory


def load_file(path: Path) -> bytes:
    file_bytes = path.read_bytes()
    le = find_line_ending(file_bytes)
    return file_bytes.replace(le, b"\n")


@pytest.fixture(scope="session")
def temp_path(tmp_path_factory: TempPathFactory) -> Iterator[Path]:
    src = Path("tests/data").resolve(strict=True)
    dst = tmp_path_factory.mktemp("data")

    for file in src.glob("*.ipynb"):
        copy2(file, dst / file.name)

    yield dst
    rmtree(dst)


TESTS = ["ascii", "jupyterlab", "vscode", "colab", "empty_cell"]


@pytest.mark.parametrize("test", TESTS)
def test_noclean_notebook(temp_path: Path, test: str) -> None:
    dirty = temp_path / f"dirty_{test}.ipynb"
    clean = temp_path / f"clean_{test}.ipynb"

    clean_bytes = load_file(clean)
    dirty_bytes = load_file(dirty)

    assert clean_bytes != dirty_bytes


@pytest.mark.parametrize("test", TESTS)
def test_notebook(temp_path: Path, test: str) -> None:
    dirty = temp_path / f"dirty_{test}.ipynb"
    clean = temp_path / f"clean_{test}.ipynb"

    _clean_single_notebook(dirty)

    clean_bytes = load_file(clean)
    dirty_bytes = load_file(dirty)

    assert clean_bytes == dirty_bytes
