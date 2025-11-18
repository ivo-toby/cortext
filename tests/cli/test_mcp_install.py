"""Tests for cortext mcp install command."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from cortext_cli.cli import app

runner = CliRunner()


class TestMCPInstall:
    """Test mcp install command."""

    @pytest.fixture
    def workspace(self, tmp_path):
        """Create test workspace with agents configured."""
        ws = tmp_path / "workspace"
        ws.mkdir()

        # Create workspace structure
        workspace_dir = ws / ".workspace"
        workspace_dir.mkdir()

        registry = {
            "version": "1.0",
            "conversation_types": {"brainstorm": {"folder": "brainstorm"}},
        }
        (workspace_dir / "registry.json").write_text(json.dumps(registry))

        # Configure Claude
        claude_dir = ws / ".claude" / "commands"
        claude_dir.mkdir(parents=True)

        # Configure Gemini
        gemini_dir = ws / ".gemini" / "commands"
        gemini_dir.mkdir(parents=True)

        return ws

    def test_mcp_install_not_in_workspace(self, tmp_path):
        """Test mcp install fails outside workspace."""
        with patch("cortext_cli.commands.mcp.Path.cwd", return_value=tmp_path):
            result = runner.invoke(app, ["mcp", "install"])

        assert result.exit_code == 1
        assert "Not in a Cortext workspace" in result.stdout

    def test_mcp_install_no_agents(self, tmp_path):
        """Test mcp install when no agents are configured."""
        # Create workspace but no agent dirs
        workspace_dir = tmp_path / ".workspace"
        workspace_dir.mkdir()

        registry = {"version": "1.0", "conversation_types": {}}
        (workspace_dir / "registry.json").write_text(json.dumps(registry))

        with patch("cortext_cli.commands.mcp.Path.cwd", return_value=tmp_path):
            result = runner.invoke(app, ["mcp", "install"])

        assert result.exit_code == 0
        assert "No AI agents detected" in result.stdout

    def test_mcp_install_all_agents(self, workspace):
        """Test mcp install for all detected agents."""
        with patch("cortext_cli.commands.mcp.Path.cwd", return_value=workspace):
            result = runner.invoke(app, ["mcp", "install"])

        assert result.exit_code == 0

        # Check configs were created
        claude_config = workspace / ".mcp.json"
        assert claude_config.exists()

        # Verify config content
        config = json.loads(claude_config.read_text())
        assert "mcpServers" in config
        assert config["mcpServers"]["cortext"]["command"] == "cortext-mcp"

    def test_mcp_install_specific_agent(self, workspace):
        """Test mcp install --ai claude."""
        with patch("cortext_cli.commands.mcp.Path.cwd", return_value=workspace):
            result = runner.invoke(app, ["mcp", "install", "--ai", "claude"])

        assert result.exit_code == 0

        # Check only Claude config was created
        claude_config = workspace / ".mcp.json"
        assert claude_config.exists()

    def test_mcp_install_preserves_existing(self, workspace):
        """Test mcp install preserves existing configs."""
        # Create existing config
        claude_config = workspace / ".mcp.json"
        claude_config.write_text('{"existing": "config"}')

        with patch("cortext_cli.commands.mcp.Path.cwd", return_value=workspace):
            result = runner.invoke(app, ["mcp", "install"])

        assert result.exit_code == 0
        assert "already configured" in result.stdout

        # Check config was not overwritten
        config = json.loads(claude_config.read_text())
        assert "existing" in config

    def test_mcp_install_force_overwrites(self, workspace):
        """Test mcp install --force overwrites existing configs."""
        # Create existing config
        claude_config = workspace / ".mcp.json"
        claude_config.write_text('{"existing": "config"}')

        with patch("cortext_cli.commands.mcp.Path.cwd", return_value=workspace):
            result = runner.invoke(app, ["mcp", "install", "--force"])

        assert result.exit_code == 0

        # Check config was overwritten
        config = json.loads(claude_config.read_text())
        assert "existing" not in config
        assert "mcpServers" in config

    def test_mcp_install_invalid_agent(self, workspace):
        """Test mcp install with invalid agent name."""
        with patch("cortext_cli.commands.mcp.Path.cwd", return_value=workspace):
            result = runner.invoke(app, ["mcp", "install", "--ai", "invalid"])

        assert result.exit_code == 1
        assert "not found in workspace" in result.stdout

    def test_agent_detection(self, workspace):
        """Test agent detection logic."""
        from cortext_cli.commands.mcp import _detect_configured_agents

        agents = _detect_configured_agents(workspace)

        assert "claude" in agents
        assert "gemini" in agents
        assert "opencode" not in agents  # Not configured

    @patch("cortext_cli.commands.mcp._check_mcp_command", return_value=False)
    def test_mcp_install_warns_if_command_missing(self, mock_check, workspace):
        """Test warning when cortext-mcp command not found."""
        with patch("cortext_cli.commands.mcp.Path.cwd", return_value=workspace):
            result = runner.invoke(app, ["mcp", "install"])

        assert result.exit_code == 0
        assert "cortext-mcp command not found" in result.stdout
