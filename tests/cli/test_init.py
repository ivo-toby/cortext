"""Tests for init command."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestInitCommand:
    """Tests for workspace initialization."""

    def test_create_workspace_structure(self, tmp_path):
        """Test that workspace structure is created correctly."""
        from cortext_cli.commands.init import create_workspace_structure
        from cortext_cli.utils import StepTracker

        tracker = StepTracker("Test")
        create_workspace_structure(tmp_path, tracker)

        # Check core directories exist
        assert (tmp_path / ".workspace" / "memory").exists()
        assert (tmp_path / ".workspace" / "scripts" / "bash").exists()
        assert (tmp_path / ".workspace" / "scripts" / "powershell").exists()
        assert (tmp_path / ".workspace" / "templates").exists()
        assert (tmp_path / ".workspace" / "exports").exists()
        assert (tmp_path / "research").exists()
        assert (tmp_path / "ideas").exists()
        assert (tmp_path / "notes").exists()
        assert (tmp_path / "projects").exists()

    def test_create_registry(self, tmp_path):
        """Test that registry is created with correct structure."""
        from cortext_cli.commands.init import create_workspace_structure, create_registry
        from cortext_cli.utils import StepTracker

        tracker = StepTracker("Test")
        create_workspace_structure(tmp_path, tracker)
        registry = create_registry(tmp_path, tracker)

        # Check registry file exists
        registry_path = tmp_path / ".workspace" / "registry.json"
        assert registry_path.exists()

        # Check registry structure
        assert "version" in registry
        assert "conversation_types" in registry
        assert "brainstorm" in registry["conversation_types"]
        assert "debug" in registry["conversation_types"]
        assert "plan" in registry["conversation_types"]
        assert "learn" in registry["conversation_types"]
        assert "meeting" in registry["conversation_types"]
        assert "review" in registry["conversation_types"]

    def test_create_conversation_type_folders(self, tmp_path):
        """Test that conversation type folders are created."""
        from cortext_cli.commands.init import (
            create_workspace_structure,
            create_registry,
            create_conversation_type_folders,
        )
        from cortext_cli.utils import StepTracker

        tracker = StepTracker("Test")
        create_workspace_structure(tmp_path, tracker)
        registry = create_registry(tmp_path, tracker)
        create_conversation_type_folders(tmp_path, registry, tracker)

        # Check folders exist
        assert (tmp_path / "brainstorm").exists()
        assert (tmp_path / "debug").exists()
        assert (tmp_path / "plan").exists()
        assert (tmp_path / "learn").exists()
        assert (tmp_path / "meeting").exists()
        assert (tmp_path / "review").exists()

        # Check .gitkeep files
        assert (tmp_path / "brainstorm" / ".gitkeep").exists()

    def test_create_constitution(self, tmp_path):
        """Test that constitution files are created."""
        from cortext_cli.commands.init import create_workspace_structure, create_constitution
        from cortext_cli.utils import StepTracker

        tracker = StepTracker("Test")
        create_workspace_structure(tmp_path, tracker)
        create_constitution(tmp_path, tracker)

        # Check files exist
        memory_dir = tmp_path / ".workspace" / "memory"
        assert (memory_dir / "constitution.md").exists()
        assert (memory_dir / "context.md").exists()
        assert (memory_dir / "decisions.md").exists()

        # Check content
        constitution = (memory_dir / "constitution.md").read_text()
        assert "Personal Constitution" in constitution
        assert "Communication Style" in constitution

    def test_is_path_like(self):
        """Test path detection logic."""
        from cortext_cli.commands.init import is_path_like

        # Should be detected as paths
        assert is_path_like(".") is True
        assert is_path_like("..") is True
        assert is_path_like("./foo") is True
        assert is_path_like("../bar") is True
        assert is_path_like("/absolute/path") is True
        assert is_path_like("~/home/path") is True
        assert is_path_like("path/with/slashes") is True

        # Should be detected as names
        assert is_path_like("myworkspace") is False
        assert is_path_like("ai-project") is False
        assert is_path_like("workspace123") is False


class TestGitHookInstallation:
    """Tests for git hook installation."""

    def test_install_git_hooks_creates_post_commit(self, tmp_path):
        """Test that post-commit hook is installed."""
        from cortext_cli.commands.init import install_git_hooks
        from cortext_cli.utils import StepTracker

        # Create git directory structure
        git_hooks_dir = tmp_path / ".git" / "hooks"
        git_hooks_dir.mkdir(parents=True)

        # Create source hook directory with post-commit
        with patch("cortext_cli.commands.init.get_git_hooks_dir") as mock_get_hooks:
            src_hooks = tmp_path / "src_hooks"
            src_hooks.mkdir()
            post_commit = src_hooks / "post-commit"
            post_commit.write_text("#!/usr/bin/env bash\ncortext embed --all")
            mock_get_hooks.return_value = src_hooks

            tracker = StepTracker("Test")
            install_git_hooks(tmp_path, tracker)

        # Check hook was installed
        installed_hook = git_hooks_dir / "post-commit"
        assert installed_hook.exists()
        assert "cortext embed" in installed_hook.read_text()

    def test_install_git_hooks_preserves_existing(self, tmp_path):
        """Test that existing hooks are preserved and appended."""
        from cortext_cli.commands.init import install_git_hooks
        from cortext_cli.utils import StepTracker

        # Create git directory with existing hook
        git_hooks_dir = tmp_path / ".git" / "hooks"
        git_hooks_dir.mkdir(parents=True)
        existing_hook = git_hooks_dir / "post-commit"
        existing_hook.write_text("#!/usr/bin/env bash\necho 'existing hook'")

        # Create source hook
        with patch("cortext_cli.commands.init.get_git_hooks_dir") as mock_get_hooks:
            src_hooks = tmp_path / "src_hooks"
            src_hooks.mkdir()
            post_commit = src_hooks / "post-commit"
            post_commit.write_text("cortext embed --all")
            mock_get_hooks.return_value = src_hooks

            tracker = StepTracker("Test")
            install_git_hooks(tmp_path, tracker)

        # Check both hooks are present
        hook_content = existing_hook.read_text()
        assert "existing hook" in hook_content
        assert "cortext embed" in hook_content

    def test_install_git_hooks_skips_if_already_present(self, tmp_path):
        """Test that hook is not duplicated if already present."""
        from cortext_cli.commands.init import install_git_hooks
        from cortext_cli.utils import StepTracker

        # Create git directory with hook that already has cortext
        git_hooks_dir = tmp_path / ".git" / "hooks"
        git_hooks_dir.mkdir(parents=True)
        existing_hook = git_hooks_dir / "post-commit"
        existing_hook.write_text("#!/usr/bin/env bash\ncortext embed --all")

        # Create source hook
        with patch("cortext_cli.commands.init.get_git_hooks_dir") as mock_get_hooks:
            src_hooks = tmp_path / "src_hooks"
            src_hooks.mkdir()
            post_commit = src_hooks / "post-commit"
            post_commit.write_text("cortext embed --all")
            mock_get_hooks.return_value = src_hooks

            tracker = StepTracker("Test")
            install_git_hooks(tmp_path, tracker)

        # Check hook is not duplicated
        hook_content = existing_hook.read_text()
        assert hook_content.count("cortext embed") == 1

    def test_install_git_hooks_handles_missing_git_dir(self, tmp_path):
        """Test graceful handling when .git/hooks doesn't exist."""
        from cortext_cli.commands.init import install_git_hooks
        from cortext_cli.utils import StepTracker

        # No .git directory
        with patch("cortext_cli.commands.init.get_git_hooks_dir") as mock_get_hooks:
            src_hooks = tmp_path / "src_hooks"
            src_hooks.mkdir()
            mock_get_hooks.return_value = src_hooks

            tracker = StepTracker("Test")
            # Should not raise an error
            install_git_hooks(tmp_path, tracker)

    def test_install_git_hooks_handles_missing_source(self, tmp_path):
        """Test graceful handling when source hooks don't exist."""
        from cortext_cli.commands.init import install_git_hooks
        from cortext_cli.utils import StepTracker

        # Create git directory
        git_hooks_dir = tmp_path / ".git" / "hooks"
        git_hooks_dir.mkdir(parents=True)

        with patch("cortext_cli.commands.init.get_git_hooks_dir") as mock_get_hooks:
            # Point to non-existent directory
            mock_get_hooks.return_value = tmp_path / "nonexistent"

            tracker = StepTracker("Test")
            # Should not raise an error
            install_git_hooks(tmp_path, tracker)
