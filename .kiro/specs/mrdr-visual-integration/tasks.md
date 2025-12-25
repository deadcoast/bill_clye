# Implementation Plan: MRDR Visual Integration
[MRDR:doc:spec=doctags](/docs/doctags.md)

## Overview

This implementation plan transforms the MRDR Visual Integration design into actionable coding tasks. The approach builds on the existing CLI foundation, adding visual components, the UDL system, and advanced rendering capabilities. Property-based tests are integrated alongside implementation.

## Tasks

- [x] 1. Visual component infrastructure
  - [x] 1.1 Create visual components module structure
    - Create `src/mrdr/render/components/card_grid.py`
    - Create `src/mrdr/render/components/accordion.py`
    - Create `src/mrdr/render/components/line_gutter.py`
    - Create `src/mrdr/render/components/keybar.py`
    - Update `src/mrdr/render/components/__init__.py` with exports
    - _Requirements: 1.1, 1.3, 2.1, 1.5_

  - [x] 1.2 Implement Card Grid component
    - Create CardData dataclass with title, purpose, ui_description, modes fields
    - Create CardGrid class with render method using Rich tables
    - Implement _render_card method producing Rich Panels
    - _Requirements: 1.1, 1.2_

  - [x] 1.3 Write property test for Card Grid
    - **Property 1: Card Grid Layout Structure**
    - **Validates: Requirements 1.1, 1.2**

  - [x] 1.4 Implement Accordion component
    - Create AccordionSection dataclass with title, content, open fields
    - Create Accordion class with render method using Rich panels
    - Support open attribute for default-expanded sections
    - _Requirements: 1.3, 1.4_

  - [x] 1.5 Write property test for Accordion
    - **Property 2: Accordion Expandable Sections**
    - **Validates: Requirements 1.3, 1.4**

  - [x] 1.6 Implement Keybar component
    - Create Keybar class extending existing HintBar
    - Implement kbd-style formatting with Rich markup
    - _Requirements: 1.5_

  - [x] 1.7 Write property test for Keybar
    - **Property 3: Keybar Keycap Formatting**
    - **Validates: Requirements 1.5**

- [x] 2. Line Gutter implementation
  - [x] 2.1 Implement Line Gutter component
    - Create `src/mrdr/render/components/line_gutter.py`
    - Create LineGutter dataclass with content, start_line, separator fields
    - Implement render method with right-justified line numbers
    - Implement plain mode without ANSI codes
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 2.2 Write property test for Line Gutter alignment
    - **Property 4: Line Gutter Number Alignment**
    - **Validates: Requirements 2.1, 2.2, 2.5**

  - [x] 2.3 Write property test for Line Gutter plain mode
    - **Property 5: Line Gutter Plain Mode**
    - **Validates: Requirements 2.3**

  - [x] 2.4 Write property test for Line Gutter start line
    - **Property 6: Line Gutter Start Line**
    - **Validates: Requirements 2.4**

- [ ] 3. Checkpoint - Visual components complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. UDL System implementation
  - [ ] 4.1 Create UDL module structure
    - Create `src/mrdr/database/udl/__init__.py`
    - Create `src/mrdr/database/udl/schema.py` with UDLOperator, UDLDefinition models
    - Create `src/mrdr/database/udl/loader.py` for UDL file loading
    - Create `src/mrdr/database/udl/validator.py` for validation
    - _Requirements: 3.1, 3.6_

  - [ ] 4.2 Implement UDL schema models
    - Create UDLOperator model with name, open, close fields
    - Create UDLDefinition model with title, descr, lang, delimiter, operator fields
    - Add field validators for single-char delimiter and two-char operator
    - Define DOLPHIN_OPERATOR and WALRUS_OPERATOR constants
    - _Requirements: 3.1, 3.3, 3.4, 3.6_

  - [ ] 4.3 Write property test for UDL operator patterns
    - **Property 7: UDL Operator Pattern Support**
    - **Validates: Requirements 3.3, 3.4**

  - [ ] 4.4 Write property test for UDL delimiter validation
    - **Property 8: UDL Delimiter Validation**
    - **Validates: Requirements 3.6**

  - [ ] 4.5 Implement UDL loader
    - Create UDLLoader class for loading from `database/languages/udl/`
    - Implement get_udl method returning UDLDefinition
    - Implement list_udls method returning all UDL names
    - _Requirements: 3.5, 3.7_

  - [ ] 4.6 Write property test for UDL list completeness
    - **Property 9: UDL List Completeness**
    - **Validates: Requirements 3.7**

  - [ ] 4.7 Implement UDL CLI commands
    - Create `src/mrdr/cli/udl_commands.py`
    - Implement `mrdr hyde udl create <name>` command
    - Implement `mrdr hyde udl list` command
    - Implement `mrdr jekyl show udl:<name>` pattern
    - _Requirements: 3.2, 3.5, 3.7_

