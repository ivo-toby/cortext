# Brainstorm: Adding Knowledge Graph to Cortext

**ID**: 001-brainstorm-adding-knowledge-graph-to-cortext
**Date**: 2025-11-19
**Status**: In Progress

---

## Goals

Explore adding a knowledge graph layer to Cortext to complement the existing RAG (semantic search + embeddings) system. Requirements:

- Must run locally and standalone (no Neo4J-style server)
- Integration via hooks or other strategies
- Make Cortext significantly more powerful for understanding relationships between concepts, decisions, and conversations

---

## Ideas

### Why Knowledge Graph + RAG = Magic

**RAG's strength:** "Find similar content" (vector similarity)
**Knowledge Graph's strength:** "Understand relationships" (structured connections)

**Example scenarios where KG wins:**

1. "What decisions led to choosing technology X?" - Need to trace decision chains
2. "Show me all conversations that reference both topic A and topic B" - Need explicit connections
3. "What problems emerged after we made decision Y?" - Need temporal + causal relationships
4. "Which conversations influenced this planning session?" - Need to track influence/lineage

### Local Standalone Knowledge Graph Options

1. **SQLite-based graph database**
   - Ultra-lightweight, already a dependency in many projects
   - Could use schema with nodes/edges tables
   - Add graph query layer on top (similar to AlaSQL for graph queries)

2. **embedded-graph libraries**
   - TypeScript: `memgraph` or custom implementation
   - Could serialize to JSON/MessagePack for persistence
   - In-memory with periodic snapshots

3. **LevelDB/RocksDB-based**
   - Key-value store with graph traversal logic
   - Very fast, minimal overhead
   - Used by many local-first applications

---

## Research Findings

### Database Options (November 2025)

**KuzuDB Status:**

- ❌ Original project abandoned by Kùzu Inc in October 2025
- ✅ BUT: **RyuGraph** is an active fork continuing development
- Was: Embedded property graph database, implements Cypher, built for speed
- Code is still usable, just no longer maintained by original team

**Top Alternatives for Embedded/Local Graph Databases:**

