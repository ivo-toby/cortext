#!/usr/bin/env bash
# Cortext Project Management Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Project Management"

# Parse arguments
PROJECT="$1"

if [ -z "$PROJECT" ]; then
    print_error "Project name is required"
    echo "Usage: $0 <project>" >&2
    echo "Example: $0 \"Cortext Development\"" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
FOLDER=$(get_conversation_folder "projectmanage")
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
PROJECT_SLUG=$(echo "$PROJECT" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-projectmanage-${PROJECT_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory and docs subfolder
mkdir -p "$CONVERSATION_DIR"
mkdir -p "$CONVERSATION_DIR/docs"

# Ensure we're on main branch
ensure_main_branch

print_success "Created conversation: ${CONVERSATION_NAME}"

# Copy master template
PROJECT_FILE="${CONVERSATION_DIR}/project-management.md"
copy_template "project-management.md" "$PROJECT_FILE"

# Update placeholders in master template
update_date_in_file "$PROJECT_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[PROJECT NAME\]/$PROJECT/g" "$PROJECT_FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$PROJECT_FILE"
else
    sed -i "s/\[PROJECT NAME\]/$PROJECT/g" "$PROJECT_FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$PROJECT_FILE"
fi

# Copy index template
INDEX_FILE="${CONVERSATION_DIR}/index.md"
copy_template "project-index.md" "$INDEX_FILE"

# Update placeholders in index template
update_date_in_file "$INDEX_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[PROJECT NAME\]/$PROJECT/g" "$INDEX_FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$INDEX_FILE"
else
    sed -i "s/\[PROJECT NAME\]/$PROJECT/g" "$INDEX_FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$INDEX_FILE"
fi

# Initial commit
print_step "Committing project management session..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize project management: ${PROJECT}

Created conversation ${CONVERSATION_NAME}.

Type: project-management
Purpose: Project tracking and documentation
" 2>/dev/null || print_warning "Nothing new to commit"

# Create conversation tag
create_conversation_tag "$CONVERSATION_NAME"

# Dispatch conversation:create hook
dispatch_hook "conversation:create" "$CONVERSATION_DIR"

# Display summary
echo "" >&2
print_success "Project management session created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "Master file: ${PROJECT_FILE}"
print_info "Index file: ${INDEX_FILE}"
print_info "Docs folder: ${CONVERSATION_DIR}/docs/"
echo "" >&2
echo -e "${CYAN}Next steps:${NC}" >&2
echo "  1. Define project goals and roadmap" >&2
echo "  2. Add tasks and track status" >&2
echo "  3. Create documents in docs/ subfolder" >&2
echo "" >&2
