# Proposal: Extract Default Conversation Types to Constant

**Change ID:** `extract-default-conversation-types`
**Status:** Proposed
**Created:** 2025-11-16

---

## Why

The MCP server has duplicate default conversation types dictionaries in `_load_conversation_types()`:
- Lines 53-60: First fallback when registry doesn't exist
- Lines 71-78: Second fallback on exception

This violates the DRY (Don't Repeat Yourself) principle and creates maintenance burden - if a new type is added, both places need updating.

---

## What Changes

Extract the default conversation types to a single class constant `DEFAULT_CONVERSATION_TYPES` that can be referenced throughout the codebase.

**Before:**
```python
def _load_conversation_types(self) -> dict[str, str]:
    if not self.registry_path.exists():
        return {
            "brainstorm": "brainstorm",
            "debug": "debug",
            ...  # Duplicated
        }
    try:
        ...
    except Exception:
        return {
            "brainstorm": "brainstorm",
            "debug": "debug",
            ...  # Duplicated again
        }
```

**After:**
```python
DEFAULT_CONVERSATION_TYPES = {
    "brainstorm": "brainstorm",
    "debug": "debug",
    "learn": "learn",
    "meeting": "meeting",
    "plan": "plan",
    "review": "review",
}

def _load_conversation_types(self) -> dict[str, str]:
    if not self.registry_path.exists():
        return DEFAULT_CONVERSATION_TYPES.copy()
    try:
        ...
    except Exception:
        return DEFAULT_CONVERSATION_TYPES.copy()
```

---

## Impact Analysis

### Files Changed
- `src/cortext_mcp/server.py` - Extract constant, refactor `_load_conversation_types()`

### Benefits
- **Single source of truth**: One place to update when types change
- **Cleaner code**: Reduced duplication
- **Better maintainability**: Easier to add/remove types
- **Self-documenting**: Constant name explains purpose

### Risk Assessment
- **Very low risk**: Simple refactor, no behavior change
- **No breaking changes**: Internal implementation detail
- **Easy to verify**: Same functionality, just cleaner

---

## Acceptance Criteria

1. Default conversation types defined once as module or class constant
2. `_load_conversation_types()` references the constant (using `.copy()`)
3. No duplicate dictionary definitions
4. All existing functionality preserved
5. Code is more maintainable

---

## Spec Deltas

- `specs/mcp-server/spec.md` - Requirements for MCP server maintainability
