import argparse

from .clean_notebook import clean_notebook  # noqa


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    clean_notebook(args.filenames)


if __name__ == "__main__":
    main()
