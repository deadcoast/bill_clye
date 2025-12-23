# dictionary.md
<!-- NOTE: THIS SPEC IS A DRAFT, A WORK IN PROGRESS, AND NEEDS TO BE UNIFIED CORRECTLY WITH THE PROJECT ECOSYSTEM AS IT EVOLVES AND PROGRESSES-->

## Document Class Hierarchy

### `grandparent` Functions

_Top level notation, carry large weight, often used as header or footer notes_

- `NOTE`, `note` - Additional notes provided in the authors voice
- `CLAIM`, `claim` - Top level Claims, [eg: CLAIM]
- `LANG_USE` - _This tag is used to identify the additional utilization of a term in a different language._
- `FORMAT` - _This tag is used to identify the format of the documentation._
- `PURPOSE` - _This tag is used to identify the purpose of the documentation._
- `RESTRICTIONS` - _This tag is used to identify the restrictions of the documentation._
- `STYLING` - _This tag is used to identify the styling of the documentation._
- `USER` - _This tag is used to identify the user of the documentation._
- `NOTES` - _This tag is used to identify any additional important notes about the corresponding data._

### `parent` commands

- `APD` - As Per Defined in the english(or semantic syntax) language
- `OBJ_ACC`, `objective_acceptane` - A statement or claim that is obvious in nature(_understandable without further explanation_), that while still technically is disputable, such disputes would render the operator in a position that is not serious; SEE [`semantics`]

### `child` Function

_child of the parent Function, usually utilized in specific subsections such as "parent:python | child:docstring"_

- `sem`, `semantics` - APD arguing not not good faith, raising redundant points.
- `def`, `definition` - APD
- `dstr`, `docstring` - APD
- `rsch`, `research` - APD
- `stat`, `statistic` - APD
- `eg`, `example` - APD
- `vldt`, `validated` - APD
- `expr`, `experimental` - APD
- `optml`, `optimal` - APD
- `unstbl`, `unstable` - APD
- `vislap`, `visually_appealing` - APD
- `crtve`, `creative` - Creative
- `vldtd`, `validated`- APD
- `optml`, `optimal`, - APD
- `unstbl` `unstable`, - APD
- `visap`, `visually_appealing`, - APD
- `crtv`, `creative` - APD

### GRANDCHILDREN

`'research', '(RSC)`
`'statistic', '(STAT)`
`'example', '(EXM)`
