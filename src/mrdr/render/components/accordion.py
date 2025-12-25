"""Accordion component for MRDR.

This module implements the Accordion/Details visual pattern from the Visual Pattern Library,
providing collapsible sections for expandable content display.
"""

from dataclasses import dataclass, field

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


@dataclass
class AccordionSection:
    """Data for a single accordion section.

    Attributes:
        title: Section title/header.
        content: Section content (can be string or Rich renderable).
        open: Whether section is expanded by default.
    """

    title: str
    content: str
    open: bool = False


@dataclass
class Accordion:
    """Accordion component with expandable sections.

    Renders sections as Rich panels with visual indicators for
    expanded/collapsed state. In terminal output, all sections
    are rendered but styled to indicate their default state.

    Attributes:
        sections: List of AccordionSection objects.
        title: Optional accordion group title.
    """

    sections: list[AccordionSection]
    title: str | None = None

    def render(self, console: Console | None = None) -> str:
        """Render accordion sections using Rich panels.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Rendered accordion as a string.
        """
        if console is None:
            console = Console()

        with console.capture() as capture:
            if self.title:
                console.print(Text(self.title, style="bold underline"))
                console.print()

            for section in self.sections:
                panel = self._render_section(section)
                console.print(panel)
                console.print()

        return capture.get()

    def _render_section(self, section: AccordionSection) -> Panel:
        """Render a single accordion section as a Rich Panel.

        Args:
            section: AccordionSection object to render.

        Returns:
            Rich Panel containing the section content.
        """
        # Use different indicators for open/closed state
        indicator = "▼" if section.open else "▶"
        style = "bold cyan" if section.open else "dim cyan"

        title_text = Text()
        title_text.append(f"{indicator} ", style=style)
        title_text.append(section.title, style="bold" if section.open else "")

        # Show content based on open state
        if section.open:
            content = section.content
            border_style = "cyan"
        else:
            content = "[dim]Click to expand...[/dim]"
            border_style = "dim"

        return Panel(content, title=title_text, border_style=border_style)

    def render_plain(self) -> str:
        """Render accordion as plain text without ANSI codes.

        Returns:
            Plain text representation of accordion.
        """
        lines = []
        if self.title:
            lines.append(self.title)
            lines.append("=" * len(self.title))
            lines.append("")

        for section in self.sections:
            indicator = "[v]" if section.open else "[>]"
            lines.append(f"{indicator} {section.title}")
            if section.open:
                # Indent content
                for line in section.content.split("\n"):
                    lines.append(f"    {line}")
            lines.append("")

        return "\n".join(lines)
