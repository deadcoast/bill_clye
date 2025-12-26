"""Property tests for doctag database population.

Feature: mrdr-data-population, Properties 4, 5, 16
Validates: Requirements 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 9.1
"""

import json
import re
from pathlib import Path

from hypothesis import given, settings
import hypothesis.strategies as st


# Path to the doctag database
DATABASE_PATH = Path("database/doctags/doctag_database.json")

# Expected tag IDs per category
EXPECTED_DDL_IDS = [f"DDL{i:02d}" for i in range(1, 11)]  # DDL01-DDL10
EXPECTED_GRM_IDS = ["GRM01", "GRM02", "GRM05", "GRM06", "GRM07", "GRM08", "GRM09", "GRM10"]  # GRM03, GRM04 missing in source
EXPECTED_IDC_IDS = [f"IDC{i:02d}" for i in range(1, 11)]  # IDC01-IDC10
EXPECTED_FMT_IDS = [f"FMT{i:02d}" for i in range(1, 11)]  # FMT01-FMT10
EXPECTED_DOC_IDS = [f"DOC{i:02d}" for i in range(1, 6)]   # DOC01-DOC05

# All expected IDs
ALL_EXPECTED_IDS = EXPECTED_DDL_IDS + EXPECTED_GRM_IDS + EXPECTED_IDC_IDS + EXPECTED_FMT_IDS + EXPECTED_DOC_IDS

# Valid categories
VALID_CATEGORIES = ["DDL", "GRM", "IDC", "FMT", "DOC"]

# SCREAMINGSNAKE pattern: uppercase letters, digits, underscores
SCREAMINGSNAKE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")


def load_database() -> dict:
    """Load the doctag database from JSON file."""
    with open(DATABASE_PATH) as f:
        return json.load(f)


def get_doctags() -> list[dict]:
    """Get all doctag entries from the database."""
    return load_database().get("doctags", [])


# Property 4: Doctag Category Completeness
@settings(max_examples=1)
@given(st.just(None))
def test_property_4_doctag_category_completeness(_: None) -> None:
    """Property 4: Doctag Category Completeness.

    Feature: mrdr-data-population, Property 4: Doctag Category Completeness
    For any doctag category (DDL, GRM, IDC, FMT, DOC), the doctag database
    SHALL contain all expected tag IDs: DDL01-DDL10, GRM01-GRM10 (excluding
    GRM03, GRM04 which are not defined in source), IDC01-IDC10, FMT01-FMT10,
    DOC01-DOC05.
    **Validates: Requirements 2.2, 2.3, 2.4, 2.5, 2.6**
    """
    doctags = get_doctags()
    tag_ids = [tag.get("id") for tag in doctags]
    
    # Check DDL tags
    missing_ddl = [tid for tid in EXPECTED_DDL_IDS if tid not in tag_ids]
    assert not missing_ddl, f"Missing DDL tags: {missing_ddl}"
    
    # Check GRM tags (note: GRM03, GRM04 are not defined in doctags.md)
    missing_grm = [tid for tid in EXPECTED_GRM_IDS if tid not in tag_ids]
    assert not missing_grm, f"Missing GRM tags: {missing_grm}"
    
    # Check IDC tags
    missing_idc = [tid for tid in EXPECTED_IDC_IDS if tid not in tag_ids]
    assert not missing_idc, f"Missing IDC tags: {missing_idc}"
    
    # Check FMT tags
    missing_fmt = [tid for tid in EXPECTED_FMT_IDS if tid not in tag_ids]
    assert not missing_fmt, f"Missing FMT tags: {missing_fmt}"
    
    # Check DOC tags
    missing_doc = [tid for tid in EXPECTED_DOC_IDS if tid not in tag_ids]
    assert not missing_doc, f"Missing DOC tags: {missing_doc}"


