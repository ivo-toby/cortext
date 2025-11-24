# mcp-rag-tools Specification

## Purpose
TBD - created by archiving change integrate-rag-mcp. Update Purpose after archive.
## Requirements
### Requirement: MCP Server Exposes RAG Embedding Tools

The MCP server SHALL provide tools for embedding documents and workspaces.

#### Scenario: Agent Embeds Single Conversation

```
GIVEN a workspace with an unembed conversation at "brainstorm/2025-11-17/001-new-idea"
WHEN an agent calls the "embed_document" tool with path "brainstorm/2025-11-17/001-new-idea"
THEN the tool returns {"success": true, "embedded": 1, "skipped": 0, "total_files": 1}
AND the conversation is now searchable via semantic search
```

#### Scenario: Agent Embeds Entire Workspace

```
GIVEN a workspace with 10 conversations, 5 already embedded
WHEN an agent calls the "embed_workspace" tool
THEN the tool returns {"success": true, "embedded": 5, "skipped": 5}
AND all conversations are now searchable via semantic search
```

#### Scenario: Embedding Non-Existent Path

```
GIVEN a workspace
WHEN an agent calls "embed_document" with path "nonexistent/path"
THEN the tool returns {"success": false, "error": "Path not found: ..."}
```

---

### Requirement: MCP Server Exposes Semantic Search Tool

The MCP server SHALL provide a semantic search tool using embeddings.

#### Scenario: Agent Searches for Authentication Topics

```
GIVEN a workspace with embedded conversations about JWT, OAuth, and session auth
WHEN an agent calls "search_semantic" with query "authentication patterns"
THEN the tool returns results with high scores for auth-related conversations
AND results include "conversation", "score", "text", and "source_path" fields
AND results are sorted by relevance score (highest first)
```

#### Scenario: Agent Filters Search by Conversation Type

```
GIVEN a workspace with brainstorm and debug conversations
WHEN an agent calls "search_semantic" with query "api design" and conversation_type "plan"
THEN the tool returns only results from plan conversations
```

#### Scenario: Agent Filters Search by Date

```
GIVEN a workspace with conversations from multiple months
WHEN an agent calls "search_semantic" with query "kubernetes" and date_range "2025-11"
THEN the tool returns only results from November 2025
```

#### Scenario: Search with No Embeddings

```
GIVEN a workspace with no embedded conversations
WHEN an agent calls "search_semantic" with any query
THEN the tool returns {"success": true, "num_results": 0, "results": []}
```

---

### Requirement: MCP Server Exposes Document Similarity Tool

The MCP server SHALL provide a tool to find documents similar to a given source document.

#### Scenario: Agent Finds Similar Conversations

```
GIVEN a workspace with conversation A about "JWT authentication"
AND conversations B and C about "OAuth" and "API security"
WHEN an agent calls "get_similar" with source_path pointing to conversation A
THEN the tool returns conversations B and C ranked by similarity
AND results include similarity scores
```

#### Scenario: Finding Similar to Non-Existent Document

```
GIVEN a workspace
WHEN an agent calls "get_similar" with a non-existent source_path
THEN the tool returns {"success": false, "error": "Document not found: ..."}
```

---

### Requirement: MCP Server Exposes Embedding Status Tool

The MCP server SHALL provide a tool to query workspace embedding statistics.

#### Scenario: Agent Checks Embedding Coverage

```
GIVEN a workspace with 15 embedded documents
WHEN an agent calls "get_embedding_status"
THEN the tool returns total_chunks, num_documents, db_path
AND includes recent_embeddings list with timestamps
```

---

### Requirement: RAG Tools Handle Workspace Context

All RAG tools SHALL accept an optional workspace_path parameter and default to current working directory.

#### Scenario: Agent Specifies Workspace Path

```
GIVEN an agent working from outside a workspace
WHEN the agent calls "search_semantic" with workspace_path "/home/user/my-workspace"
THEN the search operates on the specified workspace
```

#### Scenario: Agent Uses Default Workspace

```
GIVEN an MCP server running in a workspace directory
WHEN the agent calls "search_semantic" without workspace_path
THEN the search operates on the current workspace
```

---

### Requirement: RAG Tools Return Consistent Error Format

All RAG tools SHALL return errors in a consistent format when operations fail.

#### Scenario: Consistent Error Response

```
GIVEN any RAG tool experiencing an error
WHEN the tool is called
THEN the response includes {"success": false, "error": "descriptive message"}
AND no exception is raised to the MCP client
```

---

