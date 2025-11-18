#!/usr/bin/env bash
# Cortext Meeting Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Meeting Notes"

# Parse arguments
MEETING="$1"

if [ -z "$MEETING" ]; then
    print_error "Meeting title is required"
    echo "Usage: $0 <meeting-title>" >&2
    echo "Example: $0 \"Sprint planning\"" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
FOLDER=$(get_conversation_folder "meeting")
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
MEETING_SLUG=$(echo "$MEETING" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-meeting-${MEETING_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory
mkdir -p "$CONVERSATION_DIR"

# Create git branch
BRANCH_NAME="conversation/${CONVERSATION_NAME}"
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

print_success "Created conversation: ${CONVERSATION_NAME}"
print_info "Branch: ${BRANCH_NAME}"

# Copy template
MEETING_FILE="${CONVERSATION_DIR}/meeting-notes.md"
copy_template "meeting-notes.md" "$MEETING_FILE"

# Update placeholders
update_date_in_file "$MEETING_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[MEETING TITLE\]/$MEETING/g" "$MEETING_FILE"
    sed -i '' "s/\[ID\]/$MEETING_SLUG/g" "$MEETING_FILE"
else
    sed -i "s/\[MEETING TITLE\]/$MEETING/g" "$MEETING_FILE"
    sed -i "s/\[ID\]/$MEETING_SLUG/g" "$MEETING_FILE"
fi

# Initial commit
print_step "Committing meeting notes..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize meeting: ${MEETING}

Created conversation ${CONVERSATION_NAME}.

Type: meeting
Purpose: Meeting notes and action items
" 2>/dev/null || print_warning "Nothing new to commit"

# Auto-embed for RAG (if available)
if [ -f "${SCRIPT_DIR}/auto-embed.sh" ]; then
    "${SCRIPT_DIR}/auto-embed.sh" "$CONVERSATION_DIR" 2>/dev/null || true
fi

# Display summary
echo "" >&2
print_success "Meeting notes created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "File: ${MEETING_FILE}"
echo "" >&2
echo -e "${CYAN}Next steps:${NC}" >&2
echo "  1. Open ${MEETING_FILE}" >&2
echo "  2. Fill in attendees and agenda" >&2
echo "  3. Take notes during meeting" >&2
echo "" >&2
