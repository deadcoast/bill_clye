# dictionary.md
<!-- 
DICT01:spec
  [1] STATUS:design
    NOTES: 
    - "THE FUNCTIONS ARE CURRENTLY EXAMPLES AND PLACEHOLDERS FOR CONTEXTUAL UNDERSTANDING IN DESIGN"
    - THIS SPEC IS A DRAFT, A WORK IN PROGRESS, AND NEEDS TO BE UNIFIED CORRECTLY WITH THE PROJECT ECOSYSTEM AS IT EVOLVES AND PROGRESSES. 
-->
 [TODO05]:tag:[GRM07]

## Definitions

`ver`, `VERSION` - Version control, a parent numeric tagging system to child:FMT01
`accro`, `ACRONYM` - Acronym accompanied by a single numeric digit to specify its letter length.
`numver`, `NUMERICVERSION` - A Grandfather term for all number based version control formats.
`simpnum`, `SIMPLENUMERIC` - Two Number `numver` identifier
`scrmsnk`, `SCREAMINSNAKE` - All Capital Name Type formatting
`rmlog`, `REMOVALLOG` - The metadata footer log, used when AI removes large portions of files

## Document Class Hierarchy

- `met`, `META`
### `grandparent` Functions [TODO05]
_Top level notation, carry large weight, often used as header or footer notes_
<pre>
- `NOTE`, `note` - Additional notes provided in the authors voice
- `CLAIM`, `claim` - Top level Claims, [eg: CLAIM]
- `LANG_USE` - _This tag is used to identify the additional utilization of a term in a different language._
- `FORMAT` - _This tag is used to identify the format of the documentation._
- `PURPOSE` - _This tag is used to identify the purpose of the documentation._
- `RESTRICTIONS` - _This tag is used to identify the restrictions of the documentation._
- `STYLING` - _This tag is used to identify the styling of the documentation._
- `USER` - _This tag is used to identify the user of the documentation._
- `NOTES` - _This tag is used to identify any additional important notes about the corresponding data._
</pre>

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
