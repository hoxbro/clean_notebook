import argparse

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
        "--remove-empty",
        dest="remove_empty",
        action="store_false",
        help="Remove empty cells",
    )
    args = parser.parse_args()

    clean_notebook(args.filenames, dryrun=args.dryrun, remove_empty=args.remove_empty)


if __name__ == "__main__":
    main()
