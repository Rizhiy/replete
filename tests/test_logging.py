from __future__ import annotations

import logging
import warnings

import pytest

from nt_utils.logging import change_logging_level, warn_with_traceback


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
