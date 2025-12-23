# newline_spec

_Designed to keep the **inline formatting** (backticks) while avoiding the token ineffeciency of constant lists and bulletpoints_

---

## RULES

- HEADERS:newline,
  - ABOVE:true,
  - BELOW:false

## Specification Definitions

### 1. The "Invisible" Table Hack

This is a clever way to force GitHub to respect newlines while keeping Markdown formatting active. If you put your list inside a single-cell HTML table, GitHub's renderer often treats the lines differently, but it can be finicky.

A more reliable version is to use a **Table** where each item is its own row. However, that's just as much work as adding dashes.

### 2. The Backslash (`\`) Method

In GitHub-Flavored Markdown, a backslash at the end of a line acts exactly like the "two spaces" rule. It’s a bit more visible than spaces, making it easier to manage.

```markdown
Item `one`\
Item `two`\
Item `three`

```

### 3. Use an Unordered List without the "Look"

If your main gripe is the **bullet point symbol** (`-`) rather than the work of typing it, you can actually use a custom HTML list style in your Markdown to hide the bullets, though GitHub's support for custom CSS in `README.md` is non-existent.

---

### The Most Efficient Solution: "Find and Replace"

Since you have "large lists," the most "pro" way to handle this without breaking your back (or your formatting) is to use a text editor (VS Code, Notepad++, or even Vim) to bulk-add the line breaks for you.

**If you use VS Code:**

1. Highlight your list.
2. Press `Ctrl + H` (Find and Replace).
3. Click the **Regex icon** (looks like `.*`).
4. **Find:** `(\n)` (or `$` depending on your editor).
5. **Replace:** `\n` (Two spaces before `\` and a newline).
6. Hit **Replace All**.

This instantly transforms a 500-line list into a GitHub-friendly format while keeping your `backticks` fully functional.

---

### Comparison of Formatting Support

| Method | Preserves Newlines? | Supports `Backticks`? | Supports **Bold**? |
| --- | --- | --- | --- |
| `<pre>` Tags | **Yes** | No | No |
| Code Blocks | **Yes** | No (renders literally) | No |
| **Two Spaces** | **Yes** | **Yes** | **Yes** |
| **Backslash `\**` | **Yes** | **Yes** | **Yes** |
