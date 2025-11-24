# rag-retrieval Specification

## Purpose
TBD - created by archiving change add-rag-pipeline. Update Purpose after archive.
## Requirements
### Requirement: Semantic Search
The RAG pipeline SHALL provide semantic search across embedded content.

#### Scenario: Search by meaning
- **WHEN** user runs `cortext search "authentication patterns" --semantic`
- **THEN** system generates embedding for query
- **AND** performs similarity search in ChromaDB
- **AND** returns top N results ranked by similarity score
- **AND** displays conversation name, chunk text, and score

#### Scenario: Filter by conversation type
- **WHEN** user searches with `--type brainstorm`
- **THEN** system filters results to only brainstorm conversations
- **AND** returns semantically similar chunks from that type only

#### Scenario: Filter by date range
- **WHEN** user searches with `--date 2025-11`
- **THEN** system filters results to conversations from that month
- **AND** returns semantically similar chunks within date range

#### Scenario: No results found
- **WHEN** query has no semantically similar content
- **THEN** system returns clear "no results" message
- **AND** suggests trying different query terms
- **AND** falls back to keyword search suggestion

### Requirement: Context Retrieval for AI Agents
The RAG pipeline SHALL expose MCP tools for AI agents to retrieve context.

#### Scenario: Agent searches workspace context
- **WHEN** AI agent calls `search_semantic` tool with query
- **THEN** system returns relevant chunks with metadata
- **AND** includes source conversation/document path
- **AND** provides similarity scores for ranking
- **AND** limits results to configurable max (default 10)

#### Scenario: Agent finds similar content
- **WHEN** AI agent calls `get_similar` tool with document path
- **THEN** system finds similar conversations/documents
- **AND** ranks by overall similarity
- **AND** excludes the source document from results
- **AND** returns top N similar items

#### Scenario: Agent embeds on-demand
- **WHEN** AI agent calls `embed_document` tool
- **THEN** system embeds specified file immediately
- **AND** returns embedding status (success, chunks created)
- **AND** updates vector store

#### Scenario: Agent checks embedding status
- **WHEN** AI agent calls `get_embedding_status` tool
- **THEN** system returns workspace embedding statistics
- **AND** lists recently embedded documents
- **AND** reports any files pending embedding

### Requirement: Result Formatting
The RAG pipeline SHALL format search results for readability.

#### Scenario: CLI search results
- **WHEN** user performs semantic search via CLI
- **THEN** results display conversation name prominently
- **AND** show relevant text chunk (truncated if long)
- **AND** include similarity percentage
- **AND** provide file path for reference

#### Scenario: MCP tool results
- **WHEN** AI agent receives search results
- **THEN** results are structured JSON
- **AND** include all metadata (path, type, date, score)
- **AND** provide enough context for agent reasoning
- **AND** are formatted for easy parsing

#### Scenario: Large result sets
- **WHEN** search returns many results
- **THEN** system limits to specified maximum
- **AND** sorts by relevance score descending
- **AND** indicates if more results available
- **AND** suggests refinement for better results

### Requirement: Graceful Degradation
The RAG pipeline SHALL handle missing dependencies gracefully.

#### Scenario: RAG not installed
- **WHEN** user attempts RAG command without `[rag]` extras installed
- **THEN** system displays helpful error message
- **AND** provides installation command: `pip install cortext[rag]`
- **AND** core Cortext functionality remains available

#### Scenario: ChromaDB unavailable
- **WHEN** vector store is corrupted or missing
- **THEN** system offers to reinitialize store
- **AND** warns about loss of existing embeddings
- **AND** provides recovery instructions

#### Scenario: Model download required
- **WHEN** sentence-transformers model not cached locally
- **THEN** system informs user of download requirement
- **AND** downloads model on first use
- **AND** caches for subsequent uses

