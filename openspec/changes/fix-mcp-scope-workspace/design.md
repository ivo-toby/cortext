## Context

The MCP server receives `WORKSPACE_PATH` as an environment variable set during registration. This creates a coupling between registration time and runtime that breaks when users work across multiple Cortext workspaces.

**Stakeholders**: All Cortext users with multiple workspaces using Claude Code or Gemini CLI.

## Goals / Non-Goals

**Goals**:
- MCP tools operate in the correct workspace based on AI agent's context
- Zero friction when switching between workspaces
- Simplify MCP registration by removing environment variables

**Non-Goals**:
- Auto-detection magic (explicit is better than implicit)
- Breaking existing RAG tool signatures (they already have workspace_path)

## Decisions

### Decision 1: Optional workspace_path parameter on all tools

**What**: Add `workspace_path` as optional parameter to `search_workspace`, `get_context`, and `get_decision_history`.

**Why**:
- AI agent knows its current working directory
- Explicit control is clearer than environment variable magic
- Consistent with RAG tools that already have this parameter
- Fallback to cwd handles cases where AI doesn't pass it

**Alternatives considered**:
- Auto-detection from cwd/git root: More magic, less explicit
- Required parameter: Too strict, breaks backward compatibility
- Keep WORKSPACE_PATH: Doesn't solve the core problem

### Decision 2: Remove WORKSPACE_PATH from registrations

**What**: MCP registration no longer includes `--env WORKSPACE_PATH=...`

**Why**:
- Registration becomes workspace-agnostic
- No "already exists" conflicts
- Simpler configuration
- Single registration works for all workspaces

### Decision 3: Fallback to cwd when workspace_path not provided

**What**: If AI doesn't pass workspace_path, use `Path.cwd()`

**Why**:
- Graceful degradation
- Works when MCP spawned from workspace directory
- Backward compatibility for tools that don't pass the parameter

## Risks / Trade-offs

- **Risk**: AI doesn't pass workspace_path correctly
  - **Mitigation**: Clear parameter description; cwd fallback usually correct

- **Trade-off**: Slightly more verbose tool calls
  - **Acceptable**: Explicitness is worth the small overhead

## Migration Plan

1. Add workspace_path parameter to core tools (backward compatible)
2. Update registrations to remove WORKSPACE_PATH env
3. Existing registrations with WORKSPACE_PATH still work (cwd fallback)

**Rollback**: If issues arise, can restore WORKSPACE_PATH support as override.

## Open Questions

- None - approach is straightforward
