# dictionary.md
[MRDR:doc:spec=doctags](/docs/doctags.md)
<!-- 
DICT01:spec
  [1] STATUS:design
    NOTES: 
    - "THE FUNCTIONS ARE CURRENTLY EXAMPLES AND PLACEHOLDERS FOR CONTEXTUAL UNDERSTANDING IN DESIGN"
    - THIS SPEC IS A DRAFT, A WORK IN PROGRESS, AND NEEDS TO BE UNIFIED CORRECTLY WITH THE PROJECT ECOSYSTEM AS IT EVOLVES AND PROGRESSES. 
-->

## MRDR DICTIONARY
`MRDR` Is a `Visual CLI Database Ecosystem` that Contains two main thematic sequences within the ecosystem.

> [!IMPORTANT]
> Correspondance:back_end `hyde`
> Correspondance:front_end `jekyl`
> CLI:cmd `mrdr hyde`
> CLI:cmd `mrdr jekyl`

- Mr Hyde is the back end correspondance on full ecosystem data correlation.
  - `doc:spec=['metadata','doctags']`
  - `cli:spec=['python','sourcecode']`
  - `python:spec=['full_scope','senior_dev']`
- Mr Jekyl is the front end correspondance on full ecosystem visual correlation.
  - `doc:spec=['visualdata','output','userexperience']`
  - `cli:spec=['CLIVISUALOUTPUT','CLIDESIGN','CLIUI','ASCIIUI']`
  - `python:spec=['richclidesign','visualenhancement','visualintegration']`

### NAMETYPES
- CHD: `chd`, `CHILD` | Child Data Hierarchy
- PNT: `pnt`, `PARENT` | Parent Data Hierarchy
- GPN: `gpn`, `GRANDPARENT` | Grandparent Data Hierarchy
- GPN01: `mrdr`, `MISTERDOCTOR` | Main CLI cmd
  - PNT01: `dr`, `DOCTOR` | CLI cmd
  - PNT02: `mr`, `MISTER` | CLI cmd
    - CHD01: `hyde` `HYDE` | CLI opt
    - CHD02: `jekyl` `JEKYL` | CLI opt
    - CHD03: `clide`, `CLIDE` | CLI opt

#### DEFINITIONS
- DEF01: `ver`, `VERSION`
Version control or Numeric Tag
- DEF02: `accro`, `ACRONYM`
ACROYNM representing a title
- DEF03: `numver`, `NUMERICVERSION`
`VERSION`(PARENT), `numver`(child) type
- DEF04: `simpnum`, `SIMPLENUMERIC`
A simple numeric `ver:numver:simpnum`numver`=`opt`:(2)
- DEF05: `scrmsnk`, `SCREAMINSNAKE` -
All Capital Name Type formatting
- DEF06: `rmlog`, `REMOVALLOG`
metadata footer log, used when AI removes large portions of files
- DEF07: `met`, `META`
Referencing the correlating METADATA
- DEF08: `add`, `ADD`
Add or Remove the correlating data
- DEF09: `cmnd`, `COMMAND`
Command that has a function
- DEF10: `glbl`, `GLOBAL`
Defines the relative action as global in the `mrdr` ecosystem
- DEF11: `clide`, `VSCLIDE`
  - `accro:vsclide="VISUAL CLI DATABASE ECOSYSTEM"`

## Document Class Hierarchy

### `grandparent` Functions [TODO05]
_Top level notation, carry large weight, often used as header or footer notes_

- `NOTE`, `note` - Additional notes provided in the authors voice\
- `CLAIM`, `claim` - Top level Claims, [eg: CLAIM]\
- `LANG_USE` - _This tag is used to identify the additional utilization of a term in a different language._
- `FORMAT` - _This tag is used to identify the format of the documentation._
- `PURPOSE` - _This tag is used to identify the purpose of the documentation._
- `RESTRICTIONS` - _This tag is used to identify the restrictions of the documentation._
- `STYLING` - _This tag is used to identify the styling of the documentation._
- `USER` - _This tag is used to identify the user of the documentation._
- `NOTES` - _This tag is used to identify any additional important notes about the corresponding data._\

### `parent` commands [TODO05]
<!--
  NOTE:
    - This section showcases:
      - newline:spec=HTMLPRE
      - HTMLPRE:styling=none
-->

<pre>
apd:ASPERDEFINED=[
  'Reference is in context to traditional definition'
  ],
objacc:OBJECTIVEACCEPTANCE=[
  'A statement or claim that is obvious in nature',
  'Understandable without further explanation',
  'While still technically sound is disputable',
  'Dispute would disqualify users intelligence'
  ]
</pre>

### `child` Function [TODO05]
_child of the parent Function, usually utilized in specific subsections such as "parent:python | child:docstring"_

`sem`, `semantics` - arguing out of good faith\
`def`, `definition` - APD\
`dstr`, `docstring` - APD\
`rsch`, `research` - APD\
`stat`, `statistic` - APD\
`eg`, `example` - APD\
`vldt`, `validated` - APD\
`expr`, `experimental` - APD\
`optml`, `optimal` - APD\
`unstbl`, `unstable` - APD\
`vislap`, `visually_appealing` - APD\
`vldtd`, `validated`- APD\
`optml`, `optimal`, - APD\
`unstbl` `unstable`, - APD\
`crtv`, `creative` - APD\

### `grandchild` [TODO05]
<pre>
`val`, `value` - The value of Parent or Child function
</pre>
