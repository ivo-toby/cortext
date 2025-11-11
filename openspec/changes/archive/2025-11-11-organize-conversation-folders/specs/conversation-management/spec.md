# Spec Delta: Conversation Management

**Capability:** conversation-management
**Change ID:** organize-conversation-folders

---

## MODIFIED Requirements

### Requirement: Conversation folders SHALL be organized by conversation type
Conversations SHALL be organized into subfolders under `conversations/` where each conversation type has its own folder matching the type name, with folder locations configurable via the registry.

**ID:** `CONV-FOLDER-001` | **Priority:** High

#### Scenario: Brainstorm conversation saves to brainstorm subfolder

**Given** a user creates a brainstorm conversation
**When** they run `brainstorm.sh "New Feature Ideas"`
**Then** the conversation MUST be created in `conversations/brainstorm/YYYY-MM-DD/###-brainstorm-topic/`
**And** the folder structure MUST follow the pattern: `{folder}/{date}/{id}-{type}-{topic}/`

**Example:**
```bash
./scripts/bash/brainstorm.sh "Product Improvements"
# Creates: conversations/brainstorm/2025-11-10/001-brainstorm-product-improvements/
```

#### Scenario: Learn conversation saves to learn subfolder

**Given** a user creates a learn conversation
**When** they run `learn.sh "Kubernetes Networking"`
**Then** the conversation MUST be created in `conversations/learn/YYYY-MM-DD/###-learn-topic/`

**Example:**
```bash
./scripts/bash/learn.sh "Kubernetes Networking"
# Creates: conversations/learn/2025-11-10/001-learn-kubernetes-networking/
```

#### Scenario: Each conversation type has its own subfolder

**Given** a user creates debug, plan, meeting, or review conversations
**When** they run any of these conversation scripts
**Then** the conversation MUST be created in `conversations/{type}/YYYY-MM-DD/###-type-topic/`

**Example:**
```bash
./scripts/bash/debug.sh "Auth Bug"
# Creates: conversations/debug/2025-11-10/001-debug-auth-bug/

./scripts/bash/plan.sh "Redesign API"
# Creates: conversations/plan/2025-11-10/002-plan-redesign-api/
```

---

### Requirement: Conversation ID SHALL increment per subfolder
Conversation IDs SHALL increment independently within each subfolder-date combination.

**ID:** `CONV-FOLDER-002` | **Priority:** Medium

#### Scenario: IDs increment per subfolder

**Given** conversations exist in multiple subfolders on the same day
**When** a new conversation is created in each subfolder
**Then** each subfolder MUST maintain its own ID sequence

**Example:**
```bash
# Same day, different subfolders
conversations/brainstorm/2025-11-10/001-brainstorm-feature-a/
conversations/brainstorm/2025-11-10/002-brainstorm-feature-b/
conversations/learn/2025-11-10/001-learn-topic-x/
conversations/debug/2025-11-10/001-debug-issue/
```

---

## ADDED Requirements

### Requirement: Folder location MUST be configurable via registry
Each conversation type SHALL have a `folder` field in the registry specifying where conversations of that type are stored.

**ID:** `CONV-FOLDER-003` | **Priority:** High

#### Scenario: Registry specifies folder for conversation type

**Given** a conversation type is registered
**When** the registry entry is created
**Then** it MUST include a `folder` field specifying the base path
**And** bash scripts MUST read this folder field to determine save location

**Example:**
```json
{
  "brainstorm": {
    "name": "Brainstorm",
    "folder": "conversations/brainstorm",
    "template": ".workspace/templates/brainstorm.md",
    "command": "/workspace.brainstorm",
    ...
  }
}
```

#### Scenario: Bash script reads folder from registry

**Given** a conversation script is executed
**When** it needs to determine where to save the conversation
**Then** it MUST read the `folder` field from registry.json for that conversation type
**And** it MUST use that folder as the base path
**And** it MUST append the date (YYYY-MM-DD) to create the full path

**Implementation:**
```bash
# In bash scripts
FOLDER=$(get_conversation_folder "brainstorm")
# Returns: conversations/brainstorm

CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
# Results in: conversations/brainstorm/2025-11-10/
```

#### Scenario: User overrides folder in registry

**Given** a user wants a conversation type to save to a different folder
**When** they edit the `folder` field in registry.json
**Then** new conversations of that type MUST use the custom folder
**And** existing conversations MUST remain in their original location

**Example:**
```json
{
  "learn": {
    "folder": "research/learning",  // Custom override
    ...
  }
}
```

---

### Requirement: Folder resolution SHALL have sensible defaults
Bash scripts SHALL provide default folder mappings if registry lookup fails.

**ID:** `CONV-FOLDER-004` | **Priority:** Medium

#### Scenario: Fallback to default folder

**Given** a conversation script cannot read the folder from registry
**When** it attempts to determine the save location
**Then** it SHALL fall back to `conversations/general`
**And** it SHALL log a warning about the fallback

**Example:**
```bash
# If registry.json missing or corrupted
FOLDER=$(get_conversation_folder "brainstorm")
# Falls back to: conversations/general
# Logs: "Warning: Could not read folder from registry, using default"
```

---

## Implementation Notes

### Default Folder Mappings

Add to initial registry creation (`init.py`):

| Type | Folder | Rationale |
|------|--------|-----------|
| brainstorm | `conversations/brainstorm` | Type name = folder name (low cognitive load) |
| debug | `conversations/debug` | Type name = folder name (low cognitive load) |
| plan | `conversations/plan` | Type name = folder name (low cognitive load) |
| learn | `conversations/learn` | Type name = folder name (low cognitive load) |
| meeting | `conversations/meeting` | Type name = folder name (low cognitive load) |
| review | `conversations/review` | Type name = folder name (low cognitive load) |
| custom | `conversations/{type-name}` | Custom types use their type name as folder |

### Bash Helper Function

Add to `scripts/bash/common.sh`:

```bash
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
```

### MCP Server Compatibility

The MCP server already searches `conversations_dir` recursively, so subfolder organization should work automatically. Verify with testing.

---

## Migration Notes

**Backward Compatibility:**
- Old workspaces with `conversations/YYYY-MM-DD/` structure continue to work
- New workspaces use `conversations/{subfolder}/YYYY-MM-DD/` structure
- Both formats coexist peacefully
- MCP search finds conversations in both formats

**Optional Migration:**
Users can manually move old conversations to new structure if desired, but it's not required.

---

## Testing

**Test Cases:**
1. Create each conversation type, verify correct subfolder used
2. Edit registry folder field, verify custom folder used
3. Test with missing/corrupted registry, verify fallback works
4. Create multiple conversations same day in different folders, verify independent ID sequences
5. Run MCP search, verify finds conversations across all subfolders
6. Test workspace-status, verify counts across subfolders
