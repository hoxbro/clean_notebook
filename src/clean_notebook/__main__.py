from __future__ import annotations

import argparse

from . import __version__
from .clean import clean_notebook


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean Jupyter Notebooks output and metadata",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Path or file with Notebook to clean",
    )
    parser.add_argument(
        "--dryrun",
        dest="dryrun",
        action="store_true",
        help="Only dry run the test",
    )
    parser.add_argument(
        "--keep-empty",
        dest="keep_empty",
        action="store_true",
        help="Keep empty cells",
    )
    parser.add_argument(
        "--ignore",
        "-i",
        dest="ignore",
        action="append",
        help="Metadata keys to ignore when cleaning",
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main() -> None:
    parser = _create_parser()
    args = parser.parse_args()
    clean_notebook(**vars(args))


if __name__ == "__main__":
    main()
