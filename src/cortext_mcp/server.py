"""MCP server implementation for Cortext workspace search."""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


class CortextMCPServer:
    """MCP server for Cortext workspace operations."""

    def __init__(self, workspace_path: Path = None):
        self.workspace_path = workspace_path or Path.cwd()
        self.registry_path = self.workspace_path / ".workspace" / "registry.json"
        # Load conversation types from registry for folder discovery
        self.conversation_types = self._load_conversation_types()

    def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Handle incoming MCP request."""
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return self.list_tools()
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            return self.call_tool(tool_name, arguments)
        elif method == "initialize":
            return self.initialize()
        else:
            return {"error": f"Unknown method: {method}"}

    def initialize(self) -> dict[str, Any]:
        """Initialize the MCP server."""
        return {
            "protocolVersion": "0.1.0",
            "serverInfo": {
                "name": "cortext-mcp",
                "version": "0.1.0",
            },
            "capabilities": {
                "tools": {},
            },
        }

    def _load_conversation_types(self) -> dict[str, str]:
        """Load conversation types and their folders from registry."""
        if not self.registry_path.exists():
            # Default types if registry doesn't exist
            return {
                "brainstorm": "brainstorm",
                "debug": "debug",
                "learn": "learn",
                "meeting": "meeting",
                "plan": "plan",
                "review": "review",
            }

        try:
            with open(self.registry_path) as f:
                registry = json.load(f)
            types = {}
            for type_name, type_config in registry.get("conversation_types", {}).items():
                types[type_name] = type_config.get("folder", type_name)
            return types
        except Exception:
            # Fallback to defaults
            return {
                "brainstorm": "brainstorm",
                "debug": "debug",
                "learn": "learn",
                "meeting": "meeting",
                "plan": "plan",
                "review": "review",
            }

    def list_tools(self) -> dict[str, Any]:
        """List available tools."""
        return {
            "tools": [
                {
                    "name": "search_workspace",
                    "description": "Search across conversations, notes, and research in the Cortext workspace",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (supports regex)",
                            },
                            "type": {
                                "type": "string",
                                "description": "Filter by conversation type (brainstorm, debug, plan, learn, meeting, review, or 'all')",
                                "default": "all",
                            },
                            "date_range": {
                                "type": "string",
                                "description": "Filter by date range. Supports YYYY-MM (month) or YYYY-MM-DD (day) format. Examples: '2025-11' or '2025-11-10'",
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results to return",
                                "default": 10,
                            },
                        },
                        "required": ["query"],
                    },
                },
                {
                    "name": "get_context",
                    "description": "Get relevant context for a topic from past conversations",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic to search for",
                            },
                            "max_results": {
                                "type": "number",
                                "description": "Maximum number of relevant conversations to return",
                                "default": 5,
                            },
                        },
                        "required": ["topic"],
                    },
                },
                {
                    "name": "get_decision_history",
                    "description": "Retrieve past decisions on a topic",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic or decision area to search for",
                            },
                        },
                        "required": ["topic"],
                    },
                },
            ]
        }

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool with given arguments."""
        if tool_name == "search_workspace":
            return self.search_workspace(**arguments)
        elif tool_name == "get_context":
            return self.get_context(**arguments)
        elif tool_name == "get_decision_history":
            return self.get_decision_history(**arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def search_workspace(
        self,
        query: str,
        type: str = "all",
        date_range: str = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search across workspace using ripgrep."""
        # Check if any conversation type folders exist
        search_paths = []
        if type == "all":
            # Search all known type folders
            for type_name, folder in self.conversation_types.items():
                folder_path = self.workspace_path / folder
                if folder_path.exists():
                    search_paths.append(str(folder_path))
        else:
            # Search specific type folder
            folder = self.conversation_types.get(type, type)
            folder_path = self.workspace_path / folder
            if folder_path.exists():
                search_paths.append(str(folder_path))

        if not search_paths:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No conversation folders found. Have you created any conversations yet?",
                    }
                ]
            }

        # Build ripgrep command
        rg_cmd = ["rg", "--json", "-i", query]

        # Filter by date range if specified
        if date_range:
            # Support both YYYY-MM and YYYY-MM-DD formats
            # YYYY-MM format: match YYYY-MM/ and YYYY-MM-DD/ directories
            # YYYY-MM-DD format: match only YYYY-MM-DD/ directory
            if len(date_range) == 7:  # YYYY-MM format
                rg_cmd.extend(["--glob", f"{date_range}*/**"])
            else:  # YYYY-MM-DD format
                rg_cmd.extend(["--glob", f"{date_range}/**"])

        # Add all search paths
        rg_cmd.extend(search_paths)

        try:
            result = subprocess.run(
                rg_cmd, capture_output=True, text=True, timeout=30
            )

            matches = []
            for line in result.stdout.splitlines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if data.get("type") == "match":
                        match_data = data.get("data", {})
                        path = match_data.get("path", {}).get("text", "")
                        line_num = match_data.get("line_number", 0)
                        line_text = match_data.get("lines", {}).get("text", "").strip()

                        # Extract conversation name from path
                        # Structure: {type}/YYYY-MM-DD/###-name/file.md
                        # The conversation name is the directory containing the file
                        path_parts = Path(path).parts
                        conv_name = "unknown"
                        # Look for conversation type folder at workspace root
                        for i, part in enumerate(path_parts):
                            if part in self.conversation_types.values():
                                # Found type folder, conversation name is at i+2
                                # {type}/YYYY-MM-DD/###-name/
                                if i + 2 < len(path_parts):
                                    conv_name = path_parts[i + 2]
                                break
                            # Also support old structure: conversations/{type}/YYYY-MM-DD/###-name/
                            if part == "conversations":
                                if i + 3 < len(path_parts):
                                    conv_name = path_parts[i + 3]
                                elif i + 2 < len(path_parts):
                                    conv_name = path_parts[i + 2]
                                break

                        matches.append(
                            {
                                "conversation": conv_name,
                                "file": str(Path(path).name),
                                "line": line_num,
                                "text": line_text,
                                "path": path,
                            }
                        )

                        if len(matches) >= limit:
                            break
                except json.JSONDecodeError:
                    continue

            if not matches:
                result_text = f"No results found for query: '{query}'"
                if type != "all":
                    result_text += f" (type: {type})"
                if date_range:
                    result_text += f" (date: {date_range})"
            else:
                result_text = f"Found {len(matches)} result(s):\n\n"
                for match in matches:
                    result_text += f"**{match['conversation']}** - {match['file']}:{match['line']}\n"
                    result_text += f"  {match['text']}\n\n"

            return {"content": [{"type": "text", "text": result_text}]}

        except subprocess.TimeoutExpired:
            return {
                "content": [
                    {"type": "text", "text": "Search timed out. Try a more specific query."}
                ]
            }
        except FileNotFoundError:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "ripgrep (rg) not found. Install it for search functionality.",
                    }
                ]
            }
        except Exception as e:
            return {"content": [{"type": "text", "text": f"Search error: {str(e)}"}]}

    def get_context(self, topic: str, max_results: int = 5) -> dict[str, Any]:
        """Get relevant context for a topic."""
        # Use search_workspace to find relevant conversations
        search_result = self.search_workspace(topic, limit=max_results)

        # Enhance with context info
        result_text = f"# Context for: {topic}\n\n"
        result_text += "Relevant conversations found:\n\n"
        result_text += search_result["content"][0]["text"]

        return {"content": [{"type": "text", "text": result_text}]}

    def get_decision_history(self, topic: str) -> dict[str, Any]:
        """Retrieve past decisions on a topic."""
        # Search in decisions.md file
        decisions_file = self.workspace_path / ".workspace" / "memory" / "decisions.md"

        if not decisions_file.exists():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No decisions log found. Create one at .workspace/memory/decisions.md",
                    }
                ]
            }

        # Search in decisions file
        try:
            rg_cmd = ["rg", "-i", "-C", "5", topic, str(decisions_file)]
            result = subprocess.run(rg_cmd, capture_output=True, text=True, timeout=10)

            if result.returncode == 0 and result.stdout:
                result_text = f"# Decision History: {topic}\n\n"
                result_text += result.stdout
            else:
                result_text = f"No decisions found related to: {topic}"

            return {"content": [{"type": "text", "text": result_text}]}

        except Exception as e:
            return {"content": [{"type": "text", "text": f"Error: {str(e)}"}]}


def main():
    """Main entry point for the MCP server."""
    server = CortextMCPServer()

    # Read from stdin and write to stdout (MCP protocol)
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = server.handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            error_response = {"error": "Invalid JSON request"}
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            error_response = {"error": str(e)}
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()
