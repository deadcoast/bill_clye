"""Property tests for conflict database population.

Feature: mrdr-data-population, Property 13
Validates: Requirements 6.5
"""

import json
from pathlib import Path

from hypothesis import given, settings
import hypothesis.strategies as st


# Path to the conflict database
DATABASE_PATH = Path("database/conflicts/conflict_database.json")

# Expected conflicts
EXPECTED_CONFLICTS = [
    "CONFLICT_TRIPLE_QUOTE",
    "CONFLICT_BLOCK_COMMENT",
    "SIMILARITY_LINE_DOC",
]


def load_database() -> dict:
    """Load the conflict database from JSON file."""
    with open(DATABASE_PATH) as f:
        return json.load(f)


def get_conflicts() -> list[dict]:
    """Get all conflict entries from the database."""
    return load_database().get("conflicts", [])


# Property 13: Conflict Entry Schema Validity
@settings(max_examples=100)
@given(entry_idx=st.integers(min_value=0, max_value=10))
def test_property_13_conflict_entry_schema_validity(entry_idx: int) -> None:
    """Property 13: Conflict Entry Schema Validity.

    Feature: mrdr-data-population, Property 13: Conflict Entry Schema Validity
    For any entry in the conflict database, the entry SHALL contain non-null
    values for: delimiter, languages (with at least 2 entries), resolution,
    attachment_rules.
    **Validates: Requirements 6.5**
    """
    conflicts = get_conflicts()
    if not conflicts:
        return  # Skip if database is empty
    
    entry_idx = entry_idx % len(conflicts)
    entry = conflicts[entry_idx]
    
    # Required fields must be non-null and non-empty
    assert entry.get("id"), f"Entry at index {entry_idx} has empty/null id"
    assert entry.get("delimiter"), f"Entry {entry.get('id')} has empty/null delimiter"
    assert entry.get("resolution"), f"Entry {entry.get('id')} has empty/null resolution"
    assert entry.get("attachment_rules"), f"Entry {entry.get('id')} has empty/null attachment_rules"
    
    # Languages must have at least 2 entries
    languages = entry.get("languages", [])
    assert isinstance(languages, list), f"Entry {entry.get('id')} languages is not a list"
    assert len(languages) >= 2, (
        f"Entry {entry.get('id')} has fewer than 2 languages: {languages}"
    )
    
    # attachment_rules must be a dict with entries for each language
    attachment_rules = entry.get("attachment_rules", {})
    assert isinstance(attachment_rules, dict), (
        f"Entry {entry.get('id')} attachment_rules is not a dict"
    )
    for lang in languages:
        assert lang in attachment_rules, (
            f"Entry {entry.get('id')} missing attachment_rule for language: {lang}"
        )


# Additional validation tests
def test_database_file_exists() -> None:
    """The conflict database file must exist."""
    assert DATABASE_PATH.exists(), f"Database file not found: {DATABASE_PATH}"


def test_database_is_valid_json() -> None:
    """The conflict database must be valid JSON."""
    try:
        load_database()
    except json.JSONDecodeError as e:
        raise AssertionError(f"Database is not valid JSON: {e}")


def test_database_has_manifest() -> None:
    """The conflict database must have a manifest."""
    db = load_database()
    assert "manifest" in db, "Database missing manifest"
    manifest = db["manifest"]
    assert manifest.get("manifest_name") == "conflict_database"
    assert manifest.get("version")
    assert manifest.get("schema_origin")


def test_all_entries_have_unique_ids() -> None:
    """All conflict entries must have unique IDs."""
    conflicts = get_conflicts()
    ids = [c.get("id") for c in conflicts]
    duplicates = [cid for cid in ids if ids.count(cid) > 1]
    assert not duplicates, f"Duplicate conflict IDs found: {set(duplicates)}"


def test_expected_conflicts_present() -> None:
    """All expected conflicts must be present in the database."""
    conflicts = get_conflicts()
    conflict_ids = [c.get("id") for c in conflicts]
    
    missing = [cid for cid in EXPECTED_CONFLICTS if cid not in conflict_ids]
    assert not missing, f"Missing expected conflicts: {missing}"


def test_python_julia_conflict_exists() -> None:
    """Python vs Julia triple-quote conflict must exist with correct rules."""
    conflicts = get_conflicts()
    triple_quote = next(
        (c for c in conflicts if c.get("id") == "CONFLICT_TRIPLE_QUOTE"),
        None
    )
    
    assert triple_quote is not None, "CONFLICT_TRIPLE_QUOTE not found"
    assert "Python" in triple_quote.get("languages", [])
    assert "Julia" in triple_quote.get("languages", [])
    
    rules = triple_quote.get("attachment_rules", {})
    assert rules.get("Python") == "internal_first_line"
    assert rules.get("Julia") == "above_target"


def test_javascript_d_conflict_exists() -> None:
    """JavaScript vs D block comment conflict must exist."""
    conflicts = get_conflicts()
    block_comment = next(
        (c for c in conflicts if c.get("id") == "CONFLICT_BLOCK_COMMENT"),
        None
    )
    
    assert block_comment is not None, "CONFLICT_BLOCK_COMMENT not found"
    assert "JavaScript" in block_comment.get("languages", [])
    assert "D" in block_comment.get("languages", [])


def test_rust_zig_similarity_exists() -> None:
    """Rust vs Zig line doc similarity must exist."""
    conflicts = get_conflicts()
    line_doc = next(
        (c for c in conflicts if c.get("id") == "SIMILARITY_LINE_DOC"),
        None
    )
    
    assert line_doc is not None, "SIMILARITY_LINE_DOC not found"
    assert "Rust" in line_doc.get("languages", [])
    assert "Zig" in line_doc.get("languages", [])
    
    rules = line_doc.get("attachment_rules", {})
    assert rules.get("Rust") == "above_target"
    assert rules.get("Zig") == "above_target"
