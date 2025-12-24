"""Main Typer application for MRDR CLI."""

import sys

import typer
from rich.console import Console

from mrdr import __app_name__, __version__

# Global state for CLI options
class CLIState:
    """Global state for CLI options."""
    
    plain: bool = False
    json: bool = False
    debug: bool = False
    _console: Console | None = None
    
    @property
    def console(self) -> Console:
        """Get the console, creating one appropriate for current state."""
        # Always create a fresh console based on current state
        if self.plain or self.json:
            return Console(force_terminal=False, no_color=True)
        return Console()
    
    def is_tty(self) -> bool:
        """Check if output is a TTY."""
        return sys.stdout.isatty()
    
    def should_use_plain(self) -> bool:
        """Determine if plain output should be used."""
        return self.plain or self.json or not self.is_tty()


state = CLIState()

app = typer.Typer(
    name=__app_name__,
    help="MRDR - The Visual Syntax CLI for docstring and syntax database.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)


def version_callback(value: bool) -> None:
    """Display version and exit."""
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "-v",
        "--version",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
    plain: bool = typer.Option(
        False,
        "--plain",
        help="Disable Rich formatting, output plain text.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output results as JSON.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug output with timing and cache info.",
    ),
) -> None:
    """MRDR - The Visual Syntax CLI.
    
    A CLI-driven syntax and docstring database that documents, categorizes,
    and displays examples for common codebases.
    
    Use 'mrdr' or 'misterdoctor' to invoke the CLI.
    """
    state.plain = plain
    state.json = json_output
    state.debug = debug
    
    # Auto-detect non-TTY and switch to plain
    if not state.is_tty() and not json_output:
        state.plain = True


# Import and register subcommand groups
from mrdr.cli.hyde_commands import hyde_app
from mrdr.cli.jekyl_commands import jekyl_app
from mrdr.cli.docstring_commands import docstring_command
from mrdr.cli.config_commands import config_app

app.add_typer(hyde_app, name="hyde")
app.add_typer(jekyl_app, name="jekyl")
app.add_typer(config_app, name="config")

# Register docstring as a direct command
app.command("docstring")(docstring_command)


@app.command("fix")
def fix_command() -> None:
    """Refresh syntax highlighting and reset CLI UI state.
    
    Use this command if you experience display issues or corrupted
    terminal output. It clears the terminal and resets the Rich console.
    """
    console = state.console
    
    # Clear the terminal
    console.clear()
    
    # Print confirmation
    if state.json:
        console.print('{"status": "ok", "message": "UI state reset"}')
    elif state.should_use_plain():
        console.print("UI state reset successfully.")
    else:
        from rich.panel import Panel
        console.print(Panel(
            "[green]✓[/green] UI state reset successfully.\n\n"
            "[dim]Terminal cleared and Rich console refreshed.[/dim]",
            title="MRDR Fix",
            border_style="green",
        ))
