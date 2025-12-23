# AGENTS.md

Project: BILL CLYE - The Syntax CLI
Purpose: A CLI-driven syntax and docstring database that documents, categorizes,
and displays examples for common codebases. The current focus is planning and
spec definition, with Python + Rich as the intended implementation stack.

Development stage: PLANNING

## Specs and Docs Map
- `docs/doc_specs/cli_spec.md`: Primary CLI design source of truth. Defines
  intended commands, options, roadmap, and the modular design intent. The main
  invocation is `bill` / `clye` (final choice still open in TODOs).
- `docs/doc_specs/metadata_spec.md`: Document metadata format for the ecosystem,
  including docstring-style header metadata and a planned YAML metadata spec.
- `docs/doc_specs/todo_spec.md`: TODO format rules (SCREAMINGSNAKE headers,
  SIMPLENUMERIC IDs, tasklist format).
- `docs/doctags.md`: Doc tag system, delimiters, grammar identifiers, and
  formatting rules that drive consistency across docs and future CLI output.
- `docs/dictionary.md`: Canonical definitions for tag terminology and hierarchy.
- `docs/TODO.md`: Active TODOs; follow the TODO spec and templates.
- `docs/repository_tree.md`: Expected repository layout; update if structure
  changes.
- `templates/docstring_template.md`, `templates/todo_template.md`: Templates for
  consistent docstrings and TODO items.

## Data Sources
- `database/`: Canonical data storage for delimiters, docstrings, operators,
  tables, and language-specific references. CLI output should eventually render
  data from this directory.
- `database/docstrings/`: Docstring examples and the database files referenced
  by the CLI spec.

## Consistency Requirements
- Keep names, tags, and terminology aligned across docs -> database -> src -> CLI.
- Use SCREAMINGSNAKE tags, SIMPLENUMERIC IDs, and delimiters as defined in
  `docs/doctags.md`.
- Maintain document metadata comments as defined in
  `docs/doc_specs/metadata_spec.md`.
- When adding TODOs, follow `docs/doc_specs/todo_spec.md` and
  `templates/todo_template.md`.

## Design Stages (Contextual Workflow)
1. Document spec and database foundations:
   - Define and stabilize tags, metadata, dictionary terms, and docstring
     examples.
2. CLI spec and UX behavior:
   - Specify commands, options, and output modules. Initial output focuses on
     docstrings, with a comprehensive modular base for future integration.
3. Python source spec and implementation:
   - Translate the CLI + document specs into `src/` using Python + Rich while
     preserving naming, tags, and behaviors from the docs.

## Notes for Agents
- Treat `docs/doc_specs/cli_spec.md` as the authoritative CLI spec until a
  dedicated Python source spec exists.
- Preserve TODO markers and open questions; do not resolve them unless asked.
- If the repository structure changes, update `docs/repository_tree.md`.
