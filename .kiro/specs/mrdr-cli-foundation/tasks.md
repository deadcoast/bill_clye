# Implementation Plan: MRDR CLI Foundation
[MRDR:doc:spec=doctags](/docs/doctags.md)

## Overview

This implementation plan transforms the MRDR CLI Foundation design into actionable coding tasks. The approach prioritizes establishing core infrastructure first, then building controllers, renderers, and finally wiring everything together. Property-based tests are integrated alongside implementation to catch errors early.

## Tasks

- [x] 1. Project setup and core infrastructure
  - [x] 1.1 Initialize Python package structure
    - Create `src/mrdr/` directory structure as defined in design
    - Set up `pyproject.toml` with dependencies: typer, rich, pydantic, pyyaml, hypothesis
    - Configure `__init__.py` with version and package metadata
    - Create `__main__.py` entry point for `python -m mrdr`
    - _Requirements: 1.1, 1.2_

  - [x] 1.2 Define protocol interfaces and base classes
    - Create `controllers/base.py` with Controller protocol
    - Create `database/base.py` with DataSource protocol
    - Create `render/base.py` with Renderer protocol
    - _Requirements: 8.2, 8.5, 8.6_

  - [x] 1.3 Implement custom exception hierarchy
    - Create `utils/errors.py` with MRDRError, DatabaseError, QueryError, ConfigError
    - Implement LanguageNotFoundError with suggestions field
    - Implement DatabaseNotFoundError with path field
    - Implement ValidationError with entry and errors fields
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 2. Database module implementation
  - [x] 2.1 Implement Pydantic data models
    - Create `database/schema.py` with SyntaxType, SyntaxLocation enums
    - Implement SyntaxSpec model with start, end, type, location fields
    - Implement PlusrepGrade model with tokens, rating, label fields
    - Implement DocstringEntry model with all fields and validation
    - _Requirements: 4.1, 4.2, 5.1_

  - [x] 2.2 Write property test for database schema validation
    - **Property 12: Database Validation**
    - **Validates: Requirements 4.1, 4.3, 4.4**

  - [x] 2.3 Implement database loader
    - Create `database/loader.py` with JSON loading from `database/docstrings/docstring_database.json`
    - Implement validation against DocstringEntry schema
    - Implement error logging and invalid entry skipping
    - _Requirements: 2.5, 4.3, 4.4_

  - [x] 2.4 Implement query operations
    - Create `database/query.py` with query by language function
    - Implement list all languages function
    - Implement fuzzy matching for suggestions using difflib
    - _Requirements: 2.1, 2.2, 2.4_

  - [x] 2.5 Write property test for query operations
    - **Property 3: Query Returns Valid Data**
    - **Property 4: List Completeness**
    - **Property 5: Invalid Language Suggestions**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4**

  - [x] 2.6 Write property test for serialization round-trip
    - **Property 6: Export Round-Trip**
    - **Property 13: Serialization Round-Trip**
    - **Validates: Requirements 2.6, 2.7, 4.6**

- [x] 3. Checkpoint - Database module complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Hyde Controller implementation
  - [x] 4.1 Implement Hyde Controller core
    - Create `controllers/hyde.py` with HydeController class
    - Implement query method returning DocstringEntry
    - Implement list_languages method
    - Implement inspect method returning detailed metadata dict
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 4.2 Implement export functionality
    - Add export method with format parameter (json/yaml)
    - Implement JSON serialization with field order preservation
    - Implement YAML serialization
    - _Requirements: 2.6, 2.7_

  - [x] 4.3 Implement database validation method
    - Add validate_database method returning list of ValidationError
    - Integrate with loader validation
    - _Requirements: 4.3, 4.4_

