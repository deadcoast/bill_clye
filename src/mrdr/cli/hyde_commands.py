"""Hyde subcommands for MRDR CLI.

This module implements the hyde subcommand group for back-end data operations
including query, list, inspect, and export commands.
"""

import json
import time
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mrdr.cli.app import state
from mrdr.controllers.hyde import HydeController
from mrdr.render.json_renderer import JSONRenderer
from mrdr.render.plain_renderer import PlainRenderer
from mrdr.utils.errors import LanguageNotFoundError

hyde_app = typer.Typer(
    name="hyde",
    help="Back-end data operations: query, list, inspect, and export.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


def get_hyde_controller() -> HydeController:
    """Get a configured HydeController instance."""
    return HydeController()


def handle_language_not_found(error: LanguageNotFoundError, console: Console) -> None:
    """Display user-friendly error with recovery suggestions."""
    suggestions_text = "\n".join(f"  • {s}" for s in error.suggestions[:5])
    console.print(Panel(
        f"[red]✖[/red] Language '[bold]{error.language}[/bold]' not found\n\n"
        f"[dim]Did you mean:[/dim]\n{suggestions_text}\n\n"
        f"[dim]Try:[/dim] mrdr hyde list",
        title="Not Found",
        border_style="red"
    ))


@hyde_app.command("query")
def query(
    language: str = typer.Argument(..., help="Programming language to query."),
) -> None:
    """Query docstring syntax data for a specific language.
    
    Returns the docstring syntax specification including delimiters,
    type, and attachment location for the specified language.
    """
    start_time = time.time()
    console = state.console
    hyde = get_hyde_controller()
    
    try:
        entry = hyde.query(language)
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            renderer = JSONRenderer()
            output = renderer.render(entry, "show")
            console.print(output)
        elif state.should_use_plain():
            renderer = PlainRenderer()
            output = renderer.render(entry, "show")
            console.print(output)
        else:
            # Rich output
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Field", style="cyan")
            table.add_column("Value")
            
            table.add_row("Language", Text(entry.language, style="bold green"))
            table.add_row("Start Delimiter", Text(repr(entry.syntax.start), style="yellow"))
            end_val = repr(entry.syntax.end) if entry.syntax.end else "None (line-based)"
            table.add_row("End Delimiter", Text(end_val, style="yellow"))
            table.add_row("Type", Text(str(entry.syntax.type), style="magenta"))
            table.add_row("Location", Text(str(entry.syntax.location), style="blue"))
            
            if entry.tags:
                table.add_row("Tags", Text(", ".join(entry.tags), style="dim"))
            
            console.print(Panel(table, title=f"[bold]{entry.language}[/bold] Docstring Syntax"))
        
        if state.debug:
            console.print(f"\n[dim]Query time: {elapsed:.2f}ms | Cache: miss[/dim]")
            
    except LanguageNotFoundError as e:
        if state.json:
            error_data = {"error": str(e), "suggestions": e.suggestions}
            console.print(json.dumps(error_data, indent=2))
        else:
            handle_language_not_found(e, console)
        raise typer.Exit(1)


@hyde_app.command("list")
def list_languages() -> None:
    """Display all supported languages in the database.
    
    Shows a complete list of all programming languages with docstring
    syntax definitions in the database.
    """
    start_time = time.time()
    console = state.console
    hyde = get_hyde_controller()
    
    languages = hyde.list_languages()
    elapsed = (time.time() - start_time) * 1000
    
    if state.json:
        renderer = JSONRenderer()
        output = renderer.render_languages(languages)
        console.print(output)
    elif state.should_use_plain():
        renderer = PlainRenderer()
        output = renderer.render(languages, "list")
        console.print(output)
    else:
        # Rich output
        table = Table(title="Supported Languages", show_header=True)
        table.add_column("#", style="dim", width=4)
        table.add_column("Language", style="cyan")
        
        for idx, lang in enumerate(sorted(languages), 1):
            table.add_row(str(idx), lang)
        
        console.print(table)
        console.print(f"\n[dim]Total: {len(languages)} languages[/dim]")
    
    if state.debug:
        console.print(f"\n[dim]Query time: {elapsed:.2f}ms | Cache: miss[/dim]")


@hyde_app.command("inspect")
def inspect(
    language: str = typer.Argument(..., help="Programming language to inspect."),
) -> None:
    """Display detailed metadata for a language.
    
    Shows comprehensive information including syntax signature,
    carrier type, attachment rules, parsing notes, and quality grade.
    """
    start_time = time.time()
    console = state.console
    hyde = get_hyde_controller()
    
    try:
        metadata = hyde.inspect(language)
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            renderer = JSONRenderer()
            output = renderer.render(metadata, "inspect")
            console.print(output)
        elif state.should_use_plain():
            renderer = PlainRenderer()
            output = renderer.render(metadata, "inspect")
            console.print(output)
        else:
            # Rich output
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Field", style="cyan", width=20)
            table.add_column("Value")
            
            for key, value in metadata.items():
                if isinstance(value, dict):
                    value_str = "\n".join(f"  {k}: {v}" for k, v in value.items())
                elif isinstance(value, list):
                    value_str = ", ".join(str(v) for v in value) if value else "[]"
                else:
                    value_str = str(value) if value is not None else "None"
                table.add_row(key, value_str)
            
            console.print(Panel(table, title="[bold]Detailed Inspection[/bold]"))
        
        if state.debug:
            console.print(f"\n[dim]Query time: {elapsed:.2f}ms | Cache: miss[/dim]")
            
    except LanguageNotFoundError as e:
        if state.json:
            error_data = {"error": str(e), "suggestions": e.suggestions}
            console.print(json.dumps(error_data, indent=2))
        else:
            handle_language_not_found(e, console)
        raise typer.Exit(1)


@hyde_app.command("export")
def export(
    language: Optional[str] = typer.Argument(
        None, help="Programming language to export. If omitted, exports all."
    ),
    format: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format: json or yaml.",
    ),
) -> None:
    """Export query results in JSON or YAML format.
    
    Exports docstring syntax data for a specific language or all languages
    in the specified format with field order preservation.
    """
    start_time = time.time()
    console = state.console
    hyde = get_hyde_controller()
    
    format_lower = format.lower()
    if format_lower not in ("json", "yaml"):
        console.print(f"[red]Error:[/red] Invalid format '{format}'. Use 'json' or 'yaml'.")
        raise typer.Exit(1)
    
    try:
        if language:
            output = hyde.export(language, format_lower)
        else:
            output = hyde.export_all(format_lower)
        
        elapsed = (time.time() - start_time) * 1000
        console.print(output)
        
        if state.debug:
            console.print(f"\n[dim]Export time: {elapsed:.2f}ms[/dim]")
            
    except LanguageNotFoundError as e:
        if state.json:
            error_data = {"error": str(e), "suggestions": e.suggestions}
            console.print(json.dumps(error_data, indent=2))
        else:
            handle_language_not_found(e, console)
        raise typer.Exit(1)
