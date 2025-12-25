"""Docstring command for MRDR CLI.

This module implements the docstring command for displaying docstring
syntax examples for programming languages.

Feature: mrdr-visual-integration
**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6**
"""

import time
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from mrdr.cli.app import state
from mrdr.cli.error_handlers import (
    display_language_not_found_error,
    display_unexpected_error,
    handle_mrdr_error,
)
from mrdr.factory import get_hyde_controller
from mrdr.render.json_renderer import JSONRenderer
from mrdr.render.plain_renderer import PlainRenderer
from mrdr.render.python_style import (
    STYLE_METADATA,
    STYLE_TEMPLATES,
    PythonDocstringStyle,
    PythonStyleRenderer,
)
from mrdr.utils.errors import LanguageNotFoundError, MRDRError


# Legacy Python docstring styles (kept for backward compatibility)
# New code should use PythonStyleRenderer from mrdr.render.python_style
PYTHON_STYLES = {
    "sphinx": {
        "name": "Sphinx (reStructuredText)",
        "example": '''"""Short summary.

:param name: Description of parameter.
:type name: str
:returns: Description of return value.
:rtype: bool
:raises ValueError: If name is empty.
"""''',
    },
    "google": {
        "name": "Google Style",
        "example": '''"""Short summary.

Args:
    name: Description of parameter.

Returns:
    Description of return value.

Raises:
    ValueError: If name is empty.
"""''',
    },
    "numpy": {
        "name": "NumPy Style",
        "example": '''"""Short summary.

Parameters
----------
name : str
    Description of parameter.

Returns
-------
bool
    Description of return value.

Raises
------
ValueError
    If name is empty.
"""''',
    },
    "epytext": {
        "name": "Epytext (Epydoc)",
        "example": '''"""Short summary.

@param name: Description of parameter.
@type name: str
@return: Description of return value.
@rtype: bool
@raise ValueError: If name is empty.
"""''',
    },
    "pep257": {
        "name": "PEP 257",
        "example": '''"""Short summary.

Extended description of function.

Arguments:
name -- Description of parameter.

Returns:
Description of return value.
"""''',
    },
}


def docstring_command(
    language: Optional[str] = typer.Argument(
        None, help="Programming language to display docstring syntax for."
    ),
    style: Optional[str] = typer.Option(
        None,
        "--style",
        "-s",
        help="Python docstring style: sphinx, google, numpy, epytext, pep257.",
    ),
    all_languages: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="List all supported languages with their signatures.",
    ),
    all_styles: bool = typer.Option(
        False,
        "--all-styles",
        help="Display all Python docstring styles in a comparison view.",
    ),
) -> None:
    """Display docstring syntax for a programming language.
    
    Shows the docstring syntax specification including delimiters,
    attachment rules, and a code example for the specified language.
    
    For Python, use --style to see specific docstring style formats,
    or --all-styles to see all styles in a comparison view.
    """
    start_time = time.time()
    console = state.console
    hyde = get_hyde_controller()
    
    # Handle --all-styles flag (Python comparison view)
    if all_styles:
        _display_all_python_styles(console, start_time)
        return
    
    # Handle --all flag
    if all_languages:
        _display_all_languages(hyde, console, start_time)
        return
    
    # Require language if not --all or --all-styles
    if not language:
        console.print("[red]Error:[/red] Please specify a language or use --all.")
        console.print("[dim]Example: mrdr docstring python[/dim]")
        console.print("[dim]Use --all-styles to see all Python docstring styles[/dim]")
        raise typer.Exit(1)
    
    # Handle Python style selection
    if style and language.lower() == "python":
        _display_python_style(style, console, start_time)
        return
    elif style and language.lower() != "python":
        console.print("[yellow]Warning:[/yellow] --style is only supported for Python.")
    
    # Display docstring for language
    try:
        entry = hyde.query(language)
        elapsed = (time.time() - start_time) * 1000
        
        if state.json:
            renderer = JSONRenderer()
            data = {
                "language": entry.language,
                "syntax": {
                    "start": entry.syntax.start,
                    "end": entry.syntax.end,
                    "type": entry.syntax.type,
                    "location": entry.syntax.location,
                },
                "tags": entry.tags,
            }
            if entry.conflict_ref:
                data["conflict_ref"] = entry.conflict_ref
            if entry.example_content:
                data["example_content"] = entry.example_content
            console.print(renderer.render(data, "show"))
        elif state.should_use_plain():
            renderer = PlainRenderer()
            console.print(renderer.render(entry, "show"))
        else:
            _display_rich_docstring(entry, console)
        
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


