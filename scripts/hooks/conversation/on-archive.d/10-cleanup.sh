#!/usr/bin/env bash
# Default hook: Clean up when conversation is archived
# Runs after a conversation is archived

# Get conversation path from argument
CONVERSATION_PATH="$1"

if [ -z "$CONVERSATION_PATH" ]; then
    exit 0
fi

# Future: Remove from active search index, update stats, etc.
# For now, this is a placeholder that does nothing

exit 0
