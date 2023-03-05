import argparse

from . import __version__
from .clean import clean_notebook


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean Jupyter Notebooks output and metadata",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("filenames", nargs="+", help="Notebook(s) to clean")
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
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args()

    clean_notebook(args.filenames, dryrun=args.dryrun, keep_empty=args.keep_empty)


if __name__ == "__main__":
    main()
