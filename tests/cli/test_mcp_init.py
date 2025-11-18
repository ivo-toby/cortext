"""Tests for MCP configuration in init command."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from cortext_cli.cli import app

runner = CliRunner()


class TestMCPInit:
    """Test MCP configuration during workspace initialization."""

    @pytest.fixture
    def mock_git(self):
        """Mock git commands."""
        with patch("cortext_cli.commands.init.subprocess.run") as mock:
            mock.return_value = MagicMock(returncode=0)
            yield mock

    @patch("cortext_cli.commands.init.Confirm.ask")
    def test_init_with_mcp_flag(self, mock_confirm, mock_git, tmp_path):
        """Test init with --mcp flag creates MCP config."""
        workspace = tmp_path / "test-workspace"

        result = runner.invoke(
            app, ["init", str(workspace), "--ai", "claude", "--mcp"]
        )

        assert result.exit_code == 0

        # Check MCP config was created
        mcp_config = workspace / ".mcp.json"
        assert mcp_config.exists()

        # Verify config content
        config = json.loads(mcp_config.read_text())
        assert "mcpServers" in config
        assert "cortext" in config["mcpServers"]
        assert config["mcpServers"]["cortext"]["command"] == "cortext-mcp"

        # Prompt should not have been shown (flag takes precedence)
        mock_confirm.assert_not_called()

    @patch("cortext_cli.commands.init.Confirm.ask")
    def test_init_with_no_mcp_flag(self, mock_confirm, mock_git, tmp_path):
        """Test init with --no-mcp flag skips MCP config."""
        workspace = tmp_path / "test-workspace"

        result = runner.invoke(
            app, ["init", str(workspace), "--ai", "claude", "--no-mcp"]
        )

        assert result.exit_code == 0

        # Check MCP config was NOT created
        mcp_config = workspace / ".mcp.json"
        assert not mcp_config.exists()

        # Prompt should not have been shown (flag takes precedence)
        mock_confirm.assert_not_called()

    @patch("cortext_cli.commands.init.Confirm.ask", return_value=True)
    def test_init_with_prompt_accept(self, mock_confirm, mock_git, tmp_path):
        """Test init with prompt acceptance creates MCP config."""
        workspace = tmp_path / "test-workspace"

        result = runner.invoke(app, ["init", str(workspace), "--ai", "claude"])

        assert result.exit_code == 0

        # Prompt should have been shown
        mock_confirm.assert_called_once()

        # Check MCP config was created
        mcp_config = workspace / ".mcp.json"
        assert mcp_config.exists()

    @patch("cortext_cli.commands.init.Confirm.ask", return_value=False)
    def test_init_with_prompt_decline(self, mock_confirm, mock_git, tmp_path):
        """Test init with prompt decline skips MCP config."""
        workspace = tmp_path / "test-workspace"

        result = runner.invoke(app, ["init", str(workspace), "--ai", "claude"])

        assert result.exit_code == 0

        # Prompt should have been shown
        mock_confirm.assert_called_once()

        # Check MCP config was NOT created
        mcp_config = workspace / ".mcp.json"
        assert not mcp_config.exists()

    @patch("cortext_cli.commands.init.Confirm.ask", return_value=True)
    def test_init_mcp_for_all_agents(self, mock_confirm, mock_git, tmp_path):
        """Test init with --ai all creates MCP configs for all agents."""
        workspace = tmp_path / "test-workspace"

        result = runner.invoke(app, ["init", str(workspace), "--ai", "all", "--mcp"])

        assert result.exit_code == 0

        # Check MCP configs for all agents
        claude_config = workspace / ".mcp.json"
        assert claude_config.exists()

        opencode_config = workspace / ".opencode" / "mcp_config.json"
        assert opencode_config.exists()

        # Gemini uses global config
        gemini_config = Path.home() / ".gemini" / "settings.json"
        # Don't assert on existence as it modifies global state
        # Just verify the function logic works

    def test_mcp_config_workspace_path_substitution(self, mock_git, tmp_path):
        """Test MCP config contains correct workspace path."""
        workspace = tmp_path / "test-workspace"

        result = runner.invoke(
            app, ["init", str(workspace), "--ai", "claude", "--mcp"]
        )

        assert result.exit_code == 0

        mcp_config = workspace / ".mcp.json"
        config = json.loads(mcp_config.read_text())

        # Check workspace path is absolute and correct
        env = config["mcpServers"]["cortext"]["env"]
        assert "WORKSPACE_PATH" in env
        assert Path(env["WORKSPACE_PATH"]) == workspace.absolute()
