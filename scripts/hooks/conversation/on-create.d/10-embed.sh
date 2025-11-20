#!/usr/bin/env bash
# Default hook: Embed conversation for RAG search
# Runs after a conversation is created

# Graceful degradation - exit silently if dependencies missing
if ! command -v cortext &> /dev/null; then
    exit 0
fi

# Check if RAG dependencies are available
if ! python3 -c "import cortext_rag" 2>/dev/null; then
    exit 0
fi

# Get conversation path from argument
CONVERSATION_PATH="$1"

if [ -z "$CONVERSATION_PATH" ]; then
    exit 0
fi

if [ ! -d "$CONVERSATION_PATH" ]; then
    exit 0
fi

# Embed the conversation
cortext embed "$CONVERSATION_PATH" 2>/dev/null || true

exit 0
