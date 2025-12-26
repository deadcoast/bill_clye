"""Property tests for dictionary database population.

Feature: mrdr-data-population, Properties 6, 7, 8
Validates: Requirements 3.2, 3.3, 3.4, 3.5, 3.6, 3.7
"""

import json
from pathlib import Path

from hypothesis import given, settings
import hypothesis.strategies as st


# Path to the dictionary database
DATABASE_PATH = Path("database/dictionary/dictionary_database.json")

# Expected grandparent terms from dictionary.md
EXPECTED_GRANDPARENTS = [
    "NOTE", "CLAIM", "LANG_USE", "FORMAT", "PURPOSE",
    "RESTRICTIONS", "STYLING", "USER", "NOTES"
]

# Expected parent terms from dictionary.md
EXPECTED_PARENTS = ["ASPERDEFINED", "OBJECTIVEACCEPTANCE"]

# Expected child terms from dictionary.md
EXPECTED_CHILDREN = [
    "SEMANTICS", "DEFINITION", "DOCSTRING", "RESEARCH", "STATISTIC",
    "EXAMPLE", "VALIDATED", "EXPERIMENTAL", "OPTIMAL", "UNSTABLE",
    "VISUALLY_APPEALING", "CREATIVE"
]

# Expected grandchild terms from dictionary.md
EXPECTED_GRANDCHILDREN = ["VALUE"]

# Expected NAMETYPE definitions
EXPECTED_NAMETYPES = ["CHILD", "PARENT", "GRANDPARENT"]

# Valid hierarchy levels
VALID_LEVELS = ["nametype", "grandparent", "parent", "child", "grandchild"]


def load_database() -> dict:
    """Load the dictionary database from JSON file."""
    with open(DATABASE_PATH) as f:
        return json.load(f)


def get_all_entries() -> list[dict]:
    """Get all entries from all hierarchy levels."""
    db = load_database()
    entries = []
    for key in ["nametypes", "grandparents", "parents", "children", "grandchildren"]:
        entries.extend(db.get(key, []))
    return entries


# Property 6: Dictionary Hierarchy Completeness
@settings(max_examples=1)
@given(st.just(None))
def test_property_6_dictionary_hierarchy_completeness(_: None) -> None:
    """Property 6: Dictionary Hierarchy Completeness.

    Feature: mrdr-data-population, Property 6: Dictionary Hierarchy Completeness
    For any valid dictionary database, the database SHALL contain all defined
    terms at each level: grandparents (NOTE, CLAIM, LANG_USE, FORMAT, PURPOSE,
    RESTRICTIONS, STYLING, USER, NOTES), parents (apd, objacc), children
    (sem, def, dstr, rsch, stat, eg, vldt, expr, optml, unstbl, vislap, crtv),
    grandchildren (val, value).
    **Validates: Requirements 3.2, 3.3, 3.4, 3.5**
    """
    db = load_database()
    
    # Check grandparents
    grandparent_names = [e.get("name") for e in db.get("grandparents", [])]
    missing_grandparents = [n for n in EXPECTED_GRANDPARENTS if n not in grandparent_names]
    assert not missing_grandparents, f"Missing grandparent terms: {missing_grandparents}"
    
    # Check parents
    parent_names = [e.get("name") for e in db.get("parents", [])]
    missing_parents = [n for n in EXPECTED_PARENTS if n not in parent_names]
    assert not missing_parents, f"Missing parent terms: {missing_parents}"
    
    # Check children
    child_names = [e.get("name") for e in db.get("children", [])]
    missing_children = [n for n in EXPECTED_CHILDREN if n not in child_names]
    assert not missing_children, f"Missing child terms: {missing_children}"
    
    # Check grandchildren
    grandchild_names = [e.get("name") for e in db.get("grandchildren", [])]
    missing_grandchildren = [n for n in EXPECTED_GRANDCHILDREN if n not in grandchild_names]
    assert not missing_grandchildren, f"Missing grandchild terms: {missing_grandchildren}"


