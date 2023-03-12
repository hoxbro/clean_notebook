from __future__ import annotations

from pathlib import Path
from shutil import copy2, rmtree
from typing import TYPE_CHECKING, Iterator

import pytest

from clean_notebook.clean import clean_single_notebook, find_line_ending

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
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


@pytest.mark.parametrize("test", [*TESTS, "ignore_slideshow"])
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

    clean_single_notebook(dirty)

    clean_bytes = load_file(clean)
    dirty_bytes = load_file(dirty)

    assert clean_bytes == dirty_bytes


def test_ignore_metadata(temp_path: Path) -> None:
    test = "ignore_slideshow"
    dirty = temp_path / f"dirty_{test}.ipynb"
    clean = temp_path / f"clean_{test}.ipynb"

    clean_single_notebook(dirty, ignore=["slideshow"])
    clean_bytes = load_file(clean)
    dirty_bytes = load_file(dirty)
    assert clean_bytes == dirty_bytes

    # Test when ignore is not added
    clean_single_notebook(dirty)
    dirty_bytes = load_file(dirty)
    assert clean_bytes != dirty_bytes


def test_empty_notebook(capsys: CaptureFixture[str], temp_path: Path) -> None:
    dirty = temp_path / "dirty_empty.ipynb"

    clean_single_notebook(dirty)

    captured = capsys.readouterr()
    assert captured.out.strip() == f"Notebook '{dirty}' does not have any valid cells."
