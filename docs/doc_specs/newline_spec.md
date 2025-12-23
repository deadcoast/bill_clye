# newline_spec.md
[MRDR:doc:spec=doctags](/docs/doctags.md)
<!-- 
  NOTE: 
    - The `mrdr:doc:spec` format is slowly introduced in this document. It is a pattern based classification for document orginazation and spec consistency.
    - All functions shown and described can be found in this documentation suite.
  mrdr:doc:spec
    - a straightforward, pattern based spec that is designed to be easily understandable by patterns alone.
    - NO PARSER OR FRAMEWORK SHOULD BE REQUIRED FOR THE DOC SPEC TO BE UNDERSTOOD.
    - DESIGNED TO BE UTILIZED IN HARMONY WITH AN AI AGENT IN AGENTIC IDE ENVIORNMENTS.
    - AN EXTENSION, OR UNIVERSAL CONNECTION FOR AGENTIC WORKFLOW ECOSYSTEMS SUCH AS:[ 'MCP', 'SKILLS', 'RULES', 'AGENT', 'CLAUDE'
-->

---

## `newline:rules --glbl`
> Headers have a blank line above them, and no blank lone below them.
- HEADERS:newline,
  - ABOVE:true,
  - BELOW:false

## `newline:spec -variants`
[TODO06](+:doctag entries && opt:variants)

### "--twospace" Rule

[FMT04](CONFIG:default:newline:spec)

The standard Markdown way to force a line break without starting a new paragraph is to add **two spaces** at the end of every line before hitting enter.

- **How it looks in an editor:** `Item 1  [space][space]`
- **Result:** Item 1
Item 2

### "--htmlbr" `<br>` Tags

If you find trailing spaces hard to see or keep track of, you can use the HTML line break tag. This is very explicit and won't be accidentally deleted by "auto-trim whitespace" settings in your code editor.

```markdown
Item 1<br>
Item 2<br>
Item 3

```

### Wrap the List in `<pre>` Tags

If you have a very long list and don't want to edit every single line, you can wrap the entire block in `<pre>` (preformatted text) tags. This tells GitHub to render the text exactly as it is typed, preserving all newlines and spaces.

```html
<pre>
Item 1
Item 2
Item 3
Item 4
</pre>

```

### Use a Code Block

If the visual style of a code block (usually a grey background with a monospaced font) works for your documentation, this is the fastest way to handle large lists.

**Type this:**

<pre>

```text
Item 1
Item 2
Item 3

```

</pre>

---

### Invisible Table

This is a clever way to force GitHub to respect newlines while keeping Markdown formatting active. If you put your list inside a single-cell HTML table, GitHub's renderer often treats the lines differently, but it can be finicky.

A more reliable version is to use a **Table** where each item is its own row. However, that's just as much work as adding dashes.

### Backslash (`\`) Method

[FMT10]
PURP: _Designed to keep the **inline formatting** (backticks) while avoiding the token ineffeciency of constant lists and bulletpoints_

`bksmtd`, `BACKSLASHMETHOD`
In GitHub-Flavored Markdown, a backslash at the end of a line acts exactly like the "two spaces" rule. It’s a bit more visible than spaces, making it easier to manage.

```markdown
Item `one`\
Item `two`\
Item `three`

```

### Use an Unordered List without the "Look"

If your main gripe is the **bullet point symbol** (`-`) rather than the work of typing it, you can actually use a custom HTML list style in your Markdown to hide the bullets, though GitHub's support for custom CSS in `README.md` is non-existent.

---

### Comparison of Formatting Support

| Method | Preserves Newlines? | Supports `Backticks`? | Supports **Bold**? |
| --- | --- | --- | --- |
| `<pre>` Tags | **Yes** | No | No |
| Code Blocks | **Yes** | No (renders literally) | No |
| **Two Spaces** | **Yes** | **Yes** | **Yes** |
| **Backslash `\**` | **Yes** | **Yes** | **Yes** |

### Summary Table

| Method | Effort | Visual Style | Best For |
| --- | --- | --- | --- |
| **Two Spaces** | Low | Standard Text | Short lists; invisible |
| **`<br>` Tag** | Medium | Standard Text | Ensuring breaks aren't deleted |
| **`<pre>` Tag** | **Lowest** | Monospaced | Very large lists; preserving layout |
| **Code Block** | **Lowest** | Monospaced/Boxed | Technical lists or logs |
