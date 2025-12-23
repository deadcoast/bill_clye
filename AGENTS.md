# Repository Guidelines

This repository is the documentation and data backbone for the BILL CLYE Syntax CLI. Most work here is Markdown and JSON that define CLI terminology, docstring formats, and reference tables.

## Project Structure & Module Organization

- `docs/`: specification and grammar notes (e.g., `docs/spec.md`).
- `database/`: curated data tables and docstring datasets.
- `database/docstrings/`: templates, examples, and the canonical JSON manifest (`docstring_database.json`).
- `cli.md`, `doc-dictionary.md`, `22_user-defined-docstrings.md`: standalone reference docs.
- `src/`: reserved for future CLI implementation (currently empty).

## Build, Test, and Development Commands

There are no build scripts or runnable CLI entrypoints yet; the CLI is still in planning (see `docs/spec.md`). Optional sanity checks:

- `python -m json.tool database/docstrings/docstring_database.json` to validate JSON syntax.
- `rg -n "TODO|FIXME" docs database` to scan for open placeholders.

## Coding Style & Naming Conventions

- Markdown is GitHub-flavored; use clear headings, short paragraphs, and fenced code blocks with language tags.
- Tag keys in docs are typically uppercase (e.g., `FORMAT`, `PURPOSE`) as shown in `doc-dictionary.md`.
- Filenames and JSON keys use `snake_case` (e.g., `docstring_database.json`, `example_content`).
- Markdown linting is configured in `.markdownlint.json` (line-length and some spacing rules are relaxed).

## Testing Guidelines

No automated tests are defined. When updating the docstring database, keep `database/docstrings/docstring_database.json` and `database/docstrings/docstring_database.md` in sync and ensure examples remain valid for their language.

## Commit & Pull Request Guidelines

- Commit messages are short and descriptive; history shows imperative, plain-language summaries (e.g., `Add initial documentation...`, `fix formatting...`).
- PRs should include: a brief summary, the files/sections changed, and any cross-file updates (for example, updating both JSON and Markdown database entries when adding a new language).
