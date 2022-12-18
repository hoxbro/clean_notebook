import argparse

from .clean import clean_notebook


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    clean_notebook(args.filenames)


if __name__ == "__main__":
    main()
