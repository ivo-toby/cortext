#!/usr/bin/env bash
# Cortext Session Commit Script
# Automatically commit the current conversation session

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Check if we're in a workspace
WORKSPACE_ROOT=$(get_workspace_root)

# Check if git is initialized
check_git_initialized

# Get current branch
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

if [ -z "$BRANCH_NAME" ] || [ "$BRANCH_NAME" = "main" ]; then
    print_warning "Not on a conversation branch, nothing to commit"
    exit 0
fi

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    print_info "No changes to commit"
    exit 0
fi

# Extract conversation info from branch name
CONV_ID=$(echo "$BRANCH_NAME" | sed 's|^conversation/||')
CONV_TYPE=$(echo "$CONV_ID" | grep -oE '[0-9]+-([a-z]+)-' | sed 's/-$//' | sed 's/^[0-9]*-//')

print_step "Committing session for: ${CONV_ID}"

# Add all changes in conversations directory
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations"
git add "${CONVERSATIONS_DIR}" 2>/dev/null || true

# Create commit message
COMMIT_MSG="[conversation] Update ${CONV_TYPE} session

Conversation: ${CONV_ID}
Auto-commit from session"

# Commit
if git commit -m "$COMMIT_MSG" 2>/dev/null; then
    print_success "Session committed"
else
    print_warning "Nothing to commit or commit failed"
fi
