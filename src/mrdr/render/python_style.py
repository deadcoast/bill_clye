"""Python docstring style renderer for MRDR.

This module provides rendering for Python docstring styles including
Sphinx, Google, NumPy, Epytext, and PEP 257 formats.

Feature: mrdr-visual-integration
**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7**
"""

from dataclasses import dataclass
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table


class PythonDocstringStyle(str, Enum):
    """Python docstring style enumeration."""

    SPHINX = "sphinx"
    GOOGLE = "google"
    NUMPY = "numpy"
    EPYTEXT = "epytext"
    PEP257 = "pep257"


# Style templates with example code for each style
STYLE_TEMPLATES: dict[PythonDocstringStyle, str] = {
    PythonDocstringStyle.SPHINX: '''def my_function(name, age):
    """
    This is a brief description of the function.

    :param name: The name of the user.
    :type name: str
    :param age: The age of the user.
    :type age: int
    :return: A greeting message.
    :rtype: str
    """
    return f"Hello {name}, you are {age} years old."
''',
    PythonDocstringStyle.GOOGLE: '''def my_function(name, age):
    """
    This is the module or function description.

    Args:
        name (str): The name of the user.
        age (int): The age of the user.

    Returns:
        str: A greeting message.
    """
    return f"Hello {name}, you are {age} years old."
''',
    PythonDocstringStyle.NUMPY: '''def my_function(name, age):
    """
    Brief description.

    Parameters
    ----------
    name : str
        The name of the user.
    age : int
        The age of the user.

    Returns
    -------
    str
        A greeting message.
    """
    return f"Hello {name}, you are {age} years old."
''',
    PythonDocstringStyle.EPYTEXT: '''def my_function(name, age):
    """
    Brief description.

    @param name: The name of the user.
    @type name: str
    @return: A greeting message.
    """
    return f"Hello {name}, you are {age} years old."
''',
    PythonDocstringStyle.PEP257: '''def my_function():
    """
    Perform a simple task and return None.

    This multi-line section expands on the summary above if
    more context is required for the developer.
    """
    pass
''',
}

# Style metadata with display names and descriptions
STYLE_METADATA: dict[PythonDocstringStyle, dict[str, str]] = {
    PythonDocstringStyle.SPHINX: {
        "name": "Sphinx (reStructuredText)",
        "description": "Uses :param:, :type:, :return:, :rtype: tags",
        "markers": [":param:", ":type:", ":return:", ":rtype:"],
    },
    PythonDocstringStyle.GOOGLE: {
        "name": "Google Style",
        "description": "Uses Args:, Returns: sections with indentation",
        "markers": ["Args:", "Returns:", "Raises:"],
    },
    PythonDocstringStyle.NUMPY: {
        "name": "NumPy Style",
        "description": "Uses Parameters, Returns headers with ---------- separators",
        "markers": ["Parameters", "----------", "Returns"],
    },
    PythonDocstringStyle.EPYTEXT: {
        "name": "Epytext (Epydoc)",
        "description": "Uses @param, @type, @return tags (Javadoc-like)",
        "markers": ["@param", "@type", "@return"],
    },
    PythonDocstringStyle.PEP257: {
        "name": "PEP 257",
        "description": "Minimal standard format with summary and description",
        "markers": [],
    },
}

# Style-specific rules (common to all styles)
STYLE_RULES: list[str] = [
    "Summary Line: Start with a concise, capitalized summary ending in a period.",
    "Structural Spacing: Insert a blank line between summary and field lists.",
    "Field Indentation: Ensure consistent indentation under respective tags.",
    "Clean Termination: Place closing triple-quotes on their own line.",
]


@dataclass
class PythonStyleRenderer:
    """Renderer for Python docstring styles.

    Provides methods to render individual styles or all styles
    for comparison, using Rich panels with syntax highlighting.
    """

    console: Console | None = None

    def __post_init__(self) -> None:
        """Initialize console if not provided."""
        if self.console is None:
            self.console = Console()

    def render_style(self, style: PythonDocstringStyle) -> Panel:
        """Render a specific Python docstring style.

        Args:
            style: The Python docstring style to render.

        Returns:
            Rich Panel containing syntax-highlighted example code.
        """
        template = STYLE_TEMPLATES[style]
        metadata = STYLE_METADATA[style]

        syntax = Syntax(
            template.strip(),
            "python",
            theme="monokai",
            line_numbers=True,
        )

        return Panel(
            syntax,
            title=f"[bold]Python[/bold] - {metadata['name']}",
            subtitle=f"[dim]{metadata['description']}[/dim]",
            border_style="green",
        )

    def render_all_styles(self) -> list[Panel]:
        """Render all Python docstring styles for comparison.

        Returns:
            List of Rich Panels, one for each style.
        """
        return [self.render_style(style) for style in PythonDocstringStyle]

    def render_comparison(self) -> str:
        """Render all styles as a comparison view.

        Returns:
            String output with all styles rendered.
        """
        if self.console is None:
            self.console = Console()

        with self.console.capture() as capture:
            for panel in self.render_all_styles():
                self.console.print(panel)
                self.console.print()  # Add spacing between panels

        return capture.get()

    def render_style_table(self) -> Table:
        """Render a summary table of all styles.

        Returns:
            Rich Table with style overview.
        """
        table = Table(
            title="Python Docstring Styles",
            show_header=True,
            border_style="cyan",
        )
        table.add_column("Style", style="bold cyan")
        table.add_column("Name", style="green")
        table.add_column("Key Markers", style="yellow")

        for style in PythonDocstringStyle:
            metadata = STYLE_METADATA[style]
            markers = ", ".join(metadata["markers"]) if metadata["markers"] else "(minimal)"
            table.add_row(
                style.value,
                metadata["name"],
                markers,
            )

        return table

    def render_plain(self, style: PythonDocstringStyle) -> str:
        """Render a style as plain text without ANSI codes.

        Args:
            style: The Python docstring style to render.

        Returns:
            Plain text representation of the style.
        """
        template = STYLE_TEMPLATES[style]
        metadata = STYLE_METADATA[style]

        lines = [
            f"=== Python Docstring Style: {metadata['name']} ===",
            "",
            f"Description: {metadata['description']}",
            "",
            "Example:",
            template.strip(),
            "",
            "Rules:",
        ]
        for rule in STYLE_RULES:
            lines.append(f"  - {rule}")
        lines.append("")

        return "\n".join(lines)

    def render_all_plain(self) -> str:
        """Render all styles as plain text.

        Returns:
            Plain text representation of all styles.
        """
        sections = []
        for style in PythonDocstringStyle:
            sections.append(self.render_plain(style))
        return "\n".join(sections)

    def get_style_markers(self, style: PythonDocstringStyle) -> list[str]:
        """Get the key markers for a specific style.

        Args:
            style: The Python docstring style.

        Returns:
            List of marker strings that identify this style.
        """
        return STYLE_METADATA[style]["markers"]

    def get_style_name(self, style: PythonDocstringStyle) -> str:
        """Get the display name for a style.

        Args:
            style: The Python docstring style.

        Returns:
            Human-readable style name.
        """
        return STYLE_METADATA[style]["name"]
