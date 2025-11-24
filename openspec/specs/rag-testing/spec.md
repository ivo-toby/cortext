# rag-testing Specification

## Purpose
TBD - created by archiving change add-rag-pipeline. Update Purpose after archive.
## Requirements
### Requirement: Unit Test Infrastructure
The RAG pipeline SHALL have comprehensive unit tests for all core components.

#### Scenario: Embedder unit tests
- **WHEN** testing embedding generation
- **THEN** tests verify model loading behavior
- **AND** test batch embedding with mock model
- **AND** verify embedding dimensions match expected (384)
- **AND** test lazy loading and caching
- **AND** use pytest fixtures for model mocking

#### Scenario: Parser unit tests
- **WHEN** testing document parsers
- **THEN** each parser (markdown, text, pdf, docx, html) has dedicated tests
- **AND** tests verify content extraction accuracy
- **AND** test edge cases (empty files, malformed content, large files)
- **AND** verify metadata extraction (frontmatter, page numbers)
- **AND** test parser factory routing by file extension

#### Scenario: Chunking unit tests
- **WHEN** testing content chunking
- **THEN** tests verify 512-token chunk size
- **AND** verify 50-token overlap between chunks
- **AND** test boundary conditions (content shorter than chunk size)
- **AND** verify chunk metadata (position, source)
- **AND** test content hash generation consistency

#### Scenario: Indexer unit tests
- **WHEN** testing UPSERT logic
- **THEN** tests verify new content detection (no existing hash)
- **AND** verify modified content detection (hash mismatch)
- **AND** verify unchanged content skipping (hash match)
- **AND** test metadata tracking (path, hash, timestamp, chunks)
- **AND** mock ChromaDB interactions

### Requirement: Integration Test Suite
The RAG pipeline SHALL have integration tests verifying end-to-end workflows.

#### Scenario: ChromaDB integration tests
- **WHEN** testing vector store operations
- **THEN** tests use temporary ChromaDB instance
- **AND** verify add/update/delete operations
- **AND** test similarity search returns correct results
- **AND** verify persistence across restarts
- **AND** test collection management

#### Scenario: Full embedding pipeline test
- **WHEN** testing complete embed workflow
- **THEN** test creates temporary workspace with sample conversations
- **AND** runs `cortext embed --all`
- **AND** verifies all files are embedded
- **AND** checks embedding status reflects reality
- **AND** verifies incremental re-embedding (only changed files)

#### Scenario: Semantic search integration test
- **WHEN** testing search accuracy
- **THEN** test embeds known content (e.g., "authentication patterns discussion")
- **AND** performs semantic search with related query
- **AND** verifies relevant results returned first
- **AND** tests filtering by type and date range
- **AND** compares semantic vs keyword search results

#### Scenario: Auto-embed hook integration test
- **WHEN** testing post-conversation embedding
- **THEN** test simulates conversation completion
- **AND** verifies hook triggers embedding
- **AND** checks new conversation appears in vector store
- **AND** verifies embedding metadata logged

### Requirement: Test Fixtures and Utilities
The RAG pipeline SHALL provide reusable test fixtures and utilities.

#### Scenario: Sample workspace fixture
- **WHEN** integration tests need workspace data
- **THEN** fixture creates temporary workspace structure
- **AND** includes sample conversations (brainstorm, debug, plan)
- **AND** includes sample documents (PDF, DOCX, HTML)
- **AND** fixture cleans up after test completion

#### Scenario: Mock embedder fixture
- **WHEN** unit tests need fast embedding
- **THEN** fixture provides mock embedder returning deterministic vectors
- **AND** avoids loading real model (fast tests)
- **AND** maintains consistent behavior for assertions

#### Scenario: Temporary ChromaDB fixture
- **WHEN** tests need isolated vector store
- **THEN** fixture creates in-memory or temp directory ChromaDB
- **AND** isolates tests from production data
- **AND** cleans up after test

### Requirement: Test Coverage and Quality
The RAG pipeline SHALL maintain high test coverage and quality standards.

#### Scenario: Coverage threshold
- **WHEN** running test suite
- **THEN** pytest-cov reports coverage percentage
- **AND** RAG module maintains minimum 80% line coverage
- **AND** critical paths (embedding, search, UPSERT) have 95%+ coverage
- **AND** coverage report highlights untested code

#### Scenario: Test organization
- **WHEN** viewing test structure
- **THEN** tests organized in `tests/rag/` directory
- **AND** unit tests in `tests/rag/unit/`
- **AND** integration tests in `tests/rag/integration/`
- **AND** fixtures in `tests/rag/conftest.py`
- **AND** test files mirror source structure (test_embedder.py, test_store.py)

#### Scenario: CI/CD integration
- **WHEN** code is pushed
- **THEN** tests run automatically (pytest)
- **AND** failures block merge
- **AND** coverage report generated
- **AND** slow tests marked and can be skipped locally

#### Scenario: Performance benchmarks
- **WHEN** testing performance characteristics
- **THEN** benchmark tests measure embedding time per document
- **AND** measure search latency
- **AND** track memory usage during batch operations
- **AND** results logged for regression detection

