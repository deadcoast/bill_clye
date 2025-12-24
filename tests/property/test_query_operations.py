"""Property tests for query operations.

Feature: mrdr-cli-foundation
Properties: 3, 4, 5
Validates: Requirements 2.1, 2.2, 2.3, 2.4
"""

import string

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.database import QueryEngine


# Create a shared query engine for tests
_query_engine = QueryEngine()


def get_valid_languages() -> list[str]:
    """Get list of valid languages from the database."""
    return _query_engine.list_languages()


# Strategy for valid language names from database
valid_language_strategy = st.sampled_from(get_valid_languages())


# Strategy for invalid language names
@st.composite
def invalid_language_strategy(draw: st.DrawFn) -> str:
    """Generate language names that don't exist in the database."""
    valid = {lang.lower() for lang in get_valid_languages()}
    # Generate random strings that aren't valid languages
    candidate = draw(
        st.text(
            alphabet=string.ascii_letters,
            min_size=3,
            max_size=15,
        )
    )
    # Ensure it's not a valid language
    if candidate.lower() in valid:
        return candidate + "xyz"
    return candidate


@given(language=valid_language_strategy)
@settings(max_examples=100)
def test_query_returns_valid_data(language: str) -> None:
    """Property 3: Query Returns Valid Data.

    Feature: mrdr-cli-foundation, Property 3: Query Returns Valid Data
    For any language that exists in the database, query SHALL return a
    DocstringEntry with all required fields populated.
    **Validates: Requirements 2.1, 2.3**
    """
    qe = QueryEngine()
    result = qe.query_by_language(language)

    assert result is not None, f"Query for '{language}' returned None"
    assert result.language.lower() == language.lower()
    assert result.syntax.start is not None
    assert result.syntax.type is not None
    assert result.syntax.location is not None


def test_list_completeness() -> None:
    """Property 4: List Completeness.

    Feature: mrdr-cli-foundation, Property 4: List Completeness
    For any database state, list_languages SHALL return a list containing
    exactly all languages present in the database, with no duplicates and
    no omissions.
    **Validates: Requirements 2.2**
    """
    qe = QueryEngine()
    languages = qe.list_languages()

    # No duplicates
    assert len(languages) == len(set(languages)), "Duplicate languages found"

    # All languages are queryable
    for lang in languages:
        entry = qe.query_by_language(lang)
        assert entry is not None, f"Language '{lang}' in list but not queryable"

    # All entries are in the list
    all_entries = qe.loader.get_entries()
    entry_languages = {e.language for e in all_entries}
    list_languages = set(languages)
    assert entry_languages == list_languages, "List does not match all entries"


@given(invalid_lang=invalid_language_strategy())
@settings(max_examples=100)
def test_invalid_language_suggestions(invalid_lang: str) -> None:
    """Property 5: Invalid Language Suggestions.

    Feature: mrdr-cli-foundation, Property 5: Invalid Language Suggestions
    For any language string that does not exist in the database, the query
    SHALL return None and get_suggestions SHALL return suggestions from the
    database (using fuzzy matching).
    **Validates: Requirements 2.4**
    """
    qe = QueryEngine()

    # Query should return None for invalid language
    result = qe.query_by_language(invalid_lang)
    assert result is None, f"Query for invalid '{invalid_lang}' should return None"

    # Suggestions should come from valid languages
    suggestions = qe.get_suggestions(invalid_lang, cutoff=0.3)
    valid_languages = set(qe.list_languages())

    for suggestion in suggestions:
        assert suggestion in valid_languages, (
            f"Suggestion '{suggestion}' not in valid languages"
        )


def test_query_case_insensitive() -> None:
    """Query should be case-insensitive."""
    qe = QueryEngine()

    # Test various case combinations
    python_lower = qe.query_by_language("python")
    python_upper = qe.query_by_language("PYTHON")
    python_mixed = qe.query_by_language("PyThOn")

    assert python_lower is not None
    assert python_upper is not None
    assert python_mixed is not None
    assert python_lower.language == python_upper.language == python_mixed.language
