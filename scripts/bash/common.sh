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

# Dispatch hook event to the hooks system
dispatch_hook() {
    local event="$1"
    shift || true

    local workspace_root
    workspace_root=$(get_workspace_root 2>/dev/null) || return 0

    local dispatcher="${workspace_root}/hooks/dispatch.sh"

    # Silently succeed if dispatcher doesn't exist
    if [ ! -x "$dispatcher" ]; then
        return 0
    fi

    # Call dispatcher with event and arguments
    "$dispatcher" "$event" "$@" || true
}

# ============================================================================
# Session Management Utilities
# ============================================================================
# These utilities manage conversation session state for resumption.
#
# Session storage structure (per conversation):
#   .session/
#     session.json    - Metadata, agent config, status
#     messages.jsonl  - Chat history (JSON Lines format)
#
# session.json schema:
# {
#   "version": "1.0",
#   "conversation_id": "001-brainstorm-topic",
#   "conversation_type": "brainstorm",
#   "status": "active|paused|completed",
#   "created_at": "ISO8601",
#   "last_active": "ISO8601",
#   "message_count": number,
#   "agent_config": {
#     "command": "/workspace.brainstorm",
#     "system_prompt_hash": "sha256:...",
#     "model": "model-id",
#     "tools": ["tool1", "tool2"]
#   },
#   "context_summary": "Brief description of conversation state"
# }
# ============================================================================

# Get session directory path for a conversation
get_session_path() {
    local conversation_dir="$1"
    echo "${conversation_dir}/.session"
}

# Initialize session directory for a conversation
init_session() {
    local conversation_dir="$1"
    local conversation_id="$2"
    local conversation_type="$3"
    local command="$4"

    local session_dir=$(get_session_path "$conversation_dir")
    mkdir -p "$session_dir"

    local current_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Create initial session.json
    cat > "${session_dir}/session.json" << EOF
{
  "version": "1.0",
  "conversation_id": "${conversation_id}",
  "conversation_type": "${conversation_type}",
  "status": "active",
  "created_at": "${current_time}",
  "last_active": "${current_time}",
  "message_count": 0,
  "agent_config": {
    "command": "${command}",
    "system_prompt_hash": "",
    "model": "",
    "tools": []
  },
  "context_summary": ""
}
EOF

    # Create empty messages file
    touch "${session_dir}/messages.jsonl"

    print_success "Session initialized"
}

# Update session metadata
update_session() {
    local conversation_dir="$1"
    local status="$2"
    local message_count="$3"
    local context_summary="$4"

    local session_file="$(get_session_path "$conversation_dir")/session.json"

    if [ ! -f "$session_file" ]; then
        print_warning "No session file found"
        return 1
    fi

    local current_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Update session.json using jq
    local tmp_file=$(mktemp)
    jq --arg status "$status" \
       --arg last_active "$current_time" \
       --arg message_count "$message_count" \
       --arg summary "$context_summary" \
       '.status = $status | .last_active = $last_active | .message_count = ($message_count | tonumber) | .context_summary = $summary' \
       "$session_file" > "$tmp_file" && mv "$tmp_file" "$session_file"
}

# Append message to session history
append_message() {
    local conversation_dir="$1"
    local role="$2"
    local content="$3"

    local messages_file="$(get_session_path "$conversation_dir")/messages.jsonl"
    local current_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Escape content for JSON
    local escaped_content=$(echo "$content" | jq -Rs '.')

    # Append message as JSON line
    echo "{\"role\":\"${role}\",\"content\":${escaped_content},\"timestamp\":\"${current_time}\"}" >> "$messages_file"
}

# Load session metadata
load_session() {
    local conversation_dir="$1"
    local session_file="$(get_session_path "$conversation_dir")/session.json"

    if [ -f "$session_file" ]; then
        cat "$session_file"
    else
        echo "{}"
    fi
}

# Check if conversation has session state
has_session() {
    local conversation_dir="$1"
    local session_file="$(get_session_path "$conversation_dir")/session.json"

    [ -f "$session_file" ]
}

# Get session status
get_session_status() {
    local conversation_dir="$1"
    local session_file="$(get_session_path "$conversation_dir")/session.json"

    if [ -f "$session_file" ]; then
        jq -r '.status // "unknown"' "$session_file"
    else
        echo "none"
    fi
}

# List all conversations with session state
list_sessions() {
    local workspace_root=$(get_workspace_root)
    local parent_dir=$(dirname "$workspace_root")

    # Find all session.json files
    find "$parent_dir" -path "*/.session/session.json" -type f 2>/dev/null | while read session_file; do
        local conv_dir=$(dirname $(dirname "$session_file"))
        local session_data=$(cat "$session_file")

        local conv_id=$(echo "$session_data" | jq -r '.conversation_id')
        local conv_type=$(echo "$session_data" | jq -r '.conversation_type')
        local status=$(echo "$session_data" | jq -r '.status')
        local last_active=$(echo "$session_data" | jq -r '.last_active')
        local summary=$(echo "$session_data" | jq -r '.context_summary')

        # Output as JSON for easy parsing
        jq -n \
            --arg dir "$conv_dir" \
            --arg id "$conv_id" \
            --arg type "$conv_type" \
            --arg status "$status" \
            --arg last_active "$last_active" \
            --arg summary "$summary" \
            '{dir: $dir, id: $id, type: $type, status: $status, last_active: $last_active, summary: $summary}'
    done
}

# Export functions for use in other scripts (bash only)
# Note: export -f is bash-specific and will fail in zsh/sh
if [ -n "$BASH_VERSION" ]; then
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
    export -f dispatch_hook
    # Session management
    export -f get_session_path
    export -f init_session
    export -f update_session
    export -f append_message
    export -f load_session
    export -f has_session
    export -f get_session_status
    export -f list_sessions
fi
