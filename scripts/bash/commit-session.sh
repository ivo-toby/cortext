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

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    print_info "No changes to commit"
    exit 0
fi

# Add all changes in conversations directory
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations"
git add "${CONVERSATIONS_DIR}" 2>/dev/null || true

# Check if anything was staged
if git diff --cached --quiet; then
    print_info "No conversation changes to commit"
    exit 0
fi

print_step "Committing conversation session..."

# Create commit message
COMMIT_MSG="[conversation] Update session

Auto-commit from session"

# Commit
if git commit -m "$COMMIT_MSG" 2>/dev/null; then
    print_success "Session committed"
else
    print_warning "Nothing to commit or commit failed"
fi
