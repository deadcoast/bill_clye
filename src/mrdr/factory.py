"""Factory functions for MRDR component instantiation.

This module provides factory functions for creating and wiring together
the MRDR components with proper dependency injection.

The dependency chain is:
    ConfigLoader → DatabaseLoader → HydeController → JekylController → Renderer
"""

from pathlib import Path
from typing import Optional

from rich.console import Console

from mrdr.config.loader import ConfigLoader
from mrdr.controllers.hyde import HydeController
from mrdr.controllers.jekyl import JekylController
from mrdr.database.conflict.loader import ConflictLoader
from mrdr.database.dictionary.loader import DictionaryLoader
from mrdr.database.doctag.loader import DoctagLoader
from mrdr.database.loader import DatabaseLoader
from mrdr.database.python_styles.loader import PythonStylesLoader
from mrdr.database.udl.loader import UDLLoader
from mrdr.render.base import Renderer
from mrdr.render.json_renderer import JSONRenderer
from mrdr.render.plain_renderer import PlainRenderer
from mrdr.render.rich_renderer import RichRenderer


# Singleton instances for shared state
_config_loader: Optional[ConfigLoader] = None
_database_loader: Optional[DatabaseLoader] = None
_hyde_controller: Optional[HydeController] = None
_doctag_loader: Optional[DoctagLoader] = None
_dictionary_loader: Optional[DictionaryLoader] = None
_python_styles_loader: Optional[PythonStylesLoader] = None
_conflict_loader: Optional[ConflictLoader] = None
_udl_loader: Optional[UDLLoader] = None


def get_config_loader(config_path: Optional[Path] = None) -> ConfigLoader:
    """Get or create the ConfigLoader singleton.

    Args:
        config_path: Optional custom path to config file.

    Returns:
        ConfigLoader instance.
    """
    global _config_loader
    if _config_loader is None or config_path is not None:
        _config_loader = ConfigLoader(config_path)
    return _config_loader


def get_database_loader(database_path: Optional[Path] = None) -> DatabaseLoader:
    """Get or create the DatabaseLoader singleton.

    Uses the database path from config if not explicitly provided.

    Args:
        database_path: Optional custom path to database file.

    Returns:
        DatabaseLoader instance.
    """
    global _database_loader
    if _database_loader is None or database_path is not None:
        if database_path is None:
            config = get_config_loader()
            database_path = Path(config.config.database_path)
        _database_loader = DatabaseLoader(database_path)
    return _database_loader


def get_hyde_controller(database_path: Optional[Path] = None) -> HydeController:
    """Get or create the HydeController singleton.

    Wires the database loader into the Hyde controller.

    Args:
        database_path: Optional custom path to database file.

    Returns:
        HydeController instance.
    """
    global _hyde_controller
    if _hyde_controller is None or database_path is not None:
        _hyde_controller = HydeController(database_path=database_path)
    return _hyde_controller


def get_doctag_loader(database_path: Optional[Path] = None) -> DoctagLoader:
    """Get or create the DoctagLoader singleton.

    Args:
        database_path: Optional custom path to doctag database file.

    Returns:
        DoctagLoader instance.
    """
    global _doctag_loader
    if _doctag_loader is None or database_path is not None:
        _doctag_loader = DoctagLoader(database_path)
    return _doctag_loader


def get_dictionary_loader(database_path: Optional[Path] = None) -> DictionaryLoader:
    """Get or create the DictionaryLoader singleton.

    Args:
        database_path: Optional custom path to dictionary database file.

    Returns:
        DictionaryLoader instance.
    """
    global _dictionary_loader
    if _dictionary_loader is None or database_path is not None:
        _dictionary_loader = DictionaryLoader(database_path)
    return _dictionary_loader


def get_python_styles_loader(database_path: Optional[Path] = None) -> PythonStylesLoader:
    """Get or create the PythonStylesLoader singleton.

    Args:
        database_path: Optional custom path to Python styles database file.

    Returns:
        PythonStylesLoader instance.
    """
    global _python_styles_loader
    if _python_styles_loader is None or database_path is not None:
        _python_styles_loader = PythonStylesLoader(database_path)
    return _python_styles_loader


def get_conflict_loader(database_path: Optional[Path] = None) -> ConflictLoader:
    """Get or create the ConflictLoader singleton.

    Args:
        database_path: Optional custom path to conflict database file.

    Returns:
        ConflictLoader instance.
    """
    global _conflict_loader
    if _conflict_loader is None or database_path is not None:
        _conflict_loader = ConflictLoader(database_path)
    return _conflict_loader


def get_udl_loader(
    udl_path: Optional[Path] = None,
    database_path: Optional[Path] = None,
) -> UDLLoader:
    """Get or create the UDLLoader singleton.

    Args:
        udl_path: Optional custom path to UDL directory.
        database_path: Optional custom path to UDL database file.

    Returns:
        UDLLoader instance.
    """
    global _udl_loader
    if _udl_loader is None or udl_path is not None or database_path is not None:
        _udl_loader = UDLLoader(udl_path, database_path)
    return _udl_loader


def create_renderer(
    output_format: str = "rich",
    console: Optional[Console] = None,
) -> Renderer:
    """Create a renderer based on the specified output format.

    Args:
        output_format: The output format ("rich", "plain", or "json").
        console: Optional Rich Console for rich renderer.

    Returns:
        Renderer instance appropriate for the format.

    Raises:
        ValueError: If an unknown output format is specified.
    """
    format_lower = output_format.lower()
    
    if format_lower == "rich":
        return RichRenderer(console=console)
    elif format_lower == "plain":
        return PlainRenderer()
    elif format_lower == "json":
        return JSONRenderer()
    else:
        raise ValueError(f"Unknown output format: {output_format}")


def create_jekyl_controller(
    output_format: str = "rich",
    console: Optional[Console] = None,
    database_path: Optional[Path] = None,
) -> JekylController:
    """Create a JekylController with all dependencies wired.

    This is the main factory function that creates a fully-wired
    JekylController with:
    - HydeController for data operations
    - Appropriate Renderer based on output format
    - Console for output

    Args:
        output_format: The output format ("rich", "plain", or "json").
        console: Optional Rich Console for output.
        database_path: Optional custom path to database file.

    Returns:
        Fully-wired JekylController instance.
    """
    hyde = get_hyde_controller(database_path)
    renderer = create_renderer(output_format, console)
    
    if console is None:
        console = Console()
    
    return JekylController(
        hyde=hyde,
        renderer=renderer,
        console=console,
    )


def reset_singletons() -> None:
    """Reset all singleton instances.

    Useful for testing or when configuration changes require
    fresh instances.
    """
    global _config_loader, _database_loader, _hyde_controller
    global _doctag_loader, _dictionary_loader, _python_styles_loader
    global _conflict_loader, _udl_loader
    _config_loader = None
    _database_loader = None
    _hyde_controller = None
    _doctag_loader = None
    _dictionary_loader = None
    _python_styles_loader = None
    _conflict_loader = None
    _udl_loader = None


__all__ = [
    "get_config_loader",
    "get_database_loader",
    "get_hyde_controller",
    "get_doctag_loader",
    "get_dictionary_loader",
    "get_python_styles_loader",
    "get_conflict_loader",
    "get_udl_loader",
    "create_renderer",
    "create_jekyl_controller",
    "reset_singletons",
]
