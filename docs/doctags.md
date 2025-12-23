# doctags.md
[MRDR:doc:spec=doctags](/docs/doctags.md)
<!-- 
TAGS01:spec
  [1] +new_line below headers
  [2] -+new_line above headers !> lists
  [3] -+['whitespace','delimiter'] in NLP ALIAS IDENTIFIERS
  [4] docs -> src -> cli nametype cohesion
  [5] The docs, source code, and cli should be consistent
-->

## RULES

### LIST RULES

#### DEFAULT BEHAVIOR
The Backslash (`\`) Method
- In GitHub-Flavored Markdown, a backslash at the end of a line acts exactly like the "two spaces" rule. It’s a bit more visible than spaces, making it easier to manage.
```
Item `one`\
Item `two`\
Item `three`
```
- For long Lists: `<pre></pre>`

Example:
```
<pre>
[MET01] : Tags + Data + Descriptions must fit on a single line
</pre>
```

## DOCTAG SPEC

TITLE: YTAGS/
PURPOSE: Defined by a strict spec to maximize:['BREVITY', 'CONSISTENCY', 'READABILITY', 'PARSING']
</pre>

## MRDR DOCSPEC TAGS
<pre>
DOC01: `MRDR:doc:spec=doctags` - Required docspec marker for all documents. Link: /docs/doctags.md
DOC02: `MRDR:doc:spec=metadata` - Metadata spec alignment. Link: /docs/doc_specs/metadata_spec.md
DOC03: `MRDR:doc:spec=visualdata` - Visual data spec focus.
DOC04: `MRDR:doc:spec=output` - Output and display focus.
DOC05: `MRDR:doc:spec=userexperience` - UX focus.
</pre>

### FORMATTING AND RULES
- ID: `THREELETTER`
- versioning: `SIMPLENUMERIC`
- case: `SCREAMINGSNAKE`
- eg: `TAG01`

## DOC DELIMITERS
_Unique Delimiters, and their NLP based identifiers(kept unique for compatibility)_
<!-- spec:newline=BACKSLASH -->

DDL01: `+`, `ADDTACH` - add, or attach an item or reference\
DDL02: `-+`,`DELREM` - remove, or delete an item or reference\
DDL03: `!>`, `EXCEPTFOR` - "Except for [x] ID", an exception to a rule.\
DDL04: ` `\
DDL05: ` `\
DDL06: ` `\
DDL07: ` `\
DDL08: ` `\
DDL09: ` `\
DDL10: ` `

## Grammar
_Grammar or Definitions for a custom defined purpose_

GRM01: `rstr`, `RESTRICTIONS` - Prohibited practise\
GRM02: `ntype`, `NAMETYPE` - Grandparent Type\
GRM05: `dlist`, `DASHLIST` - a dash ordered list\
GRM06: `id`, `ID` - Purpose Related Identifier\
GRM07: `glbl`, `GLOBAL` - Applies Globally in the Repo\
GRM08: `met`, `METADATA` - References the docs Metadata\
GRM09: ` `\
GRM10: ` `

## Inter-Document-Commands
IDC01: `LANGUSE`, `LANGUAGEUSAGE` - Duplicated Usage\
IDC02:\
IDC03:\
IDC04:\
IDC05:\
IDC06:\
IDC07:\
IDC08:\
IDC09:\
IDC10:\

## FORMATTING
FMT01: `newline`\
- HEADERS:newline\
  - ABOVE:true,\
  - BELOW:`false`\

FMT02: `bksmtd`, `BACKSLASHMETHOD`\
FMT03: `CONFIG:DEFAULT:newline:spec=TWOSPACES`\
FMT04:\
FMT05:\
FMT06:\
FMT07:\
FMT08:\
FMT09:\
FMT10:
