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
```md
<pre>
[MET01] : Tags + Data + Descriptions must fit on a single line
</pre>
```

## DOCTAG SPEC
<pre>
TITLE: YTAGS/
PURPOSE: Defined by a strict spec to maximize:['BREVITY', 'CONSISTENCY', 'READABILITY', 'PARSING']
</pre>

## MRDR DOCSPEC TAGS
<pre>
DOC01: `MRDR:doc:spec=doctags` - Required docspec marker for all documents. Link: /docs/doctags.md
DOC02: `MRDR:doc:spec=metadata` - Metadata spec alignment. Link: /docs/docspecs/metadata_spec.md
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
DDL04: `:`, `KEYVAL` - key/value separator for tags and metadata.\
DDL05: `|`, `DOCPIPE` - file/header separator in doc links.\
DDL06: `=`, `ASSIGN` - assignment operator for inline configs.\
DDL07: `,`, `LISTSEP` - inline list separator.\
DDL08: `;`, `STMTSEP` - statement separator for compact specs.\
DDL09: `/`, `PATHSEP` - path delimiter for repo-relative references.\
DDL10: `#`, `HEADTAG` - header identifier for anchor references.

## Grammar
_Grammar or Definitions for a custom defined purpose_

GRM01: `rstr`, `RESTRICTIONS` - Prohibited practise\
GRM02: `ntype`, `NAMETYPE` - Grandparent Type\
GRM05: `dlist`, `DASHLIST` - a dash ordered list\
GRM06: `id`, `ID` - Purpose Related Identifier\
GRM07: `glbl`, `GLOBAL` - Applies Globally in the Repo\
GRM08: `met`, `METADATA` - References the docs Metadata\
GRM09: `alias`, `ALIAS` - Alternate name binding for the same command/tag.\
GRM10: `desc`, `DESCRIPTION` - Descriptive text attached to an identifier.

## Inter-Document-Commands
IDC01: `LANGUSE`, `LANGUAGEUSAGE` - Duplicated Usage\
IDC02: `DOCLINK`, `DOCREFERENCE` - File+header reference using file|## header.\
IDC03: `FILELINK`, `FILEREF` - File-only reference.\
IDC04: `HEADRLINK`, `HEADERREF` - Header-only reference within a file.\
IDC05: `REF`, `REFERENCE` - General cross-doc reference marker.\
IDC06: `SPECREF`, `SPECREFERENCE` - Spec pointer in docs.\
IDC07: `DBREF`, `DATABASEREF` - Database reference pointer.\
IDC08: `TEMPRE`, `TEMPLATEREF` - Template reference pointer.\
IDC09: `RESREF`, `RESOURCEREF` - Resource reference pointer.\
IDC10: `TODOLINK`, `TODOREF` - TODO reference pointer.

## FORMATTING
FMT01: `newline`\
- HEADERS:newline\
  - ABOVE:true,\
  - BELOW:`false`\

FMT02: `nlrule`, `NEWLINERULE` - newline rule marker.\
FMT03: `cfgdflt`, `CONFIGDEFAULT` - default config marker.\
FMT04: `twospc`, `TWOSPACES` - two-space newline variant (default).\
FMT05: `htmlbr`, `HTMLBR` - HTML `<br>` line break method.\
FMT06: `htmlpre`, `HTMLPRE` - `<pre>` block newline method.\
FMT07: `codeblk`, `CODEBLOCK` - code block newline method.\
FMT08: `tblmtd`, `TABLEMETHOD` - table-based newline method.\
FMT09: `invtable`, `INVISIBLETABLE` - invisible table variant.\
FMT10: `bksmtd`, `BACKSLASHMETHOD` - backslash newline method.
