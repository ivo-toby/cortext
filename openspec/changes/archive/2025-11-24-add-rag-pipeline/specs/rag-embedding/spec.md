## ADDED Requirements

### Requirement: Embedding Generation
The RAG pipeline SHALL generate vector embeddings from text content using sentence-transformers.

#### Scenario: Embed markdown conversation
- **WHEN** user requests embedding of a conversation file
- **THEN** system loads all-MiniLM-L6-v2 model (lazy, cached)
- **AND** parses markdown content extracting text
- **AND** chunks content into 512-token segments with 50-token overlap
- **AND** generates 384-dimensional embeddings for each chunk
- **AND** returns embeddings with chunk metadata (source, position, text)

#### Scenario: Embed PDF document
- **WHEN** user requests embedding of PDF file
- **THEN** system extracts text from PDF using pypdf
- **AND** chunks extracted text
- **AND** generates embeddings for each chunk
- **AND** preserves page number metadata

#### Scenario: Batch embedding
- **WHEN** multiple documents need embedding
- **THEN** system batches embedding requests for efficiency
- **AND** processes up to 32 chunks per batch
- **AND** shows progress indicator for large batches

### Requirement: Content Hash Tracking
The RAG pipeline SHALL track content hashes to avoid re-embedding unchanged content.

#### Scenario: New content embedding
- **WHEN** file has never been embedded
- **THEN** system computes content hash
- **AND** generates embeddings
- **AND** stores hash in metadata

#### Scenario: Modified content re-embedding
- **WHEN** file content hash differs from stored hash
- **THEN** system deletes old embeddings for that file
- **AND** generates new embeddings
- **AND** updates stored hash (UPSERT)

#### Scenario: Unchanged content skip
- **WHEN** file content hash matches stored hash
- **THEN** system skips embedding generation
- **AND** reports "already embedded" status

### Requirement: Document Parser Support
The RAG pipeline SHALL support multiple document formats through pluggable parsers.

#### Scenario: Markdown parsing
- **WHEN** file has .md extension
- **THEN** markdown parser extracts frontmatter metadata
- **AND** converts markdown to plain text
- **AND** preserves heading structure in chunks

#### Scenario: PDF parsing
- **WHEN** file has .pdf extension
- **THEN** PDF parser extracts text from all pages
- **AND** includes page number in chunk metadata

#### Scenario: Word document parsing
- **WHEN** file has .docx extension
- **THEN** DOCX parser extracts paragraph text
- **AND** preserves document structure

#### Scenario: HTML parsing
- **WHEN** file has .html or .htm extension
- **THEN** HTML parser strips tags
- **AND** extracts text content only

#### Scenario: Unsupported format
- **WHEN** file type has no registered parser
- **THEN** system returns clear error message
- **AND** suggests supported formats
