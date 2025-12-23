# TODO.md
<!-- 
**todo_spec:spec* 
  [1] REQ:['FILE,'HEADING']
  [2] DOCLINK:['FILES', 'HEADERS']
  [3] HEADERFORMAT: 'SCREAMINGSNAKE'
  [4] TASKFORMAT: 'Tasklist'
  [4] VER: 'SIMPNUM'
-->

## TODO:  MRDR DOCUMENT FORMAT
```md
# TODO.md
<!-- 
**todo:spec** 
  [1] REQ:['FILE,'HEADING']
  [2] DOCLINK:['FILES', 'HEADERS']
  [3] HEADERFORMAT: 'SCREAMINGSNAKE'
  [4] TASKFORMAT: 'Tasklist'
  [4] VER: 'SIMPNUM'
-->

---
[TODO00]
- [ ]

FILE: []()
HEADR: []()

> DIRECT LINE REFERENCE FROM THE CORRESPONDING DOCUMENT THE TODO YTAG IS LINKED

- `additional_datapoint` Context or information regarding the TODO reference
- Second `additional_datapoint` Datapoint or information regarding the TODO

- 1. First step example to complete or correct it
- 2. Second step example to complete or correct it
```

### LINE BY LINE SYNTAX BRAKDOWN
- `metadata`: is defined to start the document
- `---` indicates the seperation between header data and TODO data
  - NEVER add a `newline` between `---` (`OPERATOR`) and `TODO` (`IDENTIFIER`)
- `[TODO00]`: begins the TODO data with its `simpnum` `ver` `ID`
  - NEVER add a `newline` between `TODO00`(`IDENTIFIER`) and tasklist checkbox `- [ ]` (`OPERATOR`)
- `checkbox`: `- [ ]`
  - `tasklist` `checkbox` is designed to hold its own dedicated line.
- `ID:` `TODO`+[`simpnum`](/docs/tags.md|## FORMATTING)
  - `NOTE`: `simpnum` is the alias of `SIMPLENUMERIC` version ID formatting
- The `TODO` should only have two `additional_datapoints` (`-` based list, for clarity on TODO)
- There is `no_limit` on the steps / tasks in the `tasklist` `TODO` planning.
