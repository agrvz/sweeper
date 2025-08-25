from pathlib import Path

import click
from click.testing import CliRunner

from sweeper.option_required_if import OptionRequiredIf


def test_option_required_if():
    @click.command()
    @click.option("--type", type=click.Choice(["json", "csv"]), default="json")
    @click.option(
        "--column",
        type=click.STRING,
        cls=OptionRequiredIf,
        required_if_option="type",
        required_if_value="csv",
    )
    def cli(type, column=None):
        click.echo(f"type:[{type}], column:[{column}]")

    runner = CliRunner()
    result = runner.invoke(cli, ["--type", "json"])
    assert not result.exception
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, ["--type", "csv"])
    assert result.exception
    assert result.exit_code != 0
    assert "Required if --type=csv" in result.output

    runner = CliRunner()
    result = runner.invoke(cli, ["--type", "csv", "--column", "a"])
    assert not result.exception
    assert result.exit_code == 0


def test_option_required_if_operation():
    @click.command()
    @click.option("--path", type=click.Path(exists=False))
    @click.option(
        "--column",
        type=click.STRING,
        cls=OptionRequiredIf,
        required_if_option="path",
        required_if_value=".csv",
        required_if_option_op=lambda x: x.suffix,
    )
    def cli(path, column=None):
        click.echo(f"path:[{path}], column:[{column}]")

    runner = CliRunner()
    result = runner.invoke(cli, ["--path", Path("file.json")])
    assert not result.exception
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, ["--path", Path("file.csv"), "--column", "a"])
    assert not result.exception
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, ["--path", Path("file.csv")])
    assert result.exception
    assert result.exit_code != 0
    assert "Required if <lambda>(--path)=.csv" in result.output

