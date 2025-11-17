# Spec Delta: MCP Search

**Capability:** mcp-search
**Change ID:** refine-conversation-dating

---

## ADDED Requirements

### Requirement: Date Range Filtering SHALL support both YYYY-MM and YYYY-MM-DD formats
The MCP server's `search_workspace` tool SHALL support date range filtering with both month-level (`YYYY-MM`) and day-level (`YYYY-MM-DD`) granularity to accommodate both old and new conversation directory formats.

**ID:** `MCP-SEARCH-001` | **Priority:** High

#### Scenario: Filter by specific day

**Given** conversations exist in directories:
- `conversations/2025-11-10/001-brainstorm-feature/`
- `conversations/2025-11-10/002-debug-auth/`
- `conversations/2025-11-11/001-plan-redesign/`

**When** a user searches with `date_range: "2025-11-10"`
**Then** the search MUST return only conversations from `2025-11-10/` directories
**And** conversations from other days MUST be excluded

**Example:**
```python
# MCP tool call
search_workspace(
    query="authentication",
    date_range="2025-11-10"
)

# Returns only conversations from 2025-11-10/ directory
```

#### Scenario: Filter by month (backward compatibility)

**Given** conversations exist in both formats:
- `conversations/2025-11/001-old-conversation/` (old format)
- `conversations/2025-11-10/001-new-conversation/` (new format)
- `conversations/2025-11-11/002-another-new/` (new format)

**When** a user searches with `date_range: "2025-11"`
**Then** the search MUST return conversations from:
  - `2025-11/` directory (old format)
  - All `2025-11-**/` directories (new format)
**And** all matching conversations from November 2025 MUST be included

**Example:**
```python
# MCP tool call
search_workspace(
    query="feature",
    date_range="2025-11"
)

# Returns conversations from:
# - conversations/2025-11/*
# - conversations/2025-11-01/*
# - conversations/2025-11-02/*
# - ...
# - conversations/2025-11-30/*
```

#### Scenario: No date filter specified

**Given** conversations exist in multiple date formats
**When** a user searches without specifying `date_range`
**Then** the search MUST search across ALL conversation directories
**And** results from both old and new formats MUST be included

---

### Requirement: Documentation MUST describe both date format options
The `search_workspace` tool's parameter documentation SHALL clearly describe both supported date formats (`YYYY-MM` and `YYYY-MM-DD`) and their respective search behaviors.

**ID:** `MCP-SEARCH-002` | **Priority:** Medium

#### Scenario: Tool schema description

**Given** an AI tool queries the MCP server for available tools
**When** it receives the `search_workspace` tool schema
**Then** the `date_range` parameter description MUST state:
  - Accepts `YYYY-MM` format for month-level filtering
  - Accepts `YYYY-MM-DD` format for day-level filtering
  - Month format matches all days within that month

**Example:**
```json
{
  "date_range": {
    "type": "string",
    "description": "Filter by date range. Supports YYYY-MM (month) or YYYY-MM-DD (day) format. Month format matches all days within that month. Examples: '2025-11' or '2025-11-10'"
  }
}
```

---

### Requirement: Glob Patterns MUST match both directory formats
The search implementation SHALL use glob patterns that correctly match both `YYYY-MM` and `YYYY-MM-DD` directory structures when filtering by date range.

**ID:** `MCP-SEARCH-003` | **Priority:** High

#### Scenario: Ripgrep glob pattern for day-level filter

**Given** a user specifies `date_range: "2025-11-10"`
**When** the MCP server constructs the ripgrep command
**Then** it MUST use glob pattern `2025-11-10/**`
**And** only files within that specific day's directory MUST be searched

**Implementation:**
```python
if date_range:
    rg_cmd.extend(["--glob", f"{date_range}/**"])
```

#### Scenario: Ripgrep glob pattern for month-level filter

