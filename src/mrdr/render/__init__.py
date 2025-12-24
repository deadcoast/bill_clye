"""Render module for MRDR.

This module provides renderers for different output formats:
- RichRenderer: Rich terminal UI with colors, panels, and tables
- PlainRenderer: Plain text without ANSI codes
- JSONRenderer: Valid JSON output for programmatic consumption
"""

from mrdr.render.base import Renderer
from mrdr.render.json_renderer import JSONRenderer
from mrdr.render.plain_renderer import PlainRenderer
from mrdr.render.rich_renderer import RichRenderer

__all__ = [
    "Renderer",
    "RichRenderer",
    "PlainRenderer",
    "JSONRenderer",
]
