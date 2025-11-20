#!/usr/bin/env bash
# Common utilities for Cortext scripts

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Print functions (output to stderr to avoid interfering with command substitution)
print_success() {
    echo -e "${GREEN}✓ $1${NC}" >&2
}

print_error() {
    echo -e "${RED}✗ $1${NC}" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}" >&2
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}" >&2
}

print_step() {
    echo -e "${BLUE}→ $1${NC}" >&2
}

# Get workspace root
get_workspace_root() {
    if [ -d ".workspace" ]; then
        echo "$(pwd)/.workspace"
    else
        print_error "Not in a Cortext workspace directory"
        print_info "Run 'cortext init' to initialize a workspace"
        exit 1
    fi
}

# Get conversation folder from registry
get_conversation_folder() {
    local conv_type="$1"
    local workspace_root=$(get_workspace_root)
    local registry_file="${workspace_root}/registry.json"

    # Try to read folder from registry
    if [ -f "$registry_file" ]; then
        local folder=$(jq -r ".conversation_types.\"${conv_type}\".folder // \"conversations/${conv_type}\"" "$registry_file" 2>/dev/null)
        echo "$folder"
    else
        # Fallback to type-based folder
        echo "conversations/${conv_type}"
    fi
}

# Ensure we're on main branch (or create it if needed)
ensure_main_branch() {
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

    if [ "$current_branch" != "main" ]; then
        # Check if main exists
        if git show-ref --verify --quiet refs/heads/main; then
            git checkout main 2>/dev/null
        else
            # Create main branch if it doesn't exist
            git checkout -b main 2>/dev/null || git checkout main
        fi
    fi
}

# Create a git tag for conversation start
create_conversation_tag() {
    local conv_name="$1"
    local tag_name="conv/${conv_name}"

    # Create lightweight tag pointing to current commit
    git tag "$tag_name" 2>/dev/null || print_warning "Tag ${tag_name} already exists"
}

# Get next ID (for auto-incrementing conversation IDs)
get_next_id() {
    local conversations_dir="$1"
    local max_id=0

    for dir in "${conversations_dir}"/*/; do
        if [ -d "$dir" ]; then
            local dir_name=$(basename "$dir")
            local id=$(echo "$dir_name" | grep -oE '^[0-9]+' || echo "0")
            if [ "$id" -gt "$max_id" ]; then
                max_id=$id
            fi
        fi
    done

    printf "%03d" $((max_id + 1))
}

# Copy template
copy_template() {
    local template_name="$1"
    local destination="$2"
    local workspace_root=$(get_workspace_root)
    local template_file="${workspace_root}/templates/${template_name}"

    if [ ! -f "$template_file" ]; then
        print_error "Template not found: ${template_name}"
        exit 1
    fi

    cp "$template_file" "$destination"
    print_success "Created: $(basename $destination)"
}

# Update date placeholders
update_date_in_file() {
    local file="$1"
    local current_date=$(date +%Y-%m-%d)

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/\[DATE\]/$current_date/g" "$file"
    else
        sed -i "s/\[DATE\]/$current_date/g" "$file"
    fi
}

# Check git initialized
check_git_initialized() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not a git repository"
        print_info "Initialize git with: git init"
        exit 1
    fi
}

# Display header
show_header() {
    local title="$1"
    echo -e "${CYAN}" >&2
    echo "╔════════════════════════════════════════════════════════════╗" >&2
    echo "║                                                            ║" >&2
    echo "║              🧠 Cortext                                     ║" >&2
    echo "║                                                            ║" >&2
    printf "║              %-46s║\n" "$title" >&2
    echo "║                                                            ║" >&2
    echo "╚════════════════════════════════════════════════════════════╝" >&2
    echo -e "${NC}" >&2
}

# Export functions for use in other scripts
export -f print_success
export -f print_error
export -f print_warning
export -f print_info
export -f print_step
export -f get_workspace_root
export -f get_conversation_folder
export -f ensure_main_branch
export -f create_conversation_tag
export -f get_next_id
export -f copy_template
export -f update_date_in_file
export -f check_git_initialized
export -f show_header
