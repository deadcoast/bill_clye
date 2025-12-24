"""Property tests for JSON output validity.

Feature: mrdr-cli-foundation, Property 9: JSON Output Validity
Validates: Requirements 6.2, 6.5
"""

import json

from hypothesis import given, settings

from mrdr.database.schema import DocstringEntry
from mrdr.render.json_renderer import JSONRenderer
from tests.conftest import docstring_entry_strategy


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_json_renderer_produces_valid_json(data: dict) -> None:
    """Property 9: JSON Output Validity - single entry.

    Feature: mrdr-cli-foundation, Property 9: JSON Output Validity
    For any command invoked with `--json` flag, the output SHALL be valid
    JSON that can be parsed without errors.
    **Validates: Requirements 6.2, 6.5**
    """
    entry = DocstringEntry(**data)
    renderer = JSONRenderer()

    output = renderer.render(entry, "show")

    # Output should be valid JSON
    parsed = json.loads(output)
    assert isinstance(parsed, dict)
    assert "language" in parsed
    assert "syntax" in parsed


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_json_renderer_preserves_data(data: dict) -> None:
    """Property 9: JSON Output Validity - data preservation.

    Feature: mrdr-cli-foundation, Property 9: JSON Output Validity
    For any DocstringEntry, JSON serialization SHALL preserve all field values.
    **Validates: Requirements 6.2, 6.5**
    """
    entry = DocstringEntry(**data)
    renderer = JSONRenderer()

    output = renderer.render(entry, "show")
    parsed = json.loads(output)

    # Verify key fields are preserved
    assert parsed["language"] == entry.language
    assert parsed["syntax"]["start"] == entry.syntax.start
    assert parsed["syntax"]["type"] == entry.syntax.type
    assert parsed["syntax"]["location"] == entry.syntax.location


@given(data1=docstring_entry_strategy(), data2=docstring_entry_strategy())
@settings(max_examples=100)
def test_json_renderer_compare_valid_json(data1: dict, data2: dict) -> None:
    """Property 9: JSON Output Validity - compare output.

    Feature: mrdr-cli-foundation, Property 9: JSON Output Validity
    For any compare command with `--json` flag, the output SHALL be valid JSON.
    **Validates: Requirements 6.2, 6.5**
    """
    entry1 = DocstringEntry(**data1)
    entry2 = DocstringEntry(**data2)
    renderer = JSONRenderer()

    compare_data = {"lang1": entry1, "lang2": entry2}
    output = renderer.render(compare_data, "compare")

    # Output should be valid JSON
    parsed = json.loads(output)
    assert isinstance(parsed, dict)
    assert "lang1" in parsed
    assert "lang2" in parsed


def test_json_renderer_supports_rich_returns_false() -> None:
    """JSONRenderer.supports_rich() SHALL return False."""
    renderer = JSONRenderer()
    assert renderer.supports_rich() is False


def test_json_renderer_list_valid_json() -> None:
    """JSON renderer list output SHALL be valid JSON."""
    renderer = JSONRenderer()
    languages = ["Python", "JavaScript", "Rust"]

    output = renderer.render_languages(languages)

    parsed = json.loads(output)
    assert isinstance(parsed, dict)
    assert "languages" in parsed
    assert "count" in parsed
    assert parsed["count"] == 3


def test_json_renderer_compact_output() -> None:
    """JSON renderer with indent=None SHALL produce compact output."""
    renderer = JSONRenderer(indent=None)
    entry = DocstringEntry(
        language="Python",
        syntax={
            "start": '"""',
            "end": '"""',
            "type": "literal",
            "location": "internal_first_line",
        },
    )

    output = renderer.render(entry, "show")

    # Compact output should have no newlines
    assert "\n" not in output
    # But should still be valid JSON
    parsed = json.loads(output)
    assert parsed["language"] == "Python"


def test_json_renderer_sorted_keys() -> None:
    """JSON renderer with sort_keys=True SHALL sort dictionary keys."""
    renderer = JSONRenderer(sort_keys=True)
    entry = DocstringEntry(
        language="Python",
        syntax={
            "start": '"""',
            "end": '"""',
            "type": "literal",
            "location": "internal_first_line",
        },
        tags=["scripting"],
    )

    output = renderer.render(entry, "show")

    # Keys should be sorted alphabetically
    parsed = json.loads(output)
    keys = list(parsed.keys())
    assert keys == sorted(keys)
