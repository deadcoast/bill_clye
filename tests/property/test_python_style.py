"""Property tests for Python styles database population.

Feature: mrdr-data-population, Properties 9, 10
Validates: Requirements 4.2, 4.3, 4.4, 4.5, 4.6, 4.7
"""

import json
from pathlib import Path

from hypothesis import given, settings
import hypothesis.strategies as st


# Path to the Python styles database
DATABASE_PATH = Path("database/languages/python/python_styles.json")

# Expected style names
EXPECTED_STYLES = ["sphinx", "google", "numpy", "epytext", "pep257"]

# Expected markers per style (partial matches for syntax field)
EXPECTED_MARKERS = {
    "sphinx": [":param", ":type", ":return", ":rtype"],
    "google": ["Args:", "Returns:"],
    "numpy": ["Parameters", "Returns"],  # With dashed separators
    "epytext": ["@param", "@type", "@return"],
    "pep257": [],  # Minimal style, no specific markers
}


def load_database() -> dict:
    """Load the Python styles database from JSON file."""
    with open(DATABASE_PATH) as f:
        return json.load(f)


def get_styles() -> list[dict]:
    """Get all style entries from the database."""
    return load_database().get("styles", [])


def get_style_by_name(name: str) -> dict | None:
    """Get a style entry by name."""
    styles = get_styles()
    for style in styles:
        if style.get("name") == name:
            return style
    return None


# Property 9: Python Style Completeness
@settings(max_examples=1)
@given(st.just(None))
def test_property_9_python_style_completeness(_: None) -> None:
    """Property 9: Python Style Completeness.

    Feature: mrdr-data-population, Property 9: Python Style Completeness
    For any valid Python styles database, the database SHALL contain all five
    styles (sphinx, google, numpy, epytext, pep257) with their characteristic
    markers: sphinx (:param:, :type:, :return:, :rtype:), google (Args:, Returns:),
    numpy (Parameters, Returns with dashes), epytext (@param, @type, @return).
    **Validates: Requirements 4.2, 4.3, 4.4, 4.5, 4.6**
    """
    styles = get_styles()
    style_names = [s.get("name") for s in styles]
    
    # Check all expected styles are present
    missing_styles = [name for name in EXPECTED_STYLES if name not in style_names]
    assert not missing_styles, f"Missing styles: {missing_styles}"
    
    # Check sphinx markers
    sphinx = get_style_by_name("sphinx")
    assert sphinx is not None, "Sphinx style not found"
    sphinx_marker_syntaxes = [m.get("syntax", "") for m in sphinx.get("markers", [])]
    for marker in EXPECTED_MARKERS["sphinx"]:
        assert any(marker in syntax for syntax in sphinx_marker_syntaxes), (
            f"Sphinx style missing marker containing '{marker}'"
        )
    
    # Check google markers
    google = get_style_by_name("google")
    assert google is not None, "Google style not found"
    google_marker_syntaxes = [m.get("syntax", "") for m in google.get("markers", [])]
    for marker in EXPECTED_MARKERS["google"]:
        assert any(marker in syntax for syntax in google_marker_syntaxes), (
            f"Google style missing marker containing '{marker}'"
        )
    
    # Check numpy markers (with dashed separators)
    numpy = get_style_by_name("numpy")
    assert numpy is not None, "NumPy style not found"
    numpy_marker_syntaxes = [m.get("syntax", "") for m in numpy.get("markers", [])]
    for marker in EXPECTED_MARKERS["numpy"]:
        assert any(marker in syntax for syntax in numpy_marker_syntaxes), (
            f"NumPy style missing marker containing '{marker}'"
        )
    # NumPy should have dashed separators
    assert any("---" in syntax for syntax in numpy_marker_syntaxes), (
        "NumPy style missing dashed separators"
    )
    
    # Check epytext markers
    epytext = get_style_by_name("epytext")
    assert epytext is not None, "Epytext style not found"
    epytext_marker_syntaxes = [m.get("syntax", "") for m in epytext.get("markers", [])]
    for marker in EXPECTED_MARKERS["epytext"]:
        assert any(marker in syntax for syntax in epytext_marker_syntaxes), (
            f"Epytext style missing marker containing '{marker}'"
        )
    
    # Check pep257 exists (minimal style)
    pep257 = get_style_by_name("pep257")
    assert pep257 is not None, "PEP 257 style not found"


