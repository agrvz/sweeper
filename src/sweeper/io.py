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