# Property 5: Doctag Entry Schema Validity
@settings(max_examples=100)
@given(entry_idx=st.integers(min_value=0, max_value=42))
def test_property_5_doctag_entry_schema_validity(entry_idx: int) -> None:
    """Property 5: Doctag Entry Schema Validity.

    Feature: mrdr-data-population, Property 5: Doctag Entry Schema Validity
    For any entry in the doctag database, the entry SHALL contain non-null
    values for: id, symbol, short_name, description, category.
    **Validates: Requirements 2.7**
    """
    doctags = get_doctags()
    if not doctags:
        return  # Skip if database is empty
    
    entry_idx = entry_idx % len(doctags)
    entry = doctags[entry_idx]
    
    # Required fields must be non-null and non-empty
    assert entry.get("id"), f"Entry at index {entry_idx} has empty/null id"
    assert entry.get("symbol") is not None, f"Entry {entry.get('id')} has null symbol"
    assert entry.get("short_name"), f"Entry {entry.get('id')} has empty/null short_name"
    assert entry.get("description"), f"Entry {entry.get('id')} has empty/null description"
    assert entry.get("category"), f"Entry {entry.get('id')} has empty/null category"
    
    # Category must be valid
    assert entry.get("category") in VALID_CATEGORIES, (
        f"Entry {entry.get('id')} has invalid category: {entry.get('category')}"
    )
    
    # ID must match pattern (e.g., DDL01, GRM05)
    tag_id = entry.get("id")
    assert re.match(r"^(DDL|GRM|IDC|FMT|DOC)\d{2}$", tag_id), (
        f"Entry has invalid ID format: {tag_id}"
    )


# Property 16: SCREAMINGSNAKE Case Compliance
@settings(max_examples=100)
@given(entry_idx=st.integers(min_value=0, max_value=42))
def test_property_16_screamingsnake_case_compliance(entry_idx: int) -> None:
    """Property 16: SCREAMINGSNAKE Case Compliance.

    Feature: mrdr-data-population, Property 16: SCREAMINGSNAKE Case Compliance
    For any tag identifier in the doctag database, the short_name SHALL match
    the pattern ^[A-Z][A-Z0-9_]* (SCREAMINGSNAKE case).
    **Validates: Requirements 9.1**
    """
    doctags = get_doctags()
    if not doctags:
        return  # Skip if database is empty
    
    entry_idx = entry_idx % len(doctags)
    entry = doctags[entry_idx]
    
    short_name = entry.get("short_name", "")
    
    # short_name must be SCREAMINGSNAKE case
    assert SCREAMINGSNAKE_PATTERN.match(short_name), (
        f"Entry {entry.get('id')} short_name '{short_name}' is not SCREAMINGSNAKE case"
    )


# Additional validation tests
def test_database_file_exists() -> None:
    """The doctag database file must exist."""
    assert DATABASE_PATH.exists(), f"Database file not found: {DATABASE_PATH}"


def test_database_is_valid_json() -> None:
    """The doctag database must be valid JSON."""
    try:
        load_database()
    except json.JSONDecodeError as e:
        raise AssertionError(f"Database is not valid JSON: {e}")


def test_database_has_manifest() -> None:
    """The doctag database must have a manifest."""
    db = load_database()
    assert "manifest" in db, "Database missing manifest"
    manifest = db["manifest"]
    assert manifest.get("manifest_name") == "doctag_database"
    assert manifest.get("version")
    assert manifest.get("schema_origin")


def test_all_entries_have_unique_ids() -> None:
    """All doctag entries must have unique IDs."""
    doctags = get_doctags()
    ids = [tag.get("id") for tag in doctags]
    duplicates = [tid for tid in ids if ids.count(tid) > 1]
    assert not duplicates, f"Duplicate tag IDs found: {set(duplicates)}"


def test_category_matches_id_prefix() -> None:
    """Each entry's category must match its ID prefix."""
    doctags = get_doctags()
    for tag in doctags:
        tag_id = tag.get("id", "")
        category = tag.get("category", "")
        expected_prefix = tag_id[:3]
        assert category == expected_prefix, (
            f"Tag {tag_id} has category '{category}' but ID prefix is '{expected_prefix}'"
        )
