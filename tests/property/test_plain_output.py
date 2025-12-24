"""Property tests for plain output without ANSI codes.

Feature: mrdr-cli-foundation, Property 8: Plain Output No ANSI
Validates: Requirements 3.3, 6.1, 6.4
"""

import re

from hypothesis import given, settings

from mrdr.database.schema import DocstringEntry
from mrdr.render.plain_renderer import PlainRenderer
from tests.conftest import docstring_entry_strategy


# ANSI escape sequence pattern
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_plain_renderer_show_no_ansi(data: dict) -> None:
    """Property 8: Plain Output No ANSI - show template.

    Feature: mrdr-cli-foundation, Property 8: Plain Output No ANSI
    For any command invoked with `--plain` flag, the output SHALL contain
    zero ANSI escape sequences (no characters matching `\\x1b\\[`).
    **Validates: Requirements 3.3, 6.1, 6.4**
    """
    entry = DocstringEntry(**data)
    renderer = PlainRenderer()

    output = renderer.render(entry, "show")

    # Output should contain no ANSI escape sequences
    ansi_matches = ANSI_PATTERN.findall(output)
    assert len(ansi_matches) == 0, f"Found ANSI sequences: {ansi_matches}"


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_plain_renderer_inspect_no_ansi(data: dict) -> None:
    """Property 8: Plain Output No ANSI - inspect template.

    Feature: mrdr-cli-foundation, Property 8: Plain Output No ANSI
    For any command invoked with `--plain` flag, the output SHALL contain
    zero ANSI escape sequences.
    **Validates: Requirements 3.3, 6.1, 6.4**
    """
    entry = DocstringEntry(**data)
    renderer = PlainRenderer()

    # Convert entry to dict for inspect
    inspect_data = {
        "language": entry.language,
        "syntax": {
            "start": entry.syntax.start,
            "end": entry.syntax.end,
            "type": entry.syntax.type,
            "location": entry.syntax.location,
        },
        "tags": entry.tags,
    }

    output = renderer.render(inspect_data, "inspect")

    ansi_matches = ANSI_PATTERN.findall(output)
    assert len(ansi_matches) == 0, f"Found ANSI sequences: {ansi_matches}"


@given(data1=docstring_entry_strategy(), data2=docstring_entry_strategy())
@settings(max_examples=100)
def test_plain_renderer_compare_no_ansi(data1: dict, data2: dict) -> None:
    """Property 8: Plain Output No ANSI - compare template.

    Feature: mrdr-cli-foundation, Property 8: Plain Output No ANSI
    For any command invoked with `--plain` flag, the output SHALL contain
    zero ANSI escape sequences.
    **Validates: Requirements 3.3, 6.1, 6.4**
    """
    entry1 = DocstringEntry(**data1)
    entry2 = DocstringEntry(**data2)
    renderer = PlainRenderer()

    compare_data = {"lang1": entry1, "lang2": entry2}
    output = renderer.render(compare_data, "compare")

    ansi_matches = ANSI_PATTERN.findall(output)
    assert len(ansi_matches) == 0, f"Found ANSI sequences: {ansi_matches}"


def test_plain_renderer_supports_rich_returns_false() -> None:
    """PlainRenderer.supports_rich() SHALL return False."""
    renderer = PlainRenderer()
    assert renderer.supports_rich() is False


def test_plain_renderer_list_no_ansi() -> None:
    """Plain renderer list output SHALL contain no ANSI codes."""
    renderer = PlainRenderer()
    languages = ["Python", "JavaScript", "Rust", "Go", "TypeScript"]

    output = renderer.render(languages, "list")

    ansi_matches = ANSI_PATTERN.findall(output)
    assert len(ansi_matches) == 0, f"Found ANSI sequences: {ansi_matches}"


def test_plain_renderer_show_contains_language_info() -> None:
    """Plain renderer show output SHALL contain language information."""
    renderer = PlainRenderer()
    entry = DocstringEntry(
        language="Python",
        syntax={
            "start": '"""',
            "end": '"""',
            "type": "literal",
            "location": "internal_first_line",
        },
        tags=["scripting", "dynamic"],
    )

    output = renderer.render(entry, "show")

    assert "Python" in output
    assert '"""' in output
    assert "literal" in output
    assert "internal_first_line" in output


def test_plain_renderer_compare_contains_both_languages() -> None:
    """Plain renderer compare output SHALL contain both languages."""
    renderer = PlainRenderer()
    entry1 = DocstringEntry(
        language="Python",
        syntax={
            "start": '"""',
            "end": '"""',
            "type": "literal",
            "location": "internal_first_line",
        },
    )
    entry2 = DocstringEntry(
        language="JavaScript",
        syntax={
            "start": "/**",
            "end": "*/",
            "type": "block",
            "location": "above_target",
        },
    )

    output = renderer.render({"lang1": entry1, "lang2": entry2}, "compare")

    assert "Python" in output
    assert "JavaScript" in output
    assert '"""' in output
    assert "/**" in output
