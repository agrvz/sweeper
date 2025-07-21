import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from sweeper.draw import draw, draw_command


def test_draw():
    participants = ["Harold", "Jim", "Margaret"]
    teams = ["Bengals", "Bills", "Chiefs"]
    result = draw(participants=participants, teams=teams, delay=0)
    assert len(result) == 3
    assert list(result.keys()) == ["Harold", "Jim", "Margaret"]


def test_draw_too_few_teams_raises_error():
    with pytest.raises(ValueError):
        participants = ["Harold", "Jim"]
        teams = ["Bengals"]
        draw(participants=participants, teams=teams, delay=0)


def test_draw_too_few_participants_is_ok():
    participants = ["Jim"]
    teams = ["Bengals", "Bills"]
    result = draw(participants=participants, teams=teams, delay=0)
    assert len(result) == 1
    assert next(iter(result)) == "Jim"


def test_draw_command(temp_teams_txt_file: Path, temp_participants_txt_file: Path):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--teams",
            temp_teams_txt_file,
            "--participants",
            temp_participants_txt_file,
            "--delay",
            "0",
        ],
    )
    assert result.exit_code == 0
    assert "Jim" in result.output


def test_draw_command_file_does_not_exist_raises_error():
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        ["--teams", "doesnotexist.txt", "--participants", "doesnotexist2.txt"],
    )
    assert result.exit_code != 0
    assert isinstance(result.exception, SystemExit)
    assert "File 'doesnotexist.txt' does not exist" in result.output


def test_draw_command_invalid_file_suffix_raises_error(temp_py_file: Path):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        ["--teams", temp_py_file, "--participants", temp_py_file],
    )
    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
    assert "file must be a .csv or .txt file." in result.exception.args[0]


def test_draw_command_creates_valid_output_csv_file(
    temp_teams_txt_file: Path,
    temp_participants_txt_file: Path,
    temp_output_csv_file: Path,
):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--teams",
            temp_teams_txt_file,
            "--participants",
            temp_participants_txt_file,
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
    temp_teams_txt_file: Path,
    temp_participants_txt_file: Path,
    temp_output_json_file: Path,
):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--teams",
            temp_teams_txt_file,
            "--participants",
            temp_participants_txt_file,
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
    temp_teams_txt_file: Path, temp_participants_txt_file: Path, temp_py_file: Path
):
    runner = CliRunner()
    result = runner.invoke(
        draw_command,
        [
            "--teams",
            temp_teams_txt_file,
            "--participants",
            temp_participants_txt_file,
            "--delay",
            0,
            "--output-file",
            temp_py_file,
        ],
    )
    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
    assert "Output file must be a .csv or .json file." in result.exception.args[0]
