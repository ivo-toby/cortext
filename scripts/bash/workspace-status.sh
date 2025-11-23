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
    # Count all conversations across all subfolders (conversations/{type}/YYYY-MM-DD/###-*)
    TOTAL_CONVS=$(find "$CONVERSATIONS_DIR" -mindepth 3 -maxdepth 3 -type d 2>/dev/null | wc -l)
    echo "  Total: ${TOTAL_CONVS}" >&2

    # Count today's conversations across all subfolders
    CURRENT_DAY=$(date +%Y-%m-%d)
    DAY_CONVS=$(find "$CONVERSATIONS_DIR" -mindepth 3 -maxdepth 3 -type d -path "*/${CURRENT_DAY}/*" 2>/dev/null | wc -l)
    if [ "$DAY_CONVS" -gt 0 ]; then
        echo "  Today (${CURRENT_DAY}): ${DAY_CONVS}" >&2
    fi

    # Count this month (aggregate across all subfolders matching YYYY-MM-*)
    CURRENT_MONTH=$(date +%Y-%m)
    MONTH_CONVS=$(find "$CONVERSATIONS_DIR" -mindepth 3 -maxdepth 3 -type d -path "*/${CURRENT_MONTH}*/*" 2>/dev/null | wc -l)
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
    find "$CONVERSATIONS_DIR" -mindepth 3 -maxdepth 3 -type d 2>/dev/null | sort -r | head -5 | while read conv_dir; do
        CONV_NAME=$(basename "$conv_dir")
        echo "  - ${CONV_NAME}" >&2
    done
else
    echo "  None" >&2
fi

echo "" >&2

# Resumable conversations (with session state)
echo -e "${CYAN}Resumable Sessions:${NC}" >&2
PARENT_DIR=$(dirname "$WORKSPACE_ROOT")
SESSION_COUNT=$(find "$PARENT_DIR" -path "*/.session/session.json" -type f 2>/dev/null | wc -l)

if [ "$SESSION_COUNT" -gt 0 ]; then
    # Count by status
    ACTIVE_COUNT=0
    PAUSED_COUNT=0
    COMPLETED_COUNT=0

    while read session_file; do
        STATUS=$(jq -r '.status // "unknown"' "$session_file" 2>/dev/null)
        case "$STATUS" in
            active) ACTIVE_COUNT=$((ACTIVE_COUNT + 1)) ;;
            paused) PAUSED_COUNT=$((PAUSED_COUNT + 1)) ;;
            completed) COMPLETED_COUNT=$((COMPLETED_COUNT + 1)) ;;
        esac
    done < <(find "$PARENT_DIR" -path "*/.session/session.json" -type f 2>/dev/null)

    echo "  Total: ${SESSION_COUNT}" >&2
    [ "$ACTIVE_COUNT" -gt 0 ] && echo "  Active: ${ACTIVE_COUNT}" >&2
    [ "$PAUSED_COUNT" -gt 0 ] && echo "  Paused: ${PAUSED_COUNT}" >&2
    [ "$COMPLETED_COUNT" -gt 0 ] && echo "  Completed: ${COMPLETED_COUNT}" >&2

    # Show most recent resumable
    echo "" >&2
    echo "  Most recent:" >&2
    find "$PARENT_DIR" -path "*/.session/session.json" -type f 2>/dev/null | while read session_file; do
        CONV_ID=$(jq -r '.conversation_id' "$session_file" 2>/dev/null)
        STATUS=$(jq -r '.status' "$session_file" 2>/dev/null)
        LAST_ACTIVE=$(jq -r '.last_active' "$session_file" 2>/dev/null)
        echo "    - ${CONV_ID} (${STATUS})" >&2
    done | head -3
else
    echo "  No resumable sessions" >&2
    echo "  [dim]Use /workspace.stop-conversation to save sessions[/dim]" >&2
fi

echo "" >&2
