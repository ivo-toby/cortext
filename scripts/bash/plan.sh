#!/usr/bin/env bash
# Cortext Planning Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Feature Planning"

# Parse arguments
FEATURE="$1"

if [ -z "$FEATURE" ]; then
    print_error "Feature name is required"
    echo "Usage: $0 <feature>" >&2
    echo "Example: $0 \"User authentication\"" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
FEATURE_SLUG=$(echo "$FEATURE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-plan-${FEATURE_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory
mkdir -p "$CONVERSATION_DIR"

# Create git branch
BRANCH_NAME="conversation/${CONVERSATION_NAME}"
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

print_success "Created conversation: ${CONVERSATION_NAME}"
print_info "Branch: ${BRANCH_NAME}"

# Copy template
PLAN_FILE="${CONVERSATION_DIR}/feature-planning.md"
copy_template "feature-planning.md" "$PLAN_FILE"

# Update placeholders
update_date_in_file "$PLAN_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[FEATURE NAME\]/$FEATURE/g" "$PLAN_FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$PLAN_FILE"
else
    sed -i "s/\[FEATURE NAME\]/$FEATURE/g" "$PLAN_FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$PLAN_FILE"
fi

# Initial commit
print_step "Committing planning session..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize feature planning: ${FEATURE}

Created conversation ${CONVERSATION_NAME}.

Type: planning
Purpose: Feature and project planning
" 2>/dev/null || print_warning "Nothing new to commit"

# Display summary
echo "" >&2
print_success "Planning session created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "File: ${PLAN_FILE}"
echo "" >&2
echo -e "${CYAN}Next steps:${NC}" >&2
echo "  1. Open ${PLAN_FILE}" >&2
echo "  2. Define requirements and approach" >&2
echo "  3. Break down into tasks" >&2
echo "" >&2
