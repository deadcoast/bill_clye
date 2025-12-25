"""Jekyl subcommands for MRDR CLI.

This module implements the jekyl subcommand group for front-end visual
operations including show and compare commands with Rich rendering.
"""

import json as json_module
import time

import typer
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mrdr.cli.app import state
from mrdr.cli.error_handlers import (
    display_language_not_found_error,
    display_unexpected_error,
    handle_mrdr_error,
)
from mrdr.controllers.jekyl import ShowOptions
from mrdr.database.doctag import DoctagLoader
from mrdr.database.doctag.loader import DoctagNotFoundError
from mrdr.database.udl import UDLLoader
from mrdr.database.udl.loader import UDLNotFoundError
from mrdr.factory import create_jekyl_controller
from mrdr.render.doctag_renderer import DoctagEntry, DoctagRenderer
from mrdr.render.json_renderer import JSONRenderer
from mrdr.utils.errors import LanguageNotFoundError, MRDRError

jekyl_app = typer.Typer(
    name="jekyl",
    help="Front-end visual operations: show and compare with Rich rendering.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


def get_jekyl_controller():
    """Get a configured JekylController instance using factory."""
    if state.json:
        output_format = "json"
    elif state.should_use_plain():
        output_format = "plain"
    else:
        output_format = "rich"
    
    return create_jekyl_controller(
        output_format=output_format,
        console=state.console,
    )


@jekyl_app.command("show")
def show(
    language: str = typer.Argument(..., help="Programming language to display, or 'udl:<name>' for UDL."),
    plain: bool = typer.Option(
        False,
        "--plain",
        help="Render output without Rich formatting.",
    ),
    example: bool = typer.Option(
        False,
        "--example",
        "-e",
        help="Include code example demonstrating the docstring syntax.",
    ),
    grade: bool = typer.Option(
        False,
        "--grade",
        "-g",
        help="Include PLUSREP quality grade in output.",
    ),
) -> None:
    """Display docstring syntax with Rich formatting.
    
    Renders the docstring syntax for a language using the Golden Screen
    layout with header bar, primary payload, and hints bar.
    
    Use 'udl:<name>' to display a custom UDL definition.
    """
    start_time = time.time()
    console = state.console
    
    # Override plain state if --plain flag is passed
    if plain:
        state.plain = True
    
    # Check for UDL pattern
    if language.lower().startswith("udl:"):
        udl_name = language[4:]  # Remove "udl:" prefix
        _show_udl(udl_name, start_time)
        return
    
    jekyl = get_jekyl_controller()
    options = ShowOptions(
        plain=state.should_use_plain(),
        example=example,
        grade=grade,
    )
    
    try:
        if state.json:
            # JSON output
            entry = jekyl.hyde.query(language)
            renderer = JSONRenderer()
            output = renderer.render(entry, "show")
            console.print(output)
        else:
            # Rich or plain output via JekylController
            output = jekyl.show(language, options)
            console.print(output)
        
        elapsed = (time.time() - start_time) * 1000
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms | Cache: miss[/dim]")
            
    except LanguageNotFoundError as e:
        display_language_not_found_error(e, console, state.json)
        raise typer.Exit(1)
    except MRDRError as e:
        handle_mrdr_error(e, console, state.json)
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


def _show_udl(name: str, start_time: float) -> None:
    """Display a UDL definition.
    
    Args:
        name: The UDL name to display.
        start_time: Start time for timing measurement.
    """
    import json as json_module
    
    console = state.console
    loader = UDLLoader()
    
    try:
        entry = loader.get_entry(name)
        definition = entry.definition
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            output = json_module.dumps({
                "type": "udl",
                "name": entry.name,
                "definition": {
                    "title": definition.title,
                    "description": definition.description,
                    "language": definition.language,
                    "delimiter_open": definition.delimiter_open,
                    "delimiter_close": definition.delimiter_close,
                    "bracket_open": definition.bracket_open,
                    "bracket_close": definition.bracket_close,
                    "operators": [
                        {"name": op.name, "open": op.open, "close": op.close}
                        for op in definition.operators
                    ],
                },
                "examples": entry.examples,
            }, indent=2)
            console.print(output)
        elif state.should_use_plain():
            console.print(f"UDL: {entry.name}")
            console.print(f"Title: {definition.title}")
            console.print(f"Description: {definition.description}")
            console.print(f"Language: {definition.language}")
            console.print(f"Delimiters: {definition.delimiter_open}...{definition.delimiter_close}")
            if definition.operators:
                console.print("Operators:")
                for op in definition.operators:
                    console.print(f"  {op.name}: {op.open} {op.close}")
        else:
            # Rich output
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Field", style="cyan", width=15)
            table.add_column("Value")
            
            table.add_row("Title", Text(definition.title, style="bold green"))
            table.add_row("Description", definition.description)
            table.add_row("Language", Text(definition.language, style="magenta"))
            table.add_row(
                "Delimiters",
                Text(f"{definition.delimiter_open}...{definition.delimiter_close}", style="yellow"),
            )
            table.add_row(
                "Brackets",
                Text(f"{definition.bracket_open}...{definition.bracket_close}", style="yellow"),
            )
            
            if definition.operators:
                ops_text = Text()
                for i, op in enumerate(definition.operators):
                    if i > 0:
                        ops_text.append(" | ", style="dim")
                    ops_text.append(f"{op.name} ", style="cyan")
                    ops_text.append(f"{op.open} {op.close}", style="yellow")
                table.add_row("Operators", ops_text)
            
            console.print(Panel(
                table,
                title=f"[bold]UDL: {entry.name}[/bold]",
                border_style="cyan",
            ))
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
            
    except UDLNotFoundError as e:
        if state.json:
            console.print(json_module.dumps({
                "error": "UDL not found",
                "name": name,
                "available": e.available,
            }, indent=2))
        else:
            console.print(f"[red]Error:[/red] UDL '{name}' not found.")
            if e.available:
                console.print(f"[dim]Available: {', '.join(e.available)}[/dim]")
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@jekyl_app.command("compare")
def compare(
    lang1: str = typer.Argument(..., help="First language to compare."),
    lang2: str = typer.Argument(..., help="Second language to compare."),
) -> None:
    """Display side-by-side comparison of two languages.
    
    Shows a comparison table highlighting differences and similarities
    between two programming languages' docstring syntax.
    """
    start_time = time.time()
    console = state.console
    jekyl = get_jekyl_controller()
    
    try:
        if state.json:
            # JSON output
            entry1 = jekyl.hyde.query(lang1)
            entry2 = jekyl.hyde.query(lang2)
            renderer = JSONRenderer()
            output = renderer.render({"lang1": entry1, "lang2": entry2}, "compare")
            console.print(output)
        else:
            # Rich or plain output via JekylController
            output = jekyl.compare(lang1, lang2)
            console.print(output)
        
        elapsed = (time.time() - start_time) * 1000
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms | Cache: miss[/dim]")
            
    except LanguageNotFoundError as e:
        display_language_not_found_error(e, console, state.json)
        raise typer.Exit(1)
    except MRDRError as e:
        handle_mrdr_error(e, console, state.json)
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@jekyl_app.command("doctag")
def doctag(
    tag_id: str = typer.Argument(..., help="Doctag ID to look up (e.g., DDL01, GRM05, IDC02)."),
) -> None:
    """Display doctag definition with examples.
    
    Looks up a doctag by ID and displays its definition including
    short name, full name, description, and usage example.
    
    Tag categories:
    - DDL: Document Delimiters (DDL01-DDL10)
    - GRM: Grammar definitions (GRM01-GRM10)
    - IDC: Inter-Document Commands (IDC01-IDC10)
    - FMT: Formatting rules (FMT01-FMT10)
    - DOC: Document spec markers (DOC01-DOC05)
    """
    start_time = time.time()
    console = state.console
    loader = DoctagLoader()
    
    try:
        tag = loader.get(tag_id)
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            output = json_module.dumps({
                "id": tag.id,
                "symbol": tag.symbol,
                "short_name": tag.short_name,
                "description": tag.description,
                "category": tag.category.value,
                "example": tag.example,
            }, indent=2)
            console.print(output)
        elif state.should_use_plain():
            renderer = DoctagRenderer()
            entry = DoctagEntry(
                id=tag.id,
                short_name=tag.short_name,
                full_name=tag.symbol,
                description=tag.description,
                example=tag.example,
            )
            console.print(renderer.render_entry_plain(entry))
        else:
            # Rich output
            renderer = DoctagRenderer()
            entry = DoctagEntry(
                id=tag.id,
                short_name=tag.short_name,
                full_name=tag.symbol,
                description=tag.description,
                example=tag.example,
            )
            output = renderer.render_tag_full(entry)
            console.print(output)
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
            
    except DoctagNotFoundError as e:
        if state.json:
            console.print(json_module.dumps({
                "error": "Doctag not found",
                "tag_id": tag_id,
                "available": e.available[:10],  # Show first 10
            }, indent=2))
        else:
            console.print(f"[red]Error:[/red] Doctag '{tag_id}' not found.")
            # Group available tags by category
            categories = {"DDL": [], "GRM": [], "IDC": [], "FMT": [], "DOC": []}
            for tid in e.available:
                prefix = tid[:3]
                if prefix in categories:
                    categories[prefix].append(tid)
            console.print("[dim]Available tags:[/dim]")
            for cat, tags in categories.items():
                if tags:
                    console.print(f"  [cyan]{cat}:[/cyan] {', '.join(tags)}")
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


# Example Mermaid diagrams for the diagram command
EXAMPLE_DIAGRAMS = {
    "flowchart": """flowchart TB
    A["Start"]
    B["Process Data"]
    C["Validate"]
    D["End"]
    A --> B
    B --> C
    C --> D""",
    "sequence": """sequenceDiagram
    participant Client
    participant Server
    participant Database
    Client->>Server: Request
    Server->>Database: Query
    Database->>Server: Result
    Server->>Client: Response""",
}


@jekyl_app.command("diagram")
def diagram(
    diagram_type: str = typer.Argument(
        ...,
        help="Diagram type to display (flowchart, sequence).",
    ),
) -> None:
    """Display example Mermaid diagrams rendered as ASCII art.
    
    Shows example diagrams for the specified type, demonstrating
    how Mermaid diagrams are converted to terminal-friendly ASCII.
    
    Supported diagram types:
    - flowchart: Box and arrow diagrams (TB/LR directions)
    - sequence: Participant and message diagrams
    """
    from mrdr.render.components import MermaidRenderer
    
    start_time = time.time()
    console = state.console
    
    diagram_type_lower = diagram_type.lower()
    
    if diagram_type_lower not in EXAMPLE_DIAGRAMS:
        available = ", ".join(EXAMPLE_DIAGRAMS.keys())
        if state.json:
            console.print(json_module.dumps({
                "error": "Unknown diagram type",
                "type": diagram_type,
                "available": list(EXAMPLE_DIAGRAMS.keys()),
            }, indent=2))
        else:
            console.print(f"[red]Error:[/red] Unknown diagram type '{diagram_type}'.")
            console.print(f"[dim]Available types: {available}[/dim]")
        raise typer.Exit(1)
    
    source = EXAMPLE_DIAGRAMS[diagram_type_lower]
    renderer = MermaidRenderer()
    
    try:
        output = renderer.render(source)
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            console.print(json_module.dumps({
                "type": diagram_type_lower,
                "source": source,
                "rendered": output,
            }, indent=2))
        elif state.should_use_plain():
            console.print(f"Diagram Type: {diagram_type_lower}")
            console.print()
            console.print("Source:")
            console.print(source)
            console.print()
            console.print("Rendered:")
            console.print(output)
        else:
            # Rich output
            from rich.panel import Panel
            from rich.syntax import Syntax
            
            # Show source
            syntax = Syntax(source, "text", theme="monokai")
            console.print(Panel(
                syntax,
                title=f"[bold]Mermaid Source ({diagram_type_lower})[/bold]",
                border_style="cyan",
            ))
            
            # Show rendered output
            console.print(Panel(
                output,
                title="[bold]ASCII Rendering[/bold]",
                border_style="green",
            ))
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
            
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)