- [ ] 5. Doctag Renderer implementation
  - [ ] 5.1 Create Doctag Renderer module
    - Create `src/mrdr/render/doctag_renderer.py`
    - Create DoctagType enum with DDL, GRM, IDC, FMT, DOC values
    - Create DOCTAG_COLORS mapping for semantic coloring
    - _Requirements: 4.1, 4.3, 4.4, 4.6_

  - [ ] 5.2 Implement Doctag Renderer
    - Create DoctagRenderer class with render_tag method
    - Implement _get_tag_type method for type detection
    - Apply SCREAMINGSNAKE case to identifiers
    - Render IDC tokens with link-style formatting
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.6_

  - [ ] 5.3 Write property test for Doctag token rendering
    - **Property 10: Doctag Token Rendering**
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.6**

  - [ ] 5.4 Implement Doctag lookup command
    - Add `mrdr jekyl doctag <tag_id>` command
    - Display tag definition with short name, full name, description, example
    - _Requirements: 4.5_

  - [ ] 5.5 Write property test for Doctag lookup
    - **Property 11: Doctag Lookup Display**
    - **Validates: Requirements 4.5**

- [ ] 6. Checkpoint - UDL and Doctag complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Python Style Renderer implementation
  - [ ] 7.1 Create Python Style Renderer module
    - Create `src/mrdr/render/python_style.py`
    - Create PythonDocstringStyle enum with sphinx, google, numpy, epytext, pep257
    - Create STYLE_TEMPLATES dict with example code for each style
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ] 7.2 Implement Python Style Renderer
    - Create PythonStyleRenderer class
    - Implement render_style method producing Rich Panel with Syntax
    - Implement render_all_styles method for comparison view
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [ ] 7.3 Write property test for Python style compliance
    - **Property 12: Python Style Format Compliance**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.7**

  - [ ] 7.4 Update docstring command with style support
    - Add --style flag to `mrdr docstring python` command
    - Add --all-styles flag for comparison view
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [ ] 8. Hierarchy Display implementation
  - [ ] 8.1 Create Hierarchy Display module
    - Create `src/mrdr/render/components/hierarchy.py`
    - Create HierarchyLevel enum with grandparent, parent, child, grandchild
    - Create HIERARCHY_STYLES mapping for level styling
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

  - [ ] 8.2 Implement Hierarchy Display
    - Create HierarchyNode dataclass with name, alias, level, description, children
    - Create HierarchyDisplay class with render method producing Rich Tree
    - Implement _format_node and _add_children methods
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

  - [ ] 8.3 Write property test for Hierarchy indentation
    - **Property 13: Hierarchy Level Indentation**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.5**

  - [ ] 8.4 Implement Hierarchy lookup command
    - Add `mrdr hyde hierarchy <term>` command
    - Display term position in hierarchy tree
    - _Requirements: 6.4_

  - [ ] 8.5 Write property test for Hierarchy lookup
    - **Property 14: Hierarchy Term Lookup**
    - **Validates: Requirements 6.4**

- [ ] 9. Alert Component implementation
  - [ ] 9.1 Create Alert Component module
    - Create `src/mrdr/render/components/alert.py`
    - Create AlertType enum with note, tip, important, warning, caution
    - Create ALERT_CONFIG dict with icon, color, title for each type
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

  - [ ] 9.2 Implement Alert Component
    - Create AlertComponent dataclass with alert_type, message fields
    - Implement render method producing Rich Panel with icon and color
    - Implement render_plain method for plain text output
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

  - [ ] 9.3 Write property test for Alert styling
    - **Property 18: Alert Type Styling**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**

- [ ] 10. Checkpoint - Renderers complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Mermaid Renderer implementation
  - [ ] 11.1 Create Mermaid Renderer module
    - Create `src/mrdr/render/components/mermaid.py`
    - Create MermaidRenderer class with render method
    - Implement _detect_type method for diagram type detection
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 11.2 Implement Mermaid flowchart rendering
    - Implement _render_flowchart method extracting nodes and connections
    - Render ASCII boxes with ┌─┐│└─┘ characters
    - Render arrows with │ and ▼ characters
    - _Requirements: 7.1, 7.2_

  - [ ] 11.3 Write property test for Mermaid flowchart
    - **Property 15: Mermaid Flowchart Rendering**
    - **Validates: Requirements 7.1, 7.2**

  - [ ] 11.4 Implement Mermaid sequence rendering
    - Implement _render_sequence method extracting participants and messages
    - Render participant headers and message arrows
    - _Requirements: 7.3_

  - [ ] 11.5 Write property test for Mermaid sequence
    - **Property 16: Mermaid Sequence Rendering**
    - **Validates: Requirements 7.3**

  - [ ] 11.6 Implement Mermaid fallback
    - Implement _render_fallback method returning raw source in code fence
    - Handle exceptions gracefully
    - _Requirements: 7.4_

  - [ ] 11.7 Write property test for Mermaid fallback
    - **Property 17: Mermaid Fallback**
    - **Validates: Requirements 7.4**

  - [ ] 11.8 Implement diagram command
    - Add `mrdr jekyl diagram <type>` command
    - Display example diagrams for flowchart and sequence types
    - _Requirements: 7.5_

