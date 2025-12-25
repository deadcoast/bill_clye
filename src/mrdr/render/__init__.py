"""Render module for MRDR.

This module provides renderers for different output formats:
- RichRenderer: Rich terminal UI with colors, panels, and tables
- PlainRenderer: Plain text without ANSI codes
- JSONRenderer: Valid JSON output for programmatic consumption
- DoctagRenderer: Doctag syntax highlighting with semantic coloring
- PythonStyleRenderer: Python docstring style rendering
"""

from mrdr.render.base import Renderer
from mrdr.render.doctag_renderer import (
    DOCTAG_COLORS,
    DoctagEntry,
    DoctagRenderer,
    DoctagType,
)
from mrdr.render.json_renderer import JSONRenderer
from mrdr.render.plain_renderer import PlainRenderer
from mrdr.render.python_style import (
    STYLE_METADATA,
    STYLE_RULES,
    STYLE_TEMPLATES,
    PythonDocstringStyle,
    PythonStyleRenderer,
)
from mrdr.render.rich_renderer import RichRenderer

__all__ = [
    "Renderer",
    "RichRenderer",
    "PlainRenderer",
    "JSONRenderer",
    # Doctag Renderer
    "DoctagRenderer",
    "DoctagEntry",
    "DoctagType",
    "DOCTAG_COLORS",
    # Python Style Renderer
    "PythonStyleRenderer",
    "PythonDocstringStyle",
    "STYLE_TEMPLATES",
    "STYLE_METADATA",
    "STYLE_RULES",
]
