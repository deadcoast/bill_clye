# tags.md
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

TITLE: BILLYTAGS/
PURPOSE: Defined by a strict spec to maximize:['BREVITY', 'CONSISTENCY', 'READABILITY', 'PARSING']
</pre>

### FORMATTING AND RULES
- ID: `THREELETTER`
- versioning: `SIMPLENUMERIC`
- case: `SCREAMINGSNAKE`
- eg: `TAG01`

## DOC DELIMITERS
_Unique Delimiters, and their NLP based identifiers(kept unique for compatibility)_

<pre>
DDL01: `+`, `ADDTACH` - add, or attach an item or reference
DDL02: `-+`,`DELREM` - remove, or delete an item or reference
DDL03: `!>`, `EXCEPTFOR` - "Except for [x] ID", an exception to a rule.
DDL04:
DDL05:
</pre>

## Grammar
_Grammar or Definitions for a custom defined purpose_

<pre>
GRM01: `rstr`, `RESTRICTIONS` - Strictly prohibited practise. DO NOT utilize. AVOID. etc.
GRM02: `ntype`, `NAMETYPE`
GRM05: `dlist`, `DASHLIST` - Identifies a list, beginning with the `DELIMITER`:`-`
GRM06: `fid`, `FILEID` - The identifer used to describe the purpose of a document or file.
GRM07: `glbl`, `GLOBAL` - Applies Globally in the Repo
GRM08: `met`, `METADATA` -
GRM09:
GRM10:
</pre>

## Inter-Document-Commands
<pre>
IDC01: `LANGUSE`, `LANGUAGEUSAGE` - Specific or Identical Characteristics found in another language | `eg`: "01" for first.
IDC02:
IDC03:
IDC04:
IDC05:
IDC06:
IDC07:
IDC08:
IDC09:
IDC10:
</pre>

## FORMATTING
<pre>

FMT07: `newline`
- HEADERS:newline,
  - ABOVE:true,
  - BELOW:false
FMT08:
FMT09:
FMT10:
</pre>
