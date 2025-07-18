import csv
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from sweeper.io import (
    get_lines_from_file,
    load_csv_rows_as_lists,
    load_csv_rows_as_dicts,
    load_csv,
)


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


def test_get_lines_from_file(temp_text_file):
    expected_lines = ["alpha", "bravo", "charlie"]
    with open(temp_text_file, "w") as f:
        f.write("\n".join(expected_lines))

    lines = get_lines_from_file(temp_text_file)
    assert lines == expected_lines

    temp_text_file.unlink()


def test_get_lines_from_file_invalid_path():
    invalid_path = Path("invalid/path/to/file.txt")
    with pytest.raises(FileNotFoundError):
        get_lines_from_file(invalid_path)


def test_load_csv_rows_as_lists(temp_csv_file):
    headers = ["id", "name"]
    expected_rows = [["1", "alpha"], ["2", "bravo"], ["3", "charlie"]]
    with open(temp_csv_file, "w") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(expected_rows)

    rows = load_csv_rows_as_lists(temp_csv_file)
    assert rows == expected_rows


def test_load_csv_rows_as_lists_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_csv_rows_as_lists(Path("invalid/path/to/file.csv"))


def test_load_csv_rows_as_lists_empty_file(temp_csv_file):
    with open(temp_csv_file, "w") as file:
        pass

    with pytest.raises(ValueError, match="is empty"):
        rows = load_csv_rows_as_lists(temp_csv_file)

    temp_csv_file.unlink()


def test_load_csv_rows_as_dicts(temp_csv_file):
    headers = ["id", "name"]
    expected_rows = [
        {"id": "1", "name": "alpha"},
        {"id": "2", "name": "bravo"},
        {"id": "3", "name": "charlie"},
    ]
    with open(temp_csv_file, "w") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(expected_rows)

    rows = load_csv_rows_as_dicts(temp_csv_file)
    assert rows == expected_rows


def test_load_csv_rows_as_dicts_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_csv_rows_as_dicts(Path("invalid/path/to/file.csv"))


def test_load_csv_rows_as_dicts_empty_file(temp_csv_file):
    with open(temp_csv_file, "w") as file:
        pass

    with pytest.raises(ValueError, match="is empty"):
        rows = load_csv_rows_as_dicts(temp_csv_file)

    temp_csv_file.unlink()


def test_load_csv_by_column_name():
    pass


def test_load_csv_by_column_name_invalid():
    pass


def test_load_csv_by_column_index():
    pass


def test_load_csv_by_column_index_invalid():
    pass


def test_load_csv_invalid_path():
    pass


def test_load_csv_empty_file():
    pass
