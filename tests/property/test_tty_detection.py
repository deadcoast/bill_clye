"""Property test for TTY detection.

Feature: mrdr-cli-foundation, Property 17: TTY Detection
For any invocation in a non-TTY environment (piped output), the CLI SHALL
automatically produce plain output without ANSI codes, equivalent to `--plain`.

**Validates: Requirements 6.6**
"""

import re
import subprocess
import sys

from hypothesis import given, settings
from hypothesis import strategies as st


# ANSI escape sequence pattern
ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')


# Strategy for commands that produce output
command_strategy = st.sampled_from([
    ["python", "-m", "mrdr", "hyde", "list"],
    ["python", "-m", "mrdr", "hyde", "query", "Python"],
    ["python", "-m", "mrdr", "docstring", "--all"],
])


@given(command=command_strategy)
@settings(max_examples=100)
def test_tty_detection_piped_output(command: list[str]) -> None:
    """Property 17: TTY Detection.
    
    For any invocation in a non-TTY environment (piped output), the CLI SHALL
    automatically produce plain output without ANSI codes.
    
    When running via subprocess with PIPE, stdout is not a TTY, so the CLI
    should automatically use plain output.
    """
    # Run command with piped output (non-TTY)
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    # Output should not contain ANSI escape sequences
    ansi_matches = ANSI_PATTERN.findall(result.stdout)
    assert len(ansi_matches) == 0, (
        f"Found ANSI codes in piped output: {ansi_matches[:5]}"
    )


def test_plain_flag_produces_no_ansi() -> None:
    """Test that --plain flag produces output without ANSI codes."""
    result = subprocess.run(
        ["python", "-m", "mrdr", "--plain", "hyde", "list"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    
    # Should not contain ANSI codes
    ansi_matches = ANSI_PATTERN.findall(result.stdout)
    assert len(ansi_matches) == 0


def test_json_flag_produces_no_ansi() -> None:
    """Test that --json flag produces output without ANSI codes."""
    result = subprocess.run(
        ["python", "-m", "mrdr", "--json", "hyde", "list"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    
    # Should not contain ANSI codes
    ansi_matches = ANSI_PATTERN.findall(result.stdout)
    assert len(ansi_matches) == 0


def test_piped_output_equivalent_to_plain() -> None:
    """Test that piped output is equivalent to --plain output."""
    # Run with --plain flag
    plain_result = subprocess.run(
        ["python", "-m", "mrdr", "--plain", "hyde", "list"],
        capture_output=True,
        text=True,
    )
    
    # Run without --plain (piped, so should auto-detect)
    piped_result = subprocess.run(
        ["python", "-m", "mrdr", "hyde", "list"],
        capture_output=True,
        text=True,
    )
    
    assert plain_result.returncode == 0
    assert piped_result.returncode == 0
    
    # Both should produce the same output (no ANSI in either)
    assert plain_result.stdout == piped_result.stdout
