from pathlib import Path
from click.testing import CliRunner
from cli import cli
import toml

def test_input_file_basic(tmp_path, mocker):
    """Test basic loading of URLs from an input file."""
    mock_scrape_async = mocker.AsyncMock(return_value=None)
    mocker.patch("cli.scrape_async", new=mock_scrape_async)

    urls_content = """
http://file-url1.com
http://file-url2.com
"""
    input_file = tmp_path / "urls.txt"
    input_file.write_text(urls_content)

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "--input-file", str(input_file), "-s", "h1"])

    assert result.exit_code == 0
    mock_scrape_async.assert_called_once_with(("http://file-url1.com", "http://file-url2.com"), "h1", "text", 50)
def test_input_file_cli_precedence(tmp_path, mocker):
    """Test that CLI arguments for URLs take precedence over input file URLs."""
    mock_scrape_async = mocker.AsyncMock(return_value=None)
    mocker.patch("cli.scrape_async", new=mock_scrape_async)

    urls_content = """
http://file-url1.com
"""
    input_file = tmp_path / "urls.txt"
    input_file.write_text(urls_content)

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "--input-file", str(input_file), "-s", "h1", "http://cli-url.com"])

    assert result.exit_code == 0
    mock_scrape_async.assert_called_once_with(("http://cli-url.com",), "h1", "text", 50)
def test_input_file_config_precedence(tmp_path, mocker):
    """Test that input file URLs take precedence over config file URLs."""
    mock_scrape_async = mocker.AsyncMock(return_value=None)
    mocker.patch("cli.scrape_async", new=mock_scrape_async)

    urls_content = """
http://file-url-only.com
"""
    input_file = tmp_path / "urls.txt"
    input_file.write_text(urls_content)

    config_content = """
[scrape]
urls = ["http://config-url-only.com"]
selector = "h2"
"""
    config_file = tmp_path / "test_config.toml"
    config_file.write_text(config_content)

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "--input-file", str(input_file), "--config", str(config_file)])

    assert result.exit_code == 0
    mock_scrape_async.assert_called_once_with(("http://file-url-only.com",), "h2", "text", 50)
def test_input_file_missing_selector(tmp_path, mocker):
    """Test error when selector is missing with input file."""
    mocker.patch("cli.asyncio.run", autospec=True)
    mocker.patch("rust_scraper.scrape_urls_concurrent", new=mocker.AsyncMock(return_value=([], [])))

    urls_content = """
http://file-url.com
"""
    input_file = tmp_path / "urls.txt"
    input_file.write_text(urls_content)

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "--input-file", str(input_file)])

    assert result.exit_code != 0
    assert "Error: Missing option '--selector'" in result.stderr

def test_input_file_empty_file(tmp_path, mocker):
    """Test error when input file is empty and no other URLs provided."""
    mocker.patch("cli.asyncio.run", autospec=True)
    mocker.patch("rust_scraper.scrape_urls_concurrent", new=mocker.AsyncMock(return_value=([], [])))

    input_file = tmp_path / "empty.txt"
    input_file.write_text("")

    runner = CliRunner()
    result = runner.invoke(cli, ["scrape", "--input-file", str(input_file), "-s", "h1"])

    assert result.exit_code != 0
    assert "Please provide at least one URL to scrape" in result.stderr

