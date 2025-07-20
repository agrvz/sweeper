from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest


@pytest.fixture
def temp_text_file():
    with NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as file:
        yield Path(file.name)
    file.close()


@pytest.fixture
def temp_csv_file():
    with NamedTemporaryFile(delete=False, mode="w", suffix=".csv") as file:
        yield Path(file.name)
    file.close()


@pytest.fixture
def temp_py_file():
    with NamedTemporaryFile(delete=False, mode="w", suffix=".py") as file:
        yield Path(file.name)
    file.close()
