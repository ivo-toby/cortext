## ADDED Requirements

### Requirement: MCP Server Documentation
The documentation system SHALL provide comprehensive guides for MCP server setup and usage.

#### Scenario: User configures Claude Code MCP integration
- **WHEN** user reads MCP server documentation
- **THEN** documentation includes step-by-step configuration for Claude Code
- **AND** provides example MCP settings JSON
- **AND** documents all available tools (search_workspace, get_context, get_decision_history)
- **AND** explains search query syntax and filtering options

#### Scenario: User troubleshoots MCP server
- **WHEN** user experiences MCP server issues
- **THEN** documentation provides common error messages and solutions
- **AND** explains how to verify ripgrep installation
- **AND** documents expected response formats

### Requirement: Multi-AI Tool Setup Guides
The documentation system SHALL provide tool-specific setup guides for each supported AI assistant.

#### Scenario: User sets up OpenCode
- **WHEN** user wants to configure OpenCode
- **THEN** documentation explains .opencode/ directory structure
- **AND** documents how prompts are converted from Claude format
- **AND** provides Ollama integration instructions

#### Scenario: User sets up Gemini CLI
- **WHEN** user wants to configure Gemini CLI
- **THEN** documentation explains TOML command format
- **AND** shows conversion from markdown to TOML
- **AND** provides .gemini/ directory structure

#### Scenario: User sets up Cursor
- **WHEN** user wants to configure Cursor
- **THEN** documentation explains .cursorrules file usage
- **AND** documents how to extend rules
- **AND** provides integration examples

### Requirement: Git Workflow Documentation
The documentation system SHALL provide clear git workflow conventions for workspace operations.

#### Scenario: User creates conversation branch
- **WHEN** user reads git workflow documentation
- **THEN** documentation explains branch naming: `{type}/{id}-{title}` format
- **AND** provides examples for each conversation type
- **AND** documents auto-commit behavior

#### Scenario: User commits workspace changes
- **WHEN** user needs to commit changes
- **THEN** documentation explains commit message format with [type] prefixes
- **AND** lists all valid commit types (feat, fix, docs, conversation, workspace, etc.)
- **AND** documents commit-session.sh and workspace-status.sh scripts

### Requirement: Contribution Guide
The documentation system SHALL provide comprehensive contribution guidelines for developers.

#### Scenario: Developer sets up environment
- **WHEN** developer wants to contribute
- **THEN** documentation includes development environment setup steps
- **AND** lists required tools and dependencies
- **AND** explains code organization and patterns

#### Scenario: Developer adds conversation type
- **WHEN** developer wants to add new built-in conversation type
- **THEN** documentation explains all required components (template, script, command, registry)
- **AND** provides step-by-step implementation guide
- **AND** references existing types as examples

#### Scenario: Developer submits PR
- **WHEN** developer submits pull request
- **THEN** documentation explains PR process and review criteria
- **AND** documents testing requirements
- **AND** provides code style guidelines (PEP 8, type hints, max line length)

### Requirement: Documentation Organization
The documentation system SHALL be organized for discoverability and maintainability.

#### Scenario: User finds relevant documentation
- **WHEN** user needs specific information
- **THEN** Docs/README.md provides index of all documentation
- **AND** each guide is self-contained with clear table of contents
- **AND** cross-references link related documentation

#### Scenario: Documentation stays current
- **WHEN** features are added or modified
- **THEN** documentation follows consistent markdown formatting
- **AND** includes code examples that can be validated
- **AND** provides version information where relevant
