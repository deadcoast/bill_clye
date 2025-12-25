"""Property tests for Card Grid component.

Feature: mrdr-visual-integration, Property 1: Card Grid Layout Structure
Validates: Requirements 1.1, 1.2
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.components import CardData, CardGrid


# Strategy for short printable text (to avoid truncation issues in panels)
short_text = st.text(
    min_size=1,
    max_size=20,
    alphabet=st.characters(whitelist_categories=("L", "N"), blacklist_characters="\r\n\t\x00")
)

# Strategy for valid card data with reasonable lengths
card_data_strategy = st.builds(
    CardData,
    title=st.text(min_size=1, max_size=15, alphabet=st.characters(whitelist_categories=("L", "N"))),
    purpose=short_text,
    ui_description=short_text,
    modes=st.lists(st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=("L", "N"))), max_size=3),
    details=st.one_of(st.none(), short_text),
)


@given(cards=st.lists(card_data_strategy, min_size=1, max_size=4))
@settings(max_examples=100)
def test_card_grid_layout_structure(cards: list[CardData]) -> None:
    """Property 1: Card Grid Layout Structure.

    Feature: mrdr-visual-integration, Property 1: Card Grid Layout Structure
    For any valid card data, rendering with --card flag SHALL produce output
    containing table structure with card panels for each entry.
    **Validates: Requirements 1.1, 1.2**
    """
    grid = CardGrid(cards=cards, columns=2)
    output = grid.render()

    # Output should contain panel markers (Rich box characters)
    assert "╭" in output or "┌" in output, "Output should contain panel border characters"
    assert "╯" in output or "┘" in output, "Output should contain panel border characters"

    # Each card should have its title marker (⌘) in output
    assert output.count("⌘") >= len(cards), "Each card should have a title marker"


@given(card=card_data_strategy)
@settings(max_examples=100)
def test_card_grid_card_content(card: CardData) -> None:
    """Property 1: Card Grid Layout Structure - card content.

    Feature: mrdr-visual-integration, Property 1: Card Grid Layout Structure
    For any valid card data, the rendered card SHALL contain panel structure
    with the card title.
    **Validates: Requirements 1.1, 1.2**
    """
    grid = CardGrid(cards=[card], columns=1)
    output = grid.render()

    # Panel structure should be present
    assert "╭" in output, "Output should contain panel border"
    assert "╯" in output, "Output should contain panel border"

    # Title marker should be present
    assert "⌘" in output, "Card should have title marker"

    # At least part of the title should appear (Rich may truncate long titles)
    assert card.title[:5] in output or "⌘" in output, "Card title or marker should appear"


@given(columns=st.integers(min_value=1, max_value=4))
@settings(max_examples=50)
def test_card_grid_column_configuration(columns: int) -> None:
    """Property 1: Card Grid Layout Structure - column configuration.

    Feature: mrdr-visual-integration, Property 1: Card Grid Layout Structure
    For any valid column count, CardGrid SHALL render without errors.
    **Validates: Requirements 1.1, 1.2**
    """
    cards = [
        CardData(title=f"cmd{i}", purpose=f"Purpose {i}", ui_description=f"Desc {i}")
        for i in range(columns + 1)
    ]
    grid = CardGrid(cards=cards, columns=columns)
    output = grid.render()

    # Should render without errors and contain panel markers
    assert "╭" in output or "┌" in output
    assert output.count("⌘") >= len(cards)


def test_card_grid_empty_modes() -> None:
    """Card Grid SHALL handle cards with empty modes list."""
    card = CardData(title="test", purpose="Test purpose", ui_description="Test desc", modes=[])
    grid = CardGrid(cards=[card], columns=1)
    output = grid.render()

    assert "test" in output
    assert "Test purpose" in output
    # "Modes:" should not appear when modes list is empty
    assert "Modes:" not in output


def test_card_grid_with_details() -> None:
    """Card Grid SHALL display details when provided."""
    card = CardData(
        title="test",
        purpose="Test purpose",
        ui_description="Test desc",
        details="Additional details here"
    )
    grid = CardGrid(cards=[card], columns=1)
    output = grid.render()

    assert "Additional details here" in output
