#!/usr/bin/env bash
# Cortext Brainstorm Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Brainstorming Session"

# Parse arguments
TOPIC="$1"

if [ -z "$TOPIC" ]; then
    print_error "Topic is required"
    echo "Usage: $0 <topic>" >&2
    echo "Example: $0 \"New Feature Ideas\"" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
FOLDER=$(get_conversation_folder "brainstorm")
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-brainstorm-${TOPIC_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory
mkdir -p "$CONVERSATION_DIR"

# Create git branch
BRANCH_NAME="conversation/${CONVERSATION_NAME}"
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

print_success "Created conversation: ${CONVERSATION_NAME}"
print_info "Branch: ${BRANCH_NAME}"

# Copy template
BRAINSTORM_FILE="${CONVERSATION_DIR}/brainstorm.md"
copy_template "brainstorm.md" "$BRAINSTORM_FILE"

# Update placeholders
update_date_in_file "$BRAINSTORM_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[TOPIC\]/$TOPIC/g" "$BRAINSTORM_FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$BRAINSTORM_FILE"
else
    sed -i "s/\[TOPIC\]/$TOPIC/g" "$BRAINSTORM_FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$BRAINSTORM_FILE"
fi

# Initial commit
print_step "Committing brainstorm session..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize brainstorm: ${TOPIC}

Created conversation ${CONVERSATION_NAME}.

Type: brainstorm
Purpose: Ideation and exploration
" 2>/dev/null || print_warning "Nothing new to commit"

# Auto-embed for RAG (if available)
if [ -f "${SCRIPT_DIR}/auto-embed.sh" ]; then
    "${SCRIPT_DIR}/auto-embed.sh" "$CONVERSATION_DIR" 2>/dev/null || true
fi

# Display summary
echo "" >&2
print_success "Brainstorm session created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "File: ${BRAINSTORM_FILE}"
echo "" >&2
echo -e "${CYAN}Next steps:${NC}" >&2
echo "  1. Open ${BRAINSTORM_FILE}" >&2
echo "  2. Capture ideas freely" >&2
echo "  3. Commit regularly with git" >&2
echo "" >&2
