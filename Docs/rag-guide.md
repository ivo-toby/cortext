# RAG Pipeline Guide

Semantic search and context retrieval for Cortext workspaces.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [CLI Commands](#cli-commands)
4. [Use Cases](#use-cases)
5. [MCP Tools for AI Agents](#mcp-tools-for-ai-agents)
6. [Supported File Formats](#supported-file-formats)
7. [Auto-Embed](#auto-embed)
8. [Troubleshooting](#troubleshooting)

---

## Installation

RAG features are included with Cortext by default. All necessary dependencies are installed automatically:

- **fastembed** - Lightweight local embedding model (no PyTorch/CUDA required)
- **chromadb** - Vector database
- **pypdf** - PDF parsing
- **python-docx** - Word document parsing
- **beautifulsoup4** - HTML parsing

### First Run

On first use, the embedding model (`all-MiniLM-L6-v2`) downloads automatically (~25MB). Subsequent runs use cached model.

---

## Quick Start

```bash
# Navigate to workspace
cd ~/my-workspace

# Embed all conversations
cortext embed --all

# Search by meaning
cortext search "authentication patterns" --semantic

# Check embedding status
cortext rag status
```

---

## CLI Commands

### `cortext embed`

Embed documents for semantic search.

```bash
# Embed specific file
cortext embed ./brainstorm/2025-11/001-auth-patterns/

# Embed specific document
cortext embed ./docs/research.pdf

# Embed entire workspace
cortext embed --all
```

**Output:**
```
✓ Embedding complete
  Files embedded: 12
  Files skipped (unchanged): 3
  Total files processed: 15
```

**UPSERT Logic:** Files are only re-embedded if content changes. The system tracks content hashes to avoid redundant work.

### `cortext search`

Search workspace conversations.

```bash
# Keyword search (default)
cortext search "authentication"

# Semantic search
cortext search "login security best practices" --semantic

# Filter by conversation type
cortext search "api design" --semantic --type plan

# Filter by date
cortext search "refactoring" --semantic --date 2025-11

# Limit results
cortext search "database" --semantic --limit 5
```

**Semantic vs Keyword Search:**
- **Keyword**: Fast, exact matches (ripgrep)
- **Semantic**: Meaning-based, finds related concepts

Example:
```bash
# Keyword: finds "authentication"
cortext search "authentication"

# Semantic: finds "login", "JWT", "OAuth", "auth tokens"
cortext search "authentication" --semantic
```

### `cortext rag status`

Show embedding statistics.

```bash
cortext rag status
```

**Output:**
```
RAG Embedding Status

Total Documents    15
Total Chunks       127
Database Path      /home/user/workspace/.workspace/embeddings/chroma

Recent Embeddings

Path                                           Chunks  Embedded At
.../001-auth-patterns/conversation.md          3       2025-11-10T14:30:00
.../002-login-bug/conversation.md              2       2025-11-10T14:31:00
...
```

---

## Use Cases

### Find Related Conversations Before Starting Work

```bash
# Before implementing new auth feature
cortext search "authentication" --semantic --type brainstorm
cortext search "authentication" --semantic --type debug

# Find what was discussed last month
cortext search "performance optimization" --semantic --date 2025-10
```

### Retrieve Context from Past Sessions

```bash
# Find decisions about API design
cortext search "REST API versioning" --semantic --type plan

# Find previous debugging approaches
cortext search "memory leak" --semantic --type debug
```

### Discover Similar Conversations

Use the MCP tools or search with broad queries:

```bash
# Find all discussions about databases
cortext search "database query" --semantic --limit 20
```

### Check Embedding Coverage

```bash
# What's been embedded?
cortext rag status

# Embed any new conversations
cortext embed --all
```

---

## MCP Tools for AI Agents

The RAG pipeline exposes tools for AI assistants:

### `embed_document`

Embed specific file or directory.

```python
# Tool schema
{
    "path": str,           # Path to embed
    "workspace_path": str  # Optional workspace root
}

# Response
{
    "success": True,
    "embedded": 3,
    "skipped": 0,
    "total_files": 3
}
```

### `embed_workspace`

Embed all workspace content.

```python
# Tool schema
{
    "workspace_path": str  # Optional workspace root
}

# Response
{
    "success": True,
    "embedded": 15,
    "skipped": 10
}
```

### `search_semantic`

Semantic search across workspace.

```python
# Tool schema
{
    "query": str,                    # Search text
    "workspace_path": str,           # Optional
    "n_results": int,                # Max results (default 10)
    "conversation_type": str,        # Optional filter
    "date_range": str                # Optional (YYYY-MM or YYYY-MM-DD)
}

# Response
{
    "success": True,
    "query": "authentication",
    "num_results": 3,
    "results": [
        {
            "conversation": "001-auth-patterns",
            "score": 0.85,
            "text": "JWT tokens for stateless auth...",
            "source_path": "brainstorm/2025-11-10/001-auth-patterns/conversation.md"
        }
    ]
}
```

### `get_similar`

Find similar documents.

```python
# Tool schema
{
    "source_path": str,      # Path to source document
    "workspace_path": str,   # Optional
    "n_results": int         # Max results (default 5)
}

# Response
{
    "success": True,
    "source": "brainstorm/.../conversation.md",
    "num_results": 3,
    "similar": [...]
}
```

### `get_embedding_status`

Get embedding statistics.

```python
# Tool schema
{
    "workspace_path": str    # Optional
}

# Response
{
    "success": True,
    "total_chunks": 127,
    "num_documents": 15,
    "db_path": "...",
    "recent_embeddings": [...]
}
```

---

## Supported File Formats

| Format | Extensions | Parser |
|--------|-----------|--------|
| Markdown | `.md`, `.markdown` | Extracts frontmatter, preserves structure |
| Plain Text | `.txt` | Direct text extraction |
| PDF | `.pdf` | Page-by-page text extraction |
| Word | `.docx` | Paragraph extraction |
| HTML | `.html`, `.htm` | Tag stripping, text extraction |

### Chunking

Documents are split into overlapping chunks:
- **Chunk size**: ~512 tokens (approximate)
- **Overlap**: ~50 tokens

This ensures context is preserved at chunk boundaries.

---

## Auto-Embed

Conversations and documents are automatically embedded in two ways:

### 1. On Conversation Creation

When you create a new conversation via bash scripts:
1. Bash script creates conversation directory
2. Calls `auto-embed.sh` hook
3. Embeds the conversation template

### 2. On Every Git Commit (Recommended)

A git post-commit hook automatically embeds changes after each commit:
1. Agent creates/modifies files
2. Agent commits changes
3. Post-commit hook runs `cortext embed --all`
4. Only changed files are re-embedded (UPSERT logic)

This ensures all content is indexed regardless of which AI agent creates it.

### How It Works

The post-commit hook is installed during `cortext init` in `.git/hooks/post-commit`:

```bash
#!/usr/bin/env bash
# Auto-embed after each commit
cortext embed --all 2>/dev/null || true
```

### Disable Auto-Embed

- **Disable post-commit hook:** Remove `.git/hooks/post-commit`
- **Disable conversation creation hook:** Remove `auto-embed.sh` from scripts

### Manual Re-Embed

If auto-embed fails or you modify conversations:

```bash
# Re-embed specific conversation
cortext embed ./brainstorm/2025-11-10/001-auth-patterns/

# Re-embed all (only changed files)
cortext embed --all
```

---

## Troubleshooting

### Verify Dependencies

**Check installation:**
```bash
python -c "import fastembed; import chromadb"
```

If this fails, reinstall Cortext:
```bash
pip install -e /path/to/cortext
```

### Slow First Embedding

**Issue:** First `cortext embed` takes 2-5 seconds.

**Cause:** Model download on first use (~90MB).

**Expectation:** After first load, embeddings are much faster (<100ms per document).

### No Results Found

**Issue:** Semantic search returns no results.

**Checks:**
1. Workspace is embedded: `cortext rag status`
2. Query is reasonable: Try simpler terms
3. Content exists: `cortext search "term"` (keyword)

**Try:**
```bash
# Ensure workspace is embedded
cortext embed --all

# Try broader query
cortext search "your topic" --semantic
```

### Storage Size Concerns

**Issue:** `.workspace/embeddings/` is large.

**Context:**
- Embeddings are 384-dimensional vectors
- Typical: ~1KB per chunk
- 1000 chunks ≈ 1MB storage

**Cleanup:**
```bash
# View size
du -sh .workspace/embeddings/

# Full reindex (if needed)
rm -rf .workspace/embeddings/
cortext embed --all
```

### Corrupted Vector Store

**Issue:** ChromaDB errors or inconsistent results.

**Fix:**
```bash
# Remove and recreate
rm -rf .workspace/embeddings/chroma/
cortext embed --all
```

**Warning:** This re-embeds entire workspace (may take time).

### Performance Tips

1. **Batch embedding**: Use `cortext embed --all` instead of individual files
2. **Avoid re-embedding**: System automatically skips unchanged files
3. **Filter searches**: Use `--type` and `--date` to narrow results
4. **Limit results**: Use `--limit` for faster responses

---

## Technical Details

### Embedding Model

- **Library**: fastembed (lightweight, no PyTorch required)
- **Model**: `all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Size**: ~25MB
- **Performance**: Good balance of speed and quality

### Vector Store

- **Engine**: ChromaDB (persistent)
- **Location**: `.workspace/embeddings/chroma/`
- **Search**: L2 distance with similarity scoring

### Status Tracking

- **File**: `.workspace/embeddings/status.json`
- **Tracks**: Content hash, timestamp, model info
- **Purpose**: UPSERT logic (skip unchanged)

---

## Next Steps

- Run `cortext embed --all` to index your workspace
- Try `cortext search "topic" --semantic` for semantic search
- Use `cortext rag status` to monitor embeddings
- Integrate MCP tools into your AI workflows
