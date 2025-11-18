# Tasks: Integrate RAG Tools into MCP Server

**Change ID**: integrate-rag-mcp
**Status**: In Progress

## Task List

### Phase 1: MCP Server RAG Tools Integration ✅

- [x] **1.1** Add RAG tool imports to `src/cortext_mcp/server.py`
  - Import `from cortext_rag import mcp_tools`
  - Verify imports work without RAG dependencies error

- [x] **1.2** Add `embed_document` tool to MCP server
  - Add tool definition to `list_tools()` with complete schema
  - Add handler in `call_tool()` to dispatch to `mcp_tools.embed_document()`
  - Test: Call via MCP, verify embedding occurs

- [x] **1.3** Add `embed_workspace` tool to MCP server
  - Add tool definition to `list_tools()`
  - Add handler in `call_tool()`
  - Test: Call via MCP, verify workspace-wide embedding

- [x] **1.4** Add `search_semantic` tool to MCP server
  - Add tool definition with query, filters, limit parameters
  - Add handler in `call_tool()`
  - Test: Call via MCP with various filters, verify results

- [x] **1.5** Add `get_similar` tool to MCP server
  - Add tool definition with source_path parameter
  - Add handler in `call_tool()`
  - Test: Call via MCP, verify similar documents returned

- [x] **1.6** Add `get_embedding_status` tool to MCP server
  - Add tool definition
  - Add handler in `call_tool()`
  - Test: Call via MCP, verify statistics returned

### Phase 2: MCP Agent Registration

- [ ] **2.1** Add `--mcp` and `--no-mcp` flags to init command
  - Add flags to init command signature
  - Store user preference
  - Flags take precedence over prompts

- [ ] **2.2** Add interactive MCP configuration prompt
  - Prompt: "Configure MCP server for AI agents? (Y/n)"
  - Only show if flags not provided
  - Default to "Y" (user can just press Enter)
  - On decline, show message about `cortext mcp install`

- [ ] **2.3** Create MCP config template
  - Create `templates/mcp_config.json` with placeholder
  - Support `{{WORKSPACE_PATH}}` substitution

- [ ] **2.4** Add `install_mcp_config()` function to init.py
  - Check user preference (flags or prompt)
  - Skip if `--no-mcp` or user declined
  - Check if `cortext-mcp` command exists
  - Read MCP config template
  - Substitute workspace path
  - Write to agent-specific location

- [ ] **2.5** Integrate MCP config into Claude initialization
  - Call `install_mcp_config()` after `configure_ai_tools()`
  - Create `.claude/mcp_config.json` (workspace-local)
  - Add success message to tracker

- [ ] **2.6** Integrate MCP config into Gemini initialization
  - Merge config into `~/.gemini/settings.json` (global)
  - Preserve existing settings
  - Create settings.json if doesn't exist
  - Add mcpServers.cortext entry with workspace path

- [ ] **2.7** Integrate MCP config into OpenCode initialization
  - Create `.opencode/mcp_config.json` (workspace-local)
  - Consider integration with AGENT_CONFIG.toml

- [ ] **2.8** Add MCP config validation
  - Check `cortext-mcp` in PATH before creating configs
  - Log warnings if command not found
  - Provide installation instructions
  - Still create configs (for future use)

### Phase 3: MCP Install Command

- [ ] **3.1** Create `src/cortext_cli/commands/mcp.py`
  - Create typer app for MCP commands
  - Add to CLI in `cli.py`

- [ ] **3.2** Implement `cortext mcp install` command
  - Add command signature with `--ai` and `--force` options
  - Verify in Cortext workspace
  - Detect configured agents from directories
  - Filter by `--ai` flag if provided

- [ ] **3.3** Add agent detection logic
  - Check for `.claude/commands/` → Claude configured
  - Check for `.gemini/commands/` → Gemini configured
  - Check for `.opencode/command/` → OpenCode configured
  - Return list of configured agents

- [ ] **3.4** Implement MCP config installation per agent
  - Reuse `install_mcp_config()` logic from init
  - Check if config already exists
  - Skip if exists and no `--force`
  - Create/update if `--force` or doesn't exist

- [ ] **3.5** Add Gemini settings.json merge logic
  - Read existing `~/.gemini/settings.json`
  - Merge mcpServers.cortext entry
  - Preserve other settings
  - Create file if doesn't exist

- [ ] **3.6** Add clear output messages
  - Show which agents were configured
  - Show config file paths
  - Warn if cortext-mcp not in PATH
  - Suggest how to test

### Phase 4: Testing

