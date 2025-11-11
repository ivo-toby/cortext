#!/usr/bin/env bash
# Cortext Debug Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Debug Session"

# Parse arguments
ISSUE="$1"

if [ -z "$ISSUE" ]; then
    print_error "Issue description is required"
    echo "Usage: $0 <issue>" >&2
    echo "Example: $0 \"API authentication failing\"" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
FOLDER=$(get_conversation_folder "debug")
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
ISSUE_SLUG=$(echo "$ISSUE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-debug-${ISSUE_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory
mkdir -p "$CONVERSATION_DIR"

# Create git branch
BRANCH_NAME="conversation/${CONVERSATION_NAME}"
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

print_success "Created conversation: ${CONVERSATION_NAME}"
print_info "Branch: ${BRANCH_NAME}"

# Copy template
DEBUG_FILE="${CONVERSATION_DIR}/debug-session.md"
copy_template "debug-session.md" "$DEBUG_FILE"

# Update placeholders
update_date_in_file "$DEBUG_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[ISSUE\]/$ISSUE/g" "$DEBUG_FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$DEBUG_FILE"
else
    sed -i "s/\[ISSUE\]/$ISSUE/g" "$DEBUG_FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$DEBUG_FILE"
fi

# Initial commit
print_step "Committing debug session..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize debug: ${ISSUE}

Created conversation ${CONVERSATION_NAME}.

Type: debug
Purpose: Problem solving and troubleshooting
" 2>/dev/null || print_warning "Nothing new to commit"

# Display summary
echo "" >&2
print_success "Debug session created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "File: ${DEBUG_FILE}"
echo "" >&2
echo -e "${CYAN}Next steps:${NC}" >&2
echo "  1. Open ${DEBUG_FILE}" >&2
echo "  2. Document the problem and investigation" >&2
echo "  3. Commit findings and solutions" >&2
echo "" >&2