# Property 7: Dictionary Entry Schema Validity
@settings(max_examples=100)
@given(entry_idx=st.integers(min_value=0, max_value=26))
def test_property_7_dictionary_entry_schema_validity(entry_idx: int) -> None:
    """Property 7: Dictionary Entry Schema Validity.

    Feature: mrdr-data-population, Property 7: Dictionary Entry Schema Validity
    For any entry in the dictionary database, the entry SHALL contain non-null
    values for: name, alias, level, description.
    **Validates: Requirements 3.6**
    """
    entries = get_all_entries()
    if not entries:
        return  # Skip if database is empty
    
    entry_idx = entry_idx % len(entries)
    entry = entries[entry_idx]
    
    # Required fields must be non-null and non-empty
    assert entry.get("name"), f"Entry at index {entry_idx} has empty/null name"
    assert entry.get("alias"), f"Entry {entry.get('name')} has empty/null alias"
    assert entry.get("level"), f"Entry {entry.get('name')} has empty/null level"
    assert entry.get("description"), f"Entry {entry.get('name')} has empty/null description"
    
    # Level must be valid
    assert entry.get("level") in VALID_LEVELS, (
        f"Entry {entry.get('name')} has invalid level: {entry.get('level')}"
    )


# Property 8: Dictionary NAMETYPE Definitions
@settings(max_examples=1)
@given(st.just(None))
def test_property_8_dictionary_nametype_definitions(_: None) -> None:
    """Property 8: Dictionary NAMETYPE Definitions.

    Feature: mrdr-data-population, Property 8: Dictionary NAMETYPE Definitions
    For any valid dictionary database, the database SHALL contain NAMETYPE
    entries for CHD (CHILD), PNT (PARENT), GPN (GRANDPARENT) with correct
    hierarchical relationships.
    **Validates: Requirements 3.7**
    """
    db = load_database()
    nametypes = db.get("nametypes", [])
    
    # Check all expected nametypes exist
    nametype_names = [e.get("name") for e in nametypes]
    missing_nametypes = [n for n in EXPECTED_NAMETYPES if n not in nametype_names]
    assert not missing_nametypes, f"Missing NAMETYPE definitions: {missing_nametypes}"
    
    # Check aliases
    nametype_aliases = {e.get("name"): e.get("alias") for e in nametypes}
    assert nametype_aliases.get("CHILD") == "chd", "CHILD should have alias 'chd'"
    assert nametype_aliases.get("PARENT") == "pnt", "PARENT should have alias 'pnt'"
    assert nametype_aliases.get("GRANDPARENT") == "gpn", "GRANDPARENT should have alias 'gpn'"
    
    # Check hierarchical relationships
    nametype_children = {e.get("name"): e.get("children", []) for e in nametypes}
    assert "CHILD" in nametype_children.get("PARENT", []), (
        "PARENT should have CHILD in its children"
    )
    assert "PARENT" in nametype_children.get("GRANDPARENT", []), (
        "GRANDPARENT should have PARENT in its children"
    )


# Additional validation tests
def test_database_file_exists() -> None:
    """The dictionary database file must exist."""
    assert DATABASE_PATH.exists(), f"Database file not found: {DATABASE_PATH}"


def test_database_is_valid_json() -> None:
    """The dictionary database must be valid JSON."""
    try:
        load_database()
    except json.JSONDecodeError as e:
        raise AssertionError(f"Database is not valid JSON: {e}")


def test_database_has_manifest() -> None:
    """The dictionary database must have a manifest."""
    db = load_database()
    assert "manifest" in db, "Database missing manifest"
    manifest = db["manifest"]
    assert manifest.get("manifest_name") == "dictionary_database"
    assert manifest.get("version")
    assert manifest.get("schema_origin")


def test_all_entries_have_unique_names() -> None:
    """All dictionary entries must have unique names."""
    entries = get_all_entries()
    names = [e.get("name") for e in entries]
    duplicates = [n for n in names if names.count(n) > 1]
    assert not duplicates, f"Duplicate entry names found: {set(duplicates)}"


def test_level_matches_section() -> None:
    """Each entry's level must match its section in the database."""
    db = load_database()
    
    for entry in db.get("nametypes", []):
        assert entry.get("level") == "nametype", (
            f"Entry {entry.get('name')} in nametypes has level '{entry.get('level')}'"
        )
    
    for entry in db.get("grandparents", []):
        assert entry.get("level") == "grandparent", (
            f"Entry {entry.get('name')} in grandparents has level '{entry.get('level')}'"
        )
    
    for entry in db.get("parents", []):
        assert entry.get("level") == "parent", (
            f"Entry {entry.get('name')} in parents has level '{entry.get('level')}'"
        )
    
    for entry in db.get("children", []):
        assert entry.get("level") == "child", (
            f"Entry {entry.get('name')} in children has level '{entry.get('level')}'"
        )
    
    for entry in db.get("grandchildren", []):
        assert entry.get("level") == "grandchild", (
            f"Entry {entry.get('name')} in grandchildren has level '{entry.get('level')}'"
        )