- [ ] 12. Conflict Display implementation
  - [ ] 12.1 Create Conflict Display module
    - Create `src/mrdr/render/components/conflict.py`
    - Create SyntaxConflict dataclass with languages, delimiter, resolution, attachment_rules
    - Create ConflictDisplay class
    - _Requirements: 9.1, 9.2, 9.3, 9.5_

  - [ ] 12.2 Implement Conflict Display
    - Implement render_warning method producing warning Panel
    - Implement render_table method producing conflicts Table
    - Include resolution guidance in output
    - _Requirements: 9.1, 9.2, 9.3, 9.5_

  - [ ] 12.3 Write property test for Conflict information
    - **Property 19: Conflict Information Completeness**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.5**

  - [ ] 12.4 Implement conflicts command
    - Add `mrdr jekyl conflicts` command
    - Display all known syntax conflicts in table format
    - _Requirements: 9.4_

  - [ ] 12.5 Write property test for Conflict table
    - **Property 20: Conflict Table Display**
    - **Validates: Requirements 9.4**

  - [ ] 12.6 Integrate conflict warnings into show command
    - Update `mrdr jekyl show` to display conflict warning when conflict_ref exists
    - _Requirements: 9.1_

- [ ] 13. Checkpoint - Mermaid and Conflict complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Advanced Table Renderer implementation
  - [ ] 14.1 Create Advanced Table Renderer module
    - Create `src/mrdr/render/components/table_advanced.py`
    - Create TableConfig dataclass with columns, filter, sort, pagination fields
    - Create AdvancedTableRenderer class
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [ ] 14.2 Implement table filtering
    - Implement _apply_filter method for row filtering
    - Support field=value filter syntax
    - _Requirements: 10.3_

  - [ ] 14.3 Write property test for Table row filtering
    - **Property 23: Table Row Filtering**
    - **Validates: Requirements 10.3**

  - [ ] 14.4 Implement table sorting
    - Implement _apply_sort method for column sorting
    - Support ascending/descending toggle
    - _Requirements: 10.4_

  - [ ] 14.5 Write property test for Table sorting
    - **Property 24: Table Sorting**
    - **Validates: Requirements 10.4**

  - [ ] 14.6 Implement table pagination
    - Implement _apply_pagination method
    - Implement _render_pagination_hints method
    - _Requirements: 10.5_

  - [ ] 14.7 Write property test for Table pagination
    - **Property 25: Table Pagination**
    - **Validates: Requirements 10.5**

  - [ ] 14.8 Implement column filtering
    - Update _build_table to respect columns config
    - _Requirements: 10.2_

  - [ ] 14.9 Write property test for Table column filtering
    - **Property 22: Table Column Filtering**
    - **Validates: Requirements 10.2**

  - [ ] 14.10 Implement markdown export
    - Implement export_markdown method
    - Generate valid GFM table syntax
    - _Requirements: 10.6_

  - [ ] 14.11 Write property test for Table markdown export
    - **Property 26: Table Markdown Export**
    - **Validates: Requirements 10.6**

  - [ ] 14.12 Implement table command
    - Add `mrdr jekyl table --master` command
    - Add --columns, --filter, --sort, --export options
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.6_

  - [ ] 14.13 Write property test for Master table completeness
    - **Property 21: Master Table Completeness**
    - **Validates: Requirements 10.1**

- [ ] 15. Checkpoint - Table Renderer complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. CLI integration and wiring
  - [ ] 16.1 Create visual commands module
    - Create `src/mrdr/cli/visual_commands.py`
    - Wire --card, --accordion, --gutter flags to jekyl show
    - _Requirements: 1.1, 1.3, 2.1_

  - [ ] 16.2 Update jekyl commands with visual options
    - Add --card flag to show command
    - Add --accordion flag to show command
    - Add --gutter and --start-line flags to show command
    - _Requirements: 1.1, 1.3, 2.1, 2.4_

  - [ ] 16.3 Wire UDL commands to hyde
    - Register udl subcommand group under hyde
    - Wire create, list commands
    - _Requirements: 3.2, 3.7_

  - [ ] 16.4 Wire doctag command to jekyl
    - Register doctag command under jekyl
    - _Requirements: 4.5_

  - [ ] 16.5 Wire hierarchy command to hyde
    - Register hierarchy command under hyde
    - _Requirements: 6.4_

  - [ ] 16.6 Wire diagram command to jekyl
    - Register diagram command under jekyl
    - _Requirements: 7.5_

  - [ ] 16.7 Wire conflicts command to jekyl
    - Register conflicts command under jekyl
    - _Requirements: 9.4_

  - [ ] 16.8 Wire table command to jekyl
    - Register table command under jekyl with all options
    - _Requirements: 10.1_

- [ ] 17. Final checkpoint - All tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks including property-based tests are required for comprehensive coverage
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation builds on the existing mrdr-cli-foundation
- All naming follows docs → src → cli cohesion principle from AGENTS.md
