"""Jekyl subcommands for MRDR CLI.

This module implements the jekyl subcommand group for front-end visual
operations including show and compare commands with Rich rendering.
"""

import time

import typer

from mrdr.cli.app import state
from mrdr.cli.error_handlers import (
    display_language_not_found_error,
    display_unexpected_error,
    handle_mrdr_error,
)
from mrdr.controllers.jekyl import ShowOptions
from mrdr.factory import create_jekyl_controller
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
    language: str = typer.Argument(..., help="Programming language to display."),
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
    """
    start_time = time.time()
    console = state.console
    
    # Override plain state if --plain flag is passed
    if plain:
        state.plain = True
    
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
