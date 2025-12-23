# tags.md
<!-- 
**tags.md:spec** 
  [1] Tags + Data + Descriptions must fit on a single line
  [2] +new_line below headers
  [3] -+new_line above headers !> lists
  [4] -+['whitespace','delimiter'] in NLP ALIAS IDENTIFIERS
  [5] docs -> src -> cli NAMETYPE cohesion is crucial for full scope UX in the ecosystem
  [6] The docs, source code, and cli should be consistent
-->

## DOCTAG SPEC
TITLE: BILLYTAGS
PURPOSE: Defined by a strict spec to maximize:['BREVITY', 'CONSISTENCY', 'READABILITY', 'PARSING']

### FORMATTING AND RULES
- ID: `THREELETTER`
- versioning: `SIMPLENUMERIC`
- case: `SCREAMINGSNAKE`
- eg: `TAG01`

## DOC DELIMITERS
_Unique Delimiters, and their NLP based identifiers(kept unique for compatibility)_

DDL01: `+`, `ADDTACH` - add, or attach an item or reference
DDL02: `-+`,`DELREM` - remove, or delete an item or reference
DDL03: `!>`, `EXCEPTFOR` - "Except for [x] ID", an exception to a rule.
DDL04:
DDL05:

## Grammar
_Grammar or Definitions for a custom defined purpose_

GRM01: `rstr`, `RESTRICTIONS` - Strictly prohibited practise. DO NOT utilize. AVOID. etc.
GRM02: `ntype`, `NAMETYPE`
GRM05: `dlist`, `DASHLIST` - Identifies a list, beginning with the `DELIMITER`:`-`
GRM06: `fid`, `FILEID` - The identifer used to describe the purpose of a document or file.
GRM07:
GRM08:
GRM09:
GRM10:

## Inter-Document-Commands
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

## FORMATTING
FMT02: `ver`, `VERSION` - Version control, a parent numeric tagging system to child:FMT01
FMT01: `accro`, `ACRONYM` - Acronym accompanied by a single numeric digit to specify its letter length.
FMT03: `numver`, `NUMERICVERSION` - A Grandfather term for all number based version control formats.
FMT04: `simpnum`, `SIMPLENUMERIC` - Two Number `numver` identifier
FMT05: `scrmsnk`, `SCREAMINSNAKE` - All Capital Name Type formatting
FMT06: `rmlog`, `REMOVALLOG` - The metadata footer log, used when AI removes large portions of files
FMT07:
FMT08:
FMT09:
FMT10:
