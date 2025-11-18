## Context
Cortext needs semantic search across conversations and documents. Current ripgrep-based search only supports keyword matching. Users need to find context by meaning, and AI agents need automatic context injection for relevant workspace knowledge.

## Goals / Non-Goals
**Goals:**
- Embed conversations and documents for semantic search
- Provide MCP tools for AI agents to search/retrieve context
- Auto-embed after conversation completion
- Track what's been embedded (UPSERT, avoid re-embedding)
- Support PDF, Word, HTML, Text, Markdown documents

**Non-Goals:**
- Multi-tenant support (single user workspace)
- Cloud-hosted vector store (local ChromaDB only)
- Real-time streaming embeddings
- LLM-based reranking (simple similarity for v1)

## Decisions

### Architecture: Separate RAG module
**Decision:** Create `src/cortext_rag/` as standalone module
**Alternatives:**
- Extend existing MCP server - rejected, mixing concerns
- Integrate into CLI commands - rejected, reusable logic belongs in module
**Rationale:** Clean separation allows MCP tools, CLI commands, and hooks to all use same pipeline

### Embedding Backend: sentence-transformers (initially)
**Decision:** Use sentence-transformers with all-MiniLM-L6-v2 model
**Alternatives:**
- Ollama nomic-embed-text - requires external service
- OpenAI API - requires API key, not local-first
**Rationale:** Runs locally, no external dependencies, good performance for v1. Architecture allows swapping later.

### Vector Store: ChromaDB
**Decision:** Use ChromaDB with persistent storage in `.workspace/embeddings/`
**Alternatives:**
- FAISS - no built-in persistence
- SQLite+pgvector - more complex setup
**Rationale:** Embedded database, handles persistence, simple Python API, good for single-user workspace

### Embedding Strategy: Content-hash based UPSERT
**Decision:** Hash content, only re-embed if hash changes
**Alternatives:**
- Re-embed on every request - wasteful
- Timestamp-based - misses content changes
**Rationale:** Efficient, handles edits, avoids duplicate embeddings

### Document Chunking: Fixed-size with overlap
**Decision:** 512 token chunks with 50 token overlap
**Alternatives:**
- Sentence-based chunking - irregular sizes
- Paragraph-based - too large for conversations
**Rationale:** Consistent chunk sizes, overlap preserves context at boundaries

## Component Architecture

```
src/cortext_rag/
├── __init__.py          # Public API
├── embedder.py          # Embedding generation (sentence-transformers)
├── store.py             # ChromaDB vector store operations
├── indexer.py           # Document processing, chunking, UPSERT logic
├── retriever.py         # Semantic search and context retrieval
├── parsers/             # Document type parsers
│   ├── markdown.py
│   ├── pdf.py
│   ├── docx.py
│   ├── html.py
│   └── text.py
└── models.py            # Data models (Document, Chunk, EmbeddingStatus)
```

## MCP Tools Exposed
1. `embed_document` - Embed a specific file or conversation
2. `embed_workspace` - Embed all unembedded content
3. `search_semantic` - Semantic search across embeddings
4. `get_similar` - Find similar conversations/documents
5. `get_embedding_status` - Check what's been embedded

## CLI Commands
- `cortext embed <path>` - Embed specific file/directory
- `cortext embed --all` - Embed entire workspace
- `cortext search <query> --semantic` - Semantic search (vs keyword)
- `cortext rag status` - Show embedding statistics

## Auto-Embed Hook
After each conversation (bash scripts complete), trigger embedding:
1. Detect new/modified conversation files
2. Parse and chunk content
3. Generate embeddings
4. UPSERT to ChromaDB
5. Update embedding status metadata

## Risks / Trade-offs

### Performance
**Risk:** sentence-transformers first load is slow (~2-5 seconds)
**Mitigation:** Cache model in memory during workspace session, lazy load on first embed

### Storage Size
**Risk:** Embeddings increase workspace size significantly
**Mitigation:** Use efficient model (384 dimensions), compress metadata, monitor size

### Dependency Weight
**Risk:** sentence-transformers, torch add significant package size
**Mitigation:** Make RAG optional extra: `pip install cortext[rag]`

## Migration Plan
1. Add dependencies to pyproject.toml as optional extra `[rag]`
2. Create `.workspace/embeddings/` directory on first use
3. Existing workspaces continue working without RAG
4. Users opt-in to RAG features by installing extras

## Open Questions
- Should we batch embed on workspace init, or lazy embed?
- Chunk size: 512 tokens optimal? Need benchmarking
- Model choice: all-MiniLM-L6-v2 vs all-mpnet-base-v2 (size vs quality)
