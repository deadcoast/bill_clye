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
    card: bool = typer.Option(
        False,
        "--card",
        help="Render output using card grid layout.",
    ),
    accordion: bool = typer.Option(
        False,
        "--accordion",
        help="Render output using accordion layout with expandable sections.",
    ),
    gutter: bool = typer.Option(
        False,
        "--gutter",
        help="Render code examples with line number gutter.",
    ),
    start_line: int = typer.Option(
        1,
        "--start-line",
        help="Starting line number for gutter display (default: 1).",
    ),
) -> None:
    """Display docstring syntax with Rich formatting.
    
    Renders the docstring syntax for a language using the Golden Screen
    layout with header bar, primary payload, and hints bar.
    
    Use 'udl:<name>' to display a custom UDL definition.
    
    Visual modes:
    - --card: Display as a card grid layout
    - --accordion: Display with expandable sections
    - --gutter: Display code with line numbers
    """
    from mrdr.cli.visual_commands import VisualOptions, apply_visual_options
    
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
    
    # Visual options
    visual_opts = VisualOptions(
        card=card,
        accordion=accordion,
        gutter=gutter,
        start_line=start_line,
        plain=state.should_use_plain(),
    )
    
    try:
        if state.json:
            # JSON output
            entry = jekyl.hyde.query(language)
            renderer = JSONRenderer()
            output = renderer.render(entry, "show")
            console.print(output)
        elif card or accordion or gutter:
            # Visual mode output
            entry = jekyl.hyde.query(language)
            output = apply_visual_options(entry, visual_opts, console)
            if output:
                console.print(output)
            else:
                # Fallback to standard rendering
                output = jekyl.show(language, options)
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


@jekyl_app.command("conflicts")
def conflicts() -> None:
    """Display all known syntax conflicts in table format.
    
    Shows a table of programming languages that share identical
    delimiter syntax, along with resolution guidance for each conflict.
    
    Conflicts occur when multiple languages use the same delimiter
    pattern but with different attachment rules (e.g., Python vs Julia
    both use triple quotes but attach differently).
    """
    from mrdr.render.components import ConflictDisplay, KNOWN_CONFLICTS
    
    start_time = time.time()
    console = state.console
    display = ConflictDisplay()
    
    try:
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            conflicts_data = []
            for conflict in KNOWN_CONFLICTS:
                conflicts_data.append({
                    "delimiter": conflict.delimiter,
                    "languages": conflict.languages,
                    "resolution": conflict.resolution,
                    "attachment_rules": conflict.attachment_rules,
                })
            console.print(json_module.dumps({
                "conflicts": conflicts_data,
                "count": len(conflicts_data),
            }, indent=2))
        elif state.should_use_plain():
            console.print(display.render_plain())
        else:
            # Rich output - render table
            table_output = display.render_table()
            console.print(table_output)
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
            
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@jekyl_app.command("table")
def table(
    master: bool = typer.Option(
        False,
        "--master",
        help="Display the master docstring table with all languages.",
    ),
    columns: str = typer.Option(
        None,
        "--columns",
        "-c",
        help="Comma-separated list of columns to display (e.g., 'language,syntax.type').",
    ),
    filter_opt: str = typer.Option(
        None,
        "--filter",
        "-f",
        help="Filter rows by field=value (e.g., 'syntax.type=literal').",
    ),
    sort: str = typer.Option(
        None,
        "--sort",
        "-s",
        help="Sort by field name. Prefix with '-' for descending (e.g., '-language').",
    ),
    export: str = typer.Option(
        None,
        "--export",
        "-e",
        help="Export format: 'md' for markdown.",
    ),
    page: int = typer.Option(
        1,
        "--page",
        "-p",
        help="Page number for paginated output.",
    ),
    page_size: int = typer.Option(
        20,
        "--page-size",
        help="Number of rows per page.",
    ),
) -> None:
    """Display database tables with filtering, sorting, and pagination.
    
    Renders the docstring database as a table with various options
    for filtering, sorting, and exporting data.
    
    Examples:
        mrdr jekyl table --master
        mrdr jekyl table --master --columns language,syntax.type
        mrdr jekyl table --master --filter syntax.type=literal
        mrdr jekyl table --master --sort language
        mrdr jekyl table --master --export md
    """
    from mrdr.database.loader import DatabaseLoader
    from mrdr.render.components import AdvancedTableRenderer, TableConfig
    
    start_time = time.time()
    console = state.console
    
    if not master:
        console.print("[yellow]Hint:[/yellow] Use --master to display the master docstring table.")
        raise typer.Exit(0)
    
    try:
        # Load database
        loader = DatabaseLoader()
        entries = loader.get_entries()
        
        # Convert entries to flat dictionaries for table display
        data = []
        for entry in entries:
            row = {
                "language": entry.language,
                "syntax_type": entry.syntax.type if entry.syntax else "",
                "syntax_start": entry.syntax.start if entry.syntax else "",
                "syntax_end": entry.syntax.end or "" if entry.syntax else "",
                "syntax_location": entry.syntax.location if entry.syntax else "",
                "tags": ", ".join(entry.tags) if entry.tags else "",
                "conflict_ref": entry.conflict_ref or "",
            }
            data.append(row)
        
        # Parse columns option
        column_list = None
        if columns:
            column_list = [c.strip() for c in columns.split(",")]
        
        # Parse filter option
        filter_field = None
        filter_value = None
        if filter_opt:
            if "=" in filter_opt:
                filter_field, filter_value = filter_opt.split("=", 1)
                filter_field = filter_field.strip()
                filter_value = filter_value.strip()
        
        # Parse sort option
        sort_field = None
        sort_descending = False
        if sort:
            if sort.startswith("-"):
                sort_descending = True
                sort_field = sort[1:]
            else:
                sort_field = sort
        
        # Create config
        config = TableConfig(
            columns=column_list,
            filter_field=filter_field,
            filter_value=filter_value,
            sort_field=sort_field,
            sort_descending=sort_descending,
            page_size=page_size,
            current_page=page,
        )
        
        renderer = AdvancedTableRenderer(data=data, config=config)
        elapsed = (time.time() - start_time) * 1000
        
        # Handle export
        if export:
            if export.lower() == "md":
                console.print(renderer.export_markdown())
            else:
                console.print(f"[red]Error:[/red] Unknown export format '{export}'. Use 'md' for markdown.")
                raise typer.Exit(1)
        elif state.json:
            # JSON output
            filtered_data = renderer._apply_filter()
            sorted_data = renderer._apply_sort(filtered_data)
            console.print(json_module.dumps({
                "data": sorted_data,
                "total_rows": len(sorted_data),
                "page": page,
                "page_size": page_size,
            }, indent=2))
        elif state.should_use_plain():
            console.print(renderer.render_plain())
        else:
            # Rich output
            output = renderer.render()
            console.print(output)
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms | Rows: {renderer.get_total_rows()}[/dim]")
            
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] Database not found: {e}")
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)
