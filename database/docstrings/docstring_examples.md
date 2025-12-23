# database.md
[MRDR:doc:spec=doctags](/docs/doctags.md)

## DOCSTRINGS

### PYTHON

```python
"""
format: github
purpose: visual_styling
restrictions:
  styling: general_markdown
user: "Technical Development"
  - profile: A developer and academic looking for new and creative integrations to visually enhance their scientific research paper.
  - skills: well versed and aquinted with markdown, has a advanced foundational understanding and does not require basic suggestions.
"""
```

### YAML

```yaml
format: github
purpose: visual_styling
restrictions:
  styling: general_markdown
user: "Technical Development"
  - profile: A developer and academic looking for new and creative integrations to visually enhance their scientific research paper.
  - skills: well versed and aquinted with markdown, has a advanced foundational understanding and does not require basic suggestions.
```

### JSON

```json
{
  "format": "github",
  "purpose": "visual_styling",
  "restrictions": {
    "styling": "general_markdown"
  },
  "user": "Technical Development",
  "details": [
    {
      "profile": "A developer and academic looking for new and creative integrations to visually enhance their scientific research paper.",
      "skills": "well versed and aquinted with markdown, has a advanced foundational understanding and does not require basic suggestions."
    }
  ]
}
```

### XML

```xml
<metadata>
  <format>github</format>
  <purpose>visual_styling</purpose>
  <restrictions>
    <styling>general_markdown</styling>
  </restrictions>
  <user name="Technical Development">
    <profile>A developer and academic looking for new and creative integrations to visually enhance their scientific research paper.</profile>
    <skills>well versed and aquinted with markdown, has a advanced foundational understanding and does not require basic suggestions.</skills>
  </user>
</metadata>
```

### CSS

```css
/*
format: github
purpose: visual_styling
restrictions:
  styling: general_markdown
user: "Technical Development"
  - profile: A developer and academic looking for new and creative integrations to visually enhance their scientific research paper.
  - skills: well versed and aquinted with markdown, has a advanced foundational understanding and does not require basic suggestions.
*/
```
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

### DOC TABLE CONCLUSION

| Format        | Delimiter Style | Role in Refactor                                    |
|---------------|-----------------|-----------------------------------------------------|
| **Python**    | `"""`           | Absolute Truth / Source Origin                      |
| **JSON/YAML** | Structural      | Converted to match `user` nested object/list logic. |
|               |                 |                                                     |

### Summary of Alternative Approaches

| Language | Format Style | Why it's Unique |
| --- | --- | --- |
| **Elixir** | `@doc """..."""` | Compiled into the binary; accessible at runtime. |
| **Clojure** | `"String"` | Positioned as a function argument, not a comment. |
| **Raku** | `=begin pod` | Uses a full-blown markup language inside the file. |
| **Haskell** | `> code` | Literate style; prose is the default, code is the "extra." |
| **Smalltalk** | `comment` | Often stored in the image metadata, not a text file. |
