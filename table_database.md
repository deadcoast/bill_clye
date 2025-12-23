# Docstring Tables

A **CLI docstring-table database** needs two things:

1. A **canonical metadata payload** you can parse (recommend: YAML)
2. A catalog of **language-specific doc comment/docstring delimiters** and **attachment rules** (what the docs “bind” to)

This document standardizes both in **GitHub Flavored Markdown** (GFM), with consistent naming, parsing notes, and examples.

> [!IMPORTANT]
> This file is a **reference spec** for your parser/database. “Docstring” here includes:
>
> - true docstrings (stored/attached by runtime/compiler), and
> - doc comments that external tooling parses (JSDoc, KDoc, Rustdoc, etc.)

---

## Table of Contents

- [Canonical Metadata Schema](#canonical-metadata-schema)
- [Recommended Embedding Format](#recommended-embedding-format)
- [Supported Language Signatures](#supported-language-signatures)
- [Parsing Notes](#parsing-notes)
- [Examples](#examples)
- [Duplicate & Conflict Notes](#duplicate--conflict-notes)

---

## Canonical Metadata Schema

Use this as the **single source of truth** for your CLI database entry.

### Canonical keys

| Key | Type | Description |
| --- | --- | --- |
| `user` | string | Profile label or author handle |
| `profile` | string | Short description (1–3 sentences) |
| `skills` | string | Skill summary for downstream behavior |
| `format` | string | Rendering/target format (e.g., `github`) |
| `purpose` | string | Why this metadata exists (e.g., `visual_styling`) |
| `restrictions` | object | Optional constraints for tooling |

### Canonical payload (YAML)

```yaml
format: github
purpose: cli_doc_db
user: "Technical Development"
profile: "A developer and academic looking for new and creative integrations to visually enhance their scientific research paper."
skills: "Well-versed in Markdown; advanced foundation; does not require basic suggestions."
restrictions:
  styling: general_markdown
````

### Canonical payload (JSON)

```json
{
  "format": "github",
  "purpose": "cli_doc_db",
  "user": "Technical Development",
  "profile": "A developer and academic looking for new and creative integrations to visually enhance their scientific research paper.",
  "skills": "Well-versed in Markdown; advanced foundation; does not require basic suggestions.",
  "restrictions": {
    "styling": "general_markdown"
  }
}
```

> [!TIP]
> If you want “absolute truth” language: call the above **Canonical Payload** and treat everything else as **Language Carrier Syntax**.

---

## Recommended Embedding Format

Your database will be more reliable if the *inside* of every doc carrier uses the same payload format.

**Recommendation:** embed the canonical YAML inside each language’s doc carrier.

Why YAML?

- Friendly for humans
- Easy to parse
- Preserves multi-line strings cleanly
- Maps directly to your CLI “details view”

---

## Supported Language Signatures

The table below is designed for parsing: it tells you **what delimiter to detect** and **how the documentation attaches**.

> [!NOTE]
> “Attachment” is the differentiator that resolves conflicts like Python vs Julia (same delimiter, different binding rules).

### Master table

| Language                    | Primary doc carrier                       | Kind               | Attachment                                                    | Minimal example                                                                                                               |                            |                                                                                                         |                                                                           |
| --------------------------- | ----------------------------------------- | ------------------ | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Python**                  | `"""..."""` / `'''...'''`                 | string literal     | First statement in module/class/function becomes `__doc__`    | `py\n\"\"\"format: github\nuser: \"Technical Development\"\n\"\"\"\n\ndef f():\n    \"\"\"profile: ...\"\"\"\n    return 1\n` |                            |                                                                                                         |                                                                           |
| **JavaScript / TypeScript** | `/**...*/`                                | block comment      | Tooling (JSDoc) binds to next symbol                          | `js\n/**\n * format: github\n * user: \"Technical Development\"\n */\nfunction f() {}\n`                                      |                            |                                                                                                         |                                                                           |
| **Java**                    | `/**...*/`                                | block comment      | Tooling (Javadoc) binds to next symbol                        | `java\n/**\n * format: github\n * user: \"Technical Development\"\n */\nclass X {}\n`                                         |                            |                                                                                                         |                                                                           |
| **Kotlin**                  | `/**...*/`                                | block comment      | Tooling (KDoc) binds to next symbol                           | `kt\n/**\n * format: github\n * user: \"Technical Development\"\n */\nfun f() = 1\n`                                          |                            |                                                                                                         |                                                                           |
| **Scala**                   | `/**...*/`                                | block comment      | Tooling (Scaladoc) binds to next symbol                       | `scala\n/**\n * format: github\n */\ndef f = 1\n`                                                                             |                            |                                                                                                         |                                                                           |
| **PHP**                     | `/**...*/`                                | block comment      | Tooling (phpDocumentor) binds to next symbol                  | `php\n/**\n * format: github\n */\nfunction f() {}\n`                                                                         |                            |                                                                                                         |                                                                           |
| **Swift**                   | `///` or `/**...*/`                       | line/block         | Tooling binds to next symbol (Quick Help)                     | `swift\n/// format: github\n/// user: \"Technical Development\"\nfunc f() {}\n`                                               |                            |                                                                                                         |                                                                           |
| **Rust**                    | `///` / `//!`                             | line doc           | Compiler transforms into `#[doc="..."]`                       | `rs\n/// format: github\n/// user: \"Technical Development\"\nfn f() {}\n\n//! module-level docs\n`                           |                            |                                                                                                         |                                                                           |
| **Zig**                     | `///` / `//!`                             | line doc           | `///` item docs, `//!` container/module docs                  | `zig\n//! format: github\n//! user: \"Technical Development\"\n\npub fn f() void {}\n`                                        |                            |                                                                                                         |                                                                           |
| **C#**                      | `/// <...>`                               | XML doc            | Compiler emits XML docs; binds to next symbol                 | `csharp\n/// <summary>format: github</summary>\n/// <remarks>user: Technical Development</remarks>\npublic void F() {}\n`     |                            |                                                                                                         |                                                                           |
| **F#**                      | `///`                                     | XML-ish doc        | Tooling binds to next symbol                                  | `fsharp\n/// format: github\nlet f x = x + 1\n`                                                                               |                            |                                                                                                         |                                                                           |
| **Elixir**                  | `@doc """..."""` / `@moduledoc """..."""` | attribute          | Compiled into BEAM metadata; binds to next def/module         | `elixir\n@doc \"\"\"\nformat: github\nuser: \"Technical Development\"\n\"\"\"\ndef f(), do: :ok\n`                            |                            |                                                                                                         |                                                                           |
| **Ruby**                    | `=begin`…`=end` or `#`                    | block/line         | Tooling (RDoc/YARD) conventionally binds by placement         | `rb\n=begin\nformat: github\nuser: \"Technical Development\"\n=end\n\ndef f; end\n`                                           |                            |                                                                                                         |                                                                           |
| **Lua**                     | `--[[...]]` / `--[=[...]=]`               | block comment      | Comment only; tooling/convention binds by placement           | `lua\n--[=[\nformat: github\nuser: \"Technical Development\"\n]=]\nfunction f() end\n`                                        |                            |                                                                                                         |                                                                           |
| **D**                       | `/++...+/`                                | doc block          | Ddoc binds by placement; supports nesting                     | `d\n/++\n  format: github\n  user: \"Technical Development\"\n+/\nvoid f() {}\n`                                              |                            |                                                                                                         |                                                                           |
| **Julia**                   | `"""..."""`                               | string literal     | Docstring binds to the following object (preceding placement) | `julia\n\"\"\"\nformat: github\nuser: \"Technical Development\"\n\"\"\"\nfunction f()\n  1\nend\n`                            |                            |                                                                                                         |                                                                           |
| **Clojure**                 | `"..."` (string literal)                  | argument metadata  | String literal after name becomes docstring                   | `clj\n(defn f\n  \"format: github\\nuser: Technical Development\"\n  []\n  1)\n`                                              |                            |                                                                                                         |                                                                           |
| **Haskell**                 | `{-                                       | ...-}`/`--         | `                                                             | Haddock doc                                                                                                                   | Haddock binds by placement | ```hs\n{-                                                                                               | \nformat: github\nuser: "Technical Development"\n-}\nf :: Int\nf = 1\n``` |
| **COBOL (fixed format)**    | `*` in indicator area (col 7)             | positional comment | Comment recognized by column rules                            | `cobol\n000100* format: github\n000200* user: \"Technical Development\"\n       IDENTIFICATION DIVISION.\n`                   |                            |                                                                                                         |                                                                           |
| **Fortran (fixed form)**    | `C`/`c`/`*` in col 1                      | positional comment | Comment recognized by column rules                            | `fortran\nC format: github\nC user: \"Technical Development\"\n      PROGRAM HELLO\n      END\n`                              |                            |                                                                                                         |                                                                           |
| **OCaml**                   | `(**...*)`                                | doc comment        | OCamldoc binds to next symbol                                 | `ocaml\n(** format: github\n    user: \"Technical Development\" *)\nlet f x = x + 1\n`                                        |                            |                                                                                                         |                                                                           |
| **Raku (Perl 6)**           | `#                                        | `/`=begin pod`     | line / pod block                                              | Pod binds by placement; tool-driven                                                                                           | ```raku\n#                 | format: github\nsub f() { }\n\n=begin pod\nformat: github\nuser: "Technical Development"\n=end pod\n``` |                                                                           |
| **Erlang**                  | `%% @doc`                                 | tagged comment     | EDoc reads tagged comments                                    | `erlang\n%% @doc format: github\nf() -> ok.\n`                                                                                |                            |                                                                                                         |                                                                           |
| **Ada**                     | `--` (tooling conventions vary)           | line comment       | Convention/tooling binds by placement                         | `ada\n-- format: github\nprocedure F is\nbegin\n  null;\nend F;\n`                                                            |                            |                                                                                                         |                                                                           |

---

## Parsing Notes

### 1) Prefer “carrier detection” + “payload parse”

A robust parser typically does:

1. Detect **carrier syntax** (delimiters + placement rules)
2. Extract raw text
3. Parse **canonical payload** (YAML recommended)
4. Validate keys against the schema

### 2) Attachment rules matter

- **Python:** a triple-quoted string is only a docstring if it’s the *first statement* in the scope.
- **Julia:** same delimiter, but it binds to the *next definition* (preceding placement).
- **Rust/Zig:** doc comments are transformed/recognized by compiler; incorrect placement can fail or be ignored.

### 3) Positional languages require a different lexer

- **COBOL:** comment indicator is positional (indicator area).
- **Fortran fixed form:** comment is positional (column 1).

### 4) Nesting support (rare but valuable)

- **D** supports nested comment/doc blocks in a way most C-style syntaxes do not.
- **Lua** supports “equal padding” levels (`--[=[ ... ]=]`) to safely contain `]]`.

> [!WARNING]
> Don’t treat all `/** ... */` blocks as doc comments automatically. Many repos use them as plain block comments. Prefer heuristics:
>
> - presence of tags (`@param`, `@return`) **or**
> - presence of your canonical keys (`format:`, `user:`, etc.)

---

## Examples

### Example: Haskell (Haddock) with canonical YAML payload

```haskell
{-|
format: github
purpose: cli_doc_db
user: "Technical Development"
profile: "A developer and academic looking for new and creative integrations to visually enhance their scientific research paper."
skills: "Well-versed in Markdown; advanced foundation; does not require basic suggestions."
restrictions:
  styling: general_markdown
-}
add :: Int -> Int -> Int
add x y = x + y
```

### Example: Rust (item docs + module docs)

```rust
//! format: github
//! purpose: cli_doc_db

/// user: "Technical Development"
/// profile: "..."
pub fn add(x: i32, y: i32) -> i32 { x + y }
```

### Example: Lua (equal-padded block)

```lua
--[==[
format: github
purpose: cli_doc_db
user: "Technical Development"
]==]
function add(x, y) return x + y end
```

---

## Duplicate & Conflict Notes

### Python vs Julia (same delimiter, different binding)

- Both use `""" ... """`.
- **Python:** docstring only when it is the *first statement inside the scope*.
- **Julia:** docstring binds to the *next object* (placed immediately above it).

### Rust vs Zig (similar tokens, different semantics)

- Both support `///` and `//!`.
- Placement/attachment rules are similar, but treat them as separate carriers in your DB.

### Block comment families (Javadoc-like)

`/** ... */` appears across many ecosystems (JS/TS/Java/Kotlin/Scala/PHP).
Differentiate by:

- file extension
- optional tag sets (`@param`, `@return`, KDoc/Scaladoc differences)
- your canonical key presence

---

## Implementation Hint (DB Shape)

If your CLI needs fast lookup, a clean structure is:

- `languages[language].carriers[]` (each carrier: delimiter + kind + attachment + notes)
- `payload.schema` (canonical keys + validation rules)
- `examples[language]` (1–3 minimal snippets)

That keeps “how to find it” separate from “what it means”.

---
