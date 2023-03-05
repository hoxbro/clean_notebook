import os
import shutil
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()
PYTHON_VERSIONS = ("3.7", "3.8", "3.9", "3.10", "3.11")

nox.options.reuse_existing_virtualenvs = True

if os.environ.get("CI", None):
    nox.options.error_on_missing_interpreters = True


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    session.install("-e", ".[dev]")
    session.run("python", "-m", "pytest", "tests")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all")


@nox.session
def build(session: nox.Session) -> None:
    build_p = DIR / "build"
    if build_p.exists():
        shutil.rmtree(build_p)

    dist_p = DIR / "dist"
    if dist_p.exists():
        shutil.rmtree(dist_p)

    session.install("build")
    session.run("python", "-m", "build")
