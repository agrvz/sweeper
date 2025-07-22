import csv
import json
from pathlib import Path

import pytest

from sweeper.io import (
    get_lines_from_file,
    load_csv_rows_as_lists,
    load_csv_rows_as_dicts,
    load_csv,
    write_result_to_csv,
    write_result_to_json,
)


def test_get_lines_from_file(temp_txt_file):
    expected_lines = ["alpha", "bravo", "charlie"]
    temp_txt_file.write_text("\n".join(expected_lines))

    lines = get_lines_from_file(temp_txt_file)
    assert lines == expected_lines

    temp_txt_file.unlink()


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
    with pytest.raises(ValueError, match="is empty"):
        rows = load_csv_rows_as_lists(temp_csv_file)


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


def test_load_csv_rows_as_dicts_invalid_path_raises_error():
    with pytest.raises(FileNotFoundError):
        load_csv_rows_as_dicts(Path("invalid/path/to/file.csv"))


def test_load_csv_rows_as_dicts_empty_file_raises_error(temp_csv_file):
    with pytest.raises(ValueError, match="is empty"):
        rows = load_csv_rows_as_dicts(temp_csv_file)


def test_load_csv_by_column_name(temp_picks_csv_file):
    picks_list = load_csv(filepath=temp_picks_csv_file, column_name="name")
    assert picks_list == ["Bengals", "Bills", "Chiefs"]


def test_load_csv_by_column_name_invalid_raises_error(temp_picks_csv_file):
    with pytest.raises(ValueError, match="not found in one or more rows in file"):
        picks_list = load_csv(filepath=temp_picks_csv_file, column_name="doesnotexist")


def test_load_csv_by_column_index(temp_picks_csv_file):
    picks_list = load_csv(filepath=temp_picks_csv_file, column_index=1)
    assert picks_list == ["Bengals", "Bills", "Chiefs"]


def test_load_csv_by_column_index_invalid(temp_picks_csv_file):
    with pytest.raises(IndexError, match="out of range for one or more rows in file"):
        picks_list = load_csv(filepath=temp_picks_csv_file, column_index=5)


def test_load_csv_invalid_path_raises_error():
    with pytest.raises(FileNotFoundError):
        picks_list = load_csv(filepath="path/that/does/not/exist", column_index=1)


def test_load_csv_empty_file_raises_error(temp_csv_file):
    with pytest.raises(ValueError, match="is empty"):
        picks_list = load_csv(filepath=temp_csv_file, column_index=1)


@pytest.mark.parametrize(
    "column_name, column_index",
    [
        ("id", 0),
        ("name", 1),
        ("id", 2),
    ],
)
def test_load_csv_with_column_name_and_index_raises_error(
    temp_picks_csv_file, column_name, column_index
):
    with pytest.raises(
        ValueError, match="You must pass either column_name or column_index, not both."
    ):
        load_csv(
            filepath=temp_picks_csv_file,
            column_name=column_name,
            column_index=column_index,
        )


def test_write_result_to_csv(tmp_path: Path):
    result = {
        "Harold": "Chiefs",
        "Jim": "Bengals",
        "Margaret": "Bills",
    }
    file = tmp_path / "test_result.csv"
    write_result_to_csv(result=result, path=file)
    assert (
        file.read_text() == "entrant,pick\nHarold,Chiefs\nJim,Bengals\nMargaret,Bills\n"
    )


def test_write_result_to_json(tmp_path: Path):
    result = {
        "Harold": "Chiefs",
        "Jim": "Bengals",
        "Margaret": "Bills",
    }
    file = tmp_path / "test_result.json"
    write_result_to_json(result=result, path=file)
    with open(file, "r") as in_file:
        file_data = json.load(in_file)
        assert file_data == result
