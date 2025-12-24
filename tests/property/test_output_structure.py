"""Property tests for output structure conformance.

Feature: mrdr-cli-foundation, Property 7: Output Structure Conformance
Validates: Requirements 3.1, 3.2, 3.7
"""

from hypothesis import given, settings

from mrdr.database.schema import DocstringEntry
from mrdr.render.components.golden_screen import (
    ContextStrip,
    GoldenScreen,
    HeaderBar,
    HintBar,
)
from mrdr.render.rich_renderer import RichRenderer
from tests.conftest import docstring_entry_strategy


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_golden_screen_contains_header_bar(data: dict) -> None:
    """Property 7: Output Structure Conformance - Header bar presence.

    Feature: mrdr-cli-foundation, Property 7: Output Structure Conformance
    For any `mrdr jekyl show <language>` invocation with a valid language,
    the output SHALL contain a header bar with command context.
    **Validates: Requirements 3.1, 3.2, 3.7**
    """
    entry = DocstringEntry(**data)
    header = HeaderBar(command=f"mrdr jekyl show {entry.language}")
    hints = HintBar()
    screen = GoldenScreen(header=header, payload=f"Content for {entry.language}", hints=hints)

    output = screen.render()

    # Header bar should contain the command
    assert f"mrdr jekyl show {entry.language}" in output
    # Header bar should contain DB context
    assert "DB:" in output or "docstring_database" in output


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_golden_screen_contains_hints_bar(data: dict) -> None:
    """Property 7: Output Structure Conformance - Hints bar presence.

    Feature: mrdr-cli-foundation, Property 7: Output Structure Conformance
    For any `mrdr jekyl show <language>` invocation with a valid language,
    the output SHALL contain a hints bar with keybinds.
    **Validates: Requirements 3.1, 3.2, 3.7**
    """
    entry = DocstringEntry(**data)
    header = HeaderBar(command=f"mrdr jekyl show {entry.language}")
    hints = HintBar()  # Default hints
    screen = GoldenScreen(header=header, payload=f"Content for {entry.language}", hints=hints)

    output = screen.render()

    # Hints bar should contain default keybinds
    assert "search" in output
    assert "details" in output
    assert "filter" in output
    assert "quit" in output


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_golden_screen_contains_payload(data: dict) -> None:
    """Property 7: Output Structure Conformance - Primary payload presence.

    Feature: mrdr-cli-foundation, Property 7: Output Structure Conformance
    For any `mrdr jekyl show <language>` invocation with a valid language,
    the output SHALL contain a primary payload area.
    **Validates: Requirements 3.1, 3.2, 3.7**
    """
    entry = DocstringEntry(**data)
    payload_content = f"Docstring syntax for {entry.language}"
    header = HeaderBar(command=f"mrdr jekyl show {entry.language}")
    hints = HintBar()
    screen = GoldenScreen(header=header, payload=payload_content, hints=hints)

    output = screen.render()

    # Payload content should be present
    assert entry.language in output


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_rich_renderer_show_contains_required_elements(data: dict) -> None:
    """Property 7: Output Structure Conformance - Rich renderer show template.

    Feature: mrdr-cli-foundation, Property 7: Output Structure Conformance
    For any valid DocstringEntry, the Rich renderer's show template SHALL
    produce output containing language name and syntax information.
    **Validates: Requirements 3.1, 3.2, 3.7**
    """
    entry = DocstringEntry(**data)
    renderer = RichRenderer()

    output = renderer.render(entry, "show")

    # Output should contain language name
    assert entry.language in output
    # Output should contain syntax information
    assert "Delimiter" in output or entry.syntax.start in output


def test_header_bar_renders_command_and_db_source() -> None:
    """HeaderBar SHALL render command and database source."""
    header = HeaderBar(command="mrdr jekyl show python", db_source="DB: test.json")
    rendered = header.render()

    # Convert to plain string for assertion
    plain = rendered.plain
    assert "mrdr jekyl show python" in plain
    assert "test.json" in plain


def test_hint_bar_renders_default_keybinds() -> None:
    """HintBar SHALL render default keybind hints per Requirement 3.7."""
    hints = HintBar()
    rendered = hints.render()

    plain = rendered.plain
    # Default hints: (/) search · (↵) details · (f) filter · (q) quit
    assert "/" in plain
    assert "search" in plain
    assert "↵" in plain
    assert "details" in plain
    assert "f" in plain
    assert "filter" in plain
    assert "q" in plain
    assert "quit" in plain


def test_hint_bar_renders_custom_keybinds() -> None:
    """HintBar SHALL render custom keybind hints."""
    custom_hints = [("x", "exit"), ("h", "help")]
    hints = HintBar(hints=custom_hints)
    rendered = hints.render()

    plain = rendered.plain
    assert "x" in plain
    assert "exit" in plain
    assert "h" in plain
    assert "help" in plain


def test_context_strip_renders_count() -> None:
    """ContextStrip SHALL render item count."""
    context = ContextStrip(total_count=42)
    rendered = context.render()

    plain = rendered.plain
    assert "42" in plain
    assert "items" in plain


def test_context_strip_renders_filtered_count() -> None:
    """ContextStrip SHALL render filtered/total count."""
    context = ContextStrip(total_count=100, filtered_count=25)
    rendered = context.render()

    plain = rendered.plain
    assert "25/100" in plain
