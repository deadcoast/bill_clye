# docstring_template.md
[MRDR:doc:spec=doctags](/docs/doctags.md)

## DICTIONARY

`TITLE`: The title of the docstring design
`DESCR`: The description of the docstring design
`LANG`: The targeted language for the docstring, if `none` input `UDL`
`DELIMITER`: A SINGLE character used to identify actions, functions, methods, or id
`OPERATOR`: TWO delimeters that act as one, providing additional functionality than a delimiter alone
<!-- 
  **NOTE**:
  - Not every definition requires explanation, such as "opening, closing, and bracket".
  - Self-Explanatory words do not require explicit definition in the DICTIONARY 
 -->

## User Defined Doc String Template

TITLE: 'Pointy-Numerical-Index'
DESCR: 'Hierarchal, Numerical based BRACKET index'
LANG: UDL

### Pointy Numerical Index - A numerical and BRACKET hierachal index design

```pindx
<(1)
  CLAIM:{
    sky_color:"The color of the observable sky is blue during the day"
      objective_acceptance:[
        "No further specification given, the sky is blue.",
        "The sky is blue almost always, the claim obviously corresponds to the way humans witness the sky majority of time."
        ],
      semantics:[
        "They sky is grey when its overcast at daytime",
        "One could argue the sky is orange during a sunset"
        ]
    },

<(2)
  CLAIM:{
    hand_fingers:"Humans have 5 fingers on each hand"
      objective_acceptance:[
        "Humans have 5 fingers on each hand",
        ],
      semantics:[
        "Humans have 4 fingers and one thumb"
        ]
    },
>
```

### DELIMETER

OPENING: `<`
CLOSING: `>`
BRACKET: `(`, `)`

### OPERATORS

- `dolphin` OPERATOR `<:`, `:>`
- `walrus` OPERATOR `:=`, `=:`

## DOCSTRING VARIANTS

### `dolphin`

OPERATOR: `<:`, `:>`

```udl
<:(1)
The context of the docstring here
:>
```

### `walrus`

OPERATOR: `:=`, `=:`

```udl
:=(1)
The context of the docstring here
=:
```
