# Requirements Document: MRDR Visual Integration
[MRDR:doc:spec=doctags](/docs/doctags.md)

## Introduction

This document defines the requirements for the MRDR Visual Integration feature—extending the CLI foundation with advanced visual patterns, the UDL (User Defined Language) docstring system, comprehensive doctag rendering, Python docstring style support, and the full visual pattern library integration. This spec focuses on integrating all designed frameworks from the documentation suite into the working CLI.

## Glossary

- **Visual_Pattern_Library**: Collection of GitHub-Flavored Markdown patterns for rich CLI UI documentation rendering
- **UDL_System**: User Defined Language docstring template system supporting custom delimiter patterns
- **Doctag_Renderer**: Component that renders doctag syntax with proper delimiter highlighting
- **Line_Gutter**: Line number gutterguard UI component for Rich output
- **Card_Grid**: Table-based card layout component for command documentation
- **Accordion_Spec**: Collapsible details/summary component for expandable content
- **Pseudo_Tab**: Multiple details blocks simulating tabbed interface
- **Keybar_Component**: Keycap-styled keybind display component
- **Mermaid_Renderer**: Component for rendering Mermaid diagrams in terminal
- **Python_Style_Renderer**: Component for rendering Python docstring styles (Sphinx, Google, NumPy, Epytext, PEP257)
- **Dolphin_Operator**: UDL operator pattern using `<:` and `:>` delimiters
- **Walrus_Operator**: UDL operator pattern using `:=` and `=:` delimiters
- **Hierarchy_Display**: Component for rendering grandparent/parent/child data hierarchies

## Requirements

### Requirement 1: Visual Pattern Library Integration

**User Story:** As a developer, I want rich visual output patterns in the CLI, so that documentation feels interactive and modern like the visual pattern library spec.

#### Acceptance Criteria

1. WHEN `mrdr jekyl show <language> --card` is invoked, THE Jekyl_Controller SHALL render output using the Card_Grid layout pattern
2. THE Card_Grid component SHALL display: command name, purpose, UI description, and modes in a table-based card format
3. WHEN `mrdr jekyl show <language> --accordion` is invoked, THE Jekyl_Controller SHALL render expandable sections using Rich details panels
4. THE Accordion_Spec component SHALL support `open` attribute for default-expanded sections
5. WHEN rendering keybind hints, THE Keybar_Component SHALL use `<kbd>` style formatting with Rich markup
6. THE Visual_Pattern_Library components SHALL support theme-aware rendering based on terminal capabilities

### Requirement 2: Line Number Gutter Guard

**User Story:** As a developer, I want line-numbered code display, so that I can reference specific lines in docstring examples.

#### Acceptance Criteria

1. WHEN `mrdr jekyl show <language> --gutter` is invoked, THE Jekyl_Controller SHALL display code with line number gutters
2. THE Line_Gutter component SHALL render line numbers in a dim style separated by `|` from content
3. WHEN `mrdr jekyl show <language> --plain` is combined with `--gutter`, THE Line_Gutter SHALL render without ANSI codes
4. THE Line_Gutter component SHALL support configurable starting line number via `--start-line <n>` option
5. THE Line_Gutter component SHALL align line numbers right-justified based on total line count

### Requirement 3: UDL (User Defined Language) System

**User Story:** As a power user, I want to define custom docstring formats, so that I can document proprietary or experimental syntax patterns.

#### Acceptance Criteria

1. THE UDL_System SHALL support custom docstring definitions with TITLE, DESCR, LANG, DELIMITER, and OPERATOR fields
2. WHEN `mrdr hyde udl create <name>` is invoked, THE Hyde_Controller SHALL create a new UDL template in `database/languages/udl/`
3. THE UDL_System SHALL support the Dolphin_Operator pattern with `<:` opening and `:>` closing delimiters
4. THE UDL_System SHALL support the Walrus_Operator pattern with `:=` opening and `=:` closing delimiters
5. WHEN `mrdr jekyl show udl:<name>` is invoked, THE Jekyl_Controller SHALL render the custom UDL docstring format
6. THE UDL_System SHALL validate that DELIMITER is a single character and OPERATOR is exactly two characters
7. WHEN `mrdr hyde udl list` is invoked, THE Hyde_Controller SHALL display all registered UDL definitions

### Requirement 4: Doctag Rendering System

**User Story:** As a documentation author, I want doctags rendered with proper syntax highlighting, so that tag patterns are visually distinct and parseable.

#### Acceptance Criteria

1. THE Doctag_Renderer SHALL highlight delimiter tokens (DDL01-DDL10) with distinct colors
2. WHEN rendering doctags, THE Doctag_Renderer SHALL apply SCREAMINGSNAKE case styling to tag identifiers
3. THE Doctag_Renderer SHALL render grammar tokens (GRM01-GRM10) with semantic coloring
4. THE Doctag_Renderer SHALL render inter-document commands (IDC01-IDC10) as clickable-style links
5. WHEN `mrdr jekyl doctag <tag_id>` is invoked, THE Jekyl_Controller SHALL display the tag definition with examples
6. THE Doctag_Renderer SHALL support formatting tokens (FMT01-FMT10) with appropriate visual indicators

