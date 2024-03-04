import pickle
import warnings
from pathlib import Path

try:
    import pytest
    import yaml
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "this file requires optional dependencies, please install using: replete[testing]",
    ) from exc


DATA_DIRECTORY_NAME = "data"


@pytest.fixture(scope="module")
def build_data_file_full_path(request):
    def path_builder(file_path: Path) -> Path:
        test_module_name = Path(request.fspath).stem
        return Path(request.fspath).parent / DATA_DIRECTORY_NAME / test_module_name / file_path

    return path_builder


@pytest.fixture(scope="module")
def load_file(build_data_file_full_path):
    def loader(file_path: Path):
        full_file_path = build_data_file_full_path(file_path)
        ext = full_file_path.suffix
        if ext == ".pkl":
            with full_file_path.open("rb") as f:
                warnings.simplefilter("ignore")
                return pickle.load(f)  # noqa: S301
        elif ext == ".yaml":
            with full_file_path.open("r") as f:
                return yaml.safe_load(f)
        elif ext == ".txt":
            with full_file_path.open() as f:
                return f.read()
        else:
            raise ValueError(f"Unknown file type: {ext=}")

    return loader
