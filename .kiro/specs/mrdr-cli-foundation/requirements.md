# Requirements Document
[MRDR:doc:spec=doctags](/docs/doctags.md)

## Introduction

This document defines the requirements for the MRDR CLI Foundation—a comprehensive, modular Python CLI that serves as the Visual Syntax Database Ecosystem. The CLI provides two operational controllers (`hyde` for back-end data correlation, `jekyl` for front-end visual rendering) and initially focuses on docstring display with a future-proof modular architecture.

## Glossary

- **MRDR_CLI**: The main command-line interface invoked via `mrdr` or `misterdoctor`
- **Hyde_Controller**: Back-end correlation controller managing data, metadata, and database operations
- **Jekyl_Controller**: Front-end correlation controller managing visual output, Rich rendering, and UX
- **Docstring_Database**: JSON/YAML data store containing syntax signatures for 25+ programming languages
- **Rich_Renderer**: Python Rich library integration for terminal UI output
- **PLUSREP_System**: Quality grading system using `+` and `.` tokens for reputation weighting
- **Canonical_Payload**: Standardized YAML/JSON metadata schema for database entries
- **Carrier_Syntax**: Language-specific docstring delimiter patterns
- **Golden_Screen**: Canonical output template defining visual layout structure

## Requirements

### Requirement 1: CLI Entry Point and Command Structure

**User Story:** As a developer, I want to invoke the MRDR CLI with intuitive commands, so that I can access docstring data and visual output efficiently.

#### Acceptance Criteria

1. THE MRDR_CLI SHALL accept `mrdr` as the primary command invocation
2. THE MRDR_CLI SHALL accept `misterdoctor` as an alias for the primary command
3. WHEN a user invokes `mrdr` without arguments, THE MRDR_CLI SHALL display a help menu with available commands
4. WHEN a user invokes `mrdr hyde`, THE Hyde_Controller SHALL activate for back-end operations
5. WHEN a user invokes `mrdr jekyl`, THE Jekyl_Controller SHALL activate for front-end operations
6. THE MRDR_CLI SHALL support `-h` and `--help` options for all commands and subcommands
7. THE MRDR_CLI SHALL support `-v` and `--version` to display current version

### Requirement 2: Hyde Controller - Data Operations

**User Story:** As a developer, I want to query and manage the docstring database through the hyde controller, so that I can access syntax information programmatically.

#### Acceptance Criteria

1. WHEN `mrdr hyde query <language>` is invoked, THE Hyde_Controller SHALL return docstring syntax data for the specified language
2. WHEN `mrdr hyde list` is invoked, THE Hyde_Controller SHALL display all supported languages in the database
3. WHEN `mrdr hyde inspect <language>` is invoked, THE Hyde_Controller SHALL display detailed metadata including syntax signature, carrier type, attachment rules, and parsing notes
4. WHEN a queried language does not exist in the database, THE Hyde_Controller SHALL return an error message with suggested alternatives
5. THE Hyde_Controller SHALL load data from `database/docstrings/docstring_database.json` as the primary data source
6. WHEN `mrdr hyde export --format json` is invoked, THE Hyde_Controller SHALL output query results in JSON format
7. WHEN `mrdr hyde export --format yaml` is invoked, THE Hyde_Controller SHALL output query results in YAML format

### Requirement 3: Jekyl Controller - Visual Output

**User Story:** As a developer, I want rich visual output of docstring information, so that I can quickly understand syntax patterns through an intuitive terminal UI.

#### Acceptance Criteria

1. WHEN `mrdr jekyl show <language>` is invoked, THE Jekyl_Controller SHALL render docstring syntax using Rich panels and tables
2. THE Jekyl_Controller SHALL display output following the Golden_Screen layout: header bar, primary payload, context strip, hint bar, footer
3. WHEN `mrdr jekyl show <language> --plain` is invoked, THE Jekyl_Controller SHALL render output without Rich formatting
4. WHEN `mrdr jekyl compare <lang1> <lang2>` is invoked, THE Jekyl_Controller SHALL display a side-by-side comparison table
5. THE Jekyl_Controller SHALL apply syntax highlighting to code examples using Rich Syntax
6. WHEN `mrdr jekyl show <language> --example` is invoked, THE Jekyl_Controller SHALL include a code example demonstrating the docstring syntax
7. THE Jekyl_Controller SHALL display keybind hints in the footer: `(/) search · (↵) details · (f) filter · (q) quit`

### Requirement 4: Database Schema and Data Integrity

**User Story:** As a system maintainer, I want a well-defined database schema, so that data remains consistent and parseable across all operations.

#### Acceptance Criteria

1. THE Docstring_Database SHALL store entries with required fields: `language`, `syntax.start`, `syntax.end`, `syntax.type`, `syntax.location`
2. THE Docstring_Database SHALL support optional fields: `tags`, `example_content`, `conflict_ref`, `parsing_rule`, `metadata`
3. WHEN loading the database, THE Hyde_Controller SHALL validate all entries against the Canonical_Payload schema
4. IF a database entry fails validation, THEN THE Hyde_Controller SHALL log the error and skip the invalid entry
5. THE Docstring_Database SHALL use JSON as the primary storage format with YAML as an alternative
6. WHEN serializing database entries, THE Hyde_Controller SHALL preserve field order for consistency
7. THE Docstring_Database SHALL support conflict references for languages with identical delimiters (e.g., Python vs Julia `"""`)

