#!/usr/bin/env bash
# Cortext Workspace Status Script
# Show current workspace state

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Workspace Status"

# Check if we're in a workspace
WORKSPACE_ROOT=$(get_workspace_root)

# Git status
echo -e "${CYAN}Git Status:${NC}" >&2
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
echo "  Branch: ${BRANCH_NAME}" >&2

# Check for uncommitted changes
if git diff --quiet && git diff --cached --quiet; then
    print_success "Working tree clean"
else
    print_warning "Uncommitted changes present"
    git status --short
fi

echo "" >&2

# Conversation count
echo -e "${CYAN}Conversations:${NC}" >&2
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations"
if [ -d "$CONVERSATIONS_DIR" ]; then
    TOTAL_CONVS=$(find "$CONVERSATIONS_DIR" -mindepth 2 -maxdepth 2 -type d | wc -l)
    echo "  Total: ${TOTAL_CONVS}" >&2

    # This day and month
    CURRENT_DAY=$(date +%Y-%m-%d)
    DAY_DIR="${CONVERSATIONS_DIR}/${CURRENT_DAY}"
    if [ -d "$DAY_DIR" ]; then
        DAY_CONVS=$(find "$DAY_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
        echo "  Today (${CURRENT_DAY}): ${DAY_CONVS}" >&2
    fi

    # Count this month (aggregate of all YYYY-MM-* directories)
    CURRENT_MONTH=$(date +%Y-%m)
    MONTH_CONVS=$(find "$CONVERSATIONS_DIR" -mindepth 1 -maxdepth 1 -type d -name "${CURRENT_MONTH}*" -exec find {} -mindepth 1 -maxdepth 1 -type d \; 2>/dev/null | wc -l)
    if [ "$MONTH_CONVS" -gt 0 ]; then
        echo "  This month (${CURRENT_MONTH}): ${MONTH_CONVS}" >&2
    fi
else
    echo "  No conversations yet" >&2
fi

echo "" >&2

# Registry info
REGISTRY_FILE="${WORKSPACE_ROOT}/registry.json"
if [ -f "$REGISTRY_FILE" ]; then
    echo -e "${CYAN}Conversation Types:${NC}" >&2
    BUILTIN_COUNT=$(grep -o '"built_in": true' "$REGISTRY_FILE" | wc -l)
    CUSTOM_COUNT=$(grep -o '"built_in": false' "$REGISTRY_FILE" | wc -l)
    echo "  Built-in: ${BUILTIN_COUNT}" >&2
    echo "  Custom: ${CUSTOM_COUNT}" >&2
fi

echo "" >&2

# Recent conversations
echo -e "${CYAN}Recent Conversations:${NC}" >&2
if [ -d "$CONVERSATIONS_DIR" ]; then
    find "$CONVERSATIONS_DIR" -mindepth 2 -maxdepth 2 -type d | sort -r | head -5 | while read conv_dir; do
        CONV_NAME=$(basename "$conv_dir")
        echo "  - ${CONV_NAME}" >&2
    done
else
    echo "  None" >&2
fi

echo "" >&2
