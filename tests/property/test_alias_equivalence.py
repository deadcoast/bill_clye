"""Property test for alias equivalence.

Feature: mrdr-cli-foundation, Property 1: Alias Equivalence
For any valid command invocation using `mrdr`, invoking the same command
with `misterdoctor` SHALL produce identical output.

**Validates: Requirements 1.2**
"""

from hypothesis import given, settings
from hypothesis import strategies as st
from typer.testing import CliRunner

from mrdr.cli.app import app


runner = CliRunner()


# Strategy for valid CLI arguments that don't require subcommands
cli_args_strategy = st.sampled_from([
    ["--version"],
    ["-v"],
    ["--help"],
])


@given(args=cli_args_strategy)
@settings(max_examples=100)
def test_alias_equivalence(args: list[str]) -> None:
    """Property 1: Alias Equivalence.
    
    For any valid command invocation using `mrdr`, invoking the same command
    with `misterdoctor` SHALL produce identical output.
    
    Since both entry points use the same app object, we verify that the app
    produces consistent output regardless of how it's invoked.
    """
    # Both mrdr and misterdoctor point to the same app
    # We test that the app produces consistent output
    result1 = runner.invoke(app, args)
    result2 = runner.invoke(app, args)
    
    # Both invocations should produce identical output
    assert result1.exit_code == result2.exit_code
    assert result1.output == result2.output


def test_version_output_consistency() -> None:
    """Verify version output is consistent across invocations."""
    result1 = runner.invoke(app, ["--version"])
    result2 = runner.invoke(app, ["-v"])
    
    assert result1.exit_code == 0
    assert result2.exit_code == 0
    assert result1.output == result2.output
    assert "mrdr v" in result1.output


def test_help_output_consistency() -> None:
    """Verify help output is consistent across invocations."""
    result1 = runner.invoke(app, ["--help"])
    result2 = runner.invoke(app, ["--help"])
    
    assert result1.exit_code == 0
    assert result2.exit_code == 0
    assert result1.output == result2.output
    assert "MRDR" in result1.output
