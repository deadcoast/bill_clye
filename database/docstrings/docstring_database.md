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

---

### Docstring Database: All Supported Syntax

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

I hear you—you're looking for different **character-based syntax** for defining docstrings, not entirely different language paradigms like literate programming. You want the "flavor" of the characters used to be unique while still functioning as a recognizable block of text within the code.

Here are official, character-driven docstring formats that use unconventional symbols or positioning.

---

### 1. Fortran 90+: The "Fixed-Column" Legacy

In older but still "official" and maintained Fortran standards, documentation isn't just about the character, but the **column position**. While modern Fortran uses `!`, the historical "Fixed Form" required a specific character in the very first column.

```fortran
C     This 'C' must be in column 1.
C     It is the official "docstring" indicator for 
C     fixed-form Fortran source code.
      PROGRAM HELLO
```

### 2. D Language: The "Plus" Docstrings

D uses a variation of the C-style comment, but replaces the second asterisk with a **plus sign**. This was intentionally chosen to allow docstrings to nest within each other without the "middle" of one comment accidentally closing another—a common frustration in C/C++.

```d
/++
 + This is a "Ddoc" (D Documentation) block.
 + Using the '+' allows you to nest /+ other comments +/
 + inside this docstring safely.
 +/
void myFunction() {}
```

### 3. Julia: The "Pre-Function" Triple Quote

Julia follows Python’s triple-quote style, but with a "conflicting" twist: the docstring **must** appear *above* the function, not inside it. In Python, placing a string above a function makes it a loose string; in Julia, the compiler treats it as a formal docstring attached to the object following it.

```julia
"""
    multiply(x, y)

This is an official Julia docstring. 
Notice it sits *outside* the function body.
"""
function multiply(x, y)
    return x * y
end

```

### 4. Lua: The "Double Bracket"

Lua uses double hyphens for comments, but for multi-line doc-style blocks, it uses an "Equal Sign" sandwich. You can add any number of `=` signs between the brackets to ensure the docstring doesn't get closed by code appearing inside it (like a string that contains `]]`).

```lua
--[[
    This is the standard multi-line comment.
--]]

--[=[
    This is a "Level 1" docstring. 
    It will only close when it sees a bracket with exactly one '='.
    Example: print([[Hello]]) won't break this block.
--]=]

```

### 5. COBOL: The "Asterisk-Space"

In COBOL, docstrings are officially identified by an asterisk in the 7th character column (the "Indicator Area"). Anything before it is a line number, and the asterisk itself tells the compiler "this is a comment/document line."

```cobol
000100* THIS IS A FORMAL DOCSTRING IN COBOL
000200* IT MUST START AT COLUMN 7.
       IDENTIFICATION DIVISION.

```

---

### Comparison of Character-Based Syntax

| Language | Character Signature | Unique Trait |
| --- | --- | --- |
| **D** | `/++ ... +/` | Uses plus signs to allow nesting. |
| **Julia** | `""" ... """` (Pre-code) | Positioned *above* the code, unlike Python. |
| **Lua** | `--[===[ ... ]===]` | Uses "Equal Sign" padding to prevent accidental escapes. |
| **Fortran** | `C` in Column 1 | Column-specific identification (Positional). |
| **Pascal** | `(* ... *)` | Uses "Star-Parens" instead of slashes or brackets. |

---

Many popular programming languages use specific syntax for multi-line comments that are designed to be parsed into documentation (often called "doc comments"). While Python uses triple quotes, most C-style languages use a variation of the forward slash and asterisk.

Here are the most popular languages that use multi-line docstrings similar to Python and the corrected JavaScript format.

---

### 1. JavaScript / TypeScript / Java / PHP

These languages all follow the **JSDoc** or **Javadoc** convention. While a standard multi-line comment is `/* ... */`, a documentation block specifically starts with **two** asterisks.

```javascript
/**
 * This is a formal docstring in JS/TS/Java.
 * It often includes tags like @param or @return.
 */
function example() {}

```

### 2. Rust

Rust is unique because it uses "doc comments" that are technically line-based but function exactly like docstrings.

* **`///`**: Documents the item following it.
* **`//!`**: Documents the item enclosing it (like the header of a file).

```rust
/// Adds one to the number given.
/// 
/// # Examples
/// ...
fn add_one(x: i32) -> i32 { x + 1 }

```

