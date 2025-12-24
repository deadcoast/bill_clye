# TODO.md
[MRDR:doc:spec=doctags](/docs/doctags.md)
<!-- 
todo:spec*
  [1] REQ:['FILE,'HEADING']
  [2] DOCLINK:['FILES', 'HEADERS']
  [3] HEADERFORMAT: 'SCREAMINGSNAKE'
  [4] TASKFORMAT: 'Tasklist'
  [4] VER: 'SIMPNUM'
-->

> For Template, SEE [TODO TEMPLATE](/templates/todo_template.md)
> For spec document, SEE [TODO SPECIFICATION](/docs/doc_specs/todo_spec.md)
> Completed tasks are logged in [CHANGELOG](/CHANGELOG.md)

## TODO.01 <!-- todo:type:simpnum:spec=PARENT -->

---
[TODO-0.1.3]
- [ ]

TASK:
REF: [cli_spec.md](/docs/doc_specs/cli_spec.md|## CLI SPECIFICATIONS)
```
[!NOTE]
>  MRDR documents, categorizes and collects data from syntax and languages for future database usage, all predetermined essential data should be entered into the  MRDR documents. [TODO-03]
```

- _This section contains a global dictionary of all the terms and their definitions that are used in the documentation._
- _If any definitions have exact duplicates in other languages, identiy the additional utilization with tag `[+LANG_USE]` but always keep the more widely accepted or pupular nametype for these documents_

---
[TODO-0.1.5]
- [ ]

TASK: DEFINE AND POPULATE THE DATA IN THE RELEVANT TAGGED FILES.
REF: `GLOBAL` TODO TASK.

---

## TODO.02

---
[TODO-0.2.1]

- [ ] <!-- TODO:tasklist:chekbox:spec=[PRIMARY == "PrimaryIndicatorSuccessfulTask":accro='PIST'] -->
REF: [FILE LINK TITLE](path/to/file/reference.md|## HEADER REFERENCE) <!-- Correct Header Linking Format for github -->

> DIRECT LINE REFERENCE FROM THE CORRESPONDING DOCUMENT THE TODO BILLYTAG IS LINKED <!-- TODO tags originate in other files, then are populated here. This section must ALWAYS provide a corresponding TODOTAG with the correct IDENTIFIER -->

- `additional_datapoint` Essential Context regarding the files specific TODOTAG call
- Second `additional_datapoint` Datapoint or information relating to the source file and its TODOTAG

<!-- tasklist:checkbox:spec -->
- [ ] 1. Example: Step to complete or correct first task
  - [ ] 2. Example: Subtask to complete or correct correlated to the SecondaryTasks

---

## FOOTER REMOVALLOG METADATA - A CHANGELOG EXPLICITLY FOR REMOVED DATA, INLINE
REMOVED_DATA:
```md
---
[TODO-0.1.1] <!-- todo:type:SemVer=CHILD -->
- [ ]

TASK: Extract data from the spec and populate `doctags.md` with the relevant data
REF: [cli_spec.md](/docs/doc_specs/cli_spec.md|## CLI SPECIFICATIONS)
```
> MRDR documents, categorizes and collects data from syntax and languages for future database usage, all predetermined essential data should be entered into the  MRDR documents.
```

- _This section contains a global dictionary of all the terms and their definitions that are used in the documentation._
- _If any definitions have exact duplicates in other languages, identiy the additional utilization with tag `+LANG_USE` but always keep the more widely accepted or pupular nametype for these documents
- RESOLUTION: Doctags placeholders populated; verify for completeness and naming cohesion.

---
[TODO-0.1.2]
- [ ]

TASK: Is it plausible to use both `mrdr` and `misterdoctor` as the MAIN cli command call? If so, SKIP `TODO2`
FILE: [cli_spec.md](/docs/doc_specs/cli_spec.md|## INTRODUCTION)
```
`MRDR` CLI output features (pulled from the designed database) in the initial design will be minimal, but that does not mean the DEVELOPMENT and SPEC will be minimal.
> command: <!-- [TODO01: DECIDE ON ONE DEFINITIVE COMMAND] --> `mrdr`, `misterdoctor`
```

- RESOLUTION: `misterdoctor` is the alias for `mrdr`.
- (1).SPEC_DESIGN_PURPOSE: To maximize initial CLI design depth, the first spec will focus on full scope foundational modular cli development, if done correctly `database_display_integration` should be much easier.
  - `database_display_integration`: The CLI pulling data from the database, and displaying them in the CLI, such as the (currently planned) integration 'docstrings'.

---
[TODO-0.1.4]
- [ ]

TASK: Needs Complete development for YAML metadata OPTION (opposed to the  MRDR metadata format) in the Ecosystem.
REF: [metadata_spec.md](/docs/doc_specs/metadata_spec.md|## YAML METADATA SPEC)
```
N/A
```
- _NA_
- _NA_
- RESOLUTION: YAML metadata spec drafted in `docs/doc_specs/metadata_spec.md`.
```
