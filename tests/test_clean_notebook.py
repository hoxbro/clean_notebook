from __future__ import annotations

import uuid
from pathlib import Path
from shutil import copy2, rmtree
from typing import TYPE_CHECKING, Iterator

import pytest

from clean_notebook.clean import _find_line_ending, clean_single_notebook

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from _pytest.tmpdir import TempPathFactory


def load_file(path: Path) -> bytes:
    file_bytes = path.read_bytes()
    le = _find_line_ending(file_bytes)
    return file_bytes.replace(le, b"\n")


@pytest.fixture
def temp_path(tmp_path_factory: TempPathFactory) -> Iterator[Path]:
    src = Path("tests/data").resolve(strict=True)
    dst = tmp_path_factory.mktemp("data")

    for file in src.glob("*.ipynb"):
        copy2(file, dst / file.name)

    yield dst
    rmtree(dst)


TESTS = ["ascii", "jupyterlab", "vscode", "colab", "empty_cell", "empty_multi_cell"]


@pytest.mark.parametrize("test", [*TESTS, "ignore_slideshow", "id", "newline"])
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

    assert clean_single_notebook(dirty)

    clean_bytes = load_file(clean)
    dirty_bytes = load_file(dirty)

    assert clean_bytes == dirty_bytes


def test_notebook_strip_newline(temp_path: Path) -> None:
    test = "newline"
    dirty = temp_path / f"dirty_{test}.ipynb"
    clean = temp_path / f"clean_{test}.ipynb"

    assert clean_single_notebook(dirty, strip=True)

    clean_bytes = load_file(clean)
    dirty_bytes = load_file(dirty)

    assert clean_bytes == dirty_bytes


def test_ignore_metadata(temp_path: Path) -> None:
    test = "ignore_slideshow"
    dirty = temp_path / f"dirty_{test}.ipynb"
    clean = temp_path / f"clean_{test}.ipynb"

    assert clean_single_notebook(dirty, ignore=["slideshow"])
    clean_bytes = load_file(clean)
    dirty_bytes = load_file(dirty)
    assert clean_bytes == dirty_bytes

    # Test when ignore is not added
    clean_single_notebook(dirty)
    dirty_bytes = load_file(dirty)
    assert clean_bytes != dirty_bytes


def test_notebook_id(temp_path: Path, monkeypatch: MonkeyPatch) -> None:
    test = "id"
    dirty = temp_path / f"dirty_{test}.ipynb"
    clean = temp_path / f"clean_{test}.ipynb"

    ids = [
        "3d183bd1-509f-4758-9f2d-db94b23c58f9",
        "66cdc779-4931-4306-881a-4bf30cb0fdbb",
        "5cbb8154-79ee-4290-953c-89a89b4276b7",
    ]
    iterator = iter(ids)
    monkeypatch.setattr(uuid, "uuid4", lambda: next(iterator))

    clean_single_notebook(dirty)
    clean_bytes = load_file(clean)
    dirty_bytes = load_file(dirty)
    assert clean_bytes == dirty_bytes


def test_notebook_no_overwrite_ids(temp_path: Path) -> None:
    test = "id"
    clean = temp_path / f"clean_{test}.ipynb"
    assert not clean_single_notebook(clean)


def test_empty_notebook(capsys: CaptureFixture[str], temp_path: Path) -> None:
    dirty = temp_path / "dirty_empty.ipynb"

    clean_single_notebook(dirty)

    captured = capsys.readouterr()
    assert captured.out.strip() == f"Notebook '{dirty}' does not have any valid cells."


def test_bad_json(capsys: CaptureFixture[str], temp_path: Path) -> None:
    file = temp_path / "dirty_bad_json.ipynb"
    with pytest.raises(SystemExit):
        clean_single_notebook(file)
    captured = capsys.readouterr()
    msg = f"{file}: Failed to json decode (Expecting ',' delimiter: line 23 column 1 (char 412))"
    assert captured.out.strip() == msg