### 3. Swift

Swift uses a mix of the Javadoc style and a specific triple-slash style. Both are recognized by Xcode to generate "Quick Help" documentation.

```swift
/**
 This is a multi-line docstring in Swift.
 It supports Markdown formatting.
*/

/// Or you can use triple slashes 
/// for each line.

```

### 4. Csharp

C# primarily uses **XML documentation comments**. These are triple-slashed and use tags to define the structure, which the compiler can then use to generate an external XML file.

```csharp
/// <summary>
/// This method does something important.
/// </summary>
/// <param name="input">Description of input.</param>
public void Process(string input) {}

```

### 5. Ruby

Ruby uses a unique syntax called **RDOC**. While you can use `#` for every line, multi-line blocks are often wrapped in `=begin` and `=end`.

```ruby
=begin
This is a multi-line comment block 
often used for documentation in Ruby.
=end
def my_method
end

```

---

### Summary Table

| Language | Docstring Syntax | Convention Name |
| --- | --- | --- |
| **Python** | `""" ... """` | PEP 257 |
| **JavaScript/Java** | `/** ... */` | JSDoc / Javadoc |
| **Rust** | `///` | Rustdoc |
| **C#** | `/// <summary>` | XML Doc Comments |
| **Swift** | `/** ... */` or `///` | Swift Markup |

Would you like me to show you how to generate a documentation website (like Sphinx or Doxygen) using these docstrings?

When you step away from the standard C-style or Pythonic conventions, you find languages that treat documentation as a core architectural component rather than just "comments the compiler ignores."

## Less known Docstrings

Experimental, "official" ways docstrings that have been implemented in various ecosystems.

---

### 1. Elixir: The Module Attribute

In Elixir, docstrings are not comments at all; they are **Module Attributes**. Because they are defined as `@doc` or `@moduledoc`, the documentation is compiled into the bytecode itself. This allows the language to access documentation at runtime via the `h` helper in the terminal.

```elixir
defmodule Math do
  @moduledoc """
  This is a module-level docstring. 
  It is a first-class citizen in the language.
  """

  @doc "Adds two numbers together."
  def add(a, b), do: a + b
end

```

### 2. Clojure (Lisp): The Embedded String

In many Lisps, specifically Clojure, the docstring is an optional argument placed **inside** the function definition, between the name and the parameter list. It is literally just a string literal that the `defn` macro knows how to handle.

```clojure
(defn my-function
  "This is the official docstring location. 
   It sits between the name and the params."
  [x y]
  (+ x y))

```

### 3. Perl 6 (Raku): Pod6

Raku (formerly Perl 6) uses **Pod6**, a system where documentation is interleaved with code using specific delimiters. It feels like writing a markup language directly inside your source file. It is highly controversial because it can make the code look like a document rather than a program.

```raku
#| This is a "leading" docstring for the subroutine
sub hello($name) {
    say "Hello $name";
}

=begin pod
=head1 Documentation Block
This is an official Pod6 block. It can contain 
complex structures like tables or lists.
=end pod

```

### 4. Haskell: Haddock (Bird Tracks)

While Haskell supports standard multi-line comments, the "Bird Track" style is a more "literate programming" approach. It flips the script: the file is a text document by default, and lines starting with `>` are the actual code.

```haskell
This is a literate Haskell file (.lhs).
Everything is a docstring by default.

> add :: Int -> Int -> Int
> add x y = x + y

You can continue explaining your logic here without comments.

```

### 5. Zig: Top-level Doc Comments

Zig uses `//!` and `///`, but what makes them "weird" compared to others is their strictness. They are not just ignored; if a doc comment is placed in an "invalid" spot (like before a variable that isn't exported), the compiler can actually throw an error or warning, treating documentation as a semantic requirement of the code structure.

---

### Summary of Alternative Approaches

| Language | Format Style | Why it's Unique |
| --- | --- | --- |
| **Elixir** | `@doc """..."""` | Compiled into the binary; accessible at runtime. |
| **Clojure** | `"String"` | Positioned as a function argument, not a comment. |
| **Raku** | `=begin pod` | Uses a full-blown markup language inside the file. |
| **Haskell** | `> code` | Literate style; prose is the default, code is the "extra." |
| **Smalltalk** | `comment` | Often stored in the image metadata, not a text file. |
