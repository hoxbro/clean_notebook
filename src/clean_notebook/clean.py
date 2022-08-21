from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def clean_notebook(files: list[str | Path], dryrun: bool = False):
    for file in files:
        _clean_single_notebook(file, dryrun)


def _clean_single_notebook(file: str | Path, dryrun: bool = False):
    if not str(file).endswith(".ipynb"):
        return

    with open(file, encoding="utf8") as f:
        nb = json.load(f)

    cleaned = False
    for cell in nb["cells"]:
        cleaned |= _update_value(cell, "outputs", [])
        cleaned |= _update_value(cell, "execution_count", None)
        cleaned |= _update_value(cell, "metadata", {})

    metadata = {"language_info": {"name": "python", "pygments_lexer": "ipython3"}}
    cleaned |= _update_value(nb, "metadata", metadata)

    if cleaned:
        if not dryrun:
            with open(file, "w", encoding="utf8") as f:
                json.dump(nb, f, indent=1)  # , ensure_ascii=False)
        print(f"Cleaned notebook: {file}")

    return nb


def _update_value(dct: dict[str, Any], key: str, value: Any) -> bool:
    if key in dct and dct[key] != value:
        dct[key] = value
        return True
    else:
        return False


if __name__ == "__main__":
    clean_notebook(["test"])
