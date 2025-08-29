import json
from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from sweeper.draw import draw, draw_command


def test_draw():
    entrants = ["Harold", "Jim", "Margaret"]
    picks = ["Bengals", "Bills", "Chiefs"]
    result = draw(entrants=entrants, picks=picks, delay=0)
    assert len(result) == 3
    assert list(result.keys()) == ["Harold", "Jim", "Margaret"]


def test_draw_too_few_picks_raises_error():
    with pytest.raises(ValueError):
        entrants = ["Harold", "Jim"]
        picks = ["Bengals"]
        draw(entrants=entrants, picks=picks, delay=0)


def test_draw_too_few_entrants_is_ok():
    entrants = ["Jim"]
    picks = ["Bengals", "Bills"]
    result = draw(entrants=entrants, picks=picks, delay=0)
    assert len(result) == 1
    assert next(iter(result)) == "Jim"


def test_draw_entrants_are_not_unique():
    entrants = ["Harold", "Jim", "Harold"]
    picks = ["Bengals", "Bills", "Chiefs"]
    with pytest.raises(ValueError):
        result = draw(entrants=entrants, picks=picks, delay=0)


def test_draw_picks_are_not_unique():
    entrants = ["Harold", "Jim", "Margaret"]
    picks = ["Bengals", "Bills", "Bengals"]
    with pytest.raises(ValueError):
        result = draw(entrants=entrants, picks=picks, delay=0)


def test_draw_debug_mode():
    entrants = ["Harold", "Jim", "Margaret", "John", "Tony", "Gordon"]
    picks = ["Bengals", "Bills", "Chiefs", "Dolphins", "Eagles", "Falcons"]
    expected_result = {
        "Harold": "Bengals",
        "Jim": "Bills",
        "Margaret": "Chiefs",
        "John": "Dolphins",
        "Tony": "Eagles",
        "Gordon": "Falcons",
    }
    for _ in range(100):
        result = draw(entrants=entrants, picks=picks, delay=0, debug=True)
        assert result == expected_result


def test_draw_command(temp_picks_txt_file: Path, temp_entrants_txt_file: Path):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--picks",
            temp_picks_txt_file,
            "--entrants",
            temp_entrants_txt_file,
            "--delay",
            "0",
        ],
    )
    assert result.exit_code == 0
    assert "Jim" in result.output


def test_draw_command_passes_on_arguments(
    mocker, temp_picks_txt_file: Path, temp_entrants_txt_file: Path
):
    mock_draw = mocker.patch("sweeper.draw.draw")
    mock_get_lines = mocker.patch("sweeper.draw.get_lines_from_file")
    mock_get_lines.side_effect = [
        ["Harold", "Jim", "Margaret"],
        ["Bengals", "Bills", "Chiefs"],
    ]

    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--entrants",
            temp_entrants_txt_file,
            "--picks",
            temp_picks_txt_file,
            "--delay",
            0,
            "--draw-order",
            "shuffle",
            "--output-file",
            "output.csv",
            "--quiet",
        ],
    )
    mock_get_lines.assert_any_call(filepath=temp_picks_txt_file)
    mock_get_lines.assert_any_call(filepath=temp_entrants_txt_file)
    mock_draw.assert_called_once_with(
        entrants=["Harold", "Jim", "Margaret"],
        picks=["Bengals", "Bills", "Chiefs"],
        draw_order="shuffle",
        delay=0.0,
        quiet=True,
    )


def test_draw_command_file_does_not_exist_raises_error():
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        ["--picks", "doesnotexist.txt", "--entrants", "doesnotexist2.txt"],
    )
    assert result.exit_code != 0
    assert isinstance(result.exception, SystemExit)
    assert "File 'doesnotexist.txt' does not exist" in result.output


def test_draw_command_with_csv_columns(
    mocker, temp_entrants_csv_file, temp_picks_csv_file
):
    mock_load_csv = mocker.patch("sweeper.draw.load_csv")

    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--entrants",
            temp_entrants_csv_file,
            "--entrants-column",
            1,
            "--picks",
            temp_picks_csv_file,
            "--picks-column",
            1,
            "--delay",
            0,
        ],
    )

    mock_load_csv.assert_any_call(filepath=temp_entrants_csv_file, column_index=1)
    mock_load_csv.assert_any_call(filepath=temp_picks_csv_file, column_index=1)


def test_draw_command_with_csv_but_no_column_raises_error(
    mocker, temp_entrants_csv_file, temp_picks_csv_file
):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--entrants",
            temp_entrants_csv_file,
            "--picks",
            temp_picks_csv_file,
            "--picks-column",
            1,
            "--delay",
            0,
        ],
    )
    assert result.exit_code != 0
    assert isinstance(result.exception, SystemExit)
    assert (
        "Missing option '--entrants-column'. Required if <lambda>(--entrants)=.csv"
        in result.output
    )


def test_draw_command_invalid_file_suffix_raises_error(temp_py_file: Path):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        ["--picks", temp_py_file, "--entrants", temp_py_file],
    )
    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
    assert "file must be a .csv or .txt file" in result.exception.args[0]


def test_draw_command_creates_valid_output_csv_file(
    temp_picks_txt_file: Path,
    temp_entrants_txt_file: Path,
    temp_output_csv_file: Path,
):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--picks",
            temp_picks_txt_file,
            "--entrants",
            temp_entrants_txt_file,
            "--delay",
            0,
            "--output-file",
            temp_output_csv_file,
        ],
    )
    assert result.exit_code == 0
    file_data = temp_output_csv_file.read_text()
    assert "Harold" in file_data
    assert "Jim" in file_data
    assert "Margaret" in file_data


def test_draw_command_creates_valid_output_json_file(
    temp_picks_txt_file: Path,
    temp_entrants_txt_file: Path,
    temp_output_json_file: Path,
):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--picks",
            temp_picks_txt_file,
            "--entrants",
            temp_entrants_txt_file,
            "--delay",
            0,
            "--output-file",
            temp_output_json_file,
        ],
    )
    assert result.exit_code == 0
    with open(temp_output_json_file, "r") as in_file:
        file_data = json.load(in_file)
        assert isinstance(file_data, dict)
        assert len(file_data) == 3
        assert list(file_data.keys()) == ["Harold", "Jim", "Margaret"]


def test_draw_command_invalid_output_file_suffix_raises_error(
    temp_picks_txt_file: Path, temp_entrants_txt_file: Path, temp_py_file: Path
):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--picks",
            temp_picks_txt_file,
            "--entrants",
            temp_entrants_txt_file,
            "--delay",
            0,
            "--output-file",
            temp_py_file,
        ],
    )
    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
    assert "Output file must be a .csv or .json file" in result.exception.args[0]
