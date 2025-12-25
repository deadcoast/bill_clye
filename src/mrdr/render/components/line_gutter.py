"""Line Gutter component for MRDR.

This module implements the Line Number Gutter Guard visual pattern,
providing line-numbered code display for docstring examples.
"""

from dataclasses import dataclass

from rich.console import Console
from rich.text import Text


@dataclass
class LineGutter:
    """Line number gutter component for code display.

    Renders content with right-justified line numbers separated
    by a configurable separator from the content.

    Attributes:
        content: The content to display with line numbers.
        start_line: Starting line number (default: 1).
        separator: Separator between line number and content (default: "│").
    """

    content: str
    start_line: int = 1
    separator: str = "│"

    def render(self, console: Console | None = None, plain: bool = False) -> str:
        """Render content with line number gutter.

        Args:
            console: Optional Rich Console instance.
            plain: If True, render without ANSI codes.

        Returns:
            Rendered content with line numbers.
        """
        lines = self.content.split("\n")
        total_lines = len(lines) + self.start_line - 1
        width = len(str(total_lines))

        result = []
        for i, line in enumerate(lines):
            line_num = self.start_line + i
            if plain:
                result.append(f"{line_num:>{width}}{self.separator} {line}")
            else:
                result.append(
                    f"[dim]{line_num:>{width}}[/dim][dim]{self.separator}[/dim] {line}"
                )

        if plain:
            return "\n".join(result)

        # For Rich output, render through console
        if console is None:
            console = Console()

        with console.capture() as capture:
            for line in result:
                console.print(line, highlight=False)

        return capture.get()

    def render_rich(self, console: Console | None = None) -> Text:
        """Render content with line number gutter as Rich Text.

        Args:
            console: Optional Rich Console instance (unused, for API consistency).

        Returns:
            Rich Text object with formatted line numbers.
        """
        lines = self.content.split("\n")
        total_lines = len(lines) + self.start_line - 1
        width = len(str(total_lines))

        text = Text()
        for i, line in enumerate(lines):
            line_num = self.start_line + i
            text.append(f"{line_num:>{width}}", style="dim")
            text.append(self.separator, style="dim")
            text.append(f" {line}\n")

        return text

    def get_line_count(self) -> int:
        """Get the total number of lines in the content.

        Returns:
            Number of lines.
        """
        return len(self.content.split("\n"))

    def get_max_line_number(self) -> int:
        """Get the maximum line number that will be displayed.

        Returns:
            Maximum line number.
        """
        return self.start_line + self.get_line_count() - 1
