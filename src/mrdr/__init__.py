"""
MRDR - The Visual Syntax CLI.

A CLI-driven syntax and docstring database that documents, categorizes,
and displays examples for common codebases.
"""

__version__ = "0.1.0"
__app_name__ = "mrdr"
__app_alias__ = "misterdoctor"

# Re-export factory functions for convenient access
from mrdr.factory import (
    create_jekyl_controller,
    create_renderer,
    get_config_loader,
    get_database_loader,
    get_hyde_controller,
    reset_singletons,
)

__all__ = [
    "__version__",
    "__app_name__",
    "__app_alias__",
    "get_config_loader",
    "get_database_loader",
    "get_hyde_controller",
    "create_renderer",
    "create_jekyl_controller",
    "reset_singletons",
]
