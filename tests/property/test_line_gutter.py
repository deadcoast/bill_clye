"""Property tests for Line Gutter component.

Feature: mrdr-visual-integration, Properties 4, 5, 6: Line Gutter
Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5
"""

import re

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.components import LineGutter


# Strategy for multiline content (1-20 lines)
multiline_content_strategy = st.lists(
    st.text(
        min_size=0,
        max_size=50,
        alphabet=st.characters(
            whitelist_categories=("L", "N", "P", "S"),
            blacklist_characters="\r\n\x00",
        ),
    ),
    min_size=1,
    max_size=20,
).map(lambda lines: "\n".join(lines))

# Strategy for start line numbers (reasonable range)
start_line_strategy = st.integers(min_value=1, max_value=1000)

# Strategy for separator characters
separator_strategy = st.sampled_from(["│", "|", ":", " "])


@given(content=multiline_content_strategy)
@settings(max_examples=100)
def test_line_gutter_number_alignment(content: str) -> None:
    """Property 4: Line Gutter Number Alignment.

    Feature: mrdr-visual-integration, Property 4: Line Gutter Number Alignment
    For any content with N lines rendered with --gutter flag, line numbers
    SHALL be right-justified to width of N, separated by separator from content.
    **Validates: Requirements 2.1, 2.2, 2.5**
    """
    gutter = LineGutter(content=content, start_line=1, separator="│")
    output = gutter.render(plain=True)

    lines = content.split("\n")
    output_lines = output.split("\n")
    total_lines = len(lines)
    width = len(str(total_lines))

    # Should have same number of output lines as input lines
    assert len(output_lines) == len(lines), "Output should have same line count as input"

    # Each line should start with right-justified line number
    for i, output_line in enumerate(output_lines):
        line_num = i + 1
        expected_prefix = f"{line_num:>{width}}│"
        assert output_line.startswith(expected_prefix), (
            f"Line {i+1} should start with right-justified number '{expected_prefix}', "
            f"got '{output_line[:len(expected_prefix)+5]}'"
        )


@given(content=multiline_content_strategy, start_line=start_line_strategy)
@settings(max_examples=100)
def test_line_gutter_alignment_with_start_line(content: str, start_line: int) -> None:
    """Property 4: Line Gutter Number Alignment with custom start line.

    Feature: mrdr-visual-integration, Property 4: Line Gutter Number Alignment
    For any content with N lines and start_line S, line numbers SHALL be
    right-justified to width of (S + N - 1).
    **Validates: Requirements 2.1, 2.2, 2.5**
    """
    gutter = LineGutter(content=content, start_line=start_line, separator="│")
    output = gutter.render(plain=True)

    lines = content.split("\n")
    output_lines = output.split("\n")
    max_line_num = start_line + len(lines) - 1
    width = len(str(max_line_num))

    # Each line number should be right-justified to the width of max line number
    for i, output_line in enumerate(output_lines):
        line_num = start_line + i
        expected_prefix = f"{line_num:>{width}}│"
        assert output_line.startswith(expected_prefix), (
            f"Line {i+1} should start with right-justified number '{expected_prefix}'"
        )


@given(content=multiline_content_strategy, separator=separator_strategy)
@settings(max_examples=100)
def test_line_gutter_separator(content: str, separator: str) -> None:
    """Property 4: Line Gutter Number Alignment - separator.

    Feature: mrdr-visual-integration, Property 4: Line Gutter Number Alignment
    For any separator character, the output SHALL use that separator between
    line number and content.
    **Validates: Requirements 2.1, 2.2, 2.5**
    """
    gutter = LineGutter(content=content, start_line=1, separator=separator)
    output = gutter.render(plain=True)

    output_lines = output.split("\n")

    # Each line should contain the separator
    for output_line in output_lines:
        assert separator in output_line, f"Output line should contain separator '{separator}'"


