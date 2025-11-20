#!/usr/bin/env bash
# Cortext Review Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Review Session"

# Parse arguments
REVIEW_TITLE="$1"

if [ -z "$REVIEW_TITLE" ]; then
    print_error "Review title is required"
    echo "Usage: $0 <review-title>" >&2
    echo "Example: $0 \"API design review\"" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
FOLDER=$(get_conversation_folder "review")
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
REVIEW_SLUG=$(echo "$REVIEW_TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-review-${REVIEW_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory
mkdir -p "$CONVERSATION_DIR"

# Create git branch
BRANCH_NAME="conversation/${CONVERSATION_NAME}"
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

print_success "Created conversation: ${CONVERSATION_NAME}"
print_info "Branch: ${BRANCH_NAME}"

# Copy template
REVIEW_FILE="${CONVERSATION_DIR}/review.md"
copy_template "review-template.md" "$REVIEW_FILE"

# Update placeholders
update_date_in_file "$REVIEW_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[TITLE\]/$REVIEW_TITLE/g" "$REVIEW_FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$REVIEW_FILE"
else
    sed -i "s/\[TITLE\]/$REVIEW_TITLE/g" "$REVIEW_FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$REVIEW_FILE"
fi

# Initial commit
print_step "Committing review session..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize review: ${REVIEW_TITLE}

Created conversation ${CONVERSATION_NAME}.

Type: review
Purpose: Code and design review
" 2>/dev/null || print_warning "Nothing new to commit"

# Dispatch conversation:create hook
dispatch_hook "conversation:create" "$CONVERSATION_DIR"

# Display summary
echo "" >&2
print_success "Review session created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "File: ${REVIEW_FILE}"
echo "" >&2
echo -e "${CYAN}Next steps:${NC}" >&2
echo "  1. Open ${REVIEW_FILE}" >&2
echo "  2. Document what's being reviewed" >&2
echo "  3. Provide detailed feedback" >&2
echo "" >&2
