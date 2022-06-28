from __future__ import annotations

import warnings

import pytest

from nt_utils.logging import warn_with_traceback


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