**Given** a user specifies `date_range: "2025-11"`
**When** the MCP server constructs the ripgrep command
**Then** it MUST use glob pattern `2025-11*/**` to match both:
  - `2025-11/` (old format)
  - `2025-11-01/`, `2025-11-02/`, ..., `2025-11-30/` (new format)
**And** all conversations from November 2025 MUST be searched

**Implementation:**
```python
if date_range:
    # If YYYY-MM format, add wildcard to catch both formats
    if len(date_range) == 7:  # YYYY-MM
        rg_cmd.extend(["--glob", f"{date_range}*/**"])
    else:  # YYYY-MM-DD
        rg_cmd.extend(["--glob", f"{date_range}/**"])
```

---

## Implementation Notes

### Affected File

**Python Module:**
- `src/cortext_mcp/server.py` - Lines ~69-120 (search_workspace method)

### Code Changes

**Current Implementation:**
```python
"date_range": {
    "type": "string",
    "description": "Filter by date range (YYYY-MM format, e.g., '2025-11')",
},
```

**Updated Implementation:**
```python
"date_range": {
    "type": "string",
    "description": "Filter by date range. Supports YYYY-MM (month) or YYYY-MM-DD (day) format. Examples: '2025-11' or '2025-11-10'",
},
```

**Search Logic Update:**
```python
# Filter by date range if specified
if date_range:
    # Support both YYYY-MM and YYYY-MM-DD formats
    # YYYY-MM format: match YYYY-MM/ and YYYY-MM-DD/ directories
    # YYYY-MM-DD format: match only YYYY-MM-DD/ directory
    if len(date_range) == 7:  # YYYY-MM format
        rg_cmd.extend(["--glob", f"{date_range}*/**"])
    else:  # YYYY-MM-DD format
        rg_cmd.extend(["--glob", f"{date_range}/**"])
```

### Testing

**Test Cases:**

1. **Day-level filter:**
   ```python
   search_workspace(query="test", date_range="2025-11-10")
   # Should search only: conversations/2025-11-10/
   ```

2. **Month-level filter (new format):**
   ```python
   search_workspace(query="test", date_range="2025-11")
   # Should search: conversations/2025-11-**/
   ```

3. **Month-level filter (old format):**
   ```python
   search_workspace(query="test", date_range="2025-11")
   # Should search: conversations/2025-11/
   ```

4. **Month-level filter (mixed formats):**
   ```python
   # With both old and new directories present
   search_workspace(query="test", date_range="2025-11")
   # Should search both:
   # - conversations/2025-11/
   # - conversations/2025-11-01/, 2025-11-02/, etc.
   ```

5. **No filter:**
   ```python
   search_workspace(query="test")
   # Should search all conversations/
   ```

---

## Documentation Updates

**Files to Update:**

1. **`Docs/mcp-server.md`** - Update `search_workspace` tool documentation
   - Add examples for both date formats
   - Explain backward compatibility

2. **Example Documentation:**
   ```markdown
   ### Date Range Filtering

   The `date_range` parameter supports two formats:

   **Month-level (YYYY-MM):**
   - Searches all conversations from that month
   - Works with both old and new directory structures
   - Example: `"2025-11"` searches `2025-11/` and all `2025-11-DD/` directories

   **Day-level (YYYY-MM-DD):**
   - Searches conversations from that specific day only
   - Example: `"2025-11-10"` searches only `2025-11-10/` directory
   ```

---

## Edge Cases

1. **Invalid date format** - Server SHOULD return error or ignore invalid formats
2. **Future dates** - Valid but will return no results (expected behavior)
3. **Very old dates** - Should work for any valid date
4. **Partial matches** - `2025-11-1` should NOT match `2025-11-10` (strict format required)

---

## Migration Impact

**User Experience:**
- Users can continue using `date_range: "2025-11"` for month-level searches
- Users can now use `date_range: "2025-11-10"` for day-level precision
- No breaking changes to existing MCP tool usage
- Enhanced capability with backward compatibility
