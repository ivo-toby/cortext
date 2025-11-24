## Context

Cortext conversations are currently fire-and-forget from the agent's perspective. While the markdown file captures ideas and outcomes, the conversational context (what was asked, what tools were used, what the agent's instructions were) is lost when the session ends.

This design addresses: How do we persist and restore full agent context for conversation resumption?

### Constraints
- Must work with Claude Code, OpenCode, and Gemini CLI
- Cannot modify how AI tools handle their internal state
- Must be git-friendly (no binary blobs)
- Should not bloat repository with excessive history

### Stakeholders
- Users who want to continue conversations over multiple sessions
- AI agents that need context to provide coherent continuation
- Workspace tooling that needs to manage session lifecycle

## Goals / Non-Goals

### Goals
- Persist conversation context so agents can resume with full awareness
- Provide intuitive UX for finding and resuming conversations
- Support all existing conversation types (brainstorm, debug, plan, learn, etc.)
- Keep storage format human-readable and git-diff friendly

### Non-Goals
- Real-time sync between multiple agents (single-agent sessions only)
- Cross-workspace conversation sharing
- Automatic context compression/summarization (future enhancement)
- Tool execution replay (we persist what happened, not replay capability)

## Decisions

### Decision 1: Session Storage Location
**Store session state in `.session/` subdirectory within each conversation folder**

```
conversations/2025-11-22/001-brainstorm-topic/
├── brainstorm.md              # The conversation content
└── .session/
    ├── session.json           # Metadata, agent config
    └── messages.jsonl         # Chat history (JSON Lines)
```

**Rationale:**
- Keeps session data co-located with conversation
- `.session/` prefix hides from casual browsing
- Git-trackable but can be .gitignored if desired
- Easy to prune/archive independently

**Alternatives considered:**
- Central session store (`.workspace/sessions/`) - Harder to keep in sync, loses locality
- Embedded in markdown frontmatter - Gets unwieldy with message history
- SQLite database - Not git-friendly, requires tooling to inspect

### Decision 2: Message History Format
**Use JSON Lines (`.jsonl`) for message history**

```jsonl
{"role": "user", "content": "Let's brainstorm API design", "timestamp": "2025-11-22T10:30:00Z"}
{"role": "assistant", "content": "Great! What's the core problem...", "timestamp": "2025-11-22T10:30:15Z"}
```

**Rationale:**
- Append-only writes during conversation
- Easy to tail/stream
- Good git diffs (one line per message)
- Simple to parse in any language

**Alternatives considered:**
- Single JSON array - Full rewrite on each append, poor git diffs
- Markdown transcript - Loses structure, hard to parse
- Protocol buffers - Not human-readable

### Decision 3: Session Metadata Schema
**`session.json` captures everything needed to reinitialize the agent**

```json
{
  "version": "1.0",
  "conversation_id": "001-brainstorm-api-design",
  "conversation_type": "brainstorm",
  "status": "active",
  "created_at": "2025-11-22T10:30:00Z",
  "last_active": "2025-11-22T11:45:00Z",
  "message_count": 24,
  "agent_config": {
    "command": "/workspace.brainstorm",
    "system_prompt_hash": "sha256:abc123...",
    "model": "claude-sonnet-4-5-20250929",
    "tools": ["mcp__cortext__search_workspace", "mcp__cortext__get_context"]
  },
  "context_summary": "Discussing REST vs GraphQL for internal APIs, leaning toward REST for simplicity"
}
```

**Key fields:**
- `status`: active | paused | completed
- `agent_config`: Captures what made this conversation possible
- `system_prompt_hash`: Reference to the command file version used
- `context_summary`: Human-readable state for quick orientation

### Decision 4: Resume Command UX
**Primary: `/workspace.resume` slash command with interactive selection**

Flow:
1. User runs `/workspace.resume`
2. Agent queries for recent active/paused conversations
3. Displays list with: type, title, last active, status, summary
4. User selects or types search term
5. Agent loads session and continues with injected context

**Secondary: `cortext resume <id>` CLI command**
- Direct resume by conversation ID
- Supports fuzzy matching on title
- Opens appropriate AI tool with context pre-loaded

