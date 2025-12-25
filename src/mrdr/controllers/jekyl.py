"""Jekyl Controller - Front-end visual correlation controller.

This module implements the Jekyl controller which manages visual output,
Rich rendering, and UX for the MRDR CLI.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from mrdr.controllers.hyde import HydeController
from mrdr.database.schema import DocstringEntry
from mrdr.render.base import Renderer
from mrdr.render.components.golden_screen import (
    ContextStrip,
    GoldenScreen,
    HeaderBar,
    HintBar,
)
from mrdr.render.components.plusrep import PlusrepDisplay


@dataclass
class ShowOptions:
    """Options for the show command.

    Attributes:
        plain: If True, render without Rich formatting.
        example: If True, include example content in output.
        grade: If True, include PLUSREP grade in output.
    """

    plain: bool = False
    example: bool = False
    grade: bool = False


@dataclass
class JekylController:
    """Front-end visual correlation controller.

    Manages visual output, Rich rendering, and UX. Consumes data
    from HydeController and renders it using the configured Renderer.

    Attributes:
        hyde: HydeController instance for data operations.
        renderer: Renderer instance for output formatting.
        console: Optional Rich Console for direct output.
    """

    hyde: HydeController
    renderer: Renderer
    console: Console = field(default_factory=Console)

    def show(self, language: str, options: Optional[ShowOptions] = None) -> str:
        """Display docstring syntax with Rich formatting.

        Renders the docstring syntax for a language using the Golden Screen
        layout with header bar, primary payload, and hints bar.

        Args:
            language: The programming language name (case-insensitive).
            options: ShowOptions controlling output behavior.

        Returns:
            The rendered output as a string.

        Raises:
            LanguageNotFoundError: If the language is not in the database.
        """
        if options is None:
            options = ShowOptions()

        # Get entry from Hyde controller
        entry = self.hyde.query(language)

        # Build the payload content
        payload = self._build_show_payload(entry, options)

        # Create Golden Screen layout
        header = HeaderBar(command=f"mrdr jekyl show {entry.language}")
        hints = HintBar()
        context = ContextStrip(total_count=1)

        screen = GoldenScreen(
            header=header,
            payload=payload,
            context=context,
            hints=hints,
        )

        return screen.render(self.console)

    def _build_show_payload(
        self, entry: DocstringEntry, options: ShowOptions
    ) -> Panel:
        """Build the payload panel for show command.

        Args:
            entry: The DocstringEntry to display.
            options: ShowOptions controlling what to include.

        Returns:
            Rich Panel containing the formatted entry.
        """
        from rich.console import Group
        from mrdr.render.components import ConflictDisplay

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

        # Include PLUSREP grade if requested and available
        if options.grade and entry.plusrep:
            plusrep_display = PlusrepDisplay(grade=entry.plusrep)
            table.add_row("Grade", plusrep_display.render())

        # Include example content if requested and available
        if options.example and entry.example_content:
            table.add_row("", Text(""))  # Spacer
            table.add_row("Example", Text(""))
            # Add example as syntax-highlighted code
            syntax = Syntax(
                entry.example_content,
                entry.language.lower(),
                theme="monokai",
                line_numbers=False,
            )
            table.add_row("", syntax)

        main_panel = Panel(table, title=f"[bold]{entry.language}[/bold] Docstring Syntax")

        # Check for conflict and add warning panel if exists
        if entry.conflict_ref:
            conflict_display = ConflictDisplay()
            conflict = conflict_display.find_conflict_for_language(entry.language)
            if conflict:
                warning_panel = conflict_display._render_warning_panel(entry.language, conflict)
                return Panel(
                    Group(main_panel, Text(""), warning_panel),
                    title=f"[bold]{entry.language}[/bold] Docstring Syntax",
                    border_style="cyan",
                )

        return main_panel

    def compare(self, lang1: str, lang2: str) -> str:
        """Display side-by-side comparison of two languages.

        Args:
            lang1: First language name.
            lang2: Second language name.

        Returns:
            The rendered comparison as a string.

        Raises:
            LanguageNotFoundError: If either language is not in the database.
        """
        # Get entries from Hyde controller
        entry1 = self.hyde.query(lang1)
        entry2 = self.hyde.query(lang2)

        # Build comparison table
        table = Table(title="Language Comparison", show_header=True)
        table.add_column("Field", style="cyan")
        table.add_column(entry1.language, style="green")
        table.add_column(entry2.language, style="yellow")

        table.add_row("Start", repr(entry1.syntax.start), repr(entry2.syntax.start))
        table.add_row(
            "End",
            repr(entry1.syntax.end) if entry1.syntax.end else "None",
            repr(entry2.syntax.end) if entry2.syntax.end else "None",
        )
        table.add_row("Type", str(entry1.syntax.type), str(entry2.syntax.type))
        table.add_row(
            "Location", str(entry1.syntax.location), str(entry2.syntax.location)
        )

        if entry1.tags or entry2.tags:
            tags1 = ", ".join(entry1.tags) if entry1.tags else "-"
            tags2 = ", ".join(entry2.tags) if entry2.tags else "-"
            table.add_row("Tags", tags1, tags2)

        if entry1.conflict_ref or entry2.conflict_ref:
            conflict1 = entry1.conflict_ref or "-"
            conflict2 = entry2.conflict_ref or "-"
            table.add_row("Conflict", conflict1, conflict2)

        # Create Golden Screen layout
        header = HeaderBar(command=f"mrdr jekyl compare {entry1.language} {entry2.language}")
        hints = HintBar()
        context = ContextStrip(total_count=2)

        screen = GoldenScreen(
            header=header,
            payload=table,
            context=context,
            hints=hints,
        )

        return screen.render(self.console)

    def render_golden_screen(
        self, content: Any, command: str, count: int = 1
    ) -> str:
        """Render content using Golden Screen layout.

        Args:
            content: The primary content to render.
            command: The command string for the header.
            count: Item count for context strip.

        Returns:
            The rendered output as a string.
        """
        header = HeaderBar(command=command)
        hints = HintBar()
        context = ContextStrip(total_count=count)

        screen = GoldenScreen(
            header=header,
            payload=content,
            context=context,
            hints=hints,
        )

        return screen.render(self.console)

    def execute(self, command: str, **kwargs: Any) -> Any:
        """Execute a controller command.

        Implements the Controller protocol for command dispatch.

        Args:
            command: The command to execute (show, compare).
            **kwargs: Additional arguments for the command.

        Returns:
            The result of the command execution.

        Raises:
            ValueError: If an unknown command is specified.
        """
        commands = {
            "show": lambda: self.show(
                kwargs["language"],
                kwargs.get("options"),
            ),
            "compare": lambda: self.compare(
                kwargs["lang1"],
                kwargs["lang2"],
            ),
        }

        if command not in commands:
            raise ValueError(f"Unknown command: {command}")

        return commands[command]()
