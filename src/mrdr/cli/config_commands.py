"""Config subcommands for MRDR CLI.

This module implements the config subcommand group for viewing and
modifying CLI configuration settings.
"""

import json

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mrdr.cli.app import state
from mrdr.factory import get_config_loader
from mrdr.render.json_renderer import JSONRenderer

config_app = typer.Typer(
    name="config",
    help="View and modify CLI configuration settings.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@config_app.command("show")
def show() -> None:
    """Display current configuration settings.
    
    Shows all configuration values including defaults, file settings,
    and environment variable overrides.
    """
    console = state.console
    loader = get_config_loader()
    
    config_dict = loader.show()
    
    if state.json:
        renderer = JSONRenderer()
        console.print(renderer.render(config_dict, "config"))
    elif state.should_use_plain():
        lines = ["=== MRDR Configuration ===", ""]
        
        for key, value in config_dict.items():
            if isinstance(value, dict):
                lines.append(f"{key}:")
                for k, v in value.items():
                    lines.append(f"    {k}: {v}")
            else:
                lines.append(f"{key}: {value}")
        
        lines.extend(["", f"Config file: {loader.config_path}", ""])
        console.print("\n".join(lines))
    else:
        table = Table(show_header=True, title="MRDR Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        def add_config_rows(d: dict, prefix: str = "") -> None:
            for key, value in d.items():
                full_key = f"{prefix}{key}" if prefix else key
                if isinstance(value, dict):
                    add_config_rows(value, f"{full_key}.")
                else:
                    table.add_row(full_key, str(value))
        
        add_config_rows(config_dict)
        
        console.print(table)
        console.print(f"\n[dim]Config file: {loader.config_path}[/dim]")


@config_app.command("set")
def set_config(
    key: str = typer.Argument(..., help="Configuration key to set (e.g., 'default_output')."),
    value: str = typer.Argument(..., help="Value to set."),
) -> None:
    """Set a configuration value.
    
    Modifies the configuration file at ~/.mrdr/config.yaml.
    
    Valid keys:
    - default_output: Output format (rich, plain, json)
    - database_path: Path to docstring database
    - show_hints: Show keybind hints (true/false)
    - debug_mode: Enable debug output (true/false)
    - theme.primary_color: Primary theme color
    - theme.accent_color: Accent theme color
    - theme.error_color: Error theme color
    - theme.plusrep_positive: PLUSREP positive color
    - theme.plusrep_negative: PLUSREP negative color
    """
    console = state.console
    loader = get_config_loader()
    
    try:
        loader.set(key, value)
        
        if state.json:
            result = {"success": True, "key": key, "value": value}
            renderer = JSONRenderer()
            console.print(renderer.render(result, "config"))
        elif state.should_use_plain():
            console.print(f"Set {key} = {value}")
        else:
            console.print(Panel(
                f"[green]✓[/green] Set [cyan]{key}[/cyan] = [yellow]{value}[/yellow]",
                title="Configuration Updated",
                border_style="green",
            ))
            
    except ValueError as e:
        if state.json:
            error_data = {"error": str(e), "key": key}
            console.print(json.dumps(error_data, indent=2))
        else:
            console.print(Panel(
                f"[red]✖[/red] {e}",
                title="Configuration Error",
                border_style="red",
            ))
        raise typer.Exit(1)


@config_app.command("get")
def get_config(
    key: str = typer.Argument(..., help="Configuration key to get."),
) -> None:
    """Get a specific configuration value.
    
    Retrieves the current value for a configuration key.
    """
    console = state.console
    loader = get_config_loader()
    
    try:
        value = loader.get(key)
        
        if state.json:
            result = {"key": key, "value": value}
            renderer = JSONRenderer()
            console.print(renderer.render(result, "config"))
        elif state.should_use_plain():
            console.print(f"{key}: {value}")
        else:
            console.print(f"[cyan]{key}[/cyan]: [green]{value}[/green]")
            
    except KeyError as e:
        if state.json:
            error_data = {"error": str(e), "key": key}
            console.print(json.dumps(error_data, indent=2))
        else:
            console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@config_app.command("path")
def config_path() -> None:
    """Display the configuration file path.
    
    Shows the location of the configuration file.
    """
    console = state.console
    loader = get_config_loader()
    
    path = str(loader.config_path)
    exists = loader.config_path.exists()
    
    if state.json:
        result = {"path": path, "exists": exists}
        renderer = JSONRenderer()
        console.print(renderer.render(result, "config"))
    elif state.should_use_plain():
        status = "exists" if exists else "not found"
        console.print(f"Config path: {path} ({status})")
    else:
        status_text = "[green]exists[/green]" if exists else "[yellow]not found[/yellow]"
        console.print(f"Config path: [cyan]{path}[/cyan] ({status_text})")
