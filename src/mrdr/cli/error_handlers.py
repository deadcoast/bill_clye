"""Error handlers for MRDR CLI.

This module provides centralized error handling for the CLI, including
user-friendly error display with Rich panels and debug file logging.
"""

import json
import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Callable, TypeVar

from rich.console import Console
from rich.panel import Panel

from mrdr.utils.errors import (
    MRDRError,
    DatabaseError,
    DatabaseNotFoundError,
    ValidationError,
    QueryError,
    LanguageNotFoundError,
    ConfigError,
)
from mrdr.utils.suggestions import (
    get_command_suggestions,
    get_language_suggestions,
    MRDR_COMMANDS,
)


# Type variable for generic error handler decorator
T = TypeVar("T")

# Debug log file location
DEBUG_LOG_DIR = Path.home() / ".mrdr" / "logs"
DEBUG_LOG_FILE = DEBUG_LOG_DIR / "error.log"


def setup_debug_logging() -> logging.Logger:
    """Set up debug file logging for unexpected errors.
    
    Returns:
        Configured logger instance.
    """
    DEBUG_LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("mrdr.debug")
    logger.setLevel(logging.DEBUG)
    
    # File handler for debug logs
    if not logger.handlers:
        handler = logging.FileHandler(DEBUG_LOG_FILE, mode="a")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def log_unexpected_error(error: Exception, context: str = "") -> None:
    """Log an unexpected error to the debug file.
    
    Args:
        error: The exception that occurred.
        context: Additional context about where the error occurred.
    """
    logger = setup_debug_logging()
    
    timestamp = datetime.now().isoformat()
    tb = traceback.format_exc()
    
    logger.error(f"Unexpected error at {timestamp}")
    if context:
        logger.error(f"Context: {context}")
    logger.error(f"Error type: {type(error).__name__}")
    logger.error(f"Error message: {str(error)}")
    logger.error(f"Traceback:\n{tb}")
    logger.error("-" * 80)


def display_language_not_found_error(
    error: LanguageNotFoundError,
    console: Console,
    use_json: bool = False,
) -> None:
    """Display user-friendly error for language not found.
    
    Args:
        error: The LanguageNotFoundError exception.
        console: Rich console for output.
        use_json: If True, output as JSON.
    """
    if use_json:
        error_data = {
            "error": "LanguageNotFoundError",
            "message": str(error),
            "language": error.language,
            "suggestions": error.suggestions,
        }
        console.print(json.dumps(error_data, indent=2))
    else:
        suggestions_text = "\n".join(f"  • {s}" for s in error.suggestions[:5])
        if not suggestions_text:
            suggestions_text = "  (no similar languages found)"
        
        console.print(Panel(
            f"[red]✖[/red] Language '[bold]{error.language}[/bold]' not found\n\n"
            f"[dim]Did you mean:[/dim]\n{suggestions_text}\n\n"
            f"[dim]Try:[/dim] mrdr hyde list",
            title="Not Found",
            border_style="red"
        ))


def display_database_not_found_error(
    error: DatabaseNotFoundError,
    console: Console,
    use_json: bool = False,
) -> None:
    """Display user-friendly error for database not found.
    
    Args:
        error: The DatabaseNotFoundError exception.
        console: Rich console for output.
        use_json: If True, output as JSON.
    """
    if use_json:
        error_data = {
            "error": "DatabaseNotFoundError",
            "message": str(error),
            "path": error.path,
        }
        console.print(json.dumps(error_data, indent=2))
    else:
        console.print(Panel(
            f"[red]✖[/red] Database file not found\n\n"
            f"[dim]Expected path:[/dim]\n  {error.path}\n\n"
            f"[dim]Please ensure the database file exists at the expected location.[/dim]",
            title="Database Error",
            border_style="red"
        ))


def display_validation_error(
    error: ValidationError,
    console: Console,
    use_json: bool = False,
) -> None:
    """Display user-friendly error for validation failures.
    
    Args:
        error: The ValidationError exception.
        console: Rich console for output.
        use_json: If True, output as JSON.
    """
    if use_json:
        error_data = {
            "error": "ValidationError",
            "message": str(error),
            "entry": error.entry,
            "errors": error.errors,
        }
        console.print(json.dumps(error_data, indent=2))
    else:
        errors_text = "\n".join(f"  • {e}" for e in error.errors[:5])
        console.print(Panel(
            f"[red]✖[/red] Validation failed for '[bold]{error.entry}[/bold]'\n\n"
            f"[dim]Errors:[/dim]\n{errors_text}",
            title="Validation Error",
            border_style="red"
        ))


def display_config_error(
    error: ConfigError,
    console: Console,
    use_json: bool = False,
) -> None:
    """Display user-friendly error for configuration issues.
    
    Args:
        error: The ConfigError exception.
        console: Rich console for output.
        use_json: If True, output as JSON.
    """
    if use_json:
        error_data = {
            "error": "ConfigError",
            "message": str(error),
        }
        console.print(json.dumps(error_data, indent=2))
    else:
        console.print(Panel(
            f"[red]✖[/red] Configuration error\n\n"
            f"[dim]Details:[/dim] {str(error)}\n\n"
            f"[dim]Try:[/dim] mrdr config show",
            title="Config Error",
            border_style="red"
        ))


