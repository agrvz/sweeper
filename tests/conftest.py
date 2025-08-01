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
def temp_picks_txt_file(tmp_path: Path):
    temp_file = tmp_path / "picks_txt_file.txt"
    temp_file.write_text("Bengals\nBills\nChiefs")
    yield temp_file


@pytest.fixture
def temp_entrants_txt_file(tmp_path: Path):
    temp_file = tmp_path / "entrants_txt_file.txt"
    temp_file.write_text("Harold\nJim\nMargaret")
    yield temp_file


@pytest.fixture
def temp_picks_csv_file(tmp_path: Path):
    temp_file = tmp_path / "picks_csv_file.csv"
    temp_file.write_text("id,name\n1,Bengals\n2,Bills\n3,Chiefs")
    yield temp_file


@pytest.fixture
def temp_entrants_csv_file(tmp_path: Path):
    temp_file = tmp_path / "entrants_csv_file.csv"
    temp_file.write_text("id,name\n1,Harold\n2,Jim\n3,Margaret")
    yield temp_file


@pytest.fixture
def temp_output_csv_file(tmp_path: Path):
    temp_file = tmp_path / "output_csv_file.csv"
    temp_file.write_text("")
    yield temp_file


@pytest.fixture
def temp_output_json_file(tmp_path: Path):
    temp_file = tmp_path / "output_json_file.json"
    temp_file.write_text("{}")
    yield temp_file
