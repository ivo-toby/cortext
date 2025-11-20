#!/usr/bin/env bash
# Cortext Hook Dispatcher
# Routes events to appropriate hook scripts in .d/ directories

set -e

# Get the workspace root (where .workspace is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="${SCRIPT_DIR%/.workspace/hooks}"

# Parse event name (format: category:action)
EVENT="$1"
shift || true

if [ -z "$EVENT" ]; then
    echo "Usage: dispatch.sh <event> [args...]" >&2
    echo "Example: dispatch.sh conversation:create /path/to/conv" >&2
    exit 1
fi

# Split event into category and action
CATEGORY="${EVENT%%:*}"
ACTION="${EVENT##*:}"

# Handle git hooks (no colon separator)
if [ "$CATEGORY" = "$ACTION" ]; then
    # It's a git hook like "pre-commit" or "post-checkout"
    HOOK_DIR="${SCRIPT_DIR}/git/${EVENT}.d"
else
    # It's a lifecycle hook like "conversation:create"
    HOOK_DIR="${SCRIPT_DIR}/${CATEGORY}/on-${ACTION}.d"
fi

# Check if hook directory exists
if [ ! -d "$HOOK_DIR" ]; then
    # No hooks configured for this event - exit silently
    exit 0
fi

# Debug output if enabled
if [ "${CORTEXT_HOOKS_DEBUG:-0}" = "1" ]; then
    echo "[hooks] Dispatching event: $EVENT" >&2
    echo "[hooks] Hook directory: $HOOK_DIR" >&2
fi

# Execute all scripts in the .d directory in alphanumeric order
for script in "$HOOK_DIR"/*.sh; do
    # Skip if no scripts found (glob returns literal pattern)
    [ -e "$script" ] || continue

    # Skip non-executable scripts
    if [ ! -x "$script" ]; then
        if [ "${CORTEXT_HOOKS_DEBUG:-0}" = "1" ]; then
            echo "[hooks] Skipping non-executable: $script" >&2
        fi
        continue
    fi

    if [ "${CORTEXT_HOOKS_DEBUG:-0}" = "1" ]; then
        echo "[hooks] Running: $(basename "$script")" >&2
    fi

    # Execute script with all remaining arguments
    # If script fails, stop execution and return its exit code
    "$script" "$@" || exit $?
done

exit 0