- [x] 5. Render module implementation
  - [x] 5.1 Implement Rich renderer
    - Create `render/rich_renderer.py` with RichRenderer class
    - Implement render method using Rich Console
    - Implement supports_rich returning True
    - _Requirements: 3.1, 3.5_

  - [x] 5.2 Implement Golden Screen components
    - Create `render/components/golden_screen.py` with GoldenScreen dataclass
    - Implement HeaderBar component with command and db_source
    - Implement HintBar component with keybind hints
    - Implement render method producing Rich Panel layout
    - _Requirements: 3.2, 3.7_

  - [x] 5.3 Write property test for output structure
    - **Property 7: Output Structure Conformance**
    - **Validates: Requirements 3.1, 3.2, 3.7**

  - [x] 5.4 Implement plain text renderer
    - Create `render/plain_renderer.py` with PlainRenderer class
    - Implement render method producing plain text without ANSI
    - Implement supports_rich returning False
    - _Requirements: 3.3, 6.1_

  - [x] 5.5 Write property test for plain output
    - **Property 8: Plain Output No ANSI**
    - **Validates: Requirements 3.3, 6.1, 6.4**

  - [x] 5.6 Implement JSON renderer
    - Create `render/json_renderer.py` with JSONRenderer class
    - Implement render method producing valid JSON string
    - _Requirements: 6.2_

  - [x] 5.7 Write property test for JSON output
    - **Property 9: JSON Output Validity**
    - **Validates: Requirements 6.2, 6.5**

  - [x] 5.8 Implement PLUSREP display component
    - Create `render/components/plusrep.py` with PlusrepDisplay class
    - Implement token rendering with color coding (green for +, red for .)
    - Implement rating calculation: (count of '+') - 2
    - _Requirements: 5.2, 5.3, 5.4_

  - [x] 5.9 Write property test for PLUSREP calculation
    - **Property 14: PLUSREP Calculation**
    - **Validates: Requirements 5.1, 5.3**

- [x] 6. Checkpoint - Render module complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Jekyl Controller implementation
  - [x] 7.1 Implement Jekyl Controller core
    - Create `controllers/jekyl.py` with JekylController class
    - Inject HydeController and Renderer dependencies
    - Implement show method for single language display
    - _Requirements: 3.1, 8.2_

  - [x] 7.2 Implement compare functionality
    - Add compare method accepting two language names
    - Implement side-by-side table rendering
    - _Requirements: 3.4_

  - [x] 7.3 Write property test for compare
    - **Property 10: Compare Shows Both Languages**
    - **Validates: Requirements 3.4**

  - [x] 7.4 Implement example inclusion
    - Add --example flag handling in show method
    - Include example_content in output when flag is set
    - _Requirements: 3.6_

  - [x] 7.5 Write property test for example inclusion
    - **Property 11: Example Inclusion**
    - **Validates: Requirements 3.6**

  - [x] 7.6 Implement PLUSREP display integration
    - Add --grade flag handling in show method
    - Integrate PlusrepDisplay component
    - _Requirements: 5.2_

  - [x] 7.7 Write property test for PLUSREP display
    - **Property 15: PLUSREP Display**
    - **Validates: Requirements 5.2**

- [x] 8. Configuration module implementation
  - [x] 8.1 Implement config schema
    - Create `config/schema.py` with OutputFormat enum
    - Implement ThemeConfig model
    - Implement MRDRConfig model with defaults
    - _Requirements: 9.4_

  - [x] 8.2 Implement config loader
    - Create `config/loader.py` with ConfigLoader class
    - Implement load from `~/.mrdr/config.yaml`
    - Implement environment variable override with MRDR_ prefix
    - Implement fallback to defaults when no config exists
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

  - [x] 8.3 Write property test for config loading
    - **Property 20: Config Loading**
    - **Property 21: Environment Variable Override**
    - **Validates: Requirements 9.2, 9.3**

  - [x] 8.4 Implement config set functionality
    - Add set method to ConfigLoader
    - Implement persistence to config file
    - _Requirements: 9.6_

  - [x] 8.5 Write property test for config set
    - **Property 22: Config Set Persistence**
    - **Validates: Requirements 9.6**

