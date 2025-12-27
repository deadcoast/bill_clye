# Implementation Plan: MRDR Data Population
[MRDR:doc:spec=doctags](/docs/doctags.md)

## Overview

This implementation plan transforms the MRDR Data Population design into actionable coding tasks. The approach prioritizes creating database JSON files first, then updating loaders and schemas, and finally wiring everything together. Property-based tests are integrated alongside implementation to validate data integrity.

## Tasks

- [x] 1. Docstring Database Expansion
  - [x] 1.1 Expand docstring_database.json with additional languages
    - Add entries for: TypeScript, Java, Kotlin, Scala, PHP, Swift, Zig, F#, Ruby, Ada, OCaml, Clojure, Fortran
    - Each entry must include: language, syntax.start, syntax.end, syntax.type, syntax.location
    - Add tags, example_content, and conflict_ref where applicable
    - _Requirements: 1.1, 1.2, 1.5_

  - [x] 1.2 Add conflict references to existing entries
    - Update Python entry with conflict_ref to Julia
    - Update Julia entry with conflict_ref to Python
    - Update JavaScript entry with conflict_ref to D
    - Update D entry with conflict_ref to JavaScript
    - _Requirements: 1.4_

  - [x] 1.3 Add PLUSREP grades to select entries
    - Add plusrep field to Python, JavaScript, Rust entries
    - Ensure tokens are 6 characters, rating matches formula
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [x] 1.4 Write property test for docstring database
    - **Property 1: Docstring Database Language Count**
    - **Property 2: Docstring Entry Schema Validity**
    - **Property 3: Conflict Reference Consistency**
    - **Validates: Requirements 1.1, 1.2, 1.4**

- [x] 2. Doctag Database Creation
  - [x] 2.1 Create doctag_database.json file
    - Create `database/doctags/` directory
    - Create `database/doctags/doctag_database.json` with manifest
    - _Requirements: 2.1_

  - [x] 2.2 Populate DDL (Delimiter) tags
    - Add DDL01-DDL10 entries from doctags.md
    - Include: id, symbol, short_name, description, category, example
    - DDL01: `+` ADDTACH, DDL02: `-+` DELREM, DDL03: `!>` EXCEPTFOR, etc.
    - _Requirements: 2.2, 2.7_

  - [x] 2.3 Populate GRM (Grammar) tags
    - Add GRM01-GRM10 entries from doctags.md
    - GRM01: rstr RESTRICTIONS, GRM02: ntype NAMETYPE, etc.
    - _Requirements: 2.3, 2.7_

  - [x] 2.4 Populate IDC (Inter-Document Command) tags
    - Add IDC01-IDC10 entries from doctags.md
    - IDC01: LANGUSE, IDC02: DOCLINK, IDC03: FILELINK, etc.
    - _Requirements: 2.4, 2.7_

  - [x] 2.5 Populate FMT (Formatting) tags
    - Add FMT01-FMT10 entries from doctags.md
    - FMT01: newline, FMT02: nlrule, FMT03: cfgdflt, etc.
    - _Requirements: 2.5, 2.7_

  - [x] 2.6 Populate DOC (Document Spec) tags
    - Add DOC01-DOC05 entries from doctags.md
    - DOC01: MRDR:doc:spec=doctags, DOC02: MRDR:doc:spec=metadata, etc.
    - _Requirements: 2.6, 2.7_

  - [x] 2.7 Write property test for doctag database
    - **Property 4: Doctag Category Completeness**
    - **Property 5: Doctag Entry Schema Validity**
    - **Property 16: SCREAMINGSNAKE Case Compliance**
    - **Validates: Requirements 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 9.1**

