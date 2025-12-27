"""Property tests for cross-database consistency.

Feature: mrdr-data-population, Properties 17, 18
Validates: Requirements 9.3, 10.1, 10.2
"""

import json
import re
from pathlib import Path

from hypothesis import given, settings
import hypothesis.strategies as st


# Database paths
DOCSTRING_DB_PATH = Path("database/docstrings/docstring_database.json")
CONFLICT_DB_PATH = Path("database/conflicts/conflict_database.json")
DOCTAG_DB_PATH = Path("database/doctags/doctag_database.json")
DICTIONARY_DB_PATH = Path("database/dictionary/dictionary_database.json")


def load_docstring_database() -> dict:
    """Load the docstring database from JSON file."""
    with open(DOCSTRING_DB_PATH) as f:
        return json.load(f)


def load_conflict_database() -> dict:
    """Load the conflict database from JSON file."""
    with open(CONFLICT_DB_PATH) as f:
        return json.load(f)


def load_doctag_database() -> dict:
    """Load the doctag database from JSON file."""
    with open(DOCTAG_DB_PATH) as f:
        return json.load(f)


def load_dictionary_database() -> dict:
    """Load the dictionary database from JSON file."""
    with open(DICTIONARY_DB_PATH) as f:
        return json.load(f)


def get_docstring_entries() -> list[dict]:
    """Get all entries from the docstring database."""
    return load_docstring_database().get("entries", [])


def get_conflict_entries() -> list[dict]:
    """Get all entries from the conflict database."""
    return load_conflict_database().get("conflicts", [])


# Property 17: Cross-Database Term Consistency
@settings(max_examples=1)
@given(st.just(None))
def test_property_17_cross_database_term_consistency(_: None) -> None:
    """Property 17: Cross-Database Term Consistency.

    Feature: mrdr-data-population, Property 17: Cross-Database Term Consistency
    For any term that appears in multiple databases (e.g., language names in
    docstrings and conflicts), the term SHALL use identical spelling and casing
    across all occurrences.
    **Validates: Requirements 9.3**
    """
    # Collect language names from docstring database
    docstring_entries = get_docstring_entries()
    docstring_languages = {entry.get("language") for entry in docstring_entries if entry.get("language")}
    
    # Collect language names from conflict database
    conflict_entries = get_conflict_entries()
    conflict_languages = set()
    for conflict in conflict_entries:
        languages = conflict.get("languages", [])
        conflict_languages.update(languages)
        # Also check attachment_rules keys
        attachment_rules = conflict.get("attachment_rules", {})
        conflict_languages.update(attachment_rules.keys())
    
    # All languages in conflict database must exist in docstring database
    # with identical spelling and casing
    missing_in_docstring = conflict_languages - docstring_languages
    assert not missing_in_docstring, (
        f"Languages in conflict database not found in docstring database "
        f"(case-sensitive): {missing_in_docstring}"
    )
    
    # Check for case-insensitive duplicates within docstring database
    # (e.g., "Python" and "python" would be a consistency violation)
    lower_to_original: dict[str, list[str]] = {}
    for lang in docstring_languages:
        lower = lang.lower()
        if lower not in lower_to_original:
            lower_to_original[lower] = []
        lower_to_original[lower].append(lang)
    
    duplicates = {k: v for k, v in lower_to_original.items() if len(v) > 1}
    assert not duplicates, (
        f"Case-inconsistent language names found in docstring database: {duplicates}"
    )


# Property 18: Example Content Canonical Format
@settings(max_examples=100)
@given(entry_idx=st.integers(min_value=0, max_value=24))
def test_property_18_example_content_canonical_format(entry_idx: int) -> None:
    """Property 18: Example Content Canonical Format.

    Feature: mrdr-data-population, Property 18: Example Content Canonical Format
    For any docstring entry with non-null example_content, the content SHALL
    contain references to canonical payload fields (format, purpose, or user).
    **Validates: Requirements 10.1, 10.2**
    """
    entries = get_docstring_entries()
    if entry_idx >= len(entries):
        entry_idx = entry_idx % len(entries)
    
    entry = entries[entry_idx]
    example_content = entry.get("example_content")
    
    # Skip entries without example_content
    if example_content is None:
        return
    
    # Canonical payload fields that should be present
    # At least one of: format, purpose, user
    canonical_fields = ["format", "purpose", "user"]
    
    # Check if at least one canonical field is present
    has_canonical_field = any(
        re.search(rf'\b{field}\s*[:=]', example_content, re.IGNORECASE)
        for field in canonical_fields
    )
    
    assert has_canonical_field, (
        f"Entry '{entry.get('language')}' has example_content but no canonical "
        f"payload fields (format, purpose, or user). Content: {example_content[:100]}..."
    )


def test_all_entries_with_example_content_have_canonical_fields() -> None:
    """All entries with example_content must have at least one canonical field."""
    entries = get_docstring_entries()
    canonical_fields = ["format", "purpose", "user"]
    
    entries_with_content = [
        entry for entry in entries
        if entry.get("example_content") is not None
    ]
    
    for entry in entries_with_content:
        example_content = entry.get("example_content", "")
        language = entry.get("language", "unknown")
        
        has_canonical_field = any(
            re.search(rf'\b{field}\s*[:=]', example_content, re.IGNORECASE)
            for field in canonical_fields
        )
        
        assert has_canonical_field, (
            f"Entry '{language}' has example_content but no canonical "
            f"payload fields (format, purpose, or user)"
        )


def test_conflict_languages_match_docstring_languages() -> None:
    """All languages in conflict database must exist in docstring database."""
    docstring_entries = get_docstring_entries()
    docstring_languages = {entry.get("language") for entry in docstring_entries}
    
    conflict_entries = get_conflict_entries()
    
    for conflict in conflict_entries:
        conflict_id = conflict.get("id", "unknown")
        languages = conflict.get("languages", [])
        
        for lang in languages:
            assert lang in docstring_languages, (
                f"Conflict '{conflict_id}' references language '{lang}' "
                f"not found in docstring database"
            )


def test_conflict_attachment_rules_match_docstring_locations() -> None:
    """Attachment rules in conflicts should match docstring locations."""
    docstring_entries = get_docstring_entries()
    lang_to_location = {
        entry.get("language"): entry.get("syntax", {}).get("location")
        for entry in docstring_entries
    }
    
    conflict_entries = get_conflict_entries()
    
    for conflict in conflict_entries:
        conflict_id = conflict.get("id", "unknown")
        attachment_rules = conflict.get("attachment_rules", {})
        
        for lang, rule in attachment_rules.items():
            docstring_location = lang_to_location.get(lang)
            if docstring_location:
                assert rule == docstring_location, (
                    f"Conflict '{conflict_id}' has attachment rule '{rule}' for "
                    f"'{lang}' but docstring database has location '{docstring_location}'"
                )


def test_database_files_exist() -> None:
    """All database files must exist."""
    assert DOCSTRING_DB_PATH.exists(), f"Docstring database not found: {DOCSTRING_DB_PATH}"
    assert CONFLICT_DB_PATH.exists(), f"Conflict database not found: {CONFLICT_DB_PATH}"
    assert DOCTAG_DB_PATH.exists(), f"Doctag database not found: {DOCTAG_DB_PATH}"
    assert DICTIONARY_DB_PATH.exists(), f"Dictionary database not found: {DICTIONARY_DB_PATH}"