def _display_all_languages(hyde, console: Console, start_time: float) -> None:
    """Display all languages with their signatures.
    
    Args:
        hyde: HydeController instance for data operations.
        console: Rich Console for output.
        start_time: Start time for timing calculation.
    """
    languages = hyde.list_languages()
    elapsed = (time.time() - start_time) * 1000
    
    if state.json:
        entries = []
        for lang in languages:
            try:
                entry = hyde.query(lang)
                entries.append({
                    "language": entry.language,
                    "start": entry.syntax.start,
                    "end": entry.syntax.end,
                    "type": entry.syntax.type,
                })
            except LanguageNotFoundError:
                pass
        renderer = JSONRenderer()
        console.print(renderer.render({"languages": entries, "count": len(entries)}, "list"))
    elif state.should_use_plain():
        lines = ["=== Supported Languages ===", ""]
        for lang in sorted(languages):
            try:
                entry = hyde.query(lang)
                sig = f"{repr(entry.syntax.start)} ... {repr(entry.syntax.end) if entry.syntax.end else '(line)'}"
                lines.append(f"  {lang:<15} {sig}")
            except LanguageNotFoundError:
                lines.append(f"  {lang:<15} (error loading)")
        lines.extend(["", f"Total: {len(languages)} languages", ""])
        console.print("\n".join(lines))
    else:
        table = Table(title="Supported Languages", show_header=True)
        table.add_column("Language", style="cyan")
        table.add_column("Start", style="yellow")
        table.add_column("End", style="yellow")
        table.add_column("Type", style="magenta")
        
        for lang in sorted(languages):
            try:
                entry = hyde.query(lang)
                end_val = repr(entry.syntax.end) if entry.syntax.end else "(line)"
                table.add_row(
                    lang,
                    repr(entry.syntax.start),
                    end_val,
                    str(entry.syntax.type),
                )
            except LanguageNotFoundError:
                table.add_row(lang, "-", "-", "-")
        
        console.print(table)
        console.print(f"\n[dim]Total: {len(languages)} languages[/dim]")
    
    if state.debug:
        console.print(f"\n[dim]Query time: {elapsed:.2f}ms | Cache: miss[/dim]")


def _display_all_python_styles(console: Console, start_time: float) -> None:
    """Display all Python docstring styles in a comparison view.
    
    Args:
        console: Rich Console for output.
        start_time: Start time for timing calculation.
    """
    elapsed = (time.time() - start_time) * 1000
    renderer = PythonStyleRenderer(console=console)
    
    if state.json:
        # JSON output with all styles
        styles_data = []
        for style in PythonDocstringStyle:
            metadata = STYLE_METADATA[style]
            styles_data.append({
                "style": style.value,
                "name": metadata["name"],
                "description": metadata["description"],
                "markers": metadata["markers"],
                "example": STYLE_TEMPLATES[style],
            })
        json_renderer = JSONRenderer()
        console.print(json_renderer.render({
            "language": "Python",
            "styles": styles_data,
            "count": len(styles_data),
        }, "list"))
    elif state.should_use_plain():
        # Plain text output
        console.print(renderer.render_all_plain())
    else:
        # Rich output with panels
        console.print("[bold cyan]Python Docstring Styles Comparison[/bold cyan]\n")
        
        # First show summary table
        console.print(renderer.render_style_table())
        console.print()
        
        # Then show each style
        for panel in renderer.render_all_styles():
            console.print(panel)
            console.print()
    
    if state.debug:
        console.print(f"\n[dim]Query time: {elapsed:.2f}ms[/dim]")


def _display_python_style(style: str, console: Console, start_time: float) -> None:
    """Display a specific Python docstring style.
    
    Uses the PythonStyleRenderer for consistent rendering.
    
    Args:
        style: The style name (sphinx, google, numpy, epytext, pep257).
        console: Rich Console for output.
        start_time: Start time for timing calculation.
    """
    style_lower = style.lower()
    elapsed = (time.time() - start_time) * 1000
    
    # Validate style
    valid_styles = [s.value for s in PythonDocstringStyle]
    if style_lower not in valid_styles:
        console.print(f"[red]Error:[/red] Unknown style '{style}'.")
        console.print(f"[dim]Valid styles: {', '.join(valid_styles)}[/dim]")
        raise typer.Exit(1)
    
    # Get the enum value
    style_enum = PythonDocstringStyle(style_lower)
    renderer = PythonStyleRenderer(console=console)
    metadata = STYLE_METADATA[style_enum]
    
    if state.json:
        data = {
            "language": "Python",
            "style": style_lower,
            "style_name": metadata["name"],
            "description": metadata["description"],
            "markers": metadata["markers"],
            "example": STYLE_TEMPLATES[style_enum],
        }
        json_renderer = JSONRenderer()
        console.print(json_renderer.render(data, "show"))
    elif state.should_use_plain():
        console.print(renderer.render_plain(style_enum))
    else:
        console.print(renderer.render_style(style_enum))
    
    if state.debug:
        console.print(f"\n[dim]Query time: {elapsed:.2f}ms[/dim]")


def _display_rich_docstring(entry, console: Console) -> None:
    """Display docstring entry with Rich formatting."""
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
    
    if entry.conflict_ref:
        table.add_row("Conflict", Text(entry.conflict_ref, style="red"))
    
    # Add example if available
    if entry.example_content:
        table.add_row("", Text(""))  # Spacer
        table.add_row("Example", Text(""))
        syntax = Syntax(
            entry.example_content,
            entry.language.lower(),
            theme="monokai",
            line_numbers=False,
        )
        table.add_row("", syntax)
    
    console.print(Panel(table, title=f"[bold]{entry.language}[/bold] Docstring Syntax"))
