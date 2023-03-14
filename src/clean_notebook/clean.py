from __future__ import annotations

import json
from pathlib import Path
from typing import Any, AnyStr, Iterator


def clean_notebook(
    paths: list[str | Path],
    *,
    dryrun: bool = False,
    keep_empty: bool = False,
    ignore: list[str] | None = None,
) -> None:
    files = sorted(_get_files(paths))
    for file in files:
        clean_single_notebook(file, dryrun=dryrun, keep_empty=keep_empty, ignore=ignore)


def find_line_ending(s: AnyStr) -> AnyStr:
    if isinstance(s, str):
        endings = ["\n", "\r", "\r\n"]
    elif isinstance(s, bytes):
        endings = [b"\n", b"\r", b"\r\n"]
    else:
        raise ValueError("Not str or bytes")

    counter = {s.count(e): e for e in endings}
    return counter[max(counter)]


def clean_single_notebook(
    file: Path,
    *,
    dryrun: bool = False,
    keep_empty: bool = False,
    ignore: list[str] | None = None,
) -> bool:
    with open(file, encoding="utf8") as f:
        raw = f.read()

    newline = find_line_ending(raw)
    nb = json.loads(raw)

    cleaned = False
    for cell in nb["cells"]:
        cleaned |= _update_value(cell, "outputs", [])
        cleaned |= _update_value(cell, "execution_count", None)
        cell_metadata = _ignore(cell, ignore)
        cleaned |= _update_value(cell, "metadata", cell_metadata)
        if not cell["source"] and not keep_empty:
            nb["cells"].remove(cell)
            cleaned = True

    if not nb["cells"]:
        print(f"Notebook '{file}' does not have any valid cells.")
        return True

    metadata = {"language_info": {"name": "python", "pygments_lexer": "ipython3"}}
    cleaned |= _update_value(nb, "metadata", metadata)

    if cleaned and not dryrun:
        with open(file, "w", encoding="utf8", newline=newline) as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write(newline)  # empty line at the end of the file
        print(f"Cleaned notebook: {file}")
    elif cleaned:
        print(f"Cleaned notebook (dryrun): {file}")

    return cleaned


def _update_value(dct: dict[str, Any], key: str, value: Any) -> bool:
    if key in dct and dct[key] != value:
        dct[key] = value
        return True
    else:
        return False


def _get_files(paths: list[str | Path]) -> Iterator[Path]:
    for path in map(Path, paths):
        if path.is_file() and path.suffix == ".ipynb":
            yield path
        if path.is_dir():
            for file in path.rglob("*.ipynb"):
                if file.parent.name != ".ipynb_checkpoints":
                    yield file


def _ignore(cell: dict[str, Any], ignore: list[str] | None) -> dict[str, Any]:
    if "metadata" in cell and ignore:
        return {k: v for k, v in cell["metadata"].items() if k in ignore}
    return {}