### Requirement 5: PLUSREP Grading Integration

**User Story:** As a quality reviewer, I want to grade docstring examples using the PLUSREP system, so that I can track and display quality metrics.

#### Acceptance Criteria

1. THE PLUSREP_System SHALL use a 6-token scale: `[++++++]` (MAXIMUM) to `[+.....]` (RESET)
2. WHEN `mrdr jekyl show <language> --grade` is invoked, THE Jekyl_Controller SHALL display the PLUSREP rating for that entry
3. THE PLUSREP_System SHALL calculate ratings based on: consistency, accuracy, and design quality weights
4. WHEN displaying PLUSREP output, THE Jekyl_Controller SHALL render tokens with color coding: `+` in green, `.` in red
5. THE Docstring_Database SHALL support an optional `plusrep` field for storing quality grades

### Requirement 6: Output Modes and Formatting

**User Story:** As a developer, I want multiple output formats, so that I can integrate MRDR output into different workflows.

#### Acceptance Criteria

1. THE MRDR_CLI SHALL support `--plain` flag to disable Rich formatting globally
2. THE MRDR_CLI SHALL support `--json` flag to output results as JSON
3. THE MRDR_CLI SHALL support `--debug` flag to display timing, query IDs, and cache status
4. WHEN `--plain` is active, THE Jekyl_Controller SHALL output plain text without ANSI codes
5. WHEN `--json` is active, THE Hyde_Controller SHALL serialize output to valid JSON
6. THE MRDR_CLI SHALL detect non-TTY environments and automatically fall back to plain output

### Requirement 7: Error Handling and Recovery

**User Story:** As a user, I want clear error messages with recovery suggestions, so that I can resolve issues without frustration.

#### Acceptance Criteria

1. WHEN an unknown command is invoked, THE MRDR_CLI SHALL display the closest matching command suggestion
2. WHEN the database file is missing, THE MRDR_CLI SHALL display an error with the expected file path
3. WHEN a query returns no results, THE Jekyl_Controller SHALL display recovery suggestions and example queries
4. IF an unexpected error occurs, THEN THE MRDR_CLI SHALL log the stack trace to a debug file and display a user-friendly message
5. THE MRDR_CLI SHALL support `mrdr fix` command to refresh syntax highlighting or reset CLI UI state

### Requirement 8: Modular Architecture

**User Story:** As a maintainer, I want a modular codebase, so that new features can be added without modifying core components.

#### Acceptance Criteria

1. THE MRDR_CLI SHALL separate concerns into distinct modules: `cli`, `hyde`, `jekyl`, `database`, `render`
2. THE Hyde_Controller SHALL expose a public API that Jekyl_Controller consumes without direct database access
3. THE Jekyl_Controller SHALL use pluggable renderers that can be swapped without modifying core logic
4. WHEN adding a new output format, THE MRDR_CLI architecture SHALL require only a new renderer module
5. THE MRDR_CLI SHALL use dependency injection for database and renderer components
6. THE MRDR_CLI SHALL define interfaces (protocols) for Controller, Renderer, and DataSource abstractions

### Requirement 9: Configuration and Customization

**User Story:** As a power user, I want to customize CLI behavior through configuration, so that I can tailor the experience to my workflow.

#### Acceptance Criteria

1. THE MRDR_CLI SHALL support a configuration file at `~/.mrdr/config.yaml`
2. WHEN a config file exists, THE MRDR_CLI SHALL load user preferences for default output format, theme, and keybinds
3. THE MRDR_CLI SHALL support environment variable overrides with `MRDR_` prefix (e.g., `MRDR_OUTPUT_FORMAT`)
4. WHEN no config exists, THE MRDR_CLI SHALL use sensible defaults without requiring configuration
5. THE MRDR_CLI SHALL support `mrdr config show` to display current configuration
6. THE MRDR_CLI SHALL support `mrdr config set <key> <value>` to modify configuration

### Requirement 10: Docstring Display Feature

**User Story:** As a developer, I want to view docstring syntax examples for any supported language, so that I can write correct documentation in my projects.

#### Acceptance Criteria

1. WHEN `mrdr docstring <language>` is invoked, THE MRDR_CLI SHALL display the docstring syntax for that language
2. THE docstring display SHALL include: syntax signature, delimiter characters, attachment rules, and a code example
3. WHEN `mrdr docstring <language> --style <style>` is invoked for Python, THE MRDR_CLI SHALL display the specified style (sphinx, google, numpy, epytext, pep257)
4. THE MRDR_CLI SHALL support `mrdr docstring --all` to list all supported languages with their signatures
5. WHEN displaying docstring examples, THE Jekyl_Controller SHALL apply language-appropriate syntax highlighting
6. THE docstring display SHALL include conflict notes when languages share identical delimiters

