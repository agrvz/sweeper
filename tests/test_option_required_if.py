from pathlib import Path

import click
import pytest
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


def test_option_required_if_value_transform_missing_value():
    """
    Test that required_if_value must be passed if
    required_if_value_transform is provided.
    """
    with pytest.raises(AssertionError):

        @click.command()
        @click.option("--name", type=click.STRING)
        @click.option(
            "--abbrev",
            type=click.STRING,
            cls=OptionRequiredIf,
            required_if_option="name",
            required_if_value_transform=sum,
        )
        def cli(name, abbrev=None):
            click.echo(f"name:[{name}], abbrev:[{abbrev}]")


def test_option_required_if_value_transform():
    def upper_case(x: str) -> str:
        return x.upper()

    @click.command()
    @click.option("--name", type=click.STRING)
    @click.option(
        "--abbrev",
        type=click.STRING,
        cls=OptionRequiredIf,
        required_if_option="name",
        required_if_value="TOM",
        required_if_value_transform=upper_case,
    )
    def cli(name, abbrev=None):
        click.echo(f"name:[{name}], abbrev:[{abbrev}]")

    runner = CliRunner()
    result = runner.invoke(cli, ["--name", "sam"])
    assert not result.exception
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, ["--name", "tom", "--abbrev", "t"])
    assert not result.exception
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, ["--name", "tom"])
    assert result.exception
    assert result.exit_code != 0
    assert "Required if upper_case(--name)=TOM" in result.output


def test_option_required_if_value_transform_lambda():
    @click.command()
    @click.option("--path", type=click.Path(exists=False))
    @click.option(
        "--column",
        type=click.STRING,
        cls=OptionRequiredIf,
        required_if_option="path",
        required_if_value=".csv",
        required_if_value_transform=lambda x: x.suffix,
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


def test_option_required_if_value_check():
    def longer_than_5(x: str) -> bool:
        return len(x) > 5

    @click.command()
    @click.option("--name", type=click.STRING)
    @click.option(
        "--abbrev",
        type=click.STRING,
        cls=OptionRequiredIf,
        required_if_option="name",
        required_if_value_check=longer_than_5,
    )
    def cli(name, abbrev=None):
        click.echo(f"name:[{name}], abbrev:[{abbrev}]")

    runner = CliRunner()
    result = runner.invoke(cli, ["--name", "abc"])
    assert not result.exception
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, ["--name", "abcdefg", "--abbrev", "ab"])
    assert not result.exception
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, ["--name", "abcdefg"])
    assert result.exception
    assert result.exit_code != 0
    assert "Required if longer_than_5(--name) is True" in result.output


def test_option_required_if_no_value():
    """
    Test that an option is required if another option is passed, regardless of
    its value - i.e. if only required_if_option is provided to OptionRequiredIf.
    """

    @click.command()
    @click.option("--name", type=click.STRING)
    @click.option(
        "--abbrev",
        type=click.STRING,
        cls=OptionRequiredIf,
        required_if_option="name",
    )
    def cli(name, abbrev=None):
        click.echo(f"name:[{name}], abbrev:[{abbrev}]")

    runner = CliRunner()
    result = runner.invoke(cli, ["--name", "abc"])
    assert result.exception
    assert result.exit_code != 0
    assert "Required if --name is passed" in result.output
