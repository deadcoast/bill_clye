"""Rich-based renderer for MRDR.

This module provides a renderer implementation using the Rich library
for terminal UI output with colors, panels, and tables.
"""

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from mrdr.database.schema import DocstringEntry


class RichRenderer:
    """Rich-based renderer for terminal output.

    Uses the Rich library to produce formatted terminal output
    with colors, panels, tables, and syntax highlighting.
    """

    def __init__(self, console: Console | None = None) -> None:
        """Initialize the Rich renderer.

        Args:
            console: Optional Rich Console instance. If not provided,
                a new Console will be created.
        """
        self._console = console or Console()

    @property
    def console(self) -> Console:
        """Get the Rich Console instance."""
        return self._console

    def render(self, data: Any, template: str) -> str:
        """Render data using the specified template.

        Args:
            data: The data to render (typically DocstringEntry or dict).
            template: The template name to use for rendering.
                Supported templates: "show", "list", "inspect", "compare"

        Returns:
            The rendered output as a string with Rich formatting.
        """
        if template == "show":
            return self._render_show(data)
        elif template == "list":
            return self._render_list(data)
        elif template == "inspect":
            return self._render_inspect(data)
        elif template == "compare":
            return self._render_compare(data)
        else:
            return self._render_default(data)

    def supports_rich(self) -> bool:
        """Check if renderer supports Rich formatting.

        Returns:
            True, as this renderer always supports Rich formatting.
        """
        return True

    def _render_show(self, data: DocstringEntry | dict[str, Any]) -> str:
        """Render a docstring entry for display.

        Args:
            data: DocstringEntry or dict with entry data.

        Returns:
            Formatted string for terminal display.
        """
        if isinstance(data, dict):
            entry = DocstringEntry(**data)
        else:
            entry = data

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Field", style="cyan")
        table.add_column("Value")

        table.add_row("Language", Text(entry.language, style="bold green"))
        table.add_row("Start Delimiter", Text(repr(entry.syntax.start), style="yellow"))
        
        end_val = repr(entry.syntax.end) if entry.syntax.end else "None (line-based)"
        table.add_row("End Delimiter", Text(end_val, style="yellow"))
        table.add_row("Type", Text(str(entry.syntax.type), style="magenta"))
        table.add_row("Location", Text(str(entry.syntax.location), style="blue"))

        if entry.tags:
            table.add_row("Tags", Text(", ".join(entry.tags), style="dim"))

        if entry.conflict_ref:
            table.add_row("Conflict", Text(entry.conflict_ref, style="red"))

        with self._console.capture() as capture:
            self._console.print(
                Panel(table, title=f"[bold]{entry.language}[/bold] Docstring Syntax")
            )

        return capture.get()

    def _render_list(self, data: list[str]) -> str:
        """Render a list of languages.

        Args:
            data: List of language names.

        Returns:
            Formatted string with language list.
        """
        table = Table(title="Supported Languages", show_header=True)
        table.add_column("#", style="dim", width=4)
        table.add_column("Language", style="cyan")

        for idx, lang in enumerate(sorted(data), 1):
            table.add_row(str(idx), lang)

        with self._console.capture() as capture:
            self._console.print(table)

        return capture.get()

    def _render_inspect(self, data: dict[str, Any]) -> str:
        """Render detailed inspection output.

        Args:
            data: Dictionary with detailed entry metadata.

        Returns:
            Formatted string with inspection details.
        """
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Field", style="cyan", width=20)
        table.add_column("Value")

        for key, value in data.items():
            if isinstance(value, dict):
                value_str = "\n".join(f"  {k}: {v}" for k, v in value.items())
            elif isinstance(value, list):
                value_str = ", ".join(str(v) for v in value) if value else "[]"
            else:
                value_str = str(value) if value is not None else "None"
            table.add_row(key, value_str)

        with self._console.capture() as capture:
            self._console.print(
                Panel(table, title="[bold]Detailed Inspection[/bold]")
            )

        return capture.get()

    def _render_compare(self, data: dict[str, Any]) -> str:
        """Render side-by-side comparison of two languages.

        Args:
            data: Dictionary with 'lang1' and 'lang2' DocstringEntry objects.

        Returns:
            Formatted comparison table.
        """
        lang1 = data.get("lang1")
        lang2 = data.get("lang2")

        if not lang1 or not lang2:
            return "Error: Both languages required for comparison"

        if isinstance(lang1, dict):
            lang1 = DocstringEntry(**lang1)
        if isinstance(lang2, dict):
            lang2 = DocstringEntry(**lang2)

        table = Table(title="Language Comparison", show_header=True)
        table.add_column("Field", style="cyan")
        table.add_column(lang1.language, style="green")
        table.add_column(lang2.language, style="yellow")

        table.add_row("Start", repr(lang1.syntax.start), repr(lang2.syntax.start))
        table.add_row(
            "End",
            repr(lang1.syntax.end) if lang1.syntax.end else "None",
            repr(lang2.syntax.end) if lang2.syntax.end else "None",
        )
        table.add_row("Type", str(lang1.syntax.type), str(lang2.syntax.type))
        table.add_row("Location", str(lang1.syntax.location), str(lang2.syntax.location))

        with self._console.capture() as capture:
            self._console.print(table)

        return capture.get()

    def _render_default(self, data: Any) -> str:
        """Default rendering for unknown templates.

        Args:
            data: Any data to render.

        Returns:
            Pretty-printed representation of the data.
        """
        with self._console.capture() as capture:
            self._console.print(data)

        return capture.get()

    def render_syntax(self, code: str, language: str) -> str:
        """Render code with syntax highlighting.

        Args:
            code: The code to highlight.
            language: The programming language for highlighting.

        Returns:
            Syntax-highlighted code string.
        """
        syntax = Syntax(code, language, theme="monokai", line_numbers=False)
        
        with self._console.capture() as capture:
            self._console.print(syntax)

        return capture.get()
