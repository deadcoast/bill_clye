# Requirements Document: MRDR Data Population
[MRDR:doc:spec=doctags](/docs/doctags.md)

## Introduction

This document defines the requirements for populating the MRDR database ecosystem with the comprehensive data described in the documentation suite. The CLI framework and visual components are implemented, but the underlying data sources remain sparse. This spec focuses on creating and populating JSON databases, expanding language coverage, and ensuring data consistency across the ecosystem.

## Glossary

- **Docstring_Database**: Primary JSON database storing syntax signatures for programming languages
- **Doctag_Database**: JSON database storing DDL, GRM, IDC, FMT, DOC tag definitions from doctags.md
- **Dictionary_Database**: JSON database storing the MRDR dictionary hierarchy from dictionary.md
- **UDL_Database**: JSON database storing User Defined Language templates
- **Python_Styles_Database**: JSON database storing Python docstring style definitions
- **Conflict_Database**: JSON database storing syntax conflict information
- **PLUSREP_Grade**: Quality rating using 6-token scale from `[++++++]` to `[+.....]`
- **Canonical_Payload**: Standardized YAML/JSON metadata schema for database entries
- **Carrier_Syntax**: Language-specific docstring delimiter patterns

## Requirements

### Requirement 1: Docstring Database Expansion

**User Story:** As a developer, I want comprehensive docstring syntax data for all major programming languages, so that I can reference correct documentation patterns for any language I work with.

#### Acceptance Criteria

1. THE Docstring_Database SHALL contain entries for at least 25 programming languages as defined in table_database.md
2. WHEN a language entry is added, THE entry SHALL include: language name, syntax.start, syntax.end, syntax.type, syntax.location
3. THE Docstring_Database SHALL include optional fields: tags, example_content, conflict_ref, parsing_rule, metadata, plusrep
4. WHEN languages share identical delimiters, THE entries SHALL include conflict_ref pointing to the conflicting language
5. THE Docstring_Database SHALL include entries for: Python, JavaScript, TypeScript, Java, Kotlin, Scala, PHP, Swift, Rust, Zig, C#, F#, Elixir, Ruby, Lua, D, Julia, Haskell, COBOL, Raku, Erlang, Ada, OCaml, Clojure, Fortran
6. WHEN a language has multiple docstring styles, THE entry SHALL document the primary/official style

### Requirement 2: Doctag Database Creation

**User Story:** As a documentation author, I want a structured database of all doctags, so that the CLI can render and look up tag definitions programmatically.

#### Acceptance Criteria

1. THE Doctag_Database SHALL be stored at `database/doctags/doctag_database.json`
2. THE Doctag_Database SHALL contain all DDL (Delimiter) tags DDL01-DDL10 as defined in doctags.md
3. THE Doctag_Database SHALL contain all GRM (Grammar) tags GRM01-GRM10 as defined in doctags.md
4. THE Doctag_Database SHALL contain all IDC (Inter-Document Command) tags IDC01-IDC10 as defined in doctags.md
5. THE Doctag_Database SHALL contain all FMT (Formatting) tags FMT01-FMT10 as defined in doctags.md
6. THE Doctag_Database SHALL contain all DOC (Document Spec) tags DOC01-DOC05 as defined in doctags.md
7. WHEN a doctag entry is created, THE entry SHALL include: id, symbol, short_name, description, category, example

### Requirement 3: Dictionary Hierarchy Database

**User Story:** As a user, I want the MRDR dictionary hierarchy stored in a structured format, so that the CLI can display and navigate the term relationships.

#### Acceptance Criteria

1. THE Dictionary_Database SHALL be stored at `database/dictionary/dictionary_database.json`
2. THE Dictionary_Database SHALL contain all grandparent functions: NOTE, CLAIM, LANG_USE, FORMAT, PURPOSE, RESTRICTIONS, STYLING, USER, NOTES
3. THE Dictionary_Database SHALL contain all parent commands: apd (ASPERDEFINED), objacc (OBJECTIVEACCEPTANCE)
4. THE Dictionary_Database SHALL contain all child functions: sem, def, dstr, rsch, stat, eg, vldt, expr, optml, unstbl, vislap, crtv
5. THE Dictionary_Database SHALL contain grandchild entries: val, value
6. WHEN a term entry is created, THE entry SHALL include: name, alias, level, description, children (if applicable)
7. THE Dictionary_Database SHALL include NAMETYPE definitions: CHD, PNT, GPN with their hierarchical relationships

