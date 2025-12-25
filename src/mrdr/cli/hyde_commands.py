"""Hyde subcommands for MRDR CLI.

This module implements the hyde subcommand group for back-end data operations
including query, list, inspect, export, and hierarchy commands.
"""

import time
from typing import Optional

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
from mrdr.cli.udl_commands import udl_app
from mrdr.database.hierarchy import build_dictionary_hierarchy, get_all_terms
from mrdr.factory import get_hyde_controller
from mrdr.render.components import HierarchyDisplay
from mrdr.render.json_renderer import JSONRenderer
from mrdr.render.plain_renderer import PlainRenderer
from mrdr.utils.errors import LanguageNotFoundError, MRDRError

hyde_app = typer.Typer(
    name="hyde",
    help="Back-end data operations: query, list, inspect, and export.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Register UDL subcommand group
hyde_app.add_typer(udl_app, name="udl")


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
        display_language_not_found_error(e, console, state.json)
        raise typer.Exit(1)
    except MRDRError as e:
        handle_mrdr_error(e, console, state.json)
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
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
        display_language_not_found_error(e, console, state.json)
        raise typer.Exit(1)
    except MRDRError as e:
        handle_mrdr_error(e, console, state.json)
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
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
        display_language_not_found_error(e, console, state.json)
        raise typer.Exit(1)
    except MRDRError as e:
        handle_mrdr_error(e, console, state.json)
        raise typer.Exit(1)
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@hyde_app.command("hierarchy")
def hierarchy(
    term: Optional[str] = typer.Argument(
        None, help="Term to look up in the dictionary hierarchy."
    ),
) -> None:
    """Display the dictionary hierarchy or look up a specific term.

    Shows the MRDR dictionary hierarchy tree structure. If a term is provided,
    displays the term's position in the hierarchy with its ancestors.

    Examples:
        mrdr hyde hierarchy          # Show full hierarchy
        mrdr hyde hierarchy sem      # Look up 'sem' term
        mrdr hyde hierarchy NOTE     # Look up 'NOTE' term
    """
    start_time = time.time()
    console = state.console

    root = build_dictionary_hierarchy()
    display = HierarchyDisplay(root=root)

    if term:
        # Look up specific term
        found_node = display.find_node(term)
        if found_node:
            ancestors = display.get_ancestors(term)
            elapsed = (time.time() - start_time) * 1000

            if state.json:
                import json

                result = {
                    "term": found_node.name,
                    "alias": found_node.alias,
                    "level": found_node.level.value,
                    "description": found_node.description,
                    "ancestors": [
                        {"name": a.name, "alias": a.alias, "level": a.level.value}
                        for a in ancestors
                    ],
                }
                console.print(json.dumps(result, indent=2))
            elif state.should_use_plain():
                console.print(f"Term: {found_node.name}")
                console.print(f"Alias: {found_node.alias}")
                console.print(f"Level: {found_node.level.value}")
                console.print(f"Description: {found_node.description}")
                if ancestors:
                    path = " > ".join(a.name for a in ancestors)
                    console.print(f"Path: {path} > {found_node.name}")
            else:
                # Rich output - show term info and path
                text = Text()
                text.append("Term: ", style="dim")
                text.append(f"{found_node.name}", style="bold cyan")
                text.append(f" ({found_node.alias})\n", style="dim")
                text.append("Level: ", style="dim")
                text.append(f"{found_node.level.value}\n", style="magenta")
                if found_node.description:
                    text.append("Description: ", style="dim")
                    text.append(f"{found_node.description}\n", style="italic")
                if ancestors:
                    text.append("\nHierarchy Path:\n", style="bold")
                    path_parts = [a.name for a in ancestors] + [found_node.name]
                    for i, part in enumerate(path_parts):
                        indent = "  " * i
                        if i == len(path_parts) - 1:
                            text.append(f"{indent}└── ", style="dim")
                            text.append(f"{part}", style="bold green")
                        else:
                            text.append(f"{indent}├── ", style="dim")
                            text.append(f"{part}\n", style="cyan")

                console.print(Panel(text, title="[bold]Hierarchy Lookup[/bold]"))

            if state.debug:
                console.print(f"\n[dim]Lookup time: {elapsed:.2f}ms[/dim]")
        else:
            # Term not found - suggest similar terms
            all_terms = get_all_terms()
            suggestions = [t for t in all_terms if term.lower() in t.lower()][:5]

            console.print(f"[red]Error:[/red] Term '{term}' not found in hierarchy.")
            if suggestions:
                console.print(f"[dim]Did you mean: {', '.join(suggestions)}?[/dim]")
            raise typer.Exit(1)
    else:
        # Show full hierarchy
        elapsed = (time.time() - start_time) * 1000

        if state.json:
            import json

            def node_to_dict(node):
                return {
                    "name": node.name,
                    "alias": node.alias,
                    "level": node.level.value,
                    "description": node.description,
                    "children": [node_to_dict(c) for c in node.children],
                }

            console.print(json.dumps(node_to_dict(root), indent=2))
        elif state.should_use_plain():
            output = display.render()
            # Strip ANSI codes for plain output
            import re

            plain_output = re.sub(r"\x1b\[[0-9;]*m", "", output)
            console.print(plain_output)
        else:
            tree = display.render_tree()
            console.print(Panel(tree, title="[bold]MRDR Dictionary Hierarchy[/bold]"))

        if state.debug:
            console.print(f"\n[dim]Render time: {elapsed:.2f}ms[/dim]")
