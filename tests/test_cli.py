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

def test_cli_network_error_reporting(mocker):
    """Test that network errors from Rust core are reported correctly."""
    mocker.patch("cli.scrape_async", side_effect=Exception("Network error: Host not found"))

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "http://test.com", "-s", "h1"])

    assert result.exit_code == 1
    assert "Network Error: Host not found" in result.stderr

def test_cli_http_error_reporting(mocker):
    """Test that HTTP errors from Rust core are reported correctly."""
    mocker.patch("cli.scrape_async", side_effect=Exception("HTTP Status Error: 404 Not Found"))

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "http://test.com", "-s", "h1"])

    assert result.exit_code == 1
    assert "HTTP Error: 404 Not Found" in result.stderr

def test_cli_runtime_error_reporting(mocker):
    """Test that generic runtime errors from Rust core are reported correctly."""
    mocker.patch("cli.scrape_async", side_effect=Exception("Runtime Error: Internal Rust error"))

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "http://test.com", "-s", "h1"])

    assert result.exit_code == 1
    assert "Runtime Error: An unexpected error occurred in the Rust core. Details: Internal Rust error" in result.stderr
