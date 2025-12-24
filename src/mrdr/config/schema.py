"""Configuration schema for MRDR CLI.

Defines Pydantic models for configuration validation and defaults.
"""

from enum import Enum
from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    """Output format options for CLI commands."""

    RICH = "rich"
    PLAIN = "plain"
    JSON = "json"


class ThemeConfig(BaseModel):
    """Visual theme configuration."""

    primary_color: str = "cyan"
    accent_color: str = "green"
    error_color: str = "red"
    plusrep_positive: str = "green"
    plusrep_negative: str = "red"


class MRDRConfig(BaseModel):
    """Main configuration schema for MRDR CLI.

    Attributes:
        default_output: Default output format (rich, plain, json)
        theme: Visual theme configuration
        database_path: Path to the docstring database
        show_hints: Whether to show keybind hints in output
        debug_mode: Enable debug output with timing info
    """

    default_output: OutputFormat = OutputFormat.RICH
    theme: ThemeConfig = Field(default_factory=ThemeConfig)
    database_path: str = "database/docstrings/docstring_database.json"
    show_hints: bool = True
    debug_mode: bool = False
