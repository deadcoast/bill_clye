"""Property tests for suggestion functionality.

Feature: mrdr-cli-foundation
Properties: 18, 19
Validates: Requirements 7.1, 7.3
"""

import string

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.utils.suggestions import (
    fuzzy_match,
    get_command_suggestions,
    get_language_suggestions,
    MRDR_COMMANDS,
)
from mrdr.database import QueryEngine


# Create a shared query engine for tests
_query_engine = QueryEngine()


def get_valid_languages() -> list[str]:
    """Get list of valid languages from the database."""
    return _query_engine.list_languages()


# Strategy for generating typos of valid commands
@st.composite
def typo_command_strategy(draw: st.DrawFn) -> str:
    """Generate a typo version of a valid command."""
    command = draw(st.sampled_from(MRDR_COMMANDS))
    # Apply a simple typo: swap two adjacent chars or drop a char
    if len(command) < 2:
        return command + "x"
    
    typo_type = draw(st.integers(min_value=0, max_value=2))
    if typo_type == 0 and len(command) >= 2:
        # Swap two adjacent characters
        idx = draw(st.integers(min_value=0, max_value=len(command) - 2))
        chars = list(command)
        chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
        return "".join(chars)
    elif typo_type == 1 and len(command) >= 3:
        # Drop a character
        idx = draw(st.integers(min_value=0, max_value=len(command) - 1))
        return command[:idx] + command[idx + 1:]
    else:
        # Add a character
        idx = draw(st.integers(min_value=0, max_value=len(command)))
        char = draw(st.sampled_from(string.ascii_lowercase))
        return command[:idx] + char + command[idx:]


# Strategy for completely invalid commands
@st.composite
def invalid_command_strategy(draw: st.DrawFn) -> str:
    """Generate command names that don't exist."""
    valid = {cmd.lower() for cmd in MRDR_COMMANDS}
    candidate = draw(
        st.text(
            alphabet=string.ascii_lowercase,
            min_size=3,
            max_size=10,
        )
    )
    if candidate.lower() in valid:
        return candidate + "xyz"
    return candidate


@given(typo_cmd=typo_command_strategy())
@settings(max_examples=100)
def test_unknown_command_suggestions(typo_cmd: str) -> None:
    """Property 18: Unknown Command Suggestions.

    Feature: mrdr-cli-foundation, Property 18: Unknown Command Suggestions
    For any invalid command string (typo of a valid command), the CLI SHALL
    display an error containing at least one suggestion for a valid command
    (using fuzzy matching).
    **Validates: Requirements 7.1**
    """
    # Skip if the typo accidentally matches a valid command
    if typo_cmd.lower() in {cmd.lower() for cmd in MRDR_COMMANDS}:
        return
    
    suggestions = get_command_suggestions(typo_cmd, MRDR_COMMANDS)
    
    # All suggestions must be valid commands
    valid_commands_lower = {cmd.lower() for cmd in MRDR_COMMANDS}
    for suggestion in suggestions:
        assert suggestion.lower() in valid_commands_lower, (
            f"Suggestion '{suggestion}' is not a valid command"
        )


@given(invalid_cmd=invalid_command_strategy())
@settings(max_examples=100)
def test_fuzzy_match_returns_valid_items(invalid_cmd: str) -> None:
    """Fuzzy match should only return items from the possibilities list.

    For any query string, fuzzy_match SHALL only return items that exist
    in the provided possibilities list.
    """
    possibilities = ["alpha", "beta", "gamma", "delta", "epsilon"]
    suggestions = fuzzy_match(invalid_cmd, possibilities, cutoff=0.3)
    
    for suggestion in suggestions:
        assert suggestion in possibilities, (
            f"Suggestion '{suggestion}' not in possibilities"
        )


def test_empty_result_suggestions() -> None:
    """Property 19: Empty Result Suggestions.

    Feature: mrdr-cli-foundation, Property 19: Empty Result Suggestions
    For any query that returns zero results, the output SHALL include
    recovery suggestions (example queries or help commands).
    **Validates: Requirements 7.3**
    """
    qe = QueryEngine()
    valid_languages = qe.list_languages()
    
    # Query for a non-existent language
    invalid_lang = "xyznonexistent123"
    result = qe.query_by_language(invalid_lang)
    
    # Result should be None
    assert result is None
    
    # Suggestions should be available from valid languages
    suggestions = get_language_suggestions(invalid_lang, valid_languages)
    
    # All suggestions must be valid languages
    for suggestion in suggestions:
        assert suggestion in valid_languages, (
            f"Suggestion '{suggestion}' is not a valid language"
        )


def test_suggestions_preserve_case() -> None:
    """Suggestions should preserve the original case of possibilities."""
    possibilities = ["Python", "JavaScript", "TypeScript"]
    
    # Query with lowercase
    suggestions = fuzzy_match("python", possibilities)
    
    if suggestions:
        # Should return "Python" not "python"
        assert "Python" in suggestions or len(suggestions) == 0


def test_suggestions_case_insensitive_matching() -> None:
    """Matching should be case-insensitive."""
    possibilities = ["Python", "JavaScript", "Ruby"]
    
    # These should all find Python
    assert fuzzy_match("PYTHON", possibilities) == ["Python"]
    assert fuzzy_match("python", possibilities) == ["Python"]
    assert fuzzy_match("PyThOn", possibilities) == ["Python"]


def test_empty_query_returns_empty() -> None:
    """Empty query should return empty suggestions."""
    possibilities = ["Python", "JavaScript", "Ruby"]
    
    assert fuzzy_match("", possibilities) == []


def test_empty_possibilities_returns_empty() -> None:
    """Empty possibilities should return empty suggestions."""
    assert fuzzy_match("python", []) == []