### Decision 5: Context Injection Strategy
**Two-phase loading: Command first, then history injection**

When resuming a conversation:

**Phase 1: Load original command**
The system MUST invoke the original slash command (e.g., `/workspace.brainstorm`) to load the agent's system prompt. This ensures the agent has the same behavioral instructions.

**Phase 2: Inject conversation context**
After the command loads, inject the resume context:
```
[RESUMED CONVERSATION]
You are continuing a previous conversation.

Conversation: brainstorm / API Design Discussion
Last active: 2 hours ago
Messages: 24 exchanges
Summary: Discussing REST vs GraphQL for internal APIs, leaning toward REST for simplicity

Previous context is loaded. The user expects you to continue where you left off.
Review the conversation history and pick up naturally.
[END RESUMED CONTEXT]
```

Plus the full message history is available to the agent.

**Implementation flow:**
1. User selects conversation to resume
2. System reads `session.json` to get original command
3. System invokes that command (loads system prompt)
4. System appends resume context block
5. System loads message history
6. Agent continues with full context

**Rationale:**
- Agent gets the same behavioral instructions from the command
- Commands may be updated - user gets latest improvements
- Agents can't truly "remember" - we simulate by providing full context
- Summary helps agent quickly orient without reading all messages
- Clear markers help agent understand this is a continuation

**Handling command changes:**
- If the command file was modified since original conversation, use the new version
- Store `system_prompt_hash` in session to detect changes
- Optionally warn user if prompt changed significantly

### Decision 6: Save Behavior
**Dual approach: smart detection + explicit command**

**Primary: Explicit stop command**
- `/workspace.stop-conversation` explicitly saves and pauses
- Agent confirms save and reminds user about `/workspace.resume`
- Clear, predictable behavior

**Secondary: Smart detection**
- Agent detects natural pause signals in conversation
- Phrases like "let's stop", "that's enough", "I need to go"
- Agent saves and confirms when detected

**Prompting behavior:**
- If conversation runs long without save, agent may prompt: "Would you like me to save this session?"
- User can decline and continue

**No save on:**
- Every message (too noisy for git)
- User explicitly declines save

## Risks / Trade-offs

### Risk: Repository bloat from message history
**Mitigation:**
- Use `.jsonl` for efficient storage
- Document how to add `.session/` to `.gitignore` if desired
- Future: Add history pruning/summarization

### Risk: Context too large for agent context window
**Mitigation:**
- Summarize older messages (keep last N full, summarize rest)
- Track token count in session metadata
- Future: Smart context compression

### Risk: Stale system prompts
**Mitigation:**
- Store hash of system prompt used
- Warn if resuming with different prompt version
- Always use current prompt (don't restore old behavior)

### Risk: Cross-tool compatibility
**Mitigation:**
- Use JSON format all tools can parse
- Context injection works for any tool that supports slash commands
- Test with Claude Code, OpenCode, Gemini CLI

### Trade-off: Privacy/security of message history
**Consideration:**
- Messages stored in plaintext
- Document that session data should be treated as sensitive
- Future: Optional encryption

## Migration Plan

### Phase 1: Foundation (this proposal)
1. Define session storage format
2. Implement `/workspace.resume` command
3. Add session save to all conversation commands
4. Add `cortext resume` CLI

### Phase 2: Enhancements (future proposals)
- Context summarization for long conversations
- Multi-session conversation threads
- Cross-workspace resume
- Analytics on conversation patterns

### Rollback
- Session directories can be deleted without affecting conversations
- Commands work with or without session data
- No schema migrations needed

## Open Questions

1. **How much history to inject?**
   - All messages vs. last N vs. smart summarization
   - Start with all, add summarization later

2. **How to handle tool availability changes?**
   - Resume may occur with different MCP servers connected
   - Decision: Use current tools, warn if critical tools missing

3. **Should `/workspace.resume` be the only entry point?**
   - Alternative: `cortext brainstorm --continue`
   - Decision: Start with dedicated command, consider variants later

4. **Git commit behavior for sessions?**
   - Auto-commit sessions with conversation commits?
   - Decision: Include in conversation commit, make it a single unit
