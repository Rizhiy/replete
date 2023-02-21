from __future__ import annotations

import logging
import warnings
from pathlib import Path

import pytest

from nt_utils import assert_with_logging, setup_logging, warn_with_traceback
from nt_utils.logging import change_logging_level, offset_logger_level


def test_warnings_traceback(capsys):
    with pytest.warns(UserWarning), warn_with_traceback():
        warnings.warn("Test")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert len(captured.err) > 4

    with pytest.warns(UserWarning):
        warnings.warn("Test")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_change_logging_level(caplog):
    caplog.set_level(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("before")
    with change_logging_level(logging.WARNING):
        logger.info("inside")
    logger.info("after")
    assert "before" in caplog.text
    assert "inside" not in caplog.text
    assert "after" in caplog.text


def test_assert_with_logging(caplog):
    assert_with_logging(True, "bar")
    with pytest.raises(AssertionError):
        assert_with_logging(False, "foo")
    assert caplog.record_tuples == [("root", logging.CRITICAL, "foo")]


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        (0, [("test_logger", 20, "foo"), ("test_logger", 20, "bar")]),
        (10, [("test_logger", 20, "foo"), ("test_logger", 30, "bar")]),
    ],
)
def test_offset_logger_level(amount, expected, caplog):
    caplog.set_level(logging.DEBUG)
    logger = logging.getLogger("test_logger")
    logger.log(logging.INFO, "foo")
    offset_logger_level(logger, amount)
    logger.log(logging.INFO, "bar")

    assert caplog.record_tuples == expected


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {
            "log_file": Path("foo"),
            "print_level": "INFO",
            "append": True,
            "level_styles_update": {"warning": {"color": "red"}},
            "field_styles_update": {"levelname": {"color": "yellow"}},
            "disable_colors": True,
        },
    ],
)
def test_setup_logging(kwargs, tmp_path):
    if "log_file" in kwargs:
        kwargs["log_file"] = tmp_path / kwargs["log_file"]
    setup_logging(**kwargs)
