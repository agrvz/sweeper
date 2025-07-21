from pathlib import Path

import pytest


@pytest.fixture
def temp_txt_file(tmp_path: Path):
    temp_file = tmp_path / "temp_txt_file.txt"
    temp_file.write_text("")
    yield temp_file


@pytest.fixture
def temp_csv_file(tmp_path: Path):
    temp_file = tmp_path / "temp_csv_file.csv"
    temp_file.write_text("")
    yield temp_file


@pytest.fixture
def temp_py_file(tmp_path: Path):
    temp_file = tmp_path / "temp_py_file.py"
    temp_file.write_text("")
    yield temp_file


@pytest.fixture
def temp_teams_txt_file(tmp_path: Path):
    temp_file = tmp_path / "teams_txt_file.txt"
    temp_file.write_text("Bengals\nBills\nChiefs")
    yield temp_file


@pytest.fixture
def temp_participants_txt_file(tmp_path: Path):
    temp_file = tmp_path / "participants_txt_file.txt"
    temp_file.write_text("Harold\nJim\nMargaret")
    yield temp_file


@pytest.fixture
def temp_teams_csv_file(tmp_path: Path):
    temp_file = tmp_path / "teams_csv_file.csv"
    temp_file.write_text("id,name\n1,Bengals\n2,Bills\n3,Chiefs")
    yield temp_file


@pytest.fixture
def temp_participants_csv_file(tmp_path: Path):
    temp_file = tmp_path / "participants_csv_file.csv"
    temp_file.write_text("id,name\n1,Harold\n2,Jim\n3,Margaret")
    yield temp_file
