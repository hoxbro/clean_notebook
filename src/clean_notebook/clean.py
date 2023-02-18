from __future__ import annotations

import json
from pathlib import Path
from typing import Any, AnyStr


def clean_notebook(
    files: list[str | Path], *, dryrun: bool = False, remove_empty: bool = True
) -> None:
    for file in sorted(files):
        clean_single_notebook(file, dryrun=dryrun, remove_empty=remove_empty)


def find_line_ending(s: AnyStr) -> AnyStr:
    if isinstance(s, str):
        endings = ["\r\n", "\n", "\r"]
    elif isinstance(s, bytes):
        endings = [b"\r\n", b"\n", b"\r"]
    else:
        raise ValueError("Not str or bytes")

    counter = {s.count(e): e for e in endings}
    return counter[max(counter)]


def clean_single_notebook(
    file: str | Path, *, dryrun: bool = False, remove_empty: bool = True
) -> bool:
    if not str(file).endswith(".ipynb"):
        return False

    with open(file, encoding="utf8") as f:
        raw = f.read()

    newline = find_line_ending(raw)
    nb = json.loads(raw)

    cleaned = False
    for cell in nb["cells"]:
        cleaned |= _update_value(cell, "outputs", [])
        cleaned |= _update_value(cell, "execution_count", None)
        cleaned |= _update_value(cell, "metadata", {})
        if not cell["source"] and remove_empty:
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