def display_unknown_command_error(
    command: str,
    console: Console,
    use_json: bool = False,
) -> None:
    """Display user-friendly error for unknown commands with suggestions.
    
    Args:
        command: The unknown command that was entered.
        console: Rich console for output.
        use_json: If True, output as JSON.
    """
    suggestions = get_command_suggestions(command, MRDR_COMMANDS)
    
    if use_json:
        error_data = {
            "error": "UnknownCommandError",
            "message": f"Unknown command: {command}",
            "command": command,
            "suggestions": suggestions,
        }
        console.print(json.dumps(error_data, indent=2))
    else:
        suggestions_text = "\n".join(f"  • mrdr {s}" for s in suggestions[:3])
        if not suggestions_text:
            suggestions_text = "  (no similar commands found)"
        
        console.print(Panel(
            f"[red]✖[/red] Unknown command '[bold]{command}[/bold]'\n\n"
            f"[dim]Did you mean:[/dim]\n{suggestions_text}\n\n"
            f"[dim]Try:[/dim] mrdr --help",
            title="Unknown Command",
            border_style="red"
        ))


def display_empty_result_error(
    query: str,
    console: Console,
    use_json: bool = False,
) -> None:
    """Display user-friendly message when query returns no results.
    
    Args:
        query: The query that returned no results.
        console: Rich console for output.
        use_json: If True, output as JSON.
    """
    if use_json:
        error_data = {
            "error": "EmptyResultError",
            "message": f"No results found for: {query}",
            "query": query,
            "suggestions": [
                "mrdr hyde list",
                "mrdr docstring --all",
            ],
        }
        console.print(json.dumps(error_data, indent=2))
    else:
        console.print(Panel(
            f"[yellow]![/yellow] No results found for '[bold]{query}[/bold]'\n\n"
            f"[dim]Try these commands:[/dim]\n"
            f"  • mrdr hyde list      - List all languages\n"
            f"  • mrdr docstring --all - Show all docstring signatures\n"
            f"  • mrdr --help         - Show available commands",
            title="No Results",
            border_style="yellow"
        ))


def display_unexpected_error(
    error: Exception,
    console: Console,
    use_json: bool = False,
    debug: bool = False,
) -> None:
    """Display user-friendly message for unexpected errors.
    
    Logs the full stack trace to the debug file and shows a
    user-friendly message.
    
    Args:
        error: The unexpected exception.
        console: Rich console for output.
        use_json: If True, output as JSON.
        debug: If True, show more details.
    """
    # Log to debug file
    log_unexpected_error(error, context="CLI execution")
    
    if use_json:
        error_data = {
            "error": "UnexpectedError",
            "message": str(error),
            "type": type(error).__name__,
            "debug_log": str(DEBUG_LOG_FILE),
        }
        if debug:
            error_data["traceback"] = traceback.format_exc()
        console.print(json.dumps(error_data, indent=2))
    else:
        message = (
            f"[red]✖[/red] An unexpected error occurred\n\n"
            f"[dim]Error:[/dim] {type(error).__name__}: {str(error)}\n\n"
            f"[dim]Debug log:[/dim] {DEBUG_LOG_FILE}\n\n"
            f"[dim]Try:[/dim] mrdr fix"
        )
        
        if debug:
            message += f"\n\n[dim]Traceback:[/dim]\n{traceback.format_exc()}"
        
        console.print(Panel(
            message,
            title="Unexpected Error",
            border_style="red"
        ))


def handle_mrdr_error(
    error: MRDRError,
    console: Console,
    use_json: bool = False,
) -> int:
    """Handle any MRDRError and display appropriate message.
    
    Args:
        error: The MRDRError exception.
        console: Rich console for output.
        use_json: If True, output as JSON.
        
    Returns:
        Exit code (1 for errors).
    """
    if isinstance(error, LanguageNotFoundError):
        display_language_not_found_error(error, console, use_json)
    elif isinstance(error, DatabaseNotFoundError):
        display_database_not_found_error(error, console, use_json)
    elif isinstance(error, ValidationError):
        display_validation_error(error, console, use_json)
    elif isinstance(error, ConfigError):
        display_config_error(error, console, use_json)
    elif isinstance(error, QueryError):
        # Generic query error
        if use_json:
            error_data = {"error": "QueryError", "message": str(error)}
            console.print(json.dumps(error_data, indent=2))
        else:
            console.print(Panel(
                f"[red]✖[/red] Query error: {str(error)}",
                title="Query Error",
                border_style="red"
            ))
    elif isinstance(error, DatabaseError):
        # Generic database error
        if use_json:
            error_data = {"error": "DatabaseError", "message": str(error)}
            console.print(json.dumps(error_data, indent=2))
        else:
            console.print(Panel(
                f"[red]✖[/red] Database error: {str(error)}",
                title="Database Error",
                border_style="red"
            ))
    else:
        # Generic MRDR error
        if use_json:
            error_data = {"error": "MRDRError", "message": str(error)}
            console.print(json.dumps(error_data, indent=2))
        else:
            console.print(Panel(
                f"[red]✖[/red] Error: {str(error)}",
                title="Error",
                border_style="red"
            ))
    
    return 1
