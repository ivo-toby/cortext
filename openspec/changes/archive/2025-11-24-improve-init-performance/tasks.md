## 1. Check for Existing MCP Installation

- [x] 1.1 Create `_check_claude_mcp_installed()` function that runs `claude mcp list` and checks for "cortext"
- [x] 1.2 Create `_check_gemini_mcp_installed()` function that checks `~/.gemini/settings.json` for cortext entry
- [x] 1.3 Create `_check_opencode_mcp_installed()` function that checks `.opencode/config.json` for cortext entry
- [x] 1.4 Update `_should_configure_mcp()` to check installation status before prompting
- [x] 1.5 Skip prompt and show "MCP already configured" message when already installed
- [ ] 1.6 Test that existing installations are correctly detected

## 2. Add Progress Feedback

- [x] 2.1 Import rich.status in init.py
- [x] 2.2 Wrap `_install_claude_mcp_config` with Status context showing "Registering MCP server with Claude Code..."
- [x] 2.3 Wrap `_install_gemini_mcp_config` with Status context showing "Configuring MCP for Gemini..."
- [x] 2.4 Wrap `_install_opencode_mcp_config` with Status context showing "Configuring MCP for OpenCode..."
- [ ] 2.5 Test progress indicators display correctly in terminal

## 3. Optimize Timeouts

- [x] 3.1 Reduce `claude mcp add` timeout from 30s to 10s in `_install_claude_mcp_config`
- [x] 3.2 Update error message for timeout to be more informative
- [x] 3.3 Verify 5s timeout is appropriate for `which cortext-mcp` check

## 4. Add Quick Mode Flag

- [x] 4.1 Add `--quick` flag to init command with appropriate help text
- [x] 4.2 When `--quick` is set, skip MCP check and registration entirely
- [x] 4.3 Add message informing user how to configure MCP later when skipped
- [ ] 4.4 Test quick mode works correctly in non-interactive environment

## 5. Cache Command Checks

- [x] 5.1 Cache result of `_check_mcp_command()` at start of configure_mcp
- [x] 5.2 Pass cached result to `_install_mcp_config_for_agent` instead of rechecking
- [x] 5.3 Verify single `which` call per init run

## 6. Testing and Validation

- [ ] 6.1 Manual test: `cortext init` skips MCP prompt when already installed
- [ ] 6.2 Manual test: `cortext init` shows progress feedback when installing MCP
- [ ] 6.3 Manual test: `cortext init --quick` completes without prompts
- [ ] 6.4 Verify timeout error messages are clear and actionable
- [ ] 6.5 Measure init time before/after to confirm improvement
