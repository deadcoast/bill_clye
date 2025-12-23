# Docstring UDL Template
[MRDR:doc:spec=doctags](/docs/doctags.md)

A reusable template for defining **docstring/doc-comment carriers** for both **official languages** and **UDLs** (User-Defined Languages), with **parser-grade** rules and GitHub Flavored Markdown formatting.

> [!IMPORTANT]
> This template treats UDL docstrings as first-class documentation carriers with the same expectations as official language docstrings:
> - deterministic detection
> - unambiguous attachment rules
> - parseable canonical payload
> - validation + test vectors

---

## 0) Metadata

| Field | Value |
| --- | --- |
| **Spec Name** | `<SPEC_NAME>` |
| **Spec Version** | `<MAJOR>.<MINOR>.<PATCH>` |
| **Status** | `<draft \| stable \| deprecated>` |
| **Last Updated** | `<YYYY-MM-DD>` |
| **Owner** | `<team/person>` |

---

## 1) Summary

### 1.1 What this defines
This document defines the **docstring carrier syntax** for:

- **Language/UDL:** `<LANGUAGE_OR_UDL_NAME>`
- **Scope:** `<module | file | class | function | item | block | mixed>`

### 1.2 Why this exists
- CLI database indexing and display of documentation metadata
- Consistent, parseable metadata embedded inside source files
- Optional tooling integration (linters, doc generators, IDE hints)

---

## 2) Goals and Non-Goals

### 2.1 Goals
- Provide a **deterministic carrier signature** (how to detect docstrings)
- Define **attachment rules** (what the doc binds to)
- Standardize a **canonical payload** (what is inside the docstring)
- Define **parsing and validation** rules + **test vectors**

### 2.2 Non-Goals
- Not a full language grammar
- Not a documentation style guide for prose quality (beyond minimum conventions)
- Not a replacement for language-native doc tooling (unless explicitly stated)

---

## 3) Canonical Payload

### 3.1 Required payload format
**Canonical payload format:** `<yaml | json | ini | toml | custom>`

> [!TIP]
> If you don’t have a strong reason otherwise, use **YAML** for readability + simple parsing.

### 3.2 Canonical keys (minimum set)

| Key | Required | Type | Description |
| --- | --- | --- | --- |
| `format` | ✅ | string | Target renderer (e.g., `github`) |
| `purpose` | ✅ | string | Why this metadata exists (e.g., `cli_doc_db`) |
| `user` | ✅ | string | Author/profile label |
| `profile` | ⛔ / ✅ | string | Short description |
| `skills` | ⛔ / ✅ | string | Skill summary |
| `restrictions` | ⛔ | object | Optional constraints for tooling |
| `tags` | ⛔ | array[string] | Optional classification tags |
| `version` | ⛔ | string | Optional payload version (if separate from spec) |

> [!NOTE]
> Mark `profile` / `skills` as required only if your CLI/database logic depends on them.

### 3.3 Canonical payload template (YAML)

