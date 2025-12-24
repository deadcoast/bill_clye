"""Property test for help availability.

Feature: mrdr-cli-foundation, Property 2: Help Availability
For any valid command path in the CLI (including subcommands), appending
`-h` or `--help` SHALL produce help text without errors.

**Validates: Requirements 1.6**
"""

from hypothesis import given, settings
from hypothesis import strategies as st
from typer.testing import CliRunner

from mrdr.cli.app import app


runner = CliRunner()


# All valid command paths in the CLI
COMMAND_PATHS = [
    [],  # Root command
    ["hyde"],
    ["hyde", "query"],
    ["hyde", "list"],
    ["hyde", "inspect"],
    ["hyde", "export"],
    ["jekyl"],
    ["jekyl", "show"],
    ["jekyl", "compare"],
    ["config"],
    ["config", "show"],
    ["config", "set"],
    ["config", "get"],
    ["config", "path"],
    ["docstring"],
]


# Strategy for valid command paths
command_path_strategy = st.sampled_from(COMMAND_PATHS)

# Strategy for help flags
help_flag_strategy = st.sampled_from(["-h", "--help"])


@given(command_path=command_path_strategy, help_flag=help_flag_strategy)
@settings(max_examples=100)
def test_help_availability(command_path: list[str], help_flag: str) -> None:
    """Property 2: Help Availability.
    
    For any valid command path in the CLI (including subcommands), appending
    `-h` or `--help` SHALL produce help text without errors.
    """
    args = command_path + [help_flag]
    result = runner.invoke(app, args)
    
    # Help should always succeed (exit code 0)
    assert result.exit_code == 0, (
        f"Help failed for {' '.join(args)}: {result.output}"
    )
    
    # Help output should contain "Usage:" or usage information
    assert "Usage:" in result.output or "usage:" in result.output.lower(), (
        f"Help output missing usage info for {' '.join(args)}"
    )


def test_root_help_shows_all_commands() -> None:
    """Test that root help shows all available commands."""
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    
    # Should list all main commands
    assert "hyde" in result.output
    assert "jekyl" in result.output
    assert "config" in result.output
    assert "docstring" in result.output


def test_subcommand_help_shows_options() -> None:
    """Test that subcommand help shows available options."""
    result = runner.invoke(app, ["hyde", "query", "--help"])
    
    assert result.exit_code == 0
    
    # Should show the command description
    assert "Query" in result.output or "query" in result.output.lower()
    
    # Should show arguments
    assert "LANGUAGE" in result.output or "language" in result.output.lower()


def test_help_short_flag_works() -> None:
    """Test that -h works as short form of --help."""
    result_short = runner.invoke(app, ["-h"])
    result_long = runner.invoke(app, ["--help"])
    
    assert result_short.exit_code == 0
    assert result_long.exit_code == 0
    
    # Both should produce the same output
    assert result_short.output == result_long.output