@given(content=multiline_content_strategy)
@settings(max_examples=100)
def test_line_gutter_plain_mode(content: str) -> None:
    """Property 5: Line Gutter Plain Mode.

    Feature: mrdr-visual-integration, Property 5: Line Gutter Plain Mode
    For any content rendered with both --gutter and --plain flags, the output
    SHALL contain line numbers but zero ANSI escape sequences.
    **Validates: Requirements 2.3**
    """
    gutter = LineGutter(content=content, start_line=1, separator="│")
    plain_output = gutter.render(plain=True)

    # No ANSI escape sequences
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
    ansi_matches = ansi_pattern.findall(plain_output)
    assert len(ansi_matches) == 0, f"Plain output should have no ANSI codes, found: {ansi_matches}"

    # Should still contain line numbers
    lines = content.split("\n")
    for i in range(len(lines)):
        line_num = str(i + 1)
        assert line_num in plain_output, f"Plain output should contain line number {line_num}"


@given(content=multiline_content_strategy, start_line=start_line_strategy)
@settings(max_examples=100)
def test_line_gutter_start_line(content: str, start_line: int) -> None:
    """Property 6: Line Gutter Start Line.

    Feature: mrdr-visual-integration, Property 6: Line Gutter Start Line
    For any start line value N, rendering with --start-line N SHALL produce
    output where first line number equals N.
    **Validates: Requirements 2.4**
    """
    gutter = LineGutter(content=content, start_line=start_line, separator="│")
    output = gutter.render(plain=True)

    output_lines = output.split("\n")
    first_line = output_lines[0]

    # First line should start with the start_line number
    # Extract the line number from the beginning of the line
    match = re.match(r"^\s*(\d+)", first_line)
    assert match is not None, f"First line should start with a number, got: {first_line}"
    first_line_num = int(match.group(1))
    assert first_line_num == start_line, (
        f"First line number should be {start_line}, got {first_line_num}"
    )


@given(content=multiline_content_strategy, start_line=start_line_strategy)
@settings(max_examples=100)
def test_line_gutter_sequential_numbers(content: str, start_line: int) -> None:
    """Property 6: Line Gutter Start Line - sequential numbering.

    Feature: mrdr-visual-integration, Property 6: Line Gutter Start Line
    For any start line value N, line numbers SHALL be sequential starting from N.
    **Validates: Requirements 2.4**
    """
    gutter = LineGutter(content=content, start_line=start_line, separator="│")
    output = gutter.render(plain=True)

    output_lines = output.split("\n")
    lines = content.split("\n")

    # Extract line numbers and verify they are sequential
    for i, output_line in enumerate(output_lines):
        expected_num = start_line + i
        match = re.match(r"^\s*(\d+)", output_line)
        assert match is not None, f"Line {i+1} should start with a number"
        actual_num = int(match.group(1))
        assert actual_num == expected_num, (
            f"Line {i+1} should have number {expected_num}, got {actual_num}"
        )


def test_line_gutter_helper_methods() -> None:
    """Test LineGutter helper methods."""
    content = "line1\nline2\nline3"
    gutter = LineGutter(content=content, start_line=5)

    assert gutter.get_line_count() == 3, "Should count 3 lines"
    assert gutter.get_max_line_number() == 7, "Max line should be 5 + 3 - 1 = 7"


def test_line_gutter_single_line() -> None:
    """Test LineGutter with single line content."""
    content = "single line"
    gutter = LineGutter(content=content, start_line=1, separator="│")
    output = gutter.render(plain=True)

    assert output == "1│ single line", f"Single line output incorrect: {output}"


def test_line_gutter_empty_lines() -> None:
    """Test LineGutter with empty lines in content."""
    content = "line1\n\nline3"
    gutter = LineGutter(content=content, start_line=1, separator="│")
    output = gutter.render(plain=True)

    output_lines = output.split("\n")
    assert len(output_lines) == 3, "Should have 3 output lines"
    assert output_lines[1] == "2│ ", "Empty line should still have line number"
