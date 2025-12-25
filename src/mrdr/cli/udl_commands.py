"""UDL subcommands for MRDR CLI.

This module implements the UDL (User Defined Language) subcommand group
for creating and managing custom docstring format definitions.
"""

import typer
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mrdr.cli.app import state
from mrdr.cli.error_handlers import display_unexpected_error
from mrdr.database.udl import UDLLoader
from mrdr.database.udl.loader import UDLNotFoundError

udl_app = typer.Typer(
    name="udl",
    help="User Defined Language operations: create, list, and manage custom docstring formats.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


def get_udl_loader() -> UDLLoader:
    """Get a configured UDLLoader instance."""
    return UDLLoader()


@udl_app.command("create")
def create(
    name: str = typer.Argument(..., help="Name for the new UDL definition."),
    title: str = typer.Option(
        None,
        "--title",
        "-t",
        help="Title for the UDL. Defaults to name if not provided.",
    ),
    description: str = typer.Option(
        "A custom UDL docstring format",
        "--description",
        "-d",
        help="Description of the UDL format.",
    ),
    delimiter_open: str = typer.Option(
        "<",
        "--open",
        "-o",
        help="Opening delimiter character (single char).",
    ),
    delimiter_close: str = typer.Option(
        ">",
        "--close",
        "-c",
        help="Closing delimiter character (single char).",
    ),
) -> None:
    """Create a new UDL (User Defined Language) template.
    
    Creates a new custom docstring format definition with the specified
    delimiters and saves it to the database/languages/udl/ directory.
    
    The new UDL will include the default dolphin (<:, :>) and walrus (:=, =:)
    operators.
    """
    console = state.console
    loader = get_udl_loader()
    
    # Validate delimiter lengths
    if len(delimiter_open) != 1:
        console.print(
            f"[red]Error:[/red] Opening delimiter must be exactly 1 character, "
            f"got '{delimiter_open}' ({len(delimiter_open)} chars)."
        )
        raise typer.Exit(1)
    
    if len(delimiter_close) != 1:
        console.print(
            f"[red]Error:[/red] Closing delimiter must be exactly 1 character, "
            f"got '{delimiter_close}' ({len(delimiter_close)} chars)."
        )
        raise typer.Exit(1)
    
    try:
        # Use title or default to name
        udl_title = title or name.replace("-", " ").replace("_", " ").title()
        
        # Create the UDL entry
        entry = loader.create_udl(
            name=name,
            title=udl_title,
            description=description,
            delimiter_open=delimiter_open,
            delimiter_close=delimiter_close,
        )
        
        # Save to disk
        file_path = loader.save_udl(entry)
        
        if state.json:
            import json
            output = json.dumps({
                "status": "created",
                "name": entry.name,
                "path": str(file_path),
                "definition": {
                    "title": entry.definition.title,
                    "description": entry.definition.description,
                    "delimiter_open": entry.definition.delimiter_open,
                    "delimiter_close": entry.definition.delimiter_close,
                    "operators": [
                        {"name": op.name, "open": op.open, "close": op.close}
                        for op in entry.definition.operators
                    ],
                },
            }, indent=2)
            console.print(output)
        elif state.should_use_plain():
            console.print(f"Created UDL: {entry.name}")
            console.print(f"Path: {file_path}")
            console.print(f"Delimiters: {delimiter_open}...{delimiter_close}")
        else:
            # Rich output
            content = Text()
            content.append("✓ ", style="green bold")
            content.append("Created UDL: ", style="")
            content.append(f"{entry.name}\n\n", style="bold cyan")
            content.append("Path: ", style="dim")
            content.append(f"{file_path}\n", style="")
            content.append("Delimiters: ", style="dim")
            content.append(f"{delimiter_open}", style="yellow")
            content.append("...", style="dim")
            content.append(f"{delimiter_close}\n", style="yellow")
            content.append("Operators: ", style="dim")
            content.append("dolphin ", style="cyan")
            content.append("<:", style="yellow")
            content.append(" ", style="")
            content.append(":>", style="yellow")
            content.append(" | walrus ", style="cyan")
            content.append(":=", style="yellow")
            content.append(" ", style="")
            content.append("=:", style="yellow")
            
            console.print(Panel(content, title="UDL Created", border_style="green"))
            
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@udl_app.command("list")
def list_udls() -> None:
    """Display all registered UDL definitions.
    
    Shows a list of all custom docstring format definitions
    stored in the database/languages/udl/ directory.
    """
    console = state.console
    loader = get_udl_loader()
    
    try:
        udl_names = loader.list_udls()
        
        if state.json:
            import json
            output = json.dumps({
                "udls": udl_names,
                "count": len(udl_names),
            }, indent=2)
            console.print(output)
        elif state.should_use_plain():
            if not udl_names:
                console.print("No UDL definitions found.")
            else:
                console.print(f"UDL Definitions ({len(udl_names)}):")
                for name in udl_names:
                    console.print(f"  - {name}")
        else:
            # Rich output
            if not udl_names:
                console.print(Panel(
                    "[dim]No UDL definitions found.[/dim]\n\n"
                    "Create one with: [cyan]mrdr hyde udl create <name>[/cyan]",
                    title="UDL Definitions",
                    border_style="yellow",
                ))
            else:
                table = Table(title="UDL Definitions", show_header=True)
                table.add_column("#", style="dim", width=4)
                table.add_column("Name", style="cyan")
                
                for idx, name in enumerate(udl_names, 1):
                    table.add_row(str(idx), name)
                
                console.print(table)
                console.print(f"\n[dim]Total: {len(udl_names)} UDL(s)[/dim]")
                
    except Exception as e:
        display_unexpected_error(e, console, state.json, state.debug)
        raise typer.Exit(1)


@udl_app.command("show")
def show_udl(
    name: str = typer.Argument(..., help="Name of the UDL to display."),
) -> None:
    """Display details of a specific UDL definition.
    
    Shows the complete definition including title, description,
    delimiters, and operators for the specified UDL.
    """
    console = state.console
    loader = get_udl_loader()
    
    try:
        entry = loader.get_entry(name)
        definition = entry.definition
        
        if state.json:
            import json
            output = json.dumps({
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
                "created_at": entry.created_at,
            }, indent=2)
            console.print(output)
        elif state.should_use_plain():
            console.print(f"UDL: {entry.name}")
            console.print(f"Title: {definition.title}")
            console.print(f"Description: {definition.description}")
            console.print(f"Language: {definition.language}")
            console.print(f"Delimiters: {definition.delimiter_open}...{definition.delimiter_close}")
            console.print(f"Brackets: {definition.bracket_open}...{definition.bracket_close}")
            if definition.operators:
                console.print("Operators:")
                for op in definition.operators:
                    console.print(f"  - {op.name}: {op.open} {op.close}")
        else:
            # Rich output
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Field", style="cyan", width=15)
            table.add_column("Value")
            
            table.add_row("Title", Text(definition.title, style="bold"))
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
            
            if entry.created_at:
                table.add_row("Created", Text(entry.created_at, style="dim"))
            
            console.print(Panel(table, title=f"[bold]{entry.name}[/bold]", border_style="cyan"))
            
    except UDLNotFoundError as e:
        if state.json:
            import json
            console.print(json.dumps({
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
