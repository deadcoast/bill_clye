# docstring_udl_template.md
[MRDR:doc:spec=doctags](/docs/doctags.md)

A reusable template for defining a **docstring / doc-comment carrier** for either an **official language** or a **UDL**.  
Designed for **parser-grade determinism** and **CLI database indexing**.

> [!IMPORTANT]
> UDL docstrings are held to the same standard as official language docstrings:
> deterministic signature, unambiguous binding, parseable payload, and test vectors.

---

## DICTIONARY

| Term | Meaning |
| --- | --- |
| `TITLE` | Name of the docstring design (carrier spec name). |
| `DESCR` | Short description of the docstring design. |
| `LANG` | Target language name; use `UDL` if not an official language. |
| `DELIMITER` | A single token/character used to open/close/mark structure. |
| `OPERATOR` | A **multi-character delimiter** that functions as a single semantic unit (e.g., `<=`), often providing behavior beyond a single delimiter. |
| `CARRIER` | The container form used to hold the doc payload (string literal, block comment, line comment, attribute, positional). |
| `PAYLOAD` | The canonical metadata content embedded inside the carrier (recommend: YAML). |
| `ATTACHMENT` | The binding rule that decides what the doc applies to (next symbol, enclosing scope, first statement, etc.). |
| `TERMINATION` | How the carrier safely closes (and how collisions are prevented). |

<!--
NOTE:
- Only define non-obvious terms.
- Avoid defining generic words like "opening/closing/bracket" unless your spec gives them special meaning.
-->

---

## User Defined Doc String Template

TITLE: `<DOCSTRING_TITLE>`
DESCR: `<DOCSTRING_DESCRIPTION>`
LANG: `<OFFICIAL_LANGUAGE_NAME | UDL>`

---

## 1) Summary

### 1.1 Design intent
- `<one_sentence_intent>`

### 1.2 Where it is used
- `<cli_database | linter | docs_generator | editor_help | mixed>`

---

## 2) Carrier Syntax

### 2.1 Carrier type
CARRIER: `<string_literal | block_comment | line_comment | attribute | positional | mixed>`

### 2.2 Primary signature

| Name | Open | Close | Multiline | Nestable | Notes |
| --- | --- | --- | --- | --- | --- |
| `<CARRIER_NAME>` | `<OPEN_TOKEN>` | `<CLOSE_TOKEN>` | `<yes/no>` | `<yes/no>` | `<notes>` |

### 2.3 Structural delimiters (if applicable)
DELIMITERS:
- OPENING: `<token>`
- CLOSING: `<token>`
- BRACKETS: `<token_set>` (optional)

### 2.4 Operators (if applicable)
OPERATORS:
- `<operator_name>`: `<OPEN_OP>`, `<CLOSE_OP>` — `<what_it_does>`
- `<operator_name>`: `<OPEN_OP>`, `<CLOSE_OP>` — `<what_it_does>`

> [!WARNING]
> If the payload can contain the close token, define a collision strategy (nesting, padding, escaping, or disallow rules).

---

## 3) Attachment Rules

ATTACHMENT: `<next_symbol | enclosing_scope | first_statement_scope | explicit_anchor | none>`

### 3.1 Deterministic binding rules
- Rule A: `<exact_rule>`
- Rule B: `<exact_rule>`
- Rule C: `<exact_rule>`

### 3.2 Disallowed placements
- `<placement_that_must_fail>`
- `<placement_that_must_fail>`

### 3.3 Ambiguity resolution (priority order)
1. `<highest_priority_resolution>`
2. `<secondary_resolution>`
3. `<fallback_resolution>`

---

## 4) Canonical Payload

PAYLOAD FORMAT: `<yaml | json | toml | custom>`

### 4.1 Required keys

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `format` | string | ✅ | Target renderer (e.g., `github`). |
| `purpose` | string | ✅ | Why this metadata exists (e.g., `cli_doc_db`). |
| `user` | string | ✅ | Author/profile label. |
| `profile` | string | ⛔/✅ | Short description. |
| `skills` | string | ⛔/✅ | Skill summary. |
| `restrictions` | object | ⛔ | Optional constraints. |
| `tags` | array[string] | ⛔ | Optional classification tags. |

### 4.2 Payload template (YAML)
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

---

## 5) Parser Requirements

### 5.1 MUST

- Detect carrier open/close
- Extract body content
- Normalize line endings (`LF` recommended)
- Parse payload format
- Validate required keys/types
- Emit a normalized DB record

### 5.2 Normalization rules

- Line endings: `<normalize_to_LF | preserve>`
- Indentation: `<strip_common_indent | preserve_exact>`
- Encoding: `<UTF-8 required>`
- Max payload size: `<N bytes/lines>`

### 5.3 Validation rules

- Unknown keys: `<allow | warn | reject>`
- Duplicate keys: `<error | last_wins | first_wins>`
- Type coercion: `<none | limited>`

---

## 6) Minimal Examples

> [!NOTE]
> Include at least one minimal valid example per signature/operator, and at least one invalid example.

### 6.1 Minimal valid carrier example

```<language_or_udl>
<OPEN_TOKEN>
<payload_here>
<CLOSE_TOKEN>
<attachment_target>
```

### 6.2 Operator variant examples (optional)

#### `<operator_name>`

OPERATOR: `<OPEN_OP>`, `<CLOSE_OP>`

```<language_or_udl>
<OPEN_OP><anchor_or_id_optional>
<payload_or_context_here>
<CLOSE_OP>
```

---

## 7) Conformance Test Vectors

### 7.1 MUST pass

- `T1`: minimal valid payload + correct binding
- `T2`: payload indentation + normalization behavior
- `T3`: multiple carriers in one file (define expected behavior)

### 7.2 MUST fail

- `F1`: unterminated carrier
- `F2`: missing required keys
- `F3`: ambiguous binding with no resolvable target (if disallowed)

Template:

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

## 8) Change Log

| Version   | Date           | Change      | Notes     |
| --------- | -------------- | ----------- | --------- |
| `<x.y.z>` | `<YYYY-MM-DD>` | `<summary>` | `<notes>` |
