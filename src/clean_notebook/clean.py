from __future__ import annotations

import json
from pathlib import Path
from typing import Any, AnyStr


def clean_notebook(files: list[str | Path], dryrun: bool = False):
    for file in sorted(files):
        _clean_single_notebook(file, dryrun)


def find_line_ending(s: AnyStr) -> AnyStr:
    if isinstance(s, str):
        endings = ["\r\n", "\n", "\r"]
    elif isinstance(s, bytes):
        endings = [b"\r\n", b"\n", b"\r"]
    else:
        raise ValueError("Not str or bytes")

    counter = {s.count(e): e for e in endings}
    return counter[max(counter)]


def _clean_single_notebook(file: str | Path, dryrun: bool = False) -> bool | None:
    if not str(file).endswith(".ipynb"):
        return None

    with open(file, encoding="utf8") as f:
        raw = f.read()

    newline = find_line_ending(raw)
    nb = json.loads(raw)

    cleaned = False
    for cell in nb["cells"]:
        cleaned |= _update_value(cell, "outputs", [])
        cleaned |= _update_value(cell, "execution_count", None)
        cleaned |= _update_value(cell, "metadata", {})

    metadata = {"language_info": {"name": "python", "pygments_lexer": "ipython3"}}
    cleaned |= _update_value(nb, "metadata", metadata)

    if cleaned and not dryrun:
        with open(file, "w", encoding="utf8", newline=newline) as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write(newline)  # empty line at the end of the file
    if cleaned:
        print(f"Cleaned notebook: {file}")

    return cleaned


def _update_value(dct: dict[str, Any], key: str, value: Any) -> bool:
    if key in dct and dct[key] != value:
        dct[key] = value
        return True
    else:
        return False


if __name__ == "__main__":
    clean_notebook(["test"])
