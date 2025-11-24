# Change: Improve init command performance with progress feedback

## Why

The `cortext init` command takes a long time to run with no progress feedback, creating a poor user experience. Users see a frozen terminal for up to 30 seconds during MCP registration, with no indication of what's happening. This causes confusion and frustration, especially for first-time users.

Root causes:
1. **Slow MCP registration** - `claude mcp add` subprocess with 30-second timeout
2. **No progress indication** - Long operations run without user feedback
3. **Excessive timeout** - 30s is too long for a simple registration command
4. **Blocking CLI calls** - Sequential subprocess calls without parallel execution

## What Changes

### 1. Check for existing MCP installation before prompting
- Check if Cortext MCP is already registered with the agent (e.g., `claude mcp list`)
- If already installed → skip prompt and registration entirely
- If not installed → prompt user and proceed with registration
- Previous change made MCP global, so no local scoping needed

### 2. Add progress feedback during slow operations
- Show spinner/status during MCP registration when it runs
- Use rich's Status context manager for visual feedback
- Display what's happening (e.g., "Registering MCP server with Claude Code...")

### 3. Reduce MCP registration timeout
- Reduce `claude mcp add` timeout from 30s to 10s
- Provide clear error message if timeout occurs
- 10s is sufficient for a local CLI operation

### 4. Optimize subprocess operations
- Cache `which cortext-mcp` result instead of calling for each agent

### 5. Add `--quick` flag for non-interactive fast init
- Skip MCP check and registration in quick mode
- Use `--quick` for CI/scripts that need fast initialization
- MCP can be configured later with `cortext mcp add`

## Impact

- **Affected specs**: `cli-init`
- **Affected code**:
  - `src/cortext_cli/commands/init.py:888-922` (`_install_claude_mcp_config`)
  - `src/cortext_cli/commands/init.py:852-862` (`_check_mcp_command`)
  - `src/cortext_cli/commands/init.py:142-208` (main init workflow)

## Benefits

- **Better UX**: Users see progress and know what's happening
- **Faster init**: Reduced timeout and optimized operations
- **Clear feedback**: Error messages explain what went wrong and how to fix
- **Scriptable**: `--quick` flag enables fast CI/automated use
