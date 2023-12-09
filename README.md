# Clean up notebook

A simple command to clean up your Jupyter notebooks.

## Usage

If you want to run this tool in a CLI, [pipx](https://pypa.github.io/pipx/) is advised.

```bash
pipx install clean-notebook
```

To use `clean-notebook` with [pre-commit](https://pre-commit.com/), add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/hoxbro/clean_notebook
  rev: "" # Use the sha / tag you want to point at
  hooks:
    - id: clean-notebook
```

## Configuration

To clean a notebook run the command `clean-notebook example.ipynb` or if you want to do it for multiple files `clean-notebook example1.ipynb example2.ipynb`.

The following arguments are supported `--dry-run` to not overwrite the file and `--keep-empty` to keep empty cells. If you want not to delete a specific metadata key, the `-i`/`--ignore` argument can be used. If more keys should be ignored: `clean-notebook . -i tags -i slideshow`. If you want remove ending newlines in code cells, use the `-s`/`--strip-trailing-newlines` argument.