```yaml
format: <format_id>
purpose: <purpose_id>
user: "<user_label>"
profile: "<one_to_three_sentences>"
skills: "<skill_summary>"
restrictions:
  <key>: <value>
tags:
  - <tag_a>
  - <tag_b>
````

### 3.4 Canonical payload template (JSON)

```json
{
  "format": "<format_id>",
  "purpose": "<purpose_id>",
  "user": "<user_label>",
  "profile": "<one_to_three_sentences>",
  "skills": "<skill_summary>",
  "restrictions": {
    "<key>": "<value>"
  },
  "tags": ["<tag_a>", "<tag_b>"]
}
```

---

## 4) Carrier Syntax Definition

### 4.1 Carrier type

**Carrier type:** `<string_literal | block_comment | line_comment | attribute | positional | mixed>`

### 4.2 Primary signature(s)

| Name               | Open           | Close           | Multiline  | Nestable   | Notes     |
| ------------------ | -------------- | --------------- | ---------- | ---------- | --------- |
| `<CARRIER_A_NAME>` | `<OPEN_TOKEN>` | `<CLOSE_TOKEN>` | `<yes/no>` | `<yes/no>` | `<notes>` |
| `<CARRIER_B_NAME>` | `<OPEN_TOKEN>` | `<CLOSE_TOKEN>` | `<yes/no>` | `<yes/no>` | `<notes>` |

### 4.3 Whitespace + indentation rules

- **Leading whitespace allowed:** `<yes/no>`
- **Must start at column:** `<N | none>`
- **Indent preserved in payload:** `<yes/no>`
- **Trailing spaces:** `<allowed/disallowed>`

### 4.4 Escaping / collision strategy

Define what happens if the payload contains your close token.

- **Collision risk:** `<low/medium/high>`
- **Mitigation strategy:**

  - `<equal-padding / nesting / escape sequences / disallow token in payload / alternate close token>`

> [!WARNING]
> If you cannot guarantee safe termination, your carrier is not parser-safe.

---

## 5) Attachment Rules (Binding Semantics)

### 5.1 Attachment target

Docstrings attach to: `<next_symbol | enclosing_scope | first_statement_scope | explicit_anchor | none>`

### 5.2 Deterministic binding rules

Specify exactly how a parser decides what the doc applies to.

- **Rule A:** `<e.g., "Doc carrier immediately precedes a declaration with no blank lines">`
- **Rule B:** `<e.g., "If placed inside a function as first statement, binds to that function">`
- **Rule C:** `<e.g., "Module-level carrier binds to file/module record">`

### 5.3 Disallowed placements

- `<placement_1>`
- `<placement_2>`
- `<placement_3>`

### 5.4 Ambiguity resolution

If multiple bindings are possible, define priority:

1. `<highest_priority_rule>`
2. `<next_priority_rule>`
3. `<fallback_rule>`

---

## 6) Parsing Requirements

### 6.1 Parser responsibilities

A compliant parser MUST:

- Detect carrier open/close tokens
- Extract raw body text
- Normalize line endings (`LF` recommended)
- Parse canonical payload format
- Validate required keys + types
- Emit a normalized DB record

### 6.2 Normalization rules

- **Line endings:** `<LF | CRLF preserved | normalize to LF>`
- **Indent handling:** `<strip common indent | preserve exactly>`
- **Encoding:** `<UTF-8 required>`
- **Max payload size:** `<N bytes/lines>` (optional)

### 6.3 Validation rules

- Required keys MUST exist: `<list>`
- Unknown keys: `<allowed | warned | rejected>`
- Type coercion: `<none | allowed for numbers/bools>`
- Duplicate keys: `<error | last wins | first wins>`

### 6.4 Output record shape (normalized)

Define what your CLI DB stores after parsing.

```yaml
language: "<LANGUAGE_OR_UDL_NAME>"
carrier: "<CARRIER_A_NAME>"
attachment:
  kind: "<module|class|function|item>"
  target: "<resolved_symbol_identifier>"
payload: <parsed_payload_object>
source:
  file: "<path>"
  line_start: <N>
  line_end: <N>
```

---

## 7) Authoring Conventions

### 7.1 Recommended ordering inside payload

1. `format`
2. `purpose`
3. `user`
4. `profile`
5. `skills`
6. `restrictions`
7. `tags`

### 7.2 Recommended style rules

- Keep `profile` to 1–3 sentences
- Keep `skills` to one concise line
- Prefer `snake_case` for keys unless your ecosystem mandates otherwise

---

## 8) Examples

> [!NOTE]
> Provide at least **one minimal valid example** and **one invalid example** per carrier.

### 8.1 Minimal valid example

```<language>
<OPEN_TOKEN>
<canonical_payload_here>
<CLOSE_TOKEN>
<declaration_or_attachment_target>
```

### 8.2 Valid example with attachment edge case

```<language>
<example_showing_binding_rule_edge_case>
```

### 8.3 Invalid example (must fail)

```<language>
<example_that_breaks_termination_or_missing_required_keys>
```

---

## 9) Conformance Test Vectors

### 9.1 MUST pass

- `T1`: minimal valid payload + correct binding
- `T2`: payload with indentation + normalization rules
- `T3`: multiple doc carriers in one file (define expected behavior)

### 9.2 MUST fail

- `F1`: unterminated carrier
- `F2`: missing required keys
- `F3`: ambiguous binding without resolvable target (if disallowed)

Represent each test as:

```yaml
id: T1
input: |
  <file_contents>
expected:
  count: 1
  records:
    - attachment:
        kind: <...>
      payload:
        format: <...>
```

---

## 10) Security, Safety, and Stability Notes

- Payload is **data**, not code. Parsers MUST NOT execute payload content.
- Enforce maximum size to avoid pathological memory usage.
- Treat unknown keys conservatively (`warn` is usually best).
- Specify versioning strategy (see below).

---

## 11) Versioning and Change Log

### 11.1 Versioning strategy

- Spec follows `<SemVer | CalVer | custom>`
- Backwards incompatible changes require `<major bump>`

### 11.2 Change log

| Version   | Date           | Change      | Notes     |
| --------- | -------------- | ----------- | --------- |
| `<x.y.z>` | `<YYYY-MM-DD>` | `<summary>` | `<notes>` |

---

## 12) References

- `<link_or_doc_name_1>`
- `<link_or_doc_name_2>`
- `<internal_parser_repo_or_doc>`
