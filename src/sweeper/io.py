import csv
import json
from pathlib import Path


def get_lines_from_file(filepath: Path) -> list:
    """
    Return contents of a text file as a list of each line in the file.
    """
    if isinstance(filepath, str):
        filepath = Path(filepath)
    with open(filepath, "r") as in_file:
        lines = in_file.read().splitlines()
    return lines


def load_csv_rows_as_lists(filepath: Path) -> list[list]:
    """
    Load a CSV file and return rows as lists. The CSV file must have a header row.
    """
    if isinstance(filepath, str):
        filepath = Path(filepath)
    with open(filepath, "r") as in_file:
        if not in_file.read():
            raise ValueError(f"CSV file {filepath} is empty.")

        in_file.seek(0)
        reader = csv.reader(in_file)
        # Skip header row
        next(reader)
        return [row for row in reader if row]


def load_csv_rows_as_dicts(filepath: Path) -> list[dict]:
    """
    Load a CSV file and return rows as dictionaries. The CSV file must have a header row.
    """
    if isinstance(filepath, str):
        filepath = Path(filepath)
    with open(filepath, "r") as in_file:
        if not in_file.read():
            raise ValueError(f"CSV file {filepath} is empty.")

        in_file.seek(0)
        reader = csv.DictReader(in_file)
        return [row for row in reader if row]


def load_csv(
    *, filepath: Path, column_name: str | None = None, column_index: int | None = None
) -> list:
    """
    Load a CSV file and return the contents of a single column as a list of strings.
    You can specify the column to load either by name or by index.
    """
    if not column_name and not column_index:
        raise ValueError("You must pass either column_name or column_index.")

    if column_name and column_index is not None:
        raise ValueError("You must pass either column_name or column_index, not both.")

    if column_name:
        rows = load_csv_rows_as_dicts(filepath)
        try:
            return [row[column_name] for row in rows]
        except KeyError:
            raise ValueError(
                f"Column '{column_name}' not found in one or more rows in file."
            )

    if column_index:
        rows = load_csv_rows_as_lists(filepath)
        try:
            return [row[column_index] for row in rows]
        except IndexError:
            raise IndexError(
                f"Column index {column_index} out of range for one or more rows in file."
            )


def write_result_to_csv(result: dict, path: Path) -> None:
    """
    Write result dictionary to CSV file.
    """
    with open(path, "w") as csv_file:
        field_names = ["entrant", "pick"]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for entrant, pick in result.items():
            writer.writerow({"entrant": entrant, "pick": pick})


def write_result_to_json(result: dict, path: Path) -> None:
    """
    Write result dictionary to JSON file.
    """
    with open(path, "w") as jsonfile:
        json.dump(result, jsonfile, indent=4)
