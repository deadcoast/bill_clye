"""Property test for debug output.

Feature: mrdr-cli-foundation, Property 16: Debug Output
For any command invoked with `--debug` flag, the output SHALL include
timing information (query time in ms) and cache status.

**Validates: Requirements 6.3**
"""

import subprocess

from hypothesis import given, settings
from hypothesis import strategies as st


# Strategy for commands that support debug output
debug_command_strategy = st.sampled_from([
    ["python", "-m", "mrdr", "--debug", "hyde", "list"],
    ["python", "-m", "mrdr", "--debug", "hyde", "query", "Python"],
    ["python", "-m", "mrdr", "--debug", "hyde", "inspect", "Python"],
    ["python", "-m", "mrdr", "--debug", "docstring", "Python"],
])


@given(command=debug_command_strategy)
@settings(max_examples=100)
def test_debug_output_includes_timing(command: list[str]) -> None:
    """Property 16: Debug Output.
    
    For any command invoked with `--debug` flag, the output SHALL include
    timing information (query time in ms) and cache status.
    """
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    output = result.stdout
    
    # Must contain timing information
    assert "time:" in output.lower() or "ms" in output, (
        f"Timing info missing in debug output: {output[-200:]}"
    )
    
    # Must contain cache status
    assert "cache" in output.lower(), (
        f"Cache status missing in debug output: {output[-200:]}"
    )


def test_debug_flag_shows_query_time() -> None:
    """Test that --debug shows query time in milliseconds."""
    result = subprocess.run(
        ["python", "-m", "mrdr", "--debug", "hyde", "list"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    
    # Should contain "ms" for milliseconds
    assert "ms" in result.stdout


def test_debug_flag_shows_cache_status() -> None:
    """Test that --debug shows cache hit/miss status."""
    result = subprocess.run(
        ["python", "-m", "mrdr", "--debug", "hyde", "query", "Python"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    
    # Should contain cache status (hit or miss)
    output_lower = result.stdout.lower()
    assert "cache" in output_lower
    assert "hit" in output_lower or "miss" in output_lower


def test_no_debug_without_flag() -> None:
    """Test that debug info is not shown without --debug flag."""
    result = subprocess.run(
        ["python", "-m", "mrdr", "--plain", "hyde", "list"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0
    
    # Should NOT contain debug timing info
    output_lower = result.stdout.lower()
    assert "query time:" not in output_lower
    assert "cache:" not in output_lower