- [x] 3. Checkpoint - Docstring and Doctag databases complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Dictionary Database Creation
  - [x] 4.1 Create dictionary_database.json file
    - Create `database/dictionary/` directory
    - Create `database/dictionary/dictionary_database.json` with manifest
    - _Requirements: 3.1_

  - [x] 4.2 Populate NAMETYPE definitions
    - Add CHD (CHILD), PNT (PARENT), GPN (GRANDPARENT) entries
    - Include hierarchical relationships
    - _Requirements: 3.7_

  - [x] 4.3 Populate grandparent functions
    - Add NOTE, CLAIM, LANG_USE, FORMAT, PURPOSE, RESTRICTIONS, STYLING, USER, NOTES
    - Each with name, alias, level=grandparent, description
    - _Requirements: 3.2, 3.6_

  - [x] 4.4 Populate parent commands
    - Add apd (ASPERDEFINED), objacc (OBJECTIVEACCEPTANCE)
    - Include full descriptions from dictionary.md
    - _Requirements: 3.3, 3.6_

  - [x] 4.5 Populate child functions
    - Add sem, def, dstr, rsch, stat, eg, vldt, expr, optml, unstbl, vislap, crtv
    - Each with name, alias, level=child, description
    - _Requirements: 3.4, 3.6_

  - [x] 4.6 Populate grandchild entries
    - Add val, value entries
    - _Requirements: 3.5, 3.6_

  - [x] 4.7 Write property test for dictionary database
    - **Property 6: Dictionary Hierarchy Completeness**
    - **Property 7: Dictionary Entry Schema Validity**
    - **Property 8: Dictionary NAMETYPE Definitions**
    - **Validates: Requirements 3.2, 3.3, 3.4, 3.5, 3.6, 3.7**

- [x] 5. Python Styles Database Creation
  - [x] 5.1 Create python_styles.json file
    - Create `database/languages/python/python_styles.json`
    - Add manifest with version
    - _Requirements: 4.1_

  - [x] 5.2 Populate Sphinx style entry
    - Add sphinx style with :param:, :type:, :return:, :rtype: markers
    - Include template_code from docstring_styles.md
    - Include rules for summary line, spacing, indentation, termination
    - _Requirements: 4.2, 4.7_

  - [x] 5.3 Populate Google style entry
    - Add google style with Args:, Returns: markers
    - Include template_code and rules
    - _Requirements: 4.3, 4.7_

  - [x] 5.4 Populate NumPy style entry
    - Add numpy style with Parameters, Returns headers and dashed separators
    - Include template_code and rules
    - _Requirements: 4.4, 4.7_

  - [x] 5.5 Populate Epytext style entry
    - Add epytext style with @param, @type, @return markers
    - Include template_code and rules
    - _Requirements: 4.5, 4.7_

  - [x] 5.6 Populate PEP 257 style entry
    - Add pep257 minimal style
    - Include template_code and rules
    - _Requirements: 4.6, 4.7_

  - [x] 5.7 Write property test for Python styles database
    - **Property 9: Python Style Completeness**
    - **Property 10: Python Style Entry Schema Validity**
    - **Validates: Requirements 4.2, 4.3, 4.4, 4.5, 4.6, 4.7**

- [x] 6. Checkpoint - Dictionary and Python styles complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. UDL Database Creation
  - [x] 7.1 Create udl_database.json file
    - Create `database/languages/udl/udl_database.json`
    - Add manifest with version
    - _Requirements: 5.1_

  - [x] 7.2 Populate Pointy-Numerical-Index template
    - Add pindx template from udl_template.md
    - Include delimiter_open=<, delimiter_close=>, brackets
    - _Requirements: 5.2, 5.5_

  - [x] 7.3 Add dolphin operator variant
    - Add dolphin template with open=<: close=:>
    - Include example usage
    - _Requirements: 5.3, 5.5_

  - [x] 7.4 Add walrus operator variant
    - Add walrus template with open=:= close==:
    - Include example usage
    - _Requirements: 5.4, 5.5_

  - [x] 7.5 Write property test for UDL database
    - **Property 11: UDL Operator Definitions**
    - **Property 12: UDL Entry Schema Validity**
    - **Validates: Requirements 5.3, 5.4, 5.5**

- [-] 8. Conflict Database Creation
  - [ ] 8.1 Create conflict_database.json file
    - Create `database/conflicts/` directory
    - Create `database/conflicts/conflict_database.json` with manifest
    - _Requirements: 6.1_

  - [ ] 8.2 Add Python vs Julia conflict
    - Document triple-quote delimiter conflict
    - Include attachment_rules: Python=internal_first_line, Julia=above_target
    - Include resolution guidance
    - _Requirements: 6.2, 6.5_

  - [ ] 8.3 Add JavaScript vs D conflict
    - Document block comment conflict with nesting differences
    - Include attachment_rules and resolution
    - _Requirements: 6.3, 6.5_

  - [ ] 8.4 Add Rust vs Zig similarity
    - Document line doc comment similarities
    - Include attachment_rules and resolution
    - _Requirements: 6.4, 6.5_

  - [ ] 8.5 Write property test for conflict database
    - **Property 13: Conflict Entry Schema Validity**
    - **Validates: Requirements 6.5**

