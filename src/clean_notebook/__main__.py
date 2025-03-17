from __future__ import annotations

import argparse

from . import __version__  # pyright: ignore[reportAttributeAccessIssue]
from .clean import clean_notebook


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean Jupyter Notebooks output and metadata",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Run clean-notebook on the given files or directories",
    )
    parser.add_argument(
        "--dryrun",
        dest="dryrun",
        action="store_true",
        help="Dry run the command",
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
    parser.add_argument(
        "--strip-trailing-newlines",
        "-s",
        dest="strip",
        action="store_true",
        help="Strip newline from the end of cells",
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main() -> None:
    parser = _create_parser()
    args = parser.parse_args()
    clean_notebook(**vars(args))


if __name__ == "__main__":
    main()
