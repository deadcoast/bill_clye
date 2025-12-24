"""Shared fixtures and strategies for MRDR tests."""

from hypothesis import strategies as st

from mrdr.database.schema import SyntaxLocation, SyntaxType

# Strategy for valid syntax types
syntax_type_strategy = st.sampled_from(list(SyntaxType))

# Strategy for valid syntax locations
syntax_location_strategy = st.sampled_from(list(SyntaxLocation))

# Strategy for valid delimiter strings
delimiter_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "P", "S")),
    min_size=1,
    max_size=10,
)

# Strategy for optional delimiter (can be None for line-based)
optional_delimiter_strategy = st.one_of(st.none(), delimiter_strategy)

# Strategy for language names
language_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L",)),
    min_size=1,
    max_size=30,
)

# Strategy for tags
tags_strategy = st.lists(
    st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("L", "N", "Pd"))),
    max_size=5,
)

# Strategy for PLUSREP tokens (exactly 6 chars of + or .)
plusrep_tokens_strategy = st.text(alphabet=["+", "."], min_size=6, max_size=6)


# Strategy for valid PLUSREP grades
@st.composite
def plusrep_grade_strategy(draw: st.DrawFn) -> dict:
    """Generate valid PLUSREP grade data."""
    tokens = draw(plusrep_tokens_strategy)
    rating = tokens.count("+") - 2
    labels = {
        4: "MAXIMUM",
        3: "GREAT",
        2: "GOOD",
        1: "FAIR",
        0: "SLOPPY",
        -1: "POOR",
        -2: "RESET",
    }
    label = labels.get(rating, "UNKNOWN")
    return {"tokens": tokens, "rating": rating, "label": label}


# Strategy for valid SyntaxSpec data
@st.composite
def syntax_spec_strategy(draw: st.DrawFn) -> dict:
    """Generate valid SyntaxSpec data."""
    return {
        "start": draw(delimiter_strategy),
        "end": draw(optional_delimiter_strategy),
        "type": draw(syntax_type_strategy).value,
        "location": draw(syntax_location_strategy).value,
    }


# Strategy for valid DocstringEntry data
@st.composite
def docstring_entry_strategy(draw: st.DrawFn) -> dict:
    """Generate valid DocstringEntry data."""
    entry = {
        "language": draw(language_strategy),
        "syntax": draw(syntax_spec_strategy()),
        "tags": draw(tags_strategy),
    }
    # Optionally add optional fields
    if draw(st.booleans()):
        entry["example_content"] = draw(st.text(min_size=0, max_size=200))
    if draw(st.booleans()):
        entry["conflict_ref"] = draw(st.text(min_size=1, max_size=50))
    if draw(st.booleans()):
        entry["parsing_rule"] = draw(st.text(min_size=1, max_size=100))
    if draw(st.booleans()):
        entry["metadata"] = draw(st.text(min_size=1, max_size=100))
    if draw(st.booleans()):
        entry["plusrep"] = draw(plusrep_grade_strategy())
    return entry