- [ ] 9. Checkpoint - UDL and Conflict databases complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Schema and Loader Updates
  - [ ] 10.1 Update doctag schema
    - Update `src/mrdr/database/doctag/schema.py` with DoctagEntry model
    - Add DoctagCategory enum with DDL, GRM, IDC, FMT, DOC
    - _Requirements: 2.7_

  - [ ] 10.2 Update doctag loader
    - Update `src/mrdr/database/doctag/loader.py` to load from new JSON path
    - Implement list_by_category method
    - _Requirements: 2.1_

  - [ ] 10.3 Create dictionary schema
    - Create `src/mrdr/database/dictionary/schema.py`
    - Add DictionaryEntry, DictionaryDatabase models
    - _Requirements: 3.6_

  - [ ] 10.4 Create dictionary loader
    - Create `src/mrdr/database/dictionary/loader.py`
    - Implement load, get_term, get_hierarchy_path methods
    - _Requirements: 3.1_

  - [ ] 10.5 Create Python styles schema
    - Create `src/mrdr/database/python_styles/schema.py`
    - Add PythonStyleEntry, PythonStyleMarker models
    - _Requirements: 4.7_

  - [ ] 10.6 Create Python styles loader
    - Create `src/mrdr/database/python_styles/loader.py`
    - Implement load, get_style methods
    - _Requirements: 4.1_

  - [ ] 10.7 Create conflict schema
    - Create `src/mrdr/database/conflict/schema.py`
    - Add ConflictEntry, ConflictDatabase models
    - _Requirements: 6.5_

  - [ ] 10.8 Create conflict loader
    - Create `src/mrdr/database/conflict/loader.py`
    - Implement load, get_conflict_for_language methods
    - _Requirements: 6.1_

  - [ ] 10.9 Update UDL loader
    - Update `src/mrdr/database/udl/loader.py` to load from new JSON path
    - _Requirements: 5.1_

- [ ] 11. Validation and Error Handling
  - [ ] 11.1 Implement validation error collection
    - Update all loaders to collect validation errors
    - Store errors with entry identifier and field failures
    - _Requirements: 8.2, 8.3_

  - [ ] 11.2 Add validate command to hyde
    - Add `mrdr hyde validate` command
    - Check all database files against schemas
    - Report validation status and errors
    - _Requirements: 8.4_

  - [ ] 11.3 Write property test for validation
    - **Property 15: Validation Error Handling**
    - **Validates: Requirements 8.1, 8.2, 8.3**

- [ ] 12. PLUSREP Integration
  - [ ] 12.1 Update PLUSREP schema validation
    - Ensure tokens pattern validation (6 chars of + and .)
    - Add rating calculation validation
    - Add label-to-rating mapping validation
    - _Requirements: 7.2, 7.3, 7.4_

  - [ ] 12.2 Write property test for PLUSREP
    - **Property 14: PLUSREP Consistency**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

- [ ] 13. Checkpoint - Schemas and loaders complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Cross-Database Consistency
  - [ ] 14.1 Add example_content to docstring entries
    - Add canonical payload examples to Python, JavaScript, Rust entries
    - Include format, purpose, user fields
    - _Requirements: 10.1, 10.2_

  - [ ] 14.2 Write property test for consistency
    - **Property 17: Cross-Database Term Consistency**
    - **Property 18: Example Content Canonical Format**
    - **Validates: Requirements 9.3, 10.1, 10.2**

- [ ] 15. Integration and Wiring
  - [ ] 15.1 Update factory.py with new loaders
    - Add factory functions for new database loaders
    - Wire into hyde controller
    - _Requirements: 8.1_

  - [ ] 15.2 Update hyde controller with new data sources
    - Add methods to access doctag, dictionary, python_styles, conflict data
    - _Requirements: 8.1_

  - [ ] 15.3 Update jekyl commands to use new data
    - Update doctag command to use new loader
    - Update hierarchy command to use dictionary loader
    - Update docstring command to use python_styles loader
    - Update conflicts command to use conflict loader
    - _Requirements: 8.1_

- [ ] 16. Final checkpoint - All tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks including property-based tests are required for comprehensive coverage
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Database JSON files are created before loaders to enable testing
- The implementation follows the docs → src → cli nametype cohesion principle
- All naming uses SCREAMINGSNAKE case for tag identifiers as defined in doctags.md
