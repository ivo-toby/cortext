# rag-documentation Specification

## Purpose
TBD - created by archiving change add-rag-pipeline. Update Purpose after archive.
## Requirements
### Requirement: RAG User Documentation
The RAG pipeline SHALL provide comprehensive user documentation with examples and use-cases.

#### Scenario: Installation guide
- **WHEN** user reads RAG documentation
- **THEN** documentation provides clear installation steps
- **AND** explains optional `[rag]` extra: `pip install cortext[rag]`
- **AND** lists all dependencies (sentence-transformers, chromadb, pypdf, python-docx)
- **AND** documents first-run model download behavior

#### Scenario: CLI command examples
- **WHEN** user wants to embed content
- **THEN** documentation shows `cortext embed <path>` with examples:
  - `cortext embed ./brainstorm/2025-11/001-new-feature/`
  - `cortext embed --all`
  - `cortext embed ./docs/research.pdf`
- **AND** explains each flag and option
- **AND** shows expected output for each command

#### Scenario: Semantic search examples
- **WHEN** user wants to search by meaning
- **THEN** documentation shows `cortext search "query" --semantic` examples:
  - Find authentication patterns: `cortext search "login security" --semantic`
  - Filter by type: `cortext search "api design" --semantic --type plan`
  - Filter by date: `cortext search "refactoring" --semantic --date 2025-11`
- **AND** compares semantic vs keyword search results
- **AND** explains similarity scoring

#### Scenario: Use-case walkthroughs
- **WHEN** user wants to understand real scenarios
- **THEN** documentation includes:
  - "Find related conversations before starting new feature"
  - "Retrieve context from past debugging sessions"
  - "Discover similar documents across workspace"
  - "Check what's been embedded and what's pending"
- **AND** each use-case shows complete command sequence
- **AND** explains expected outcomes

### Requirement: MCP Tools Documentation
The RAG pipeline SHALL document MCP tools for AI agent integration.

#### Scenario: Tool schema documentation
- **WHEN** developer integrates MCP tools
- **THEN** documentation lists all available tools:
  - `embed_document`
  - `embed_workspace`
  - `search_semantic`
  - `get_similar`
  - `get_embedding_status`
- **AND** provides JSON schema for each tool
- **AND** shows example request/response pairs

#### Scenario: Agent usage patterns
- **WHEN** AI agent needs to retrieve context
- **THEN** documentation shows common patterns:
  - "Before answering, search for relevant past conversations"
  - "Find similar features before implementing new one"
  - "Check if topic was discussed before"
- **AND** provides prompt engineering tips for agents
- **AND** explains how to interpret similarity scores

### Requirement: Troubleshooting Documentation
The RAG pipeline SHALL document common issues and solutions.

#### Scenario: Missing dependencies error
- **WHEN** user encounters "RAG not installed" error
- **THEN** documentation explains the error
- **AND** provides fix: `pip install cortext[rag]`
- **AND** suggests verifying with `pip show sentence-transformers chromadb`

#### Scenario: Slow first embedding
- **WHEN** user notices long wait on first embed
- **THEN** documentation explains model download (first time)
- **AND** documents model caching behavior
- **AND** provides performance expectations (2-5s first load, <100ms subsequent)

#### Scenario: Large workspace storage
- **WHEN** user concerned about storage size
- **THEN** documentation explains storage structure
- **AND** provides size estimates (embeddings per MB of text)
- **AND** suggests cleanup commands for old embeddings

#### Scenario: Corrupted vector store
- **WHEN** ChromaDB becomes corrupted
- **THEN** documentation explains recovery steps
- **AND** shows how to reinitialize: `rm -rf .workspace/embeddings/ && cortext embed --all`
- **AND** warns about re-embedding time for large workspaces

