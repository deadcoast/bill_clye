"""Property tests for docstring database population.

Feature: mrdr-data-population, Properties 1, 2, 3
Validates: Requirements 1.1, 1.2, 1.4
"""

import json
from pathlib import Path

from hypothesis import given, settings
import hypothesis.strategies as st

from mrdr.database.schema import DocstringEntry, SyntaxSpec


# Path to the docstring database
DATABASE_PATH = Path("database/docstrings/docstring_database.json")

# Expected minimum languages per requirement 1.1
EXPECTED_LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "Kotlin", "Scala",
    "PHP", "Swift", "Rust", "Zig", "C#", "F#", "Elixir", "Ruby",
    "Lua", "D", "Julia", "Haskell", "COBOL", "Raku", "Erlang",
    "Ada", "OCaml", "Clojure", "Fortran"
]


def load_database() -> dict:
    """Load the docstring database from JSON file."""
    with open(DATABASE_PATH) as f:
        return json.load(f)


def get_entries() -> list[dict]:
    """Get all entries from the database."""
    return load_database().get("entries", [])


# Property 1: Docstring Database Language Count
@settings(max_examples=1)
@given(st.just(None))
def test_property_1_docstring_database_language_count(_: None) -> None:
    """Property 1: Docstring Database Language Count.

    Feature: mrdr-data-population, Property 1: Docstring Database Language Count
    For any valid docstring database state, the number of language entries
    SHALL be at least 25.
    **Validates: Requirements 1.1**
    """
    entries = get_entries()
    languages = [entry.get("language") for entry in entries]
    
    # Must have at least 25 languages
    assert len(languages) >= 25, f"Expected at least 25 languages, got {len(languages)}"
    
    # All expected languages should be present
    missing = [lang for lang in EXPECTED_LANGUAGES if lang not in languages]
    assert not missing, f"Missing expected languages: {missing}"


# Property 2: Docstring Entry Schema Validity
@settings(max_examples=100)
@given(entry_idx=st.integers(min_value=0, max_value=24))
def test_property_2_docstring_entry_schema_validity(entry_idx: int) -> None:
    """Property 2: Docstring Entry Schema Validity.

    Feature: mrdr-data-population, Property 2: Docstring Entry Schema Validity
    For any entry in the docstring database, the entry SHALL contain non-null
    values for: language, syntax.start, syntax.type, syntax.location.
    **Validates: Requirements 1.2**
    """
    entries = get_entries()
    if entry_idx >= len(entries):
        entry_idx = entry_idx % len(entries)
    
    entry_data = entries[entry_idx]
    
    # Validate using Pydantic model
    entry = DocstringEntry(**entry_data)
    
    # Required fields must be non-null
    assert entry.language is not None, "language must not be null"
    assert entry.syntax.start is not None, "syntax.start must not be null"
    assert entry.syntax.type is not None, "syntax.type must not be null"
    assert entry.syntax.location is not None, "syntax.location must not be null"


# Property 3: Conflict Reference Consistency
@settings(max_examples=1)
@given(st.just(None))
def test_property_3_conflict_reference_consistency(_: None) -> None:
    """Property 3: Conflict Reference Consistency.

    Feature: mrdr-data-population, Property 3: Conflict Reference Consistency
    For any pair of languages in the docstring database with identical start
    delimiters AND different attachment locations, at least one entry SHALL
    have a conflict_ref field pointing to the other language.
    **Validates: Requirements 1.4**
    """
    entries = get_entries()
    
    # Build a map of (start delimiter, location) to languages
    # True conflicts are same delimiter with DIFFERENT locations
    delimiter_to_entries: dict[str, list[dict]] = {}
    for entry in entries:
        start = entry.get("syntax", {}).get("start")
        if start:
            if start not in delimiter_to_entries:
                delimiter_to_entries[start] = []
            delimiter_to_entries[start].append(entry)
    
    # Find true conflicts: same delimiter, different locations
    for delimiter, entries_with_delimiter in delimiter_to_entries.items():
        if len(entries_with_delimiter) < 2:
            continue
        
        # Group by location
        locations = {}
        for entry in entries_with_delimiter:
            loc = entry.get("syntax", {}).get("location")
            if loc not in locations:
                locations[loc] = []
            locations[loc].append(entry)
        
        # If all entries have the same location, no conflict
        if len(locations) <= 1:
            continue
        
        # True conflict: same delimiter, different locations
        # At least one entry should have conflict_ref
        all_languages = [e.get("language") for e in entries_with_delimiter]
        has_conflict_ref = False
        
        for entry in entries_with_delimiter:
            conflict_ref = entry.get("conflict_ref")
            if conflict_ref:
                # Check if it references another language with same delimiter
                for other_lang in all_languages:
                    if other_lang != entry.get("language") and other_lang in conflict_ref:
                        has_conflict_ref = True
                        break
            if has_conflict_ref:
                break
        
        assert has_conflict_ref, (
            f"Languages {all_languages} share delimiter '{delimiter}' with different "
            f"locations {list(locations.keys())} but none have conflict_ref"
        )


# Additional validation tests for all entries
def test_all_entries_validate_against_schema() -> None:
    """All database entries must validate against the Pydantic schema."""
    entries = get_entries()
    
    for i, entry_data in enumerate(entries):
        try:
            entry = DocstringEntry(**entry_data)
            assert entry.language, f"Entry {i} has empty language"
        except Exception as e:
            raise AssertionError(f"Entry {i} ({entry_data.get('language', 'unknown')}) failed validation: {e}")


def test_database_file_exists() -> None:
    """The docstring database file must exist."""
    assert DATABASE_PATH.exists(), f"Database file not found: {DATABASE_PATH}"


def test_database_is_valid_json() -> None:
    """The docstring database must be valid JSON."""
    try:
        load_database()
    except json.JSONDecodeError as e:
        raise AssertionError(f"Database is not valid JSON: {e}")
