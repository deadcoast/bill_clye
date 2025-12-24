# metadata_spec.md
[MRDR:doc:spec=doctags](/docs/doctags.md)

_This file explains the two seperate metadata applications for the `MRDR` Ecosystem_

## MRDR DOCSPEC REQUIREMENT
- Each document must include `[MRDR:doc:spec=doctags](/docs/doctags.md)` directly below the document title.

## MRDR ECOSYSTEM DOCUMENT METADATA SPEC

- DOCSTRING:
  - open:`<!--`
  - closed: `-->`

### EXAMPLE

[!NOTE]
> Cross reference this step by step breakdown with the metadata examples below

1. - Start Docstring `<!--`
   -> `newline`
2. - `file_name`(doctags.md) seperated by `DELIMITER`(`:`) followed with `FILEID` (`spec`)
   -> `newline`
3. - Two spaces on `newline`, [`numver`](docs/doctags.md|## FORMATTING) encased in square brackets
4. -> `newline`

> STEPS 1-4 Create this metadata so far:
```md
<!--
doctags.md:spec
  [1]

```

> To complete the docstring, add the `numver` paramaters and options, and close it.
```md
<!--
doctags.md:spec
  [1] example paramater
  [2] example paramater
-->
```

- Each `MRDR` docstring requires relevant options, variables to its hosting file.

[!IMPORTANT]
> FILE: `/docs/doctags.md`
> HEADING: `## FORMATTING`

```md
<!--
doctags.md:spec
  [1] Tags + Data + Descriptions must fit on a single line
  [2] +new_line below headers
  [3] -+new_line above headers !> lists
  [4] -+['whitespace','delimiter'] in NLP ALIAS IDENTIFIERS
  [5] docs -> src -> cli NAMETYPE cohesion is crucial for full scope UX in the ecosystem
  [6] The docs, source code, and cli should be consistent
-->

## YAML METADATA SPEC
[TODO04]

_YAML metadata is an optional alternative to the MRDR docstring comment format._

### YAML RULES
- YAML metadata must be the first block in the document.
- Use YAML front matter delimiters: `---` (open) and `---` (close).
- Required keys: `mrdr.docspec`, `mrdr.file`, `mrdr.fileid`, `mrdr.version`.
- `mrdr.docspec` must match the in-file marker `[MRDR:doc:spec=doctags](/docs/doctags.md)`.
- Link entries use repo-relative paths and headings.

### YAML EXAMPLE
```yaml
---
mrdr:
  docspec: doctags
  file: "doctags.md"
  fileid: "spec"
  version: 1
  tags:
    - metadata
    - doctags
links:
  - file: "/docs/doctags.md"
    heading: "## FORMATTING"
---
```