- [x] 9. CLI module implementation
  - [x] 9.1 Implement Typer app and entry points
    - Create `cli/app.py` with main Typer app
    - Register `mrdr` as primary command
    - Register `misterdoctor` as alias
    - Implement version callback for -v/--version
    - _Requirements: 1.1, 1.2, 1.7_

  - [x] 9.2 Write property test for alias equivalence
    - **Property 1: Alias Equivalence**
    - **Validates: Requirements 1.2**

  - [x] 9.3 Implement Hyde subcommands
    - Create `cli/hyde_commands.py` with hyde subcommand group
    - Implement `hyde query <language>` command
    - Implement `hyde list` command
    - Implement `hyde inspect <language>` command
    - Implement `hyde export --format` command
    - _Requirements: 1.4, 2.1, 2.2, 2.3, 2.6, 2.7_

  - [x] 9.4 Implement Jekyl subcommands
    - Create `cli/jekyl_commands.py` with jekyl subcommand group
    - Implement `jekyl show <language>` command with --plain, --example, --grade flags
    - Implement `jekyl compare <lang1> <lang2>` command
    - _Requirements: 1.5, 3.1, 3.3, 3.4, 3.6, 5.2_

  - [x] 9.5 Implement docstring command
    - Add `docstring <language>` command to main app
    - Implement --style flag for Python styles
    - Implement --all flag to list all languages
    - _Requirements: 10.1, 10.3, 10.4_

  - [x] 9.6 Write property test for docstring display
    - **Property 23: Docstring Display Completeness**
    - **Property 24: Python Style Selection**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.6**

  - [x] 9.7 Implement config subcommands
    - Add `config show` command
    - Add `config set <key> <value>` command
    - _Requirements: 9.5, 9.6_

  - [x] 9.8 Implement global flags
    - Add --plain global flag
    - Add --json global flag
    - Add --debug global flag
    - Implement TTY detection for automatic plain fallback
    - _Requirements: 6.1, 6.2, 6.3, 6.6_

  - [x] 9.9 Write property test for TTY detection
    - **Property 17: TTY Detection**
    - **Validates: Requirements 6.6**

  - [x] 9.10 Write property test for debug output
    - **Property 16: Debug Output**
    - **Validates: Requirements 6.3**

  - [x] 9.11 Implement help for all commands
    - Ensure -h/--help works for all commands and subcommands
    - Add descriptive help text for each command
    - _Requirements: 1.3, 1.6_

  - [x] 9.12 Write property test for help availability
    - **Property 2: Help Availability**
    - **Validates: Requirements 1.6**

  - [x] 9.13 Implement fix command
    - Add `mrdr fix` command for UI refresh
    - _Requirements: 7.5_

- [x] 10. Error handling and suggestions
  - [x] 10.1 Implement fuzzy matching for suggestions
    - Create `utils/suggestions.py` with fuzzy_match function
    - Use difflib.get_close_matches for command suggestions
    - Use difflib.get_close_matches for language suggestions
    - _Requirements: 2.4, 7.1_

  - [x] 10.2 Write property test for suggestions
    - **Property 18: Unknown Command Suggestions**
    - **Property 19: Empty Result Suggestions**
    - **Validates: Requirements 7.1, 7.3**

  - [x] 10.3 Implement error handlers in CLI
    - Add exception handlers for MRDRError hierarchy
    - Implement user-friendly error display with Rich panels
    - Implement debug file logging for unexpected errors
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 11. Checkpoint - CLI module complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Integration and wiring
  - [ ] 12.1 Wire dependency injection
    - Create factory functions for controller instantiation
    - Wire database loader → Hyde → Jekyl → Renderer chain
    - Integrate config loader into all components
    - _Requirements: 8.2, 8.5_

  - [ ] 12.2 Update pyproject.toml entry points
    - Add `mrdr` console script entry point
    - Add `misterdoctor` console script alias
    - _Requirements: 1.1, 1.2_

  - [ ] 12.3 Write integration tests
    - Test full CLI flow from entry to output
    - Test controller communication
    - _Requirements: 8.2_

- [ ] 13. Final checkpoint - All tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks including property-based tests are required for comprehensive coverage
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation follows the hyde → jekyl data flow pattern
- All naming follows docs → src → cli cohesion principle from AGENTS.md

