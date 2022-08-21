def clean_notebooks(arguments: list[str]):
    for argument in arguments:
        clean_notebook(argument)


def clean_notebook(file):
    print(file)


if __name__ == "__main__":
    clean_notebook(["test"])
