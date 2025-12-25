"""Property tests for Accordion component.

Feature: mrdr-visual-integration, Property 2: Accordion Expandable Sections
Validates: Requirements 1.3, 1.4
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.components import Accordion, AccordionSection


# Strategy for short printable text
short_text = st.text(
    min_size=1,
    max_size=30,
    alphabet=st.characters(whitelist_categories=("L", "N"), blacklist_characters="\r\n\t\x00")
)

# Strategy for accordion section
accordion_section_strategy = st.builds(
    AccordionSection,
    title=short_text,
    content=short_text,
    open=st.booleans(),
)


@given(sections=st.lists(accordion_section_strategy, min_size=1, max_size=5))
@settings(max_examples=100)
def test_accordion_expandable_sections(sections: list[AccordionSection]) -> None:
    """Property 2: Accordion Expandable Sections.

    Feature: mrdr-visual-integration, Property 2: Accordion Expandable Sections
    For any content rendered with --accordion flag, the output SHALL contain
    Rich panel markers indicating expandable sections.
    **Validates: Requirements 1.3, 1.4**
    """
    accordion = Accordion(sections=sections)
    output = accordion.render()

    # Output should contain panel markers (Rich box characters)
    assert "╭" in output or "┌" in output, "Output should contain panel border characters"
    assert "╯" in output or "┘" in output, "Output should contain panel border characters"

    # Each section should have an expand/collapse indicator
    expand_indicators = output.count("▼") + output.count("▶")
    assert expand_indicators >= len(sections), "Each section should have an indicator"


@given(section=accordion_section_strategy)
@settings(max_examples=100)
def test_accordion_open_state_indicator(section: AccordionSection) -> None:
    """Property 2: Accordion Expandable Sections - open state.

    Feature: mrdr-visual-integration, Property 2: Accordion Expandable Sections
    For any accordion section, the open attribute SHALL determine the
    expand/collapse indicator shown.
    **Validates: Requirements 1.3, 1.4**
    """
    accordion = Accordion(sections=[section])
    output = accordion.render()

    if section.open:
        # Open sections should show ▼ indicator
        assert "▼" in output, "Open section should show ▼ indicator"
        # Content should be visible
        assert section.content in output, "Open section content should be visible"
    else:
        # Closed sections should show ▶ indicator
        assert "▶" in output, "Closed section should show ▶ indicator"
        # Content should be hidden (shows placeholder)
        assert "Click to expand" in output, "Closed section should show expand hint"


@given(title=short_text)
@settings(max_examples=50)
def test_accordion_with_title(title: str) -> None:
    """Property 2: Accordion Expandable Sections - group title.

    Feature: mrdr-visual-integration, Property 2: Accordion Expandable Sections
    For any accordion with a title, the title SHALL appear in the output.
    **Validates: Requirements 1.3, 1.4**
    """
    section = AccordionSection(title="Test", content="Content", open=True)
    accordion = Accordion(sections=[section], title=title)
    output = accordion.render()

    assert title in output, "Accordion title should appear in output"


def test_accordion_plain_render() -> None:
    """Accordion plain render SHALL contain no ANSI codes."""
    import re

    sections = [
        AccordionSection(title="Open Section", content="Open content", open=True),
        AccordionSection(title="Closed Section", content="Closed content", open=False),
    ]
    accordion = Accordion(sections=sections)
    plain = accordion.render_plain()

    # No ANSI escape sequences
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
    assert len(ansi_pattern.findall(plain)) == 0

    # Should contain section titles
    assert "Open Section" in plain
    assert "Closed Section" in plain

    # Should contain indicators
    assert "[v]" in plain or "[>]" in plain


def test_accordion_empty_sections() -> None:
    """Accordion with empty sections list SHALL render without error."""
    accordion = Accordion(sections=[])
    output = accordion.render()
    # Should render without error (may be empty or minimal output)
    assert isinstance(output, str)
