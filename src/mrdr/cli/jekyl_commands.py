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
from mrdr.database.doctag.loader import DoctagNotFoundError
from mrdr.database.udl.loader import UDLNotFoundError
from mrdr.factory import (
    create_jekyl_controller,
    get_conflict_loader,
    get_doctag_loader,
    get_dictionary_loader,
    get_python_styles_loader,
    get_udl_loader,
)
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
    loader = get_udl_loader()
    
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
    loader = get_doctag_loader()
    
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
    from mrdr.render.components import ConflictDisplay
    
    start_time = time.time()
    console = state.console
    display = ConflictDisplay()
    
    try:
        # Load conflicts from the database
        loader = get_conflict_loader()
        conflict_entries = loader.get_all()
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            conflicts_data = []
            for conflict in conflict_entries:
                conflicts_data.append({
                    "id": conflict.id,
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


@jekyl_app.command("pystyle")
def pystyle(
    style_name: str = typer.Argument(
        ...,
        help="Python docstring style name (sphinx, google, numpy, epytext, pep257).",
    ),
) -> None:
    """Display Python docstring style definition with examples.
    
    Shows the markers, template code, and rules for a specific
    Python docstring style.
    
    Available styles:
    - sphinx: reStructuredText style with :param:, :type:, :return:, :rtype:
    - google: Google style with Args:, Returns: sections
    - numpy: NumPy style with Parameters, Returns headers and dashes
    - epytext: Epytext style with @param, @type, @return markers
    - pep257: Minimal PEP 257 style
    """
    from mrdr.database.python_styles.loader import PythonStyleNotFoundError
    
    start_time = time.time()
    console = state.console
    loader = get_python_styles_loader()
    
    try:
        style = loader.get_style(style_name)
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            markers_data = [
                {"name": m.name, "syntax": m.syntax, "description": m.description}
                for m in style.markers
            ]
            output = json_module.dumps({
                "name": style.name,
                "description": style.description,
                "markers": markers_data,
                "template_code": style.template_code,
                "rules": style.rules,
            }, indent=2)
            console.print(output)
        elif state.should_use_plain():
            console.print(f"Style: {style.name}")
            console.print(f"Description: {style.description}")
            console.print()
            console.print("Markers:")
            for marker in style.markers:
                console.print(f"  {marker.name}: {marker.syntax}")
                console.print(f"    {marker.description}")
            console.print()
            console.print("Template:")
            console.print(style.template_code)
            console.print()
            console.print("Rules:")
            for rule in style.rules:
                console.print(f"  - {rule}")
        else:
            # Rich output
            from rich.syntax import Syntax
            
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Field", style="cyan", width=15)
            table.add_column("Value")
            
            table.add_row("Style", Text(style.name.upper(), style="bold green"))
            table.add_row("Description", style.description)
            
            # Markers
            if style.markers:
                markers_text = Text()
                for i, marker in enumerate(style.markers):
                    if i > 0:
                        markers_text.append("\n")
                    markers_text.append(f"{marker.name}: ", style="cyan")
                    markers_text.append(f"{marker.syntax}", style="yellow")
                table.add_row("Markers", markers_text)
            
            # Rules
            if style.rules:
                rules_text = Text()
                for i, rule in enumerate(style.rules):
                    if i > 0:
                        rules_text.append("\n")
                    rules_text.append(f"• {rule}", style="dim")
                table.add_row("Rules", rules_text)
            
            console.print(Panel(
                table,
                title=f"[bold]Python Style: {style.name.upper()}[/bold]",
                border_style="cyan",
            ))
            
            # Show template code
            if style.template_code:
                syntax = Syntax(
                    style.template_code,
                    "python",
                    theme="monokai",
                    line_numbers=True,
                )
                console.print(Panel(
                    syntax,
                    title="[bold]Template Code[/bold]",
                    border_style="green",
                ))
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
            
    except PythonStyleNotFoundError as e:
        if state.json:
            console.print(json_module.dumps({
                "error": "Python style not found",
                "style": style_name,
                "available": e.available,
            }, indent=2))
        else:
            console.print(f"[red]Error:[/red] Python style '{style_name}' not found.")
            if e.available:
                console.print(f"[dim]Available styles: {', '.join(e.available)}[/dim]")
        raise typer.Exit(1)
    except FileNotFoundError:
        console.print("[red]Error:[/red] Python styles database not found.")
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@jekyl_app.command("pystyles")
def pystyles() -> None:
    """List all available Python docstring styles.
    
    Shows a summary table of all Python docstring styles with their
    key markers and descriptions.
    """
    start_time = time.time()
    console = state.console
    loader = get_python_styles_loader()
    
    try:
        styles = loader.get_all()
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            styles_data = []
            for style in styles:
                markers_data = [
                    {"name": m.name, "syntax": m.syntax}
                    for m in style.markers
                ]
                styles_data.append({
                    "name": style.name,
                    "description": style.description,
                    "markers": markers_data,
                })
            console.print(json_module.dumps({
                "styles": styles_data,
                "count": len(styles_data),
            }, indent=2))
        elif state.should_use_plain():
            console.print("Python Docstring Styles:")
            console.print()
            for style in styles:
                console.print(f"{style.name}:")
                console.print(f"  {style.description}")
                if style.markers:
                    markers = ", ".join(m.syntax for m in style.markers[:3])
                    console.print(f"  Markers: {markers}")
                console.print()
        else:
            # Rich output
            table = Table(title="Python Docstring Styles", show_header=True)
            table.add_column("Style", style="cyan")
            table.add_column("Description")
            table.add_column("Key Markers", style="yellow")
            
            for style in styles:
                markers = ", ".join(m.syntax for m in style.markers[:3])
                if len(style.markers) > 3:
                    markers += "..."
                table.add_row(style.name.upper(), style.description, markers)
            
            console.print(table)
            console.print(f"\n[dim]Total: {len(styles)} styles[/dim]")
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
            
    except FileNotFoundError:
        console.print("[red]Error:[/red] Python styles database not found.")
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@jekyl_app.command("dict")
def dictionary_lookup(
    term: str = typer.Argument(
        ...,
        help="Dictionary term to look up (name or alias).",
    ),
) -> None:
    """Look up a term in the MRDR dictionary hierarchy.
    
    Shows the term definition, hierarchy level, and path from root.
    
    Hierarchy levels:
    - grandparent: Top-level functions (NOTE, CLAIM, LANG_USE, etc.)
    - parent: Parent commands (apd, objacc)
    - child: Child functions (sem, def, dstr, etc.)
    - grandchild: Grandchild entries (val, value)
    """
    from mrdr.database.dictionary.loader import DictionaryNotFoundError
    
    start_time = time.time()
    console = state.console
    loader = get_dictionary_loader()
    
    try:
        entry = loader.get_term(term)
        path = loader.get_hierarchy_path(term)
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            path_data = [
                {"name": p.name, "alias": p.alias, "level": p.level.value}
                for p in path
            ]
            output = json_module.dumps({
                "name": entry.name,
                "alias": entry.alias,
                "level": entry.level.value,
                "description": entry.description,
                "children": entry.children,
                "hierarchy_path": path_data,
            }, indent=2)
            console.print(output)
        elif state.should_use_plain():
            console.print(f"Term: {entry.name}")
            console.print(f"Alias: {entry.alias}")
            console.print(f"Level: {entry.level.value}")
            console.print(f"Description: {entry.description}")
            if entry.children:
                console.print(f"Children: {', '.join(entry.children)}")
            if path:
                path_str = " > ".join(p.name for p in path)
                console.print(f"Path: {path_str}")
        else:
            # Rich output
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Field", style="cyan", width=15)
            table.add_column("Value")
            
            table.add_row("Term", Text(entry.name, style="bold green"))
            table.add_row("Alias", Text(entry.alias, style="yellow"))
            table.add_row("Level", Text(entry.level.value, style="magenta"))
            table.add_row("Description", entry.description)
            
            if entry.children:
                children_text = ", ".join(entry.children)
                table.add_row("Children", Text(children_text, style="dim"))
            
            console.print(Panel(
                table,
                title=f"[bold]Dictionary: {entry.name}[/bold]",
                border_style="cyan",
            ))
            
            # Show hierarchy path
            if path and len(path) > 1:
                path_text = Text()
                path_text.append("\nHierarchy Path:\n", style="bold")
                for i, p in enumerate(path):
                    indent = "  " * i
                    if i == len(path) - 1:
                        path_text.append(f"{indent}└── ", style="dim")
                        path_text.append(f"{p.name}", style="bold green")
                    else:
                        path_text.append(f"{indent}├── ", style="dim")
                        path_text.append(f"{p.name}\n", style="cyan")
                console.print(path_text)
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
            
    except DictionaryNotFoundError as e:
        if state.json:
            console.print(json_module.dumps({
                "error": "Dictionary term not found",
                "term": term,
                "available": e.available[:10],
            }, indent=2))
        else:
            console.print(f"[red]Error:[/red] Dictionary term '{term}' not found.")
            if e.available:
                console.print(f"[dim]Available terms: {', '.join(e.available[:10])}...[/dim]")
        raise typer.Exit(1)
    except FileNotFoundError:
        console.print("[red]Error:[/red] Dictionary database not found.")
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@jekyl_app.command("dictlist")
def dictionary_list(
    level: str = typer.Option(
        None,
        "--level",
        "-l",
        help="Filter by hierarchy level (grandparent, parent, child, grandchild).",
    ),
) -> None:
    """List all terms in the MRDR dictionary hierarchy.
    
    Shows all dictionary terms organized by hierarchy level.
    Use --level to filter by a specific level.
    """
    start_time = time.time()
    console = state.console
    loader = get_dictionary_loader()
    
    try:
        if level:
            entries = loader.get_entries_by_level(level)
        else:
            entries = loader.get_all()
        
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            entries_data = [
                {
                    "name": e.name,
                    "alias": e.alias,
                    "level": e.level.value,
                    "description": e.description,
                }
                for e in entries
            ]
            console.print(json_module.dumps({
                "entries": entries_data,
                "count": len(entries_data),
                "filter_level": level,
            }, indent=2))
        elif state.should_use_plain():
            if level:
                console.print(f"Dictionary Terms (level: {level}):")
            else:
                console.print("Dictionary Terms:")
            console.print()
            for entry in entries:
                console.print(f"{entry.name} ({entry.alias}): {entry.level.value}")
                console.print(f"  {entry.description}")
        else:
            # Rich output
            title = "Dictionary Terms" + (f" (level: {level})" if level else "")
            table = Table(title=title, show_header=True)
            table.add_column("Name", style="cyan")
            table.add_column("Alias", style="yellow")
            table.add_column("Level", style="magenta")
            table.add_column("Description")
            
            for entry in entries:
                table.add_row(
                    entry.name,
                    entry.alias,
                    entry.level.value,
                    entry.description[:50] + "..." if len(entry.description) > 50 else entry.description,
                )
            
            console.print(table)
            console.print(f"\n[dim]Total: {len(entries)} terms[/dim]")
        
        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
            
    except FileNotFoundError:
        console.print("[red]Error:[/red] Dictionary database not found.")
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)
