from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Any, AnyStr, Iterator

__all__ = ("clean_notebook", "clean_single_notebook")

IGNOREDIRS = (".venv", ".pixi", "site-packages", ".ipynb_checkpoints")


def clean_notebook(
    paths: list[str | Path],
    *,
    dryrun: bool = False,
    keep_empty: bool = False,
    ignore: list[str] | None = None,
    strip: bool = False,
) -> None:
    for file in sorted(_get_files(paths)):
        clean_single_notebook(
            file, dryrun=dryrun, keep_empty=keep_empty, ignore=ignore, strip=strip
        )


def clean_single_notebook(
    file: Path,
    *,
    dryrun: bool = False,
    keep_empty: bool = False,
    ignore: list[str] | None = None,
    strip: bool = False,
) -> bool:
    with open(file, encoding="utf8") as f:
        raw = f.read()

    newline = _find_line_ending(raw)
    try:
        nb = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"{file}: Failed to json decode ({e})")
        sys.exit(1)
    set_id = _check_set_id(nb)

    cleaned, sort_keys = False, False
    for cell in nb["cells"].copy():
        cleaned |= _update_value(cell, "outputs", [])
        cleaned |= _update_value(cell, "execution_count", None)
        cleaned |= _update_value(cell, "metadata", _ignore(cell, ignore))
        if strip and cell["cell_type"] == "code":
            cleaned |= _strip_trailing_newlines(cell, newline)
        if not cell["source"] and not keep_empty:
            nb["cells"].remove(cell)
            cleaned = True
        if "attachments" in cell and len(cell["attachments"]) == 0:
            del cell["attachments"]
            cleaned = True
        if set_id and cell.get("id") is None:
            sort_keys |= "id" not in cell
            cell["id"] = str(uuid.uuid4())
            cleaned = True

    if not nb["cells"]:
        print(f"Notebook '{file}' does not have any valid cells.")
        return True

    metadata = {"language_info": {"name": "python", "pygments_lexer": "ipython3"}}
    cleaned |= _update_value(nb, "metadata", metadata)

    if cleaned and not dryrun:
        with open(file, "w", encoding="utf8", newline=newline) as f:
            json.dump(nb, f, indent=1, ensure_ascii=False, sort_keys=sort_keys)
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
            if path.name in IGNOREDIRS:
                continue
            for file in path.rglob("*.ipynb"):
                if any(ps in IGNOREDIRS for ps in file.parts):
                    continue
                yield file


def _ignore(cell: dict[str, Any], ignore: list[str] | None) -> dict[str, Any]:
    if "metadata" in cell and ignore:
        return {k: v for k, v in cell["metadata"].items() if k in ignore}
    return {}


def _check_set_id(nb: dict[str, Any]) -> bool:
    # https://jupyter.org/enhancement-proposals/62-cell-id/cell-id.html
    return (nb["nbformat"] == 4 and nb["nbformat_minor"] >= 5) or nb["nbformat"] >= 5


def _find_line_ending(s: AnyStr) -> AnyStr:
    if isinstance(s, str):
        endings = ["\n", "\r", "\r\n"]
        counter = {s.count(e): e for e in endings}
        return counter[max(counter)]
    elif isinstance(s, bytes):
        endings = [b"\n", b"\r", b"\r\n"]
        counter = {s.count(e): e for e in endings}
        return counter[max(counter)]
    else:
        msg = "Not str or bytes"
        raise TypeError(msg)


def _strip_trailing_newlines(cell: dict[str, Any], newline: AnyStr) -> bool:
    cleaned = False
    while cell["source"]:
        new = cell["source"][-1].rstrip(newline)
        cleaned |= cell["source"][-1] != new
        if cleaned and new:
            cell["source"][-1] = new
        elif cleaned:
            cell["source"].pop()
            continue
        break
    return cleaned
