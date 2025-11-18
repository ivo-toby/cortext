"""Shared fixtures for RAG tests."""

import json
import tempfile
from datetime import datetime
from pathlib import Path

import pytest


@pytest.fixture
def sample_workspace(tmp_path):
    """Create a sample workspace with conversations and documents."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # Create workspace structure
    ws_dir = workspace / ".workspace"
    ws_dir.mkdir()
    (ws_dir / "memory").mkdir()
    (ws_dir / "embeddings").mkdir()
    (ws_dir / "templates").mkdir()

    # Create registry
    registry = {
        "conversation_types": {
            "brainstorm": {"folder": "brainstorm"},
            "debug": {"folder": "debug"},
            "plan": {"folder": "plan"},
        }
    }
    (ws_dir / "registry.json").write_text(json.dumps(registry))

    # Create sample brainstorm conversation
    brainstorm_dir = workspace / "brainstorm" / "2025-11-10" / "001-auth-patterns"
    brainstorm_dir.mkdir(parents=True)
    (brainstorm_dir / "conversation.md").write_text(
        """---
title: Authentication Patterns
date: 2025-11-10
type: brainstorm
---

# Authentication Patterns Discussion

## Ideas
- JWT tokens for stateless auth
- OAuth2 for third-party integration
- Session-based for traditional apps

## Considerations
- Security vs usability tradeoffs
- Token expiration strategies
- Refresh token rotation
"""
    )

    # Create sample debug conversation
    debug_dir = workspace / "debug" / "2025-11-10" / "002-login-bug"
    debug_dir.mkdir(parents=True)
    (debug_dir / "conversation.md").write_text(
        """---
title: Login Bug Investigation
date: 2025-11-10
type: debug
---

# Login Bug

## Problem
Users getting 401 errors on login.

## Root Cause
Token validation failing due to clock skew.

## Solution
Add 5-minute tolerance for token expiry checks.
"""
    )

    # Create sample plan conversation
    plan_dir = workspace / "plan" / "2025-11-11" / "003-api-redesign"
    plan_dir.mkdir(parents=True)
    (plan_dir / "conversation.md").write_text(
        """---
title: API Redesign
date: 2025-11-11
type: plan
---

# API Redesign Plan

## Goals
- Improve API consistency
- Better error handling
- OpenAPI documentation

## Tasks
1. Audit current endpoints
2. Define naming conventions
3. Implement versioning
"""
    )

    return workspace


@pytest.fixture
def mock_embedder(mocker):
    """Create mock embedder that returns deterministic vectors."""

    class MockEmbedder:
        model_name = "mock-model"
        embedding_dim = 384

        def embed(self, texts):
            """Return deterministic embeddings based on text hash."""
            embeddings = []
            for text in texts:
                # Create deterministic vector from text hash
                hash_val = hash(text) % (2**32)
                vector = [(hash_val * (i + 1)) % 1000 / 1000.0 for i in range(384)]
                embeddings.append(vector)
            return embeddings

        def embed_single(self, text):
            """Embed single text."""
            return self.embed([text])[0]

    return MockEmbedder()


@pytest.fixture
def temp_chromadb(tmp_path):
    """Create temporary ChromaDB instance."""
    try:
        import chromadb
    except ImportError:
        pytest.skip("chromadb not installed")

    db_path = tmp_path / "chroma"
    db_path.mkdir()
    client = chromadb.PersistentClient(path=str(db_path))
    return client


@pytest.fixture
def sample_markdown_file(tmp_path):
    """Create a sample markdown file."""
    md_file = tmp_path / "sample.md"
    md_file.write_text(
        """---
title: Sample Document
author: Test User
date: 2025-11-10
---

# Sample Document

This is a sample markdown document for testing purposes.

## Section 1

Some content in section 1.

## Section 2

More content in section 2.
"""
    )
    return md_file


@pytest.fixture
def sample_text_file(tmp_path):
    """Create a sample text file."""
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text(
        """This is a plain text file.
It contains multiple lines.
Used for testing the text parser.
"""
    )
    return txt_file


@pytest.fixture
def sample_html_file(tmp_path):
    """Create a sample HTML file."""
    html_file = tmp_path / "sample.html"
    html_file.write_text(
        """<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <h1>Main Heading</h1>
    <p>This is a paragraph.</p>
    <div>
        <p>Nested content here.</p>
    </div>
</body>
</html>
"""
    )
    return html_file
