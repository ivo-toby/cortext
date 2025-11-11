# Spec Delta: Registry System

**Capability:** registry-system
**Change ID:** organize-conversation-folders

---

## MODIFIED Requirements

### Requirement: Registry entries MUST include folder configuration
Each conversation type entry in the registry SHALL include a `folder` field specifying where conversations of that type are stored.

**ID:** `REG-FOLDER-001` | **Priority:** High

#### Scenario: Built-in types have folder field in registry

**Given** a new workspace is initialized with `cortext init`
**When** the registry.json file is created
**Then** each built-in conversation type MUST have a `folder` field
**And** the folder field MUST specify a path relative to workspace root

**Example:**
```json
{
  "version": "1.0",
  "conversation_types": {
    "brainstorm": {
      "name": "Brainstorm",
      "folder": "conversations/brainstorm",
      "template": ".workspace/templates/brainstorm.md",
      "command": "/workspace.brainstorm",
      "script": ".workspace/scripts/bash/brainstorm.sh",
      "built_in": true,
      "description": "Ideation and exploration",
      "sections": ["goals", "ideas", "themes", "next-steps"]
    },
    "learn": {
      "name": "Learn",
      "folder": "conversations/learn",
      "template": ".workspace/templates/learning-notes.md",
      ...
    },
    "debug": {
      "name": "Debug",
      "folder": "conversations/debug",
      "template": ".workspace/templates/debug-session.md",
      ...
    }
  }
}
```

#### Scenario: Custom types default to type-based folder

**Given** a user creates a custom conversation type
**When** the registry entry is added
**Then** the `folder` field MUST default to `conversations/{type-name}`
**And** the user SHOULD be able to specify a different folder

---

### Requirement: Folder field SHALL be readable from bash scripts
The registry's folder field MUST be accessible from bash scripts using standard JSON parsing tools.

**ID:** `REG-FOLDER-002` | **Priority:** High

#### Scenario: Bash script reads folder field

**Given** a bash script needs to determine where to save a conversation
**When** it queries the registry for a conversation type
**Then** it MUST be able to extract the folder field using `jq` or equivalent
**And** the extraction MUST handle missing fields gracefully

**Implementation:**
```bash
# Read folder from registry
FOLDER=$(jq -r ".conversation_types.\"brainstorm\".folder // \"conversations/brainstorm\"" .workspace/registry.json)
# Returns: "conversations/brainstorm" or fallback if missing
```

---

## ADDED Requirements

### Requirement: Registry MUST validate folder paths
When a conversation type is registered or modified, the folder path SHALL be validated for safety and correctness.

**ID:** `REG-FOLDER-003` | **Priority:** Medium

#### Scenario: Folder path must be relative

**Given** a user specifies a folder for a conversation type
**When** the folder path is validated
**Then** it MUST NOT be an absolute path (no leading `/`)
**And** it MUST NOT contain `..` (no parent directory traversal)
**And** it MUST be within the workspace

**Example:**
```json
// Valid
{"folder": "conversations/ideas"}
{"folder": "research/experiments"}

// Invalid
{"folder": "/tmp/conversations"}  // Absolute path
{"folder": "../other"}  // Parent traversal
```

#### Scenario: Folder is created if it doesn't exist

**Given** a conversation script uses a folder from the registry
**When** that folder doesn't exist yet
**Then** the script MUST create the folder automatically
**And** parent directories MUST be created as needed (mkdir -p)

---

### Requirement: Registry documentation SHALL explain folder configuration
The registry structure and folder field usage MUST be documented for users.

**ID:** `REG-FOLDER-004` | **Priority:** Low

#### Scenario: Documentation shows folder customization

**Given** a user wants to customize where conversations are saved
**When** they read the documentation
**Then** they MUST find clear instructions on editing the folder field
**And** examples MUST show different folder configurations
**And** limitations/constraints MUST be explained

**Documentation should include:**
- Default folder mappings for built-in types
- How to change folder for existing type
- How to specify folder for custom type
- Path format and constraints (relative, no .., etc.)
- What happens to existing conversations when folder changes

---

## Implementation Notes

### Registry Schema Update

Current registry schema:
```json
{
  "conversation_types": {
    "type_id": {
      "name": "string",
      "template": "path",
      "command": "string",
      "script": "path",
      "built_in": boolean,
      "created": "ISO-8601",
      "description": "string",
      "sections": ["array"]
    }
  }
}
```

**Add to schema**:
```json
{
  "folder": "relative/path"  // NEW FIELD
}
```

### Update `create_registry()` Function

In `src/cortext_cli/commands/init.py`, line ~283:

```python
"brainstorm": {
    "name": "Brainstorm",
    "folder": "conversations/brainstorm",  # ADD THIS
    "template": ".workspace/templates/brainstorm.md",
    ...
},
```

### Validation Logic (Future Enhancement)

Add optional validation when registry is modified:
- Check folder path is relative
- Check no parent directory traversal
- Warn if folder doesn't exist (but don't fail)

---

## Testing

**Test Cases:**
1. Initialize new workspace, verify all built-in types have folder field
2. Read folder from registry in bash, verify jq extraction works
3. Create custom type with custom folder, verify it's used
4. Edit folder field in registry, verify next conversation uses new folder
5. Test with missing folder field, verify fallback to default
6. Test with invalid folder path (absolute, ..), verify error/warning

---

## Migration

**Existing Workspaces:**
- Old registry.json without `folder` field: Scripts fall back to `conversations/general`
- Users can manually add folder fields to existing registry
- No automatic migration needed - feature degrades gracefully

**New Workspaces:**
- All conversation types have folder field from initialization
