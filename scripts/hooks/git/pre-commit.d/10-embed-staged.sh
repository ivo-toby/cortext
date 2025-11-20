#!/usr/bin/env bash
# Default hook: Embed staged markdown files before commit
# Runs as part of git pre-commit

# Graceful degradation - exit silently if dependencies missing
if ! command -v cortext &> /dev/null; then
    exit 0
fi

# Check if RAG dependencies are available
if ! python3 -c "import cortext_rag" 2>/dev/null; then
    exit 0
fi

# Get staged markdown files (added or modified)
staged_files=$(git diff --cached --name-only --diff-filter=AM -- '*.md' 2>/dev/null)

if [ -z "$staged_files" ]; then
    exit 0
fi

# Embed each staged file
for file in $staged_files; do
    if [ -f "$file" ]; then
        cortext embed "$file" 2>/dev/null || true
    fi
done

exit 0
