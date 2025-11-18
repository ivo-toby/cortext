# RAG Pipeline Implementation Tasks

## 1. Project Setup
- [x] 1.1 Add sentence-transformers, chromadb, pypdf, python-docx to pyproject.toml as optional `[rag]` extra
- [x] 1.2 Create `src/cortext_rag/` module structure
- [x] 1.3 Create data models (Document, Chunk, EmbeddingStatus) in models.py

## 2. Embedding Engine
- [x] 2.1 Implement embedder.py with sentence-transformers (all-MiniLM-L6-v2)
- [x] 2.2 Add lazy model loading with caching
- [x] 2.3 Implement batch embedding for efficiency
- [x] 2.4 Add embedding dimension and model metadata

## 3. Document Parsers
- [x] 3.1 Implement markdown.py parser (frontmatter extraction, content)
- [x] 3.2 Implement text.py parser (plain text files)
- [x] 3.3 Implement pdf.py parser (pypdf integration)
- [x] 3.4 Implement docx.py parser (python-docx integration)
- [x] 3.5 Implement html.py parser (html to text conversion)
- [x] 3.6 Create parser factory to route by file extension

## 4. Chunking and Indexing
- [x] 4.1 Implement content chunking (512 tokens, 50 overlap)
- [x] 4.2 Add content hashing for change detection
- [x] 4.3 Implement indexer.py with UPSERT logic
- [x] 4.4 Track embedding status in metadata (path, hash, timestamp, chunks)

## 5. Vector Store
- [x] 5.1 Implement store.py with ChromaDB client
- [x] 5.2 Configure persistent storage in `.workspace/embeddings/chroma/`
- [x] 5.3 Implement add/update/delete operations
- [x] 5.4 Add collection management (conversations, documents)
- [x] 5.5 Implement similarity search with score thresholds

## 6. Retrieval
- [x] 6.1 Implement retriever.py with semantic search
- [x] 6.2 Add result formatting (conversation name, chunk, score)
- [x] 6.3 Implement get_similar for finding related content
- [x] 6.4 Add filtering by conversation type and date range

## 7. MCP Tools (for AI agents)
- [x] 7.1 Create mcp_tools.py exposing RAG functions
- [x] 7.2 Implement embed_document tool
- [x] 7.3 Implement embed_workspace tool
- [x] 7.4 Implement search_semantic tool
- [x] 7.5 Implement get_similar tool
- [x] 7.6 Implement get_embedding_status tool

## 8. CLI Commands
- [x] 8.1 Add `cortext embed <path>` command
- [x] 8.2 Add `cortext embed --all` for workspace-wide embedding
- [x] 8.3 Add `cortext search --semantic` flag for semantic search
- [x] 8.4 Add `cortext rag status` command for statistics
- [x] 8.5 Handle missing RAG dependencies gracefully (helpful error message)

## 9. Auto-Embed Integration
- [x] 9.1 Create post-conversation hook in bash scripts
- [x] 9.2 Detect new/modified conversation files
- [x] 9.3 Trigger embedding pipeline automatically
- [x] 9.4 Log embedding results to conversation metadata

## 10. Test Infrastructure Setup
- [x] 10.1 Add pytest, pytest-cov, pytest-mock to pyproject.toml dev dependencies
- [x] 10.2 Create tests/rag/ directory structure (unit/, integration/, conftest.py)
- [x] 10.3 Configure pytest.ini with RAG test settings and markers
- [x] 10.4 Create sample workspace fixture in conftest.py
- [x] 10.5 Create mock embedder fixture (deterministic vectors, no model load)
- [x] 10.6 Create temporary ChromaDB fixture (isolated store)

## 11. Unit Tests
- [x] 11.1 Test embedder model loading and caching (tests/rag/unit/test_embedder.py)
- [x] 11.2 Test batch embedding with mock model
- [x] 11.3 Test markdown parser (frontmatter, content extraction)
- [x] 11.4 Test text parser
- [x] 11.5 Test PDF parser (page extraction, metadata)
- [x] 11.6 Test DOCX parser
- [x] 11.7 Test HTML parser (tag stripping)
- [x] 11.8 Test parser factory routing
- [x] 11.9 Test chunking logic (size, overlap, boundaries)
- [x] 11.10 Test content hash generation
- [x] 11.11 Test UPSERT logic (new, modified, unchanged detection)

## 12. Integration Tests
- [x] 12.1 Test ChromaDB add/update/delete operations (tests/rag/integration/)
- [x] 12.2 Test similarity search with real embeddings
- [x] 12.3 Test full embedding pipeline (workspace → vectors)
- [x] 12.4 Test incremental re-embedding (only changed files)
- [x] 12.5 Test semantic search filtering (type, date range)
- [x] 12.6 Test auto-embed hook trigger
- [x] 12.7 Benchmark embedding performance (time, memory)
- [x] 12.8 Verify 80%+ test coverage with pytest-cov

## 13. Documentation
- [x] 13.1 Create Docs/rag-guide.md with installation and setup instructions
- [x] 13.2 Document all CLI commands with examples (`embed`, `search --semantic`, `rag status`)
- [x] 13.3 Document MCP tools for AI agents (tool schemas, usage patterns)
- [x] 13.4 Add use-case examples (find related conversations, context retrieval, similar docs)
- [x] 13.5 Document supported file formats and parser behavior
- [x] 13.6 Add troubleshooting section (common errors, performance tips, storage management)
- [x] 13.7 Document auto-embed hook configuration and customization
- [x] 13.8 Update main README.md with RAG feature overview and link to guide

## Dependencies
- Tasks 2-4 can run in parallel
- Task 5 depends on task 2 (needs embedder for store tests)
- Task 6 depends on tasks 4 and 5
- Task 7 depends on task 6
- Task 8 depends on tasks 6 and 7
- Task 9 depends on task 8
- Task 10 (test infrastructure) should be set up early, after task 1
- Tasks 11-12 (unit/integration tests) run alongside implementation (tasks 2-9)
- Task 13 (documentation) depends on tasks 7, 8, 9 (document after implementation complete)
