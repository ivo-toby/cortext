#!/usr/bin/env bash
# Default hook: Rebuild embeddings if needed after checkout
# Runs as part of git post-checkout

# Graceful degradation - exit silently if dependencies missing
if ! command -v cortext &> /dev/null; then
    exit 0
fi

# Check if RAG dependencies are available
if ! python3 -c "import cortext_rag" 2>/dev/null; then
    exit 0
fi

# Check if this is a branch checkout (not a file checkout)
# $3 is 1 for branch checkout, 0 for file checkout
if [ "${3:-1}" = "0" ]; then
    exit 0
fi

# Check if embedding data exists
# If not, suggest rebuilding (don't auto-rebuild as it can be slow)
if [ ! -d ".cortext_rag" ]; then
    echo "Cortext: No embedding data found. Run 'cortext embed --all' to build search index." >&2
fi

exit 0
