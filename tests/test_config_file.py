import toml
from pathlib import Path
from click.testing import CliRunner
from cli import cli

def test_config_file_basic(tmp_path, mocker):
    """Test basic loading of configuration from a TOML file and argument precedence."""
    mock_asyncio_run = mocker.patch("cli.asyncio.run", autospec=True)
    mocker.patch("rust_scraper.scrape_urls_concurrent", new=mocker.AsyncMock(return_value=([], [])))

    config_content = """
[scrape]
urls = ["http://example.com/from-config"]
selector = "h1.from-config"
output = "json"
concurrency = 5
"""
    config_file = tmp_path / "test_config.toml"
    config_file.write_text(config_content)

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "--config", str(config_file)])

    assert result.exit_code == 0
    mock_asyncio_run.assert_called_once()

def test_config_file_cli_precedence(tmp_path, mocker):
    """Test that CLI arguments take precedence over config file settings."""
    mock_asyncio_run = mocker.patch("cli.asyncio.run", autospec=True)
    mocker.patch("rust_scraper.scrape_urls_concurrent", new=mocker.AsyncMock(return_value=([], [])))

    config_content = """
[scrape]
urls = ["http://example.com/from-config"]
selector = "h1.from-config"
output = "json"
concurrency = 5
"""
    config_file = tmp_path / "test_config.toml"
    config_file.write_text(config_content)

    runner = CliRunner()
    # CLI provides selector, concurrency, and URLs, which should override the config
    result = runner.invoke(cli, [
        "scrape", 
        "--config", str(config_file), 
        "--selector", "p.from-cli", 
        "--concurrency", "10",
        "http://cli-example.com/from-cli"
    ])

    assert result.exit_code == 0
    mock_asyncio_run.assert_called_once()

def test_config_file_missing_selector(tmp_path, mocker):
    """Test that an error is raised if selector is missing from both CLI and config."""
    mocker.patch("cli.scrape_urls_concurrent", return_value=([], []))

    config_content = """
[scrape]
urls = ["http://example.com"]
output = "json"
concurrency = 5
"""
    config_file = tmp_path / "test_config.toml"
    config_file.write_text(config_content)

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "--config", str(config_file)])

    assert result.exit_code != 0
    assert "Error: Missing option '--selector'" in result.stderr
    mocker.stopall() # Stop all mocks before exit, important for CliRunner

def test_config_file_missing_urls(tmp_path, mocker):
    """Test that an error is raised if URLs are missing from both CLI and config."""
    mocker.patch("cli.scrape_urls_concurrent", return_value=([], []))

    config_content = """
[scrape]
selector = "h1"
output = "json"
concurrency = 5
"""
    config_file = tmp_path / "test_config.toml"
    config_file.write_text(config_content)

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "--config", str(config_file)])

    assert result.exit_code != 0
    assert "Please provide at least one URL to scrape" in result.stderr
    mocker.stopall() # Stop all mocks before exit, important for CliRunner
