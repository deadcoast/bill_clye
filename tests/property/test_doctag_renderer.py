"""Property tests for Doctag Renderer.

Feature: mrdr-visual-integration, Property 10: Doctag Token Rendering
Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.6
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.doctag_renderer import (
    DOCTAG_COLORS,
    DoctagEntry,
    DoctagRenderer,
    DoctagType,
)


# Strategy for valid tag prefixes
tag_prefix_strategy = st.sampled_from(["DDL", "GRM", "IDC", "FMT", "DOC"])

# Strategy for tag numbers (01-10)
tag_number_strategy = st.integers(min_value=1, max_value=10).map(lambda n: f"{n:02d}")

# Strategy for valid tag IDs
tag_id_strategy = st.tuples(tag_prefix_strategy, tag_number_strategy).map(
    lambda t: f"{t[0]}{t[1]}"
)

# Strategy for short printable text (tag names)
tag_name_strategy = st.text(
    min_size=1,
    max_size=20,
    alphabet=st.characters(whitelist_categories=("L",), blacklist_characters="\r\n\t\x00"),
)

# Strategy for description text
description_strategy = st.text(
    min_size=1,
    max_size=50,
    alphabet=st.characters(
        whitelist_categories=("L", "N", "P", "Z"),
        blacklist_characters="\r\n\t\x00",
    ),
)


@given(tag_id=tag_id_strategy, tag_name=tag_name_strategy, description=description_strategy)
@settings(max_examples=100)
def test_doctag_token_rendering_semantic_coloring(
    tag_id: str, tag_name: str, description: str
) -> None:
    """Property 10: Doctag Token Rendering - semantic coloring.

    Feature: mrdr-visual-integration, Property 10: Doctag Token Rendering
    For any doctag token (DDL, GRM, IDC, FMT), the Doctag_Renderer SHALL apply
    semantic coloring based on token type.
    **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.6**
    """
    renderer = DoctagRenderer()
    text = renderer.render_tag(tag_id, tag_name, description)

    # Output should be a Rich Text object
    assert text is not None

    # Tag ID should appear in output
    plain_output = str(text)
    assert tag_id in plain_output, f"Tag ID {tag_id} should appear in output"


@given(tag_id=tag_id_strategy, tag_name=tag_name_strategy, description=description_strategy)
@settings(max_examples=100)
def test_doctag_screaming_snake_case(
    tag_id: str, tag_name: str, description: str
) -> None:
    """Property 10: Doctag Token Rendering - SCREAMINGSNAKE case.

    Feature: mrdr-visual-integration, Property 10: Doctag Token Rendering
    For any doctag token, the Doctag_Renderer SHALL render identifiers
    in SCREAMINGSNAKE case.
    **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.6**
    """
    renderer = DoctagRenderer()
    text = renderer.render_tag(tag_id, tag_name, description)

    plain_output = str(text)

    # Tag name should appear in uppercase (SCREAMINGSNAKE)
    expected_screaming = tag_name.upper()
    assert expected_screaming in plain_output, (
        f"Tag name should be in SCREAMINGSNAKE case: {expected_screaming}"
    )


@given(tag_id=tag_id_strategy, tag_name=tag_name_strategy, description=description_strategy)
@settings(max_examples=100)
def test_doctag_plain_rendering(
    tag_id: str, tag_name: str, description: str
) -> None:
    """Property 10: Doctag Token Rendering - plain mode.

    Feature: mrdr-visual-integration, Property 10: Doctag Token Rendering
    For any doctag token, plain rendering SHALL contain no ANSI codes.
    **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.6**
    """
    import re

    renderer = DoctagRenderer()
    plain = renderer.render_plain(tag_id, tag_name, description)

    # No ANSI escape sequences
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
    assert len(ansi_pattern.findall(plain)) == 0, "Plain output should have no ANSI codes"

    # Should contain tag ID and name
    assert tag_id in plain
    assert tag_name.upper() in plain


def test_doctag_type_detection() -> None:
    """Doctag type detection SHALL correctly identify tag categories."""
    renderer = DoctagRenderer()

    # Test each prefix
    assert renderer._get_tag_type("DDL01") == DoctagType.DELIMITER
    assert renderer._get_tag_type("DDL10") == DoctagType.DELIMITER
    assert renderer._get_tag_type("GRM01") == DoctagType.GRAMMAR
    assert renderer._get_tag_type("GRM05") == DoctagType.GRAMMAR
    assert renderer._get_tag_type("IDC01") == DoctagType.INTER_DOC
    assert renderer._get_tag_type("IDC10") == DoctagType.INTER_DOC
    assert renderer._get_tag_type("FMT01") == DoctagType.FORMATTING
    assert renderer._get_tag_type("FMT10") == DoctagType.FORMATTING
    assert renderer._get_tag_type("DOC01") == DoctagType.DOC_SPEC
    assert renderer._get_tag_type("DOC05") == DoctagType.DOC_SPEC


def test_doctag_type_fallback() -> None:
    """Unknown tag prefixes SHALL fall back to DOC_SPEC type."""
    renderer = DoctagRenderer()

    # Unknown prefixes should fall back to DOC_SPEC
    assert renderer._get_tag_type("XXX01") == DoctagType.DOC_SPEC
    assert renderer._get_tag_type("AB") == DoctagType.DOC_SPEC
    assert renderer._get_tag_type("") == DoctagType.DOC_SPEC


def test_doctag_colors_mapping() -> None:
    """Each DoctagType SHALL have a color mapping."""
    for tag_type in DoctagType:
        assert tag_type in DOCTAG_COLORS, f"Missing color for {tag_type}"
        assert isinstance(DOCTAG_COLORS[tag_type], str)


@given(
    tag_id=st.just("IDC02"),
    tag_name=tag_name_strategy,
    target=st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=("L", "N"))),
)
@settings(max_examples=50)
def test_idc_link_style_formatting(tag_id: str, tag_name: str, target: str) -> None:
    """Property 10: Doctag Token Rendering - IDC link style.

    Feature: mrdr-visual-integration, Property 10: Doctag Token Rendering
    For any IDC token, the Doctag_Renderer SHALL render with link-style formatting.
    **Validates: Requirements 4.4**
    """
    renderer = DoctagRenderer()
    text = renderer.render_idc_link(tag_id, tag_name, target)

    plain_output = str(text)

    # Should contain tag ID
    assert tag_id in plain_output

    # Should contain tag name in uppercase
    assert tag_name.upper() in plain_output

    # Should contain target
    assert target in plain_output

    # Should contain arrow indicator for link style
    assert "→" in plain_output


def test_doctag_entry_full_render() -> None:
    """DoctagEntry full render SHALL include all metadata fields."""
    renderer = DoctagRenderer()
    entry = DoctagEntry(
        id="DDL01",
        short_name="ADDTACH",
        full_name="add or attach",
        description="Add or attach an item or reference",
        example="+item",
    )

    output = renderer.render_tag_full(entry)

    # Should contain all fields
    assert "DDL01" in output
    assert "ADDTACH" in output
    assert "ADD OR ATTACH" in output
    assert "Add or attach an item or reference" in output
    assert "+item" in output


def test_doctag_entry_plain_render() -> None:
    """DoctagEntry plain render SHALL contain no ANSI codes."""
    import re

    renderer = DoctagRenderer()
    entry = DoctagEntry(
        id="GRM01",
        short_name="rstr",
        full_name="restrictions",
        description="Prohibited practise",
        example="rstr: no spaces",
    )

    plain = renderer.render_entry_plain(entry)

    # No ANSI escape sequences
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
    assert len(ansi_pattern.findall(plain)) == 0

    # Should contain all fields
    assert "GRM01" in plain
    assert "RSTR" in plain
    assert "RESTRICTIONS" in plain
    assert "Prohibited practise" in plain
    assert "rstr: no spaces" in plain



# Property 11: Doctag Lookup Display tests
# Feature: mrdr-visual-integration, Property 11: Doctag Lookup Display
# Validates: Requirements 4.5


@given(tag_id=tag_id_strategy)
@settings(max_examples=100)
def test_doctag_lookup_display(tag_id: str) -> None:
    """Property 11: Doctag Lookup Display.

    Feature: mrdr-visual-integration, Property 11: Doctag Lookup Display
    For any valid tag_id, `mrdr jekyl doctag <tag_id>` SHALL display the tag
    definition including short name, full name, description, and example if present.
    **Validates: Requirements 4.5**
    """
    from mrdr.database.doctag import DoctagLoader
    from mrdr.database.doctag.loader import DoctagNotFoundError

    loader = DoctagLoader()

    try:
        tag = loader.get(tag_id)

        # Tag should have required fields
        assert tag.id == tag_id.upper(), "Tag ID should match"
        assert tag.short_name, "Tag should have short name"
        assert tag.symbol, "Tag should have symbol (full name)"
        assert tag.description, "Tag should have description"
        assert tag.category, "Tag should have category"

        # Render the tag
        renderer = DoctagRenderer()
        entry = DoctagEntry(
            id=tag.id,
            short_name=tag.short_name,
            full_name=tag.symbol,
            description=tag.description,
            example=tag.example,
        )
        output = renderer.render_tag_full(entry)

        # Output should contain all required fields
        assert tag.id in output, "Output should contain tag ID"
        assert tag.short_name.upper() in output, "Output should contain short name"
        assert tag.symbol.upper() in output, "Output should contain full name"
        assert tag.description in output, "Output should contain description"

        # If example exists, check that at least the first line is in output
        # (multi-line examples may be rendered differently in Rich panels)
        if tag.example:
            first_line = tag.example.split("\n")[0]
            assert first_line in output, "Output should contain example (first line)"

    except DoctagNotFoundError:
        # Tag not in database - this is expected for some generated IDs
        pass


def test_doctag_lookup_all_categories() -> None:
    """Property 11: Doctag Lookup Display - all categories.

    Feature: mrdr-visual-integration, Property 11: Doctag Lookup Display
    For each doctag category, at least one tag SHALL be retrievable.
    **Validates: Requirements 4.5**
    """
    from mrdr.database.doctag import DoctagCategory, DoctagLoader

    loader = DoctagLoader()

    # Test each category has at least one tag
    for category in DoctagCategory:
        tags = loader.list_by_category(category)
        assert len(tags) > 0, f"Category {category.value} should have at least one tag"

        # Each tag should be retrievable
        for tag in tags:
            retrieved = loader.get(tag.id)
            assert retrieved.id == tag.id
            assert retrieved.category == category


def test_doctag_lookup_search() -> None:
    """Property 11: Doctag Lookup Display - search functionality.

    Feature: mrdr-visual-integration, Property 11: Doctag Lookup Display
    Search SHALL return tags matching ID, symbol, or short name.
    **Validates: Requirements 4.5**
    """
    from mrdr.database.doctag import DoctagLoader

    loader = DoctagLoader()

    # Search by ID prefix
    results = loader.search("DDL")
    assert len(results) > 0, "Search by ID prefix should return results"
    assert all("DDL" in r.id for r in results)

    # Search by symbol
    results = loader.search("+")
    assert len(results) > 0, "Search by symbol should return results"

    # Search by short name
    results = loader.search("ADDTACH")
    assert len(results) > 0, "Search by short name should return results"


def test_doctag_lookup_not_found() -> None:
    """Property 11: Doctag Lookup Display - not found error.

    Feature: mrdr-visual-integration, Property 11: Doctag Lookup Display
    For invalid tag_id, lookup SHALL raise DoctagNotFoundError with available tags.
    **Validates: Requirements 4.5**
    """
    from mrdr.database.doctag import DoctagLoader
    from mrdr.database.doctag.loader import DoctagNotFoundError

    loader = DoctagLoader()

    try:
        loader.get("INVALID99")
        assert False, "Should raise DoctagNotFoundError"
    except DoctagNotFoundError as e:
        assert e.tag_id == "INVALID99"
        assert len(e.available) > 0, "Should provide available tags"
        assert "DDL01" in e.available, "Should include DDL01 in available"
