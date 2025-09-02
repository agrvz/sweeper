from click.testing import CliRunner

from sweeper.main import sweeper


def test_sweeper():
    runner = CliRunner()
    result = runner.invoke(sweeper)
    assert result.exit_code == 2
    assert "Usage: sweeper" in result.output


def test_sweeper_version():
    runner = CliRunner()
    result = runner.invoke(sweeper, "--version")
    assert result.exit_code == 0
    assert "sweeper, version" in result.output