1. **RyuGraph** (https://github.com/predictable-labs/ryugraph)
   - Active fork of Kuzu, continuing development
   - Embedded property graph DB
   - Implements Cypher query language
   - Built for speed with vector search + full-text search built in
   - **Verdict:** Strong candidate - has the features we need + active development

2. **Cozo** (Rust-based)
   - Designed to be "SQLite-like" for graphs
   - Uses Datalog instead of Cypher
   - Lightweight and easy to use
   - Written in Rust (good performance)
   - **Verdict:** Interesting alternative, different query paradigm

3. **TinkerGraph**
   - In-memory graph database
   - Very lightweight
   - Good for prototyping
   - **Verdict:** Maybe for MVP, but needs persistence strategy

4. **ArcadeDB**
   - Multi-model: graphs + documents + key-value + time series
   - Can run embedded on single server
   - Minimal footprint
   - **Verdict:** Interesting if we want multi-model support

### MCP Server Integration

**Existing MCP Servers for Graph Databases:**

1. **mcp-knowledge-graph** by Anthropic
   - GitHub: https://github.com/shaneholloman/mcp-knowledge-graph
   - Fork focused on LOCAL development (perfect!)
   - Enables persistent memory through local knowledge graph
   - **Verdict:** Could be adapted for Cortext!

2. **Graphiti MCP Server** by Zep
   - GitHub: https://github.com/getzep/graphiti
   - Framework for temporally-aware knowledge graphs
   - Integrates user interactions continuously
   - Has MCP server component
   - **Verdict:** Interesting framework approach

3. **Neo4j MCP Server** (mcp-neo4j-cypher)
   - Official Neo4j integration
   - ❌ Requires Neo4j server (not standalone enough for our needs)

4. **Memgraph MCP Server**
   - ❌ Also requires Memgraph server running

**Key Insight from MCP Research:**
The Anthropic knowledge-graph MCP server is designed for LOCAL use and could potentially be adapted to work with whatever embedded DB we choose (RyuGraph, Cozo, etc.)

---

## The Bigger Vision: Cortext AI Workspace

### Database Decision: RyuGraph

**RyuGraph** is the stronger candidate because:

- More advanced feature set (vector search + full-text + graph)
- Better suited for scale as workspace grows
- Cypher query language is more mature/documented
- The Anthropic Memory MCP might not scale well for large workspaces

### Cortext as an MCP Server

**Key Idea:** Turn Cortext itself into an MCP server! This enables:

1. **Claude Desktop integration** - Interact with conversations and documents from Claude Desktop
2. **Cross-tool compatibility** - Any MCP-compatible client can query Cortext
3. **Exposed capabilities:**
   - Semantic search (RAG)
   - Knowledge graph queries (relationships)
   - Context retrieval
   - Decision history
   - Document embedding

### Integration with SkynetMCP

**SkynetMCP** (from brainstorm 2025-11-17) is an agent-agnostic subagent orchestration system.

**Combined with Cortext:**

- SkynetMCP spawns subagents for research tasks
- Subagents can query Cortext for context via MCP
- Research results automatically flow into Cortext knowledge graph
- Example workflow:
  ```
  Claude Desktop → SkynetMCP → spawns 3 Haiku agents
    → Each agent queries Cortext MCP for context
    → Research results stored back in Cortext knowledge graph
    → Main context preserved, knowledge grows automatically
  ```

**The Power Combo:**

- **Cortext MCP** = Knowledge layer (what do I know?)
- **SkynetMCP** = Orchestration layer (how do I get things done?)
- **Together** = AI workspace with memory and capability

### Hooks System

**Idea:** Deterministic scripts executed on specific events in the Cortext lifecycle

**Current State:**

- Only `post-commit` hook exists (runs `cortext embed --all`)
- Conversation scripts call `auto-embed.sh` manually after creation
- No systematic hook dispatch

**Problem Identified:** RAG embedding after git commits may not be working properly. The post-commit hook runs `cortext embed --all` which is expensive and might be failing silently.

#### Proposed Hook Events

**Tier 1 - Git Hooks** (`.git/hooks/`):

| Event           | When                 | Purpose                                         |
| --------------- | -------------------- | ----------------------------------------------- |
| `pre-commit`    | Before commit staged | Validate conversation metadata, lint markdown   |
| `post-commit`   | After commit         | Smart embedding (only changed files, not --all) |
| `post-checkout` | After branch switch  | Load conversation metadata, sync context        |
| `commit-msg`    | Validate commit      | Enforce `[type] Message` format                 |

**Tier 2 - Custom Cortext Hooks** (`.workspace/hooks/`):

| Event                  | When                           | Purpose                                     |
| ---------------------- | ------------------------------ | ------------------------------------------- |
| `conversation:create`  | After conversation initialized | Register in index, add to knowledge graph   |
| `conversation:update`  | After edits committed          | Update embeddings, sync graph relationships |
| `conversation:archive` | When moved to archive          | Remove from active search, update stats     |
| `branch:create`        | New conversation branch        | Create metadata, update registry            |
| `branch:delete`        | Branch deleted                 | Clean up embeddings, archive metadata       |
| `memory:update`        | Constitution/context changed   | Invalidate caches, rebuild index            |

**Tier 3 - User Interaction Events**:

| Event            | When                               | Purpose                                       |
| ---------------- | ---------------------------------- | --------------------------------------------- |
| `user:message`   | User sends message in conversation | Could trigger context lookup, log interaction |
| `agent:response` | AI responds                        | Could extract decisions/concepts for graph    |
| `session:start`  | Conversation session begins        | Load relevant context from graph              |
| `session:end`    | Conversation session ends          | Summarize, extract entities, update graph     |

#### Hook Architecture

```
.workspace/
├── hooks/
│   ├── dispatch.sh          # Main dispatcher
│   ├── conversation/
│   │   ├── on-create.sh
│   │   ├── on-update.sh
│   │   └── on-archive.sh
│   ├── branch/
│   │   ├── on-create.sh
│   │   └── on-delete.sh
│   └── memory/
│       └── on-update.sh
```

**Dispatcher Pattern:**

```bash
# dispatch.sh "event:name" [args...]
event=$1
hook_dir=".workspace/hooks/${event%:*}"
hook_script="${hook_dir}/on-${event#*:}.sh"

if [ -x "$hook_script" ]; then
    "$hook_script" "${@:2}"
fi
```

#### Knowledge Graph Integration via Hooks

The hooks system is how we populate the knowledge graph automatically:

- **conversation:create** → Create node in graph, link to conversation type
- **conversation:update** → Extract entities/concepts, create relationship edges
- **agent:response** → Parse for decisions, add to decision graph
- **session:end** → Summarize conversation, extract key relationships

This makes knowledge accumulation **deterministic and automatic**.

#### Pre-commit vs Post-commit: Critical Decision

**Pre-commit advantages:**

- Know exactly what's being committed (staged files)
- Can add RAG/KG data files to the same commit
- **Atomic**: content + embeddings always in sync
- No orphaned states

**The Merge Conflict Problem:**
If we commit RAG/KG data files, we get merge hell:

- ChromaDB = binary files + SQLite (doesn't merge)
- RyuGraph = similar binary storage
- Multiple branches = conflicting database states
- Team collaboration becomes painful

**Possible Solutions:**

1. **Don't commit data files** (current .gitignore approach)
   - Pro: No merge conflicts
   - Con: Must regenerate on clone/checkout
   - Con: Embeddings not version-controlled

2. **Commit but accept per-branch state**
   - Pro: Each branch has its own embeddings
   - Con: Merging requires manual resolution
   - Con: Bloated repo size

3. **Regenerate on demand**
   - Don't commit embeddings at all
   - Post-checkout hook: `cortext embed --all`
   - Pro: Clean git history
   - Con: Slow checkout, needs rebuild

4. **Hybrid: Source-of-truth pattern**
   - Only commit source markdown (version controlled)
   - `.gitignore` the embedding/KG data
   - Use deterministic hashing: same content → same embeddings
   - Rebuild only what's missing or changed
   - Pro: Clean history + fast rebuilds
   - Con: First clone is slower

5. **Separate storage entirely**
   - Embeddings/KG in separate location (not in repo)
   - Global or per-workspace cache
   - Pro: No git bloat at all
   - Con: Need to sync/backup separately

**Decision: Option 4 (Hybrid) - Source-of-Truth Pattern**

This is the chosen approach:

- Source files are the truth (versioned in git)
- Embeddings/KG are derived data (cached locally, `.gitignore`d)
- Smart rebuild: hash content, skip unchanged
- **Pre-commit hook** updates embeddings/KG before commit completes
- Data files stay local - no merge conflicts

**Implementation Flow:**

```
git add conversation.md
git commit
  → pre-commit hook triggers
  → embed only staged markdown files
  → update knowledge graph with new relationships
  → embeddings stay local (not committed)
  → commit only the source files
```

**For fresh clones:**

- Post-checkout hook or manual `cortext embed --all`
- Deterministic: same content → same embeddings

---

### Web-Based Frontend

**Idea:** Create a web interface for reading and searching Cortext documents

**Use cases:**

- Browse conversations visually
- Search across all documents
- Visualize knowledge graph relationships
- Share workspace content with non-CLI users

**Challenge: Inference in web frontend**

- If relying on Claude Max subscription, can't easily call API from web
- Possible solutions:
  1. **Read-only frontend** - Just browsing/searching, no inference
  2. **Proxy through local CLI** - Web calls local Claude Code
  3. **Separate API key** - For web-specific inference budget
  4. **Edge inference** - Local models (Ollama) for simple queries
  5. **Hybrid** - Embedding search works fine, only complex queries need LLM

---

## Themes

1. **MCP as universal interface** - Both Cortext and SkynetMCP expose capabilities via MCP
2. **Knowledge accumulation** - Research automatically enriches the knowledge graph
3. **Scale considerations** - RyuGraph over simpler solutions for growing workspaces
4. **Multi-interface access** - CLI (Claude Code) + Desktop (Claude Desktop) + Web (frontend)
5. **Subscription model challenges** - Need creative solutions for web inference
6. **Deterministic automation via hooks** - Scripts trigger on events, not manual invocation
7. **Graceful degradation** - Hooks fail silently if dependencies missing (existing pattern)

---

## Architecture Sketch

```
┌─────────────────────────────────────────────────────────┐
│                    Access Layers                         │
├─────────────┬─────────────┬─────────────┬───────────────┤
│ Claude Code │ Claude      │ Web         │ Other MCP     │
│ (CLI)       │ Desktop     │ Frontend    │ Clients       │
└─────┬───────┴──────┬──────┴──────┬──────┴───────┬───────┘
      │              │             │              │
      └──────────────┴──────┬──────┴──────────────┘
                            │
                    ┌───────▼────────┐
                    │  Cortext MCP   │
                    │    Server      │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
│     RAG       │   │  Knowledge    │   │   Document    │
│  (ChromaDB/   │   │    Graph      │   │   Storage     │
│  Embeddings)  │   │  (RyuGraph)   │   │   (Files)     │
└───────────────┘   └───────────────┘   └───────────────┘

        + Integration with SkynetMCP for subagent orchestration
```

---

## Next Steps

### Immediate

1. **Debug RAG embedding** - Fix the post-commit hook not triggering properly
2. **Evaluate RyuGraph** - Set up locally, test with sample data
3. **Design graph schema** - Node types, edge types, properties
4. **Define MCP interface** - What tools does Cortext MCP expose?

### Medium-term

1. **Implement hooks system** - Create `.workspace/hooks/` with dispatcher
2. **Build Cortext MCP server** - Expose RAG + graph via MCP
3. **Test with Claude Desktop** - Verify integration works
4. **Connect hooks to knowledge graph** - Auto-populate on conversation events

### Long-term

1. **Web frontend** - Read-only first, figure out inference later
2. **SkynetMCP integration** - Connect orchestration with knowledge layer
3. **Scale testing** - How does RyuGraph perform with 1000s of conversations?
4. **User interaction hooks** - Track messages/responses for deeper context

---

## Other todo's

Onboarding flow after init; we should ask a user to run a new command; /workspace-setup to go through a wizard. This will set up the constition, configure behaviour (tbd) etc.

---

## Related Conversations

- **SkynetMCP concept**: `brainstorm/2025-11-17/001-brainstorm-leveraging-subagents-in-cortext/`
  - Agent-agnostic subagent orchestration
  - Provider abstraction (Anthropic, OpenAI, Gemini, Ollama)
  - Cost controls, security boundaries
  - Detailed technical architecture

---

**Metadata**

- Created: 2025-11-19
- Tags: brainstorm, knowledge-graph, mcp, cortext, architecture
