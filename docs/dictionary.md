# dictionary.md
<!-- 
DICT01:spec
  [1] STATUS:design
    NOTES: 
    - "THE FUNCTIONS ARE CURRENTLY EXAMPLES AND PLACEHOLDERS FOR CONTEXTUAL UNDERSTANDING IN DESIGN"
    - THIS SPEC IS A DRAFT, A WORK IN PROGRESS, AND NEEDS TO BE UNIFIED CORRECTLY WITH THE PROJECT ECOSYSTEM AS IT EVOLVES AND PROGRESSES. 
-->
## MRDR index
 [TODO05]:tag:[GRM07]

## MRDR DICTIONARY

`MRDR` Is a `Visual CLI Database Ecosystem` that Contains two main thematic sequences within the

### NAMETYPES
- GLB01: `vsclide`, `VSCLIDE` | `accro`:`VISUAL CLI DATABASE ECOSYSTEM`
- PNT: `pnt`, `PARENT` | Parent Data Hierarchy
- GPN: `gpn`, `GRANDPARENT` | Grandparent Data Hierarchy
  - GPN01: `mrdr`, `MISTERDOCTOR` | Main CLI cmd
    - PNT01: `dr`, `DOCTOR` | CLI cmd
    - PNT02: `mr`, `MISTER` | CLI cmd
      - CHD03: `clide`, `CLIDE` | CLI opt
      - CHD02: `jekyl` `JEKYL` | CLI opt

#### DEFINITIONS
- DEF01: `ver`, `VERSION`
Version control or Numeric Tag
- DEF02: `accro`, `ACRONYM`
ACROYNM representing a title
- DEF03: `numver`, `NUMERICVERSION`
`VERSION`(PARENT), `numver`(child) type
- DEF04: `simpnum`, `SIMPLENUMERIC`
A simple numeric (billy)`ver:numver:simpnum`numver`=`opt`:(2)
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
<pre>
`APD` - As Per Defined in the english(or semantic syntax) language
`OBJ_ACC`, `objective_acceptane` - A statement or claim that is obvious in nature(_understandable without further explanation_), that while still technically is disputable, such disputes would render the operator in a position that is not serious; SEE [`semantics`]
</pre>

### `child` Function [TODO05]
_child of the parent Function, usually utilized in specific subsections such as "parent:python | child:docstring"_
<pre>
`sem`, `semantics` - APD arguing not not good faith, raising redundant points.
`def`, `definition` - APD
`dstr`, `docstring` - APD
`rsch`, `research` - APD
`stat`, `statistic` - APD
`eg`, `example` - APD
`vldt`, `validated` - APD
`expr`, `experimental` - APD
`optml`, `optimal` - APD
`unstbl`, `unstable` - APD
`vislap`, `visually_appealing` - APD
`crtve`, `creative` - Creative
`vldtd`, `validated`- APD
`optml`, `optimal`, - APD
`unstbl` `unstable`, - APD
`visap`, `visually_appealing`, - APD
`crtv`, `creative` - APD
</pre>

### `grandchild` [TODO05]
<pre>
`val`, `value` - The value of Parent or Child function
</pre>
