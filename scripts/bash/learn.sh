#!/usr/bin/env bash
# Cortext Learning Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Learning Session"

# Parse arguments
TOPIC="$1"

if [ -z "$TOPIC" ]; then
    print_error "Learning topic is required"
    echo "Usage: $0 <topic>" >&2
    echo "Example: $0 \"Kubernetes networking\"" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
FOLDER=$(get_conversation_folder "learn")
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-learn-${TOPIC_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory
mkdir -p "$CONVERSATION_DIR"

# Ensure we're on main branch
ensure_main_branch

print_success "Created conversation: ${CONVERSATION_NAME}"

# Initialize session for resumption support
init_session "$CONVERSATION_DIR" "$CONVERSATION_NAME" "learn" "/workspace.learn"

# Copy template
LEARN_FILE="${CONVERSATION_DIR}/learning-notes.md"
copy_template "learning-notes.md" "$LEARN_FILE"

# Update placeholders
update_date_in_file "$LEARN_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[TOPIC\]/$TOPIC/g" "$LEARN_FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$LEARN_FILE"
else
    sed -i "s/\[TOPIC\]/$TOPIC/g" "$LEARN_FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$LEARN_FILE"
fi

# Initial commit
print_step "Committing learning session..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize learning: ${TOPIC}

Created conversation ${CONVERSATION_NAME}.

Type: learning
Purpose: Learning notes and documentation
" 2>/dev/null || print_warning "Nothing new to commit"

# Create conversation tag
create_conversation_tag "$CONVERSATION_NAME"

# Dispatch conversation:create hook
dispatch_hook "conversation:create" "$CONVERSATION_DIR"

# Display summary
echo "" >&2
print_success "Learning session created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "File: ${LEARN_FILE}"
echo "" >&2
echo -e "${CYAN}Next steps:${NC}" >&2
echo "  1. Open ${LEARN_FILE}" >&2
echo "  2. Take notes as you learn" >&2
echo "  3. Document key concepts and examples" >&2
echo "" >&2