- [ ] **4.1** Unit tests for MCP RAG tool handlers
  - Mock `mcp_tools` functions
  - Test each tool handler in isolation
  - Verify error handling

- [ ] **4.2** Integration tests for MCP protocol
  - Start MCP server
  - Call each RAG tool via stdio MCP protocol
  - Verify responses match schema

- [ ] **4.3** Unit tests for init MCP flags
  - Test `--mcp` flag creates config
  - Test `--no-mcp` flag skips config
  - Test flags take precedence over prompts

- [ ] **4.4** Unit tests for `install_mcp_config()`
  - Test config file creation
  - Test path substitution
  - Test skipping existing configs
  - Test Gemini settings.json merge

- [ ] **4.5** Unit tests for `cortext mcp install`
  - Test agent detection
  - Test `--ai` flag filtering
  - Test `--force` flag
  - Test Gemini merge logic

- [ ] **4.6** E2E test with Claude Code
  - Initialize workspace with `--ai claude --mcp`
  - Start Claude in workspace
  - Verify Claude can call `search_semantic`
  - Verify results returned correctly

- [ ] **4.7** E2E test with Gemini CLI
  - Initialize workspace with `--ai gemini --mcp`
  - Verify `~/.gemini/settings.json` updated
  - Test with Gemini CLI (if available)

- [ ] **4.8** E2E test with `mcp install` command
  - Initialize workspace with `--no-mcp`
  - Run `cortext mcp install`
  - Verify MCP config created
  - Test agent can use tools

- [ ] **4.9** E2E test with semantic search workflow
  - Create test workspace with conversations
  - Embed via MCP `embed_workspace` tool
  - Search via MCP `search_semantic` tool
  - Verify relevant results returned

### Phase 5: Documentation

- [ ] **5.1** Update `Docs/mcp-server.md`
  - Document all 5 new RAG tools with schemas
  - Include example tool calls
  - Add troubleshooting section for RAG tools
  - Document Gemini CLI configuration

- [ ] **5.2** Update `Docs/rag-guide.md`
  - Add section on using RAG via MCP
  - Include agent examples (Claude, Gemini, OpenCode)
  - Explain automatic vs manual configuration
  - Link to MCP server docs

- [ ] **5.3** Update README.md MCP section
  - Mention RAG tools available via MCP
  - Note automatic configuration during init
  - Mention `--mcp` / `--no-mcp` flags
  - Link to `cortext mcp install` command

- [ ] **5.4** Document `cortext mcp install` command
  - Add to CLI reference docs
  - Include usage examples
  - Explain when to use (skipped during init, existing workspace)

- [ ] **5.5** Add MCP+RAG examples
  - Create example: "Ask Claude to find similar conversations"
  - Create example: "Search across workspace semantically"
  - Create example: "Use mcp install to add MCP later"
  - Add to user guide

### Phase 6: Polish & Release

- [ ] **6.1** Handle edge cases
  - Empty workspace (no embeddings)
  - Large workspace (performance)
  - Concurrent MCP calls
  - Multiple workspaces with same agent

- [ ] **6.2** Add logging for MCP RAG tools
  - Log tool calls for debugging
  - Track usage patterns

- [ ] **6.3** Update changelog
  - Document new MCP RAG tools
  - Document auto-MCP configuration
  - Document `cortext mcp install` command
  - Note Gemini CLI support

- [ ] **6.4** Version bump and release
  - Increment version to 0.2.0
  - Tag release
  - Update package metadata

---

## Dependencies

**Blocked By:**
- None (all dependencies complete)

**Blocks:**
- Future advanced RAG features (context injection, timeline queries)

---

## Validation Criteria

Each task complete when:
- Code changes implemented
- Tests passing
- Documentation updated
- Manual verification successful

Overall change complete when:
- All tasks marked done
- `openspec validate integrate-rag-mcp --strict` passes
- E2E test with Claude Code successful
- User can search semantically via MCP without manual config

---

## Estimated Effort

- **Phase 1**: 4 hours (straightforward tool additions)
- **Phase 2**: 8 hours (flags, prompts, multi-agent config)
- **Phase 3**: 6 hours (mcp install command + logic)
- **Phase 4**: 6 hours (expanded test coverage)
- **Phase 5**: 4 hours (comprehensive documentation)
- **Phase 6**: 2 hours (polish)

**Total**: ~30 hours over 5-7 days

---

## Notes

- Most complex part is researching correct MCP config format for Gemini/OpenCode
- RAG tools themselves are already implemented and tested
- Focus on clean MCP integration, not RAG functionality
- Consider starting with Claude-only support, add others incrementally
