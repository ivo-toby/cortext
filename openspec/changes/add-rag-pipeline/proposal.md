# Change: Add RAG Pipeline for Workspace Context Management

## Why
Cortext lacks semantic search and context retrieval capabilities. Users cannot find relevant past conversations based on meaning, only keyword search. A RAG pipeline will enable intelligent context injection, allowing AI agents to retrieve relevant workspace knowledge automatically.

## What Changes
- Add embedding generation for conversations and documents (sentence-transformers)
- Implement ChromaDB vector store for persistent embeddings
- Create auto-embed pipeline triggered after each conversation
- Add MCP tools for agents: embed, search, retrieve operations
- Support multiple document types (PDF, Word, HTML, Text, Markdown)
- Track embedding status with UPSERT logic (avoid re-embedding unchanged content)

## Impact
- Affected specs: NEW capabilities `rag-embedding`, `rag-indexing`, `rag-retrieval`
- Affected code: New `src/cortext_rag/` module, CLI commands, conversation workflow hooks
- Dependencies: sentence-transformers, chromadb, pypdf, python-docx
- **BREAKING**: Adds new required dependencies to pyproject.toml