### Requirement 5: Python Docstring Style Support

**User Story:** As a Python developer, I want to view different docstring style formats, so that I can choose and apply the correct style for my project.

#### Acceptance Criteria

1. WHEN `mrdr docstring python --style sphinx` is invoked, THE Python_Style_Renderer SHALL display Sphinx/reStructuredText format with `:param:`, `:type:`, `:return:`, `:rtype:` tags
2. WHEN `mrdr docstring python --style google` is invoked, THE Python_Style_Renderer SHALL display Google format with `Args:`, `Returns:` sections
3. WHEN `mrdr docstring python --style numpy` is invoked, THE Python_Style_Renderer SHALL display NumPy format with `Parameters`, `Returns` headers and `----------` separators
4. WHEN `mrdr docstring python --style epytext` is invoked, THE Python_Style_Renderer SHALL display Epytext format with `@param`, `@type`, `@return` tags
5. WHEN `mrdr docstring python --style pep257` is invoked, THE Python_Style_Renderer SHALL display minimal PEP 257 format
6. WHEN `mrdr docstring python --all-styles` is invoked, THE Jekyl_Controller SHALL display all five styles in a comparison view
7. THE Python_Style_Renderer SHALL include style-specific rules: summary line, structural spacing, field indentation, clean termination

### Requirement 6: Dictionary Hierarchy Display

**User Story:** As a user, I want to see data hierarchies clearly, so that I can understand the relationship between grandparent, parent, and child elements.

#### Acceptance Criteria

1. THE Hierarchy_Display component SHALL render grandparent functions (NOTE, CLAIM, LANG_USE, FORMAT, PURPOSE, RESTRICTIONS, STYLING, USER, NOTES) with top-level styling
2. THE Hierarchy_Display component SHALL render parent commands (apd, objacc) with mid-level indentation
3. THE Hierarchy_Display component SHALL render child functions (sem, def, dstr, rsch, stat, eg, vldt, expr, optml, unstbl, vislap, crtv) with nested indentation
4. WHEN `mrdr hyde hierarchy <term>` is invoked, THE Hyde_Controller SHALL display the term's position in the hierarchy tree
5. THE Hierarchy_Display component SHALL support grandchild level (val, value) with deepest indentation

### Requirement 7: Mermaid Diagram Rendering

**User Story:** As a documentation viewer, I want Mermaid diagrams rendered in the terminal, so that I can visualize architecture and flows without leaving the CLI.

#### Acceptance Criteria

1. WHEN a database entry contains Mermaid diagram content, THE Mermaid_Renderer SHALL convert it to ASCII art representation
2. THE Mermaid_Renderer SHALL support flowchart diagrams with LR (left-right) and TB (top-bottom) directions
3. THE Mermaid_Renderer SHALL support sequence diagrams with participant and message rendering
4. IF Mermaid rendering fails, THEN THE Mermaid_Renderer SHALL fall back to displaying raw Mermaid source
5. WHEN `mrdr jekyl diagram <type>` is invoked, THE Jekyl_Controller SHALL display example diagrams of the specified type

### Requirement 8: Alert Component System

**User Story:** As a CLI user, I want semantic alert messages, so that important information, tips, warnings, and cautions are visually distinct.

#### Acceptance Criteria

1. THE Alert_Component SHALL support NOTE type with blue/cyan styling and informational icon
2. THE Alert_Component SHALL support TIP type with green styling and lightbulb icon
3. THE Alert_Component SHALL support IMPORTANT type with purple styling and exclamation icon
4. THE Alert_Component SHALL support WARNING type with yellow styling and warning icon
5. THE Alert_Component SHALL support CAUTION type with red styling and stop icon
6. WHEN rendering alerts, THE Alert_Component SHALL use Rich Panel with appropriate border color

### Requirement 9: Conflict Resolution Display

**User Story:** As a developer, I want to see syntax conflicts clearly, so that I understand when languages share identical delimiters.

#### Acceptance Criteria

1. WHEN displaying a language with `conflict_ref`, THE Jekyl_Controller SHALL show a conflict warning panel
2. THE Conflict_Display component SHALL list all languages sharing the same delimiter syntax
3. THE Conflict_Display component SHALL explain the attachment rule difference (e.g., Python internal vs Julia external)
4. WHEN `mrdr jekyl conflicts` is invoked, THE Jekyl_Controller SHALL display all known syntax conflicts in a table
5. THE Conflict_Display component SHALL include resolution guidance for each conflict type

### Requirement 10: Database Table Rendering

**User Story:** As a user, I want comprehensive database tables rendered in the CLI, so that I can view all language syntax data at once.

#### Acceptance Criteria

1. WHEN `mrdr jekyl table --master` is invoked, THE Jekyl_Controller SHALL render the master docstring table with all languages
2. THE Table_Renderer SHALL support column filtering via `--columns <col1,col2,...>` option
3. THE Table_Renderer SHALL support row filtering via `--filter <field>=<value>` option
4. THE Table_Renderer SHALL support sorting via `--sort <field>` option with ascending/descending toggle
5. WHEN table output exceeds terminal height, THE Table_Renderer SHALL implement pagination with page navigation hints
6. THE Table_Renderer SHALL support export to markdown format via `--export md` option

