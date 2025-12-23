# docstring_tables.md

## Docstring Table Database

### Docstring Database Table

| Language | Syntax Signature | Character Role | Implementation Example (Absolute Truth Schema) |
| --- | --- | --- | --- |
| **Python** | `""" ... """` | Triple Quote | `"""user: "Technical Development"\n- profile: ..."""` |
| **JS / Java** | `/** ... */` | Double-Star Block | `/**\n * user: "Technical Development"\n * - profile: ...\n */` |
| **Lua** | `--[=[ ... ]=]` | Equal-Padding | `--[=[user: "Technical Development"\n- profile: ...]=]` |
| **D** | `/++ ... +/` | Nestable Plus | `/++ user: "Technical Development"\n - profile: ... +/` |
| **Julia** | `""" ... """` | Pre-Code Block | `"""user: "Technical Development"..."""\nfunction info()...` |
| **Elixir** | `@doc """..."""` | Module Attribute | `@doc """\nuser: "Technical Development"\n- profile: ...\n"""` |
| **C#** | `/// <tag>` | XML Literal | `/// <user name="Technical Development">\n/// <profile>...</profile>\n/// </user>` |
| **Rust** | `///` | Doc Line | `/// user: "Technical Development"\n/// - profile: ...` |
| **Ruby** | `=begin ... =end` | Block Toggle | `=begin\nuser: "Technical Development"\n- profile: ...\n=end` |
| **COBOL** | `*` (Col 7) | Positional | `000100* user: "Technical Development"\n000200* - profile: ...` |
| **Fortran** | `C` (Col 1) | Fixed-Form | `C     user: "Technical Development"\nC     - profile: ...` |
| **Haskell** | `{- | ... -}` | Haddock Pipe |
| **Zig** | `//!` | Module Doc | `//! user: "Technical Development"\n//! - profile: ...` |

---

### Structural "Absolute Truth" Data Objects

For your development database, these formats represent the non-commented data versions of the schema for programmatic parsing.

```json
/* JSON PRIMARY */
{
  "user": "Technical Development",
  "details": {
    "profile": "A developer and academic looking for new and creative integrations to visually enhance their scientific research paper.",
    "skills": "well versed and aquinted with markdown, has a advanced foundational understanding and does not require basic suggestions."
  }
}

```

```yaml
# YAML PRIMARY
user: "Technical Development"
profile: "A developer and academic looking for new and creative integrations to visually enhance their scientific research paper."
skills: "well versed and aquinted with markdown, has a advanced foundational understanding and does not require basic suggestions."

```

```clojure
;; CLOJURE (LISP) EMBEDDED STRING
(defn research-metadata
  "user: \"Technical Development\"
   profile: A developer and academic...
   skills: well versed and aquinted..."
  []
  (princ "Metadata Container"))

```

### Database Integration Notes

* **Key Collision:** When using the Python/Julia triple quotes, ensure your parser distinguishes between the two by file extension (`.py` vs `.jl`), as the syntax is identical but the semantic location (inside vs. outside the function) is the "Truth" differentiator.
* **Positional Parsing:** For COBOL and Fortran, your database logic must account for leading whitespace/line-numbers before the doc-character signature.
* **Nesting:** If you adopt the **D** or **Lua** styles for your own custom format, you gain the ability to store docstrings *inside* other docstrings for recursive metadata.


To maximize this database for your development needs, I have expanded the table to include legacy, functional, and niche systems. This covers almost every "Official" way a language distinguishes documentation from a standard comment or code.

---

### Master Docstring Database: Comprehensive Edition

| Language | Signature | Type | Behavior / Logic |
| --- | --- | --- | --- |
| **Python** | `""" ... """` | Literal | Internal; stored in `__doc__` attribute. [1] |
| **JS / TS / Java / PHP** | `/** ... */` | Block | **JSDoc/Javadoc** style; parsed by external tools. |
| **Lua** | `--[[ ... ]]` | Padded | Uses `[=[` to allow internal `]]` without breaking. |
| **Rust** | `///` or `//!` | Sugared | Transformed by compiler into `#[doc="..."]`. |
| **C# / F#** | `/// <tag>` | XML | Compiler-verified XML schema. |
| **Swift** | `///` or `/** */` | Markup | Supports rich Markdown for Xcode "Quick Help." |
| **D** | `/++ ... +/` | Nestable | Allows nested docstrings via plus-sign tokens. [2] |
| **Julia** | `""" ... """` | Pre-fix | Must sit *above* the target code. [1] |
| **Elixir** | `@doc """` | Attribute | Compiled into the BEAM bytecode as metadata. |
| **Ruby** | `=begin`/`=end` | RDOC | Traditionally starts at the beginning of the line. |
| **Haskell** | `{- | ... -}` | Haddock |
| **Clojure / Lisp** | `" ... "` | Position | String literal placed immediately after function name. |
| **COBOL** | `*` (Col 7) | Indicator | Positional; requires specific indentation. |
| **Fortran** | `C` or `*` (Col 1) | Fixed | Only recognized in legacy "Fixed Form" files. |
| **Raku (Perl 6)** | `# | `or`%=pod` | Pod6 |
| **Zig** | `//!` | Global | Top-level module documentation. |
| **Erlang** | `%% @doc` | EDoc | Double-percent is the official doc-parser trigger. |
| **Ada** | `-- | ` | Formal |
| **Smalltalk** | `" ... "` | Metadata | Usually handled via the GUI/Image browser. |
| **Pascal / Delphi** | `{(** ... *)}` | Bracket | Often uses `(*` or `{` with a specific compiler flag. |
| **SQL (T-SQL)** | `EXEC sys.sp...` | Procedure | Docs are often stored as `MS_Description` properties. |
| **OCaml** | `(** ... *)` | OCamldoc | Double-asterisk required for the extractor. |
| **VHDL** | `--` | Header | No specific symbol; purely convention-based headers. |
| **Kotlin** | `/** ... */` | KDoc | Similar to Javadoc but uses Markdown instead of HTML. |
| **Scala** | `/** ... */` | Scaladoc | Inherits Javadoc style with TPD support. |
| **ActionScript** | `/** ... */` | ASDoc | Legacy Adobe standard for Flash/Flex. |

---

### Duplicate & Conflict Notation

* **[1] Python vs. Julia:** Syntactically identical (`"""`). The difference is **Scope**: Python is "Internal" (inside the function), Julia is "External" (attached from above).
* **[2] JavaScript vs. D:** Both use the slash/star framework, but D’s `/++` allows for recursive nesting which the standard JS/C `/*` cannot handle (it would terminate at the first `*/` it sees).

### Database Entry Example (Haskell Syntax)

To show how your "Absolute Truth" schema fits into one of the more unique signatures from the table:

```haskell
{-| 
format: github
purpose: visual_styling
restrictions:
  styling: general_markdown
user: "Technical Development"
  - profile: A developer and academic looking for new and creative integrations to visually enhance their scientific research paper.
  - skills: well versed and aquinted with markdown, has a advanced foundational understanding and does not require basic suggestions.
-}
add x y = x + y

```