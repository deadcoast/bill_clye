"""Fuzzy matching utilities for suggestions.

This module provides fuzzy matching functions for generating helpful
suggestions when users enter invalid commands or language names.
"""

import difflib
from typing import Sequence


def fuzzy_match(
    query: str,
    possibilities: Sequence[str],
    n: int = 3,
    cutoff: float = 0.5,
) -> list[str]:
    """Find close matches for a query string using fuzzy matching.

    Uses difflib.get_close_matches to find similar strings from a list
    of possibilities. Matching is case-insensitive.

    Args:
        query: The search query string.
        possibilities: Sequence of possible matches.
        n: Maximum number of suggestions to return.
        cutoff: Similarity threshold (0.0 to 1.0). Lower values return
            more matches but with less similarity.

    Returns:
        A list of matching strings from possibilities, preserving
        original case.

    Example:
        >>> fuzzy_match("pythn", ["Python", "JavaScript", "Ruby"])
        ['Python']
        >>> fuzzy_match("jva", ["Python", "JavaScript", "Java"])
        ['Java', 'JavaScript']
    """
    if not query or not possibilities:
        return []

    # Build case-insensitive mapping
    lower_to_original: dict[str, str] = {}
    for item in possibilities:
        lower_key = item.lower()
        # Keep first occurrence if duplicates exist
        if lower_key not in lower_to_original:
            lower_to_original[lower_key] = item

    # Find matches using lowercase comparison
    matches = difflib.get_close_matches(
        query.lower(),
        lower_to_original.keys(),
        n=n,
        cutoff=cutoff,
    )

    # Return original-case versions
    return [lower_to_original[m] for m in matches]


def get_command_suggestions(
    invalid_command: str,
    valid_commands: Sequence[str],
    n: int = 3,
) -> list[str]:
    """Get suggestions for an invalid CLI command.

    Args:
        invalid_command: The command that was not recognized.
        valid_commands: List of valid command names.
        n: Maximum number of suggestions to return.

    Returns:
        A list of suggested command names.
    """
    return fuzzy_match(invalid_command, valid_commands, n=n, cutoff=0.4)


def get_language_suggestions(
    invalid_language: str,
    valid_languages: Sequence[str],
    n: int = 3,
) -> list[str]:
    """Get suggestions for an invalid language name.

    Args:
        invalid_language: The language name that was not found.
        valid_languages: List of valid language names from the database.
        n: Maximum number of suggestions to return.

    Returns:
        A list of suggested language names.
    """
    return fuzzy_match(invalid_language, valid_languages, n=n, cutoff=0.4)


# Common CLI commands for suggestion matching
MRDR_COMMANDS = [
    "hyde",
    "jekyl",
    "docstring",
    "config",
    "fix",
]

HYDE_SUBCOMMANDS = [
    "query",
    "list",
    "inspect",
    "export",
    "validate",
]

JEKYL_SUBCOMMANDS = [
    "show",
    "compare",
]

CONFIG_SUBCOMMANDS = [
    "show",
    "set",
]
