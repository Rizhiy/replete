from pathlib import Path

import pytest


def test_build_data_file_full_path(build_data_file_full_path):
    assert build_data_file_full_path("test.pkl") == Path(__file__).parent / "data" / "test_testing" / "test.pkl"


@pytest.mark.parametrize(
    ("filename", "expected"),
    [("test.pkl", {"foo": "pickle"}), ("test.yaml", {"foo": "yaml"}), ("test.txt", "foo text\n")],
)
def test_load_file(load_file, filename: str, expected: dict | str):
    assert load_file(filename) == expected
