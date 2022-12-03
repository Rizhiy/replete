from __future__ import annotations

import contextlib
import datetime as dt
import sys
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple, Optional

import pytest

from nt_utils.cli import AutoCLI, autocli

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence
    from typing import Any, Callable


@autocli(fail_on_unknown_args=False, help_width=100, max_help_position=50)
def example_cli(
    output_dir: Path,
    no_help: str,
    res_name: str = "test",
    date_: Optional[dt.date] = None,
    items: Optional[dict[str, int]] = None,
    no_type_longname: str = "no type",
) -> None:
    """
    Test function

    A function to test.

    Just as an example.

    :param output_dir: A dir
    :param res_name: Name for result
    """
    if date_ is None:
        date_ = dt.datetime.now(tz=dt.timezone.utc).date()
    print(output_dir / f"{date_.year}_{res_name}.txt")
    print(f"{items=!r}, {no_type_longname=!r}")


MAIN_NAME = "test_cli.py"
DESCRIPTION = """
  Test function

  A function to test.

  Just as an example.
"""
POSITIONAL_USAGE_TEXT = f"""
usage: {MAIN_NAME} [-h] [--res-name RES_NAME] [--date DATE] [--items [ITEMS ...]]
                   [--no-type-longname NO_TYPE_LONGNAME]
                   output_dir no_help
""".strip(
    "\n"
)
# fmt: off
OPTIONAL_HELP_TEXT = """
  --res-name RES_NAME                  Name for result (default: test)
  --date DATE                          
  --items [ITEMS ...]                  
  --no-type-longname NO_TYPE_LONGNAME
""".strip(
    "\n"
)
# fmt: on

BAD_ARGS_TEXT = f"""
{POSITIONAL_USAGE_TEXT}
{MAIN_NAME}: error: the following arguments are required: output_dir, no_help
"""

HELP_TEXT = f"""
{POSITIONAL_USAGE_TEXT}
{DESCRIPTION}
positional arguments:
  output_dir                           A dir
  no_help

options:
  -h, --help                           show this help message and exit
{OPTIONAL_HELP_TEXT}
"""

POSITIONAL_PROVIDED_HELP_TEXT = f"""
usage: {MAIN_NAME} [-h] [--output-dir OUTPUT_DIR] [--res-name RES_NAME] [--date DATE]
                   [--items [ITEMS ...]] [--no-type-longname NO_TYPE_LONGNAME]
                   no_help
{DESCRIPTION}
positional arguments:
  no_help

options:
  -h, --help                           show this help message and exit
  --output-dir OUTPUT_DIR              A dir (default: provided out)
{OPTIONAL_HELP_TEXT}
"""


class CLITestCase(NamedTuple):
    name: str
    args: Sequence[str]
    expected_stdout: str
    expected_stderr: str = ""
    expected_code: int = 0
    func: Callable[..., Any] = example_cli


CLI_TEST_CASES: Sequence[CLITestCase] = [
    CLITestCase(name="no_args", args=[], expected_stdout="", expected_stderr=BAD_ARGS_TEXT, expected_code=2),
    CLITestCase(name="help", args=["--help"], expected_stdout=HELP_TEXT),
    CLITestCase(
        name="new default",
        args=["--help"],
        expected_stdout=HELP_TEXT.replace("(default: test)", "(default: new)"),
        func=partial(example_cli, res_name="new"),
    ),
    CLITestCase(
        name="positional provided help",
        args=["--help"],
        expected_stdout=POSITIONAL_PROVIDED_HELP_TEXT,
        func=partial(example_cli, output_dir=Path("provided out")),
    ),
    CLITestCase(
        name="basic usage",
        args=["help"],
        expected_stdout="a_dir/2015_test.txt\nitems={}, no_type_longname='no type'",
        func=partial(example_cli, Path("a_dir"), date_=dt.date(2015, 1, 1)),
    ),
    CLITestCase(
        name="basic call",
        args=["some_out/dir", "help", "--date", "2012-11-10", "--items", "a", "1", "c", "3", "--no-type=typenone"],
        expected_stdout="some_out/dir/2012_test.txt\nitems={'a': 1, 'c': 3}, no_type_longname='typenone'",
    ),
    CLITestCase(
        name="override provided",
        args=["some_out/dir", "help", "--date", "2022-11-10"],
        expected_stdout="some_out/dir/2022_test.txt\nitems={}, no_type_longname='no type'",
        func=partial(example_cli, date_=dt.date(2011, 1, 1)),
    ),
    CLITestCase(
        name="no cli",
        args=["some_out/dir", "--date", "2012-11-10"],
        expected_stdout="out/2020_test.txt\nitems=None, no_type_longname='no type'",
        func=partial(example_cli.func, Path("out"), "help", date_=dt.date(2020, 1, 1)),
    ),
]


@contextlib.contextmanager
def out_capture(attr: str = "stdout") -> Generator[list[str], None, None]:
    out_data: list[str] = []

    def out_write(data: str | bytes) -> None:
        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="replace")
        out_data.append(data)

    monkeypatch = pytest.MonkeyPatch()
    try:
        monkeypatch.setattr(getattr(sys, attr), "write", out_write)
        yield out_data
    finally:
        monkeypatch.undo()


@pytest.mark.parametrize("test_case", CLI_TEST_CASES, ids=[testcase.name for testcase in CLI_TEST_CASES])
def test_example_cli(test_case: CLITestCase, monkeypatch: Any) -> None:
    monkeypatch.setattr(sys, "argv", [MAIN_NAME, *test_case.args])

    with out_capture(attr="stdout") as stdout_data, out_capture(attr="stderr") as stderr_data:
        try:
            test_case.func()
        except SystemExit as err:
            if err.code != test_case.expected_code:
                raise

    stdout = "".join(stdout_data)
    assert stdout.strip() == test_case.expected_stdout.strip()
    stderr = "".join(stderr_data)
    assert stderr.strip() == test_case.expected_stderr.strip()


def test_wrapping() -> None:
    assert isinstance(example_cli, AutoCLI)
    func = example_cli.__wrapped__
    assert func.__name__ == "example_cli"
    for attr in ["__module__", "__name__", "__qualname__", "__doc__", "__annotations__"]:
        assert getattr(example_cli, attr) == getattr(func, attr)
