import subprocess
from click.testing import CliRunner
from cli import cli

def test_cli_help():
    """Verify that the 'pyru --help' command executes successfully using CliRunner."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in result.stdout
    assert "Options:" in result.stdout
    assert "Commands:" in result.stdout
