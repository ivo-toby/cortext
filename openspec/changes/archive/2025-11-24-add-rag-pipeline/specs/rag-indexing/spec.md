## ADDED Requirements

### Requirement: Vector Store Persistence
The RAG pipeline SHALL persist embeddings in ChromaDB stored within the workspace.

#### Scenario: Initialize vector store
- **WHEN** RAG pipeline starts for first time
- **THEN** creates `.workspace/embeddings/chroma/` directory
- **AND** initializes ChromaDB with persistent storage
- **AND** creates collections for different content types

#### Scenario: Store embeddings
- **WHEN** embeddings are generated for document
- **THEN** system stores vectors in ChromaDB collection
- **AND** attaches metadata (source path, content hash, timestamp, chunk position)
- **AND** assigns unique IDs for each chunk

#### Scenario: Update embeddings (UPSERT)
- **WHEN** document is re-embedded due to content change
- **THEN** system deletes all chunks for that document
- **AND** inserts new chunks with updated embeddings
- **AND** updates metadata with new hash and timestamp

### Requirement: Embedding Status Tracking
The RAG pipeline SHALL maintain status of all indexed content.

#### Scenario: Query embedding status
- **WHEN** user runs `cortext rag status`
- **THEN** system reports total documents embedded
- **AND** total chunks in vector store
- **AND** last embedding timestamp
- **AND** storage size in MB

#### Scenario: Check specific file status
- **WHEN** user queries status of specific file
- **THEN** system reports if file is embedded
- **AND** number of chunks
- **AND** content hash
- **AND** last embedded timestamp

#### Scenario: List unembedded content
- **WHEN** user wants to see what needs embedding
- **THEN** system scans workspace for supported files
- **AND** compares against embedding metadata
- **AND** lists files not yet embedded or with changed hashes

### Requirement: Auto-Embed After Conversation
The RAG pipeline SHALL automatically embed conversations after completion.

#### Scenario: Conversation completed
- **WHEN** bash conversation script finishes
- **THEN** hook detects new conversation directory
- **AND** triggers embedding for conversation.md file
- **AND** logs embedding result to console

#### Scenario: Conversation updated
- **WHEN** existing conversation file is modified
- **THEN** auto-embed detects hash change
- **AND** re-embeds the conversation
- **AND** updates vector store with new embeddings

#### Scenario: Embedding failure handling
- **WHEN** auto-embed fails (missing dependencies, corrupt file)
- **THEN** system logs error with clear message
- **AND** conversation remains functional without embeddings
- **AND** user can retry embedding manually

### Requirement: Workspace-Wide Indexing
The RAG pipeline SHALL support embedding entire workspace contents.

#### Scenario: Embed all conversations
- **WHEN** user runs `cortext embed --all`
- **THEN** system scans all conversation directories
- **AND** filters to supported file types
- **AND** skips already-embedded unchanged files
- **AND** embeds new or modified files
- **AND** reports progress (X of Y files embedded)

#### Scenario: Embed specific directory
- **WHEN** user runs `cortext embed ./brainstorm/`
- **THEN** system recursively finds supported files in directory
- **AND** embeds each file with UPSERT logic
- **AND** respects content hash caching

#### Scenario: Incremental indexing
- **WHEN** workspace has existing embeddings
- **THEN** new `embed --all` only processes changes
- **AND** avoids re-embedding unchanged content
- **AND** completes quickly for small changes
