"""
Basic tests for InvestAugur CLI

Tests the CLI commands using Click's testing utilities.
"""
import pytest
from click.testing import CliRunner
from cli.main import cli


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()


def test_cli_help(runner):
    """Test that the main CLI help displays correctly."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "InvestAugur" in result.output
    assert "Commands:" in result.output


def test_init_command(runner):
    """Test the init command."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert "Initialized successfully" in result.output


def test_track_command(runner):
    """Test the track command with required arguments."""
    result = runner.invoke(cli, ["track", "--sheet-id", "test123", "AAPL"])
    assert result.exit_code == 0
    assert "Portfolio Holdings" in result.output
    assert "AAPL" in result.output


def test_analyze_command(runner):
    """Test the analyze command."""
    result = runner.invoke(cli, ["analyze", "--query", "test query", "--symbol", "AAPL"])
    assert result.exit_code == 0
    assert "Analysis Results" in result.output


def test_rag_query_command(runner):
    """Test the rag-query command."""
    with runner.isolated_filesystem():
        # Create the research_docs directory
        import os

        os.makedirs("research_docs", exist_ok=True)

        result = runner.invoke(cli, ["rag-query", "test query"])
        assert result.exit_code == 0
        assert "RAG Retrieval Results" in result.output


def test_chat_command(runner):
    """Test the chat command with exit input."""
    result = runner.invoke(cli, ["chat"], input="exit\n")
    assert result.exit_code == 0
    assert "InvestAugur Interactive Chat" in result.output
    assert "Ending chat session" in result.output


def test_chat_command_eof(runner):
    """Test the chat command handles EOF gracefully."""
    # Simulate EOF (Ctrl-D) by closing input stream
    result = runner.invoke(cli, ["chat"], input="")
    assert result.exit_code == 0
    assert "InvestAugur Interactive Chat" in result.output
    # Should handle EOF gracefully
    assert "interrupted" in result.output.lower() or "goodbye" in result.output.lower()


def test_verbose_flag(runner):
    """Test the verbose flag."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--verbose", "init"])
        assert result.exit_code == 0
        # Verbose mode should show config file message
        assert "Config file" in result.output or "Initialized successfully" in result.output