# Property 10: Python Style Entry Schema Validity
@settings(max_examples=100)
@given(entry_idx=st.integers(min_value=0, max_value=4))
def test_property_10_python_style_entry_schema_validity(entry_idx: int) -> None:
    """Property 10: Python Style Entry Schema Validity.

    Feature: mrdr-data-population, Property 10: Python Style Entry Schema Validity
    For any entry in the Python styles database, the entry SHALL contain non-null
    values for: name, description, markers, template_code, rules.
    **Validates: Requirements 4.7**
    """
    styles = get_styles()
    if not styles:
        return  # Skip if database is empty
    
    entry_idx = entry_idx % len(styles)
    entry = styles[entry_idx]
    
    # Required fields must be non-null and non-empty
    assert entry.get("name"), f"Entry at index {entry_idx} has empty/null name"
    assert entry.get("description"), f"Entry {entry.get('name')} has empty/null description"
    assert "markers" in entry, f"Entry {entry.get('name')} missing markers field"
    assert isinstance(entry.get("markers"), list), (
        f"Entry {entry.get('name')} markers is not a list"
    )
    assert entry.get("template_code"), f"Entry {entry.get('name')} has empty/null template_code"
    assert "rules" in entry, f"Entry {entry.get('name')} missing rules field"
    assert isinstance(entry.get("rules"), list), (
        f"Entry {entry.get('name')} rules is not a list"
    )
    assert len(entry.get("rules", [])) > 0, (
        f"Entry {entry.get('name')} has empty rules list"
    )


# Additional validation tests
def test_database_file_exists() -> None:
    """The Python styles database file must exist."""
    assert DATABASE_PATH.exists(), f"Database file not found: {DATABASE_PATH}"


def test_database_is_valid_json() -> None:
    """The Python styles database must be valid JSON."""
    try:
        load_database()
    except json.JSONDecodeError as e:
        raise AssertionError(f"Database is not valid JSON: {e}")


def test_database_has_manifest() -> None:
    """The Python styles database must have a manifest."""
    db = load_database()
    assert "manifest" in db, "Database missing manifest"
    manifest = db["manifest"]
    assert manifest.get("manifest_name") == "python_styles_database"
    assert manifest.get("version")
    assert manifest.get("schema_origin")


def test_all_entries_have_unique_names() -> None:
    """All style entries must have unique names."""
    styles = get_styles()
    names = [s.get("name") for s in styles]
    duplicates = [name for name in names if names.count(name) > 1]
    assert not duplicates, f"Duplicate style names found: {set(duplicates)}"


def test_marker_entries_have_required_fields() -> None:
    """All marker entries must have name, syntax, and description."""
    styles = get_styles()
    for style in styles:
        style_name = style.get("name", "unknown")
        for marker in style.get("markers", []):
            assert marker.get("name"), (
                f"Style {style_name} has marker with empty/null name"
            )
            assert marker.get("syntax"), (
                f"Style {style_name} marker {marker.get('name')} has empty/null syntax"
            )
            assert marker.get("description"), (
                f"Style {style_name} marker {marker.get('name')} has empty/null description"
            )


def test_template_code_contains_docstring() -> None:
    """All template_code entries must contain triple-quoted docstrings."""
    styles = get_styles()
    for style in styles:
        style_name = style.get("name", "unknown")
        template = style.get("template_code", "")
        assert '"""' in template, (
            f"Style {style_name} template_code missing triple-quoted docstring"
        )
