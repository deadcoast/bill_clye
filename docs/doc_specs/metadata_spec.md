# metadata.md

_This file explains the two seperate metadata applications for the `BILL_CLYE` Ecosystem_

## BILL_CLYE ECOSYSTEM DOCUMENT METADATA SPEC

- DOCSTRING:
  - open:`<!--`
  - closed: `-->`

### EXAMPLE

[!NOTE]
> Cross reference this step by step breakdown with the metadata examples below

1. - Start Docstring `<!--`
   -> `newline`
2. - `file_name`(tags.md) seperated by `DELIMITER`(`:`) followed with `FILEID` (`spec`)
   -> `newline`
3. - Two spaces on `newline`, [`numver`](docs/tags.md|##FORMATTING) encased in square brackets
4. -> `newline`

> STEPS 1-4 Create this metadata so far:
> A
```md
<--
tags.md:spec
  [1]

```

> To complete the docstring, add the `numver` paramaters and options, and close it.
```md
<!--
tags.md:spec
  [1] example paramater
  [2] example paramater
-->
```

- Each `BILL_CLYE` docstring requires relevant options, variables to its hosting file.

[!IMPORTANT]
> FILE: `/docs/tags.md`
> HEADING: `## FORMATTING`

```md
<!--
tags.md:spec
  [1] Tags + Data + Descriptions must fit on a single line
  [2] +new_line below headers
  [3] -+new_line above headers !> lists
  [4] -+['whitespace','delimiter'] in NLP ALIAS IDENTIFIERS
  [5] docs -> src -> cli NAMETYPE cohesion is crucial for full scope UX in the ecosystem
  [6] The docs, source code, and cli should be consistent
-->

## YAML METADATA SPEC
[TODO04]
