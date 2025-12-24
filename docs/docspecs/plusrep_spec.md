# plusrep_spec.md
[MRDR:doc:spec=doctags](/docs/doctags.md)

_This document defines the PLUSREP grading system and its output patterns._

## PLUSREP TOKENS
- `+`: Ppositive repweight token, add one reputation
- `.`: Negative repweight token, minus one reputation

## PLUSREP OUTPUT PROTOCOL
```mrdr
plusrep:output:+:[val:rep:(1 -> 6)]
  plusrep:[++++++]="MAXIMUM:rep:rating == val:rep:+4",
  plusrep:[+++++.]="GREAT:rep:rating == val:rep:+3",
  plusrep:[++++..]="GREAT:rep:rating == val:rep:+2",
  plusrep:[+++...]="GREAT:rep:rating == val:rep:+2",
  plusrep:[++....]="SLOPPY:rep:rating == val:rep:+0",
  plusrep:[++....]="REJECTED:rep:rating == val:rep:-2",
  plusrep:[+.....]="RESET:rep:rating == val:rep: -3"
```

## MRDR DOCSTRING METADATA (plusrat)
```mrdr
<!-- 
  plusrep:output:+:[val:rep:(1 -> 6)]
    GRANDPARENT: plusrep:output:+:[val:rep:(1 -> 6)]
    PARENT: plusrep:[++++++]
    CHILD: "MAXIMUM:rep:rating == val:rep:+4",
    VALUE: val:rep:+4"
-->
```

## PLUSREP GRADE WEIGHTING
```mrdr
plusrep:grade:weight=(
  +:consistency:types,
  +:accuracy:spec,
  +:quality:design
  )
```

## DIRECT USER RESPONSE PATTERN
```mrdr
<!-- plusrep:out:bars -->
  1. true [++++..]
  2. true [+++++.]
  3. true [++++..]
<!-- plusrep:conclusion:="NETPOSITIVE:rep, PLUSREP!!" -->
```

## NOTES
- Duplicate or conflicting outputs are retained as authored for later review.
