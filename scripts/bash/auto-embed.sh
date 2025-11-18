#!/usr/bin/env bash
# Cortext Auto-Embed Hook
# Embeds conversation after completion (if RAG is installed)

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Get conversation path from argument
CONVERSATION_PATH="$1"

if [ -z "$CONVERSATION_PATH" ]; then
    # No path provided, skip silently
    exit 0
fi

if [ ! -d "$CONVERSATION_PATH" ]; then
    # Path doesn't exist, skip silently
    exit 0
fi

# Check if cortext command is available
if ! command -v cortext &> /dev/null; then
    # cortext not installed, skip silently
    exit 0
fi

# Check if RAG dependencies are available (test import)
if ! python3 -c "import cortext_rag" 2>/dev/null; then
    # RAG not installed, skip silently
    exit 0
fi

# Auto-embed the conversation
print_info "Auto-embedding conversation..."
cortext embed "$CONVERSATION_PATH" 2>/dev/null || {
    print_warning "Auto-embed failed (non-critical)"
}
