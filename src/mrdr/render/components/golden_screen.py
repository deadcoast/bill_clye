"""Golden Screen layout components for MRDR.

This module implements the canonical output template defining the visual
layout structure for MRDR CLI output. The Golden Screen consists of:
- Header bar with command and database context
- Primary payload area
- Context strip (counts, filter, sort, page)
- Hint bar with keybind hints
- Optional footer for debug timings
"""

from dataclasses import dataclass, field
from typing import Any

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


@dataclass
class HeaderBar:
    """Header bar component displaying command and database context.

    Attributes:
        command: The command being executed (e.g., "mrdr jekyl show python").
        db_source: The database source path (e.g., "DB: docstring_database.json").
    """

    command: str
    db_source: str = "DB: docstring_database.json"

    def render(self) -> Text:
        """Render the header bar as Rich Text.

        Returns:
            Rich Text object with formatted header.
        """
        header = Text()
        header.append("❯ ", style="green bold")
        header.append(self.command, style="bold")
        header.append("  ", style="dim")
        header.append(f"[{self.db_source}]", style="dim cyan")
        return header


@dataclass
class HintBar:
    """Hint bar component displaying keybind hints.

    Attributes:
        hints: List of (key, action) tuples for keybind hints.
    """

    hints: list[tuple[str, str]] = field(default_factory=lambda: [
        ("/", "search"),
        ("↵", "details"),
        ("f", "filter"),
        ("q", "quit"),
    ])

    def render(self) -> Text:
        """Render the hint bar as Rich Text.

        Returns:
            Rich Text object with formatted keybind hints.
        """
        hint_text = Text()
        for i, (key, action) in enumerate(self.hints):
            if i > 0:
                hint_text.append(" · ", style="dim")
            hint_text.append(f"({key})", style="cyan bold")
            hint_text.append(f" {action}", style="dim")
        return hint_text


@dataclass
class ContextStrip:
    """Context strip showing counts, filter, sort, and page info.

    Attributes:
        total_count: Total number of items.
        filtered_count: Number of items after filtering (optional).
        current_filter: Active filter string (optional).
        sort_by: Current sort field (optional).
        page: Current page number (optional).
        total_pages: Total number of pages (optional).
    """

    total_count: int = 0
    filtered_count: int | None = None
    current_filter: str | None = None
    sort_by: str | None = None
    page: int | None = None
    total_pages: int | None = None

    def render(self) -> Text:
        """Render the context strip as Rich Text.

        Returns:
            Rich Text object with context information.
        """
        context = Text()

        # Count info
        if self.filtered_count is not None:
            context.append(f"{self.filtered_count}/{self.total_count}", style="cyan")
        else:
            context.append(f"{self.total_count}", style="cyan")
        context.append(" items", style="dim")

        # Filter info
        if self.current_filter:
            context.append(" | ", style="dim")
            context.append("filter: ", style="dim")
            context.append(self.current_filter, style="yellow")

        # Sort info
        if self.sort_by:
            context.append(" | ", style="dim")
            context.append("sort: ", style="dim")
            context.append(self.sort_by, style="magenta")

        # Page info
        if self.page is not None and self.total_pages is not None:
            context.append(" | ", style="dim")
            context.append(f"page {self.page}/{self.total_pages}", style="blue")

        return context


@dataclass
class GoldenScreen:
    """Standard output layout following visual_pattern_lib.md spec.

    The Golden Screen is the canonical output template for MRDR CLI,
    providing a consistent visual structure across all commands.

    Attributes:
        header: HeaderBar component with command and DB context.
        payload: Primary content (table, panel, tree, or any renderable).
        context: ContextStrip with counts, filter, sort, page info.
        hints: HintBar component with keybind hints.
        footer: Optional debug timings or additional info.
    """

    header: HeaderBar
    payload: Any
    context: ContextStrip | None = None
    hints: HintBar = field(default_factory=HintBar)
    footer: str | None = None

    def render(self, console: Console | None = None) -> str:
        """Render the complete Golden Screen layout.

        Args:
            console: Optional Rich Console instance. If not provided,
                a new Console will be created.

        Returns:
            The complete rendered output as a string.
        """
        if console is None:
            console = Console()

        # Build the layout components
        components = []

        # Header
        components.append(self.header.render())
        components.append(Text(""))  # Spacer

        # Context strip (if provided)
        if self.context:
            components.append(self.context.render())
            components.append(Text(""))  # Spacer

        # Main payload wrapped in panel
        if isinstance(self.payload, (Table, Panel, Text, Group)):
            components.append(self.payload)
        else:
            # Wrap raw content in a panel
            components.append(Panel(str(self.payload), border_style="dim"))

        components.append(Text(""))  # Spacer

        # Hints bar
        components.append(self.hints.render())

        # Footer (debug info)
        if self.footer:
            components.append(Text(""))  # Spacer
            components.append(Text(self.footer, style="dim italic"))

        # Render all components
        with console.capture() as capture:
            for component in components:
                console.print(component)

        return capture.get()

    def render_to_panel(self, console: Console | None = None) -> str:
        """Render the Golden Screen wrapped in a single panel.

        This provides a more compact view with all elements contained
        within a bordered panel.

        Args:
            console: Optional Rich Console instance.

        Returns:
            The rendered output as a string.
        """
        if console is None:
            console = Console()

        # Build inner content
        inner_components = []

        # Context strip
        if self.context:
            inner_components.append(self.context.render())
            inner_components.append(Text(""))

        # Payload
        if isinstance(self.payload, (Table, Panel, Text, Group)):
            inner_components.append(self.payload)
        else:
            inner_components.append(Text(str(self.payload)))

        inner_components.append(Text(""))
        inner_components.append(self.hints.render())

        if self.footer:
            inner_components.append(Text(""))
            inner_components.append(Text(self.footer, style="dim italic"))

        # Create group for inner content
        inner_group = Group(*inner_components)

        # Wrap in panel with header as title
        panel = Panel(
            inner_group,
            title=self.header.render(),
            subtitle=Text(f"[{self.header.db_source}]", style="dim"),
            border_style="cyan",
        )

        with console.capture() as capture:
            console.print(panel)

        return capture.get()