### Requirement 4: Python Docstring Styles Database

**User Story:** As a Python developer, I want all five docstring styles stored in a structured database, so that the CLI can render and compare them accurately.

#### Acceptance Criteria

1. THE Python_Styles_Database SHALL be stored at `database/languages/python/python_styles.json`
2. THE Python_Styles_Database SHALL contain Sphinx (reStructuredText) style with :param:, :type:, :return:, :rtype: markers
3. THE Python_Styles_Database SHALL contain Google style with Args:, Returns: sections
4. THE Python_Styles_Database SHALL contain NumPy style with Parameters, Returns headers and dashed separators
5. THE Python_Styles_Database SHALL contain Epytext style with @param, @type, @return markers
6. THE Python_Styles_Database SHALL contain PEP 257 minimal style
7. WHEN a style entry is created, THE entry SHALL include: name, description, markers, template_code, rules

### Requirement 5: UDL Templates Database

**User Story:** As a power user, I want predefined UDL templates available, so that I can quickly adopt custom docstring formats.

#### Acceptance Criteria

1. THE UDL_Database SHALL be stored at `database/languages/udl/udl_database.json`
2. THE UDL_Database SHALL contain the Pointy-Numerical-Index template from udl_template.md
3. THE UDL_Database SHALL contain dolphin operator variant with `<:` `:>` delimiters
4. THE UDL_Database SHALL contain walrus operator variant with `:=` `=:` delimiters
5. WHEN a UDL entry is created, THE entry SHALL include: name, title, description, language, delimiter_open, delimiter_close, operators, examples

### Requirement 6: Conflict Database

**User Story:** As a developer, I want syntax conflicts documented in a structured database, so that the CLI can warn about and explain delimiter collisions.

#### Acceptance Criteria

1. THE Conflict_Database SHALL be stored at `database/conflicts/conflict_database.json`
2. THE Conflict_Database SHALL document Python vs Julia triple-quote conflict with attachment rule differences
3. THE Conflict_Database SHALL document JavaScript vs D block comment conflict with nesting differences
4. THE Conflict_Database SHALL document Rust vs Zig line doc comment similarities
5. WHEN a conflict entry is created, THE entry SHALL include: delimiter, languages, resolution, attachment_rules

### Requirement 7: PLUSREP Grade Population

**User Story:** As a quality reviewer, I want PLUSREP grades assigned to database entries, so that quality metrics are visible in CLI output.

#### Acceptance Criteria

1. WHEN a docstring entry has quality assessment, THE entry SHALL include plusrep field with tokens, rating, label
2. THE PLUSREP tokens SHALL use exactly 6 characters of `+` and `.`
3. THE PLUSREP rating SHALL be calculated as (count of '+') - 2, ranging from -2 to +4
4. THE PLUSREP label SHALL match the rating: MAXIMUM (+4), GREAT (+2/+3), SLOPPY (0), REJECTED (-2), RESET (-3)

### Requirement 8: Database Schema Validation

**User Story:** As a maintainer, I want all database files validated against schemas, so that data integrity is guaranteed.

#### Acceptance Criteria

1. THE Database_Loader SHALL validate all JSON databases against their Pydantic schemas on load
2. WHEN a database entry fails validation, THE loader SHALL log the error and skip the invalid entry
3. THE Database_Loader SHALL report validation errors with entry identifier and specific field failures
4. THE CLI SHALL provide `mrdr hyde validate` command to check all databases

### Requirement 9: Data Consistency

**User Story:** As a maintainer, I want consistent naming and terminology across all databases, so that the ecosystem remains coherent.

#### Acceptance Criteria

1. THE database entries SHALL use SCREAMINGSNAKE case for tag identifiers as defined in doctags.md
2. THE database entries SHALL use consistent field names across all database types
3. WHEN a term appears in multiple databases, THE term SHALL use identical spelling and casing
4. THE database entries SHALL follow the docs → src → cli nametype cohesion principle from AGENTS.md

### Requirement 10: Example Content Population

**User Story:** As a developer, I want rich example content in database entries, so that I can see practical usage patterns.

#### Acceptance Criteria

1. WHEN a docstring entry has example_content, THE content SHALL demonstrate the canonical payload format
2. THE example_content SHALL include format, purpose, user fields as defined in table_database.md
3. THE example_content SHALL be valid syntax for the target language
4. WHEN displaying examples, THE CLI SHALL apply language-appropriate syntax highlighting

