"""Visual commands module for MRDR CLI.

This module provides visual rendering options for the jekyl show command,
including card grid, accordion, and line gutter display modes.
"""

from dataclasses import dataclass

from rich.console import Console

from mrdr.database.schema import DocstringEntry
from mrdr.render.components import (
    Accordion,
    AccordionSection,
    CardData,
    CardGrid,
    LineGutter,
)


@dataclass
class VisualOptions:
    """Options for visual rendering modes.

    Attributes:
        card: If True, render using card grid layout.
        accordion: If True, render using accordion layout.
        gutter: If True, render with line number gutter.
        start_line: Starting line number for gutter (default: 1).
        plain: If True, render without ANSI codes.
    """

    card: bool = False
    accordion: bool = False
    gutter: bool = False
    start_line: int = 1
    plain: bool = False


def render_entry_as_card(entry: DocstringEntry, console: Console | None = None) -> str:
    """Render a docstring entry as a card grid.

    Args:
        entry: The DocstringEntry to render.
        console: Optional Rich Console instance.

    Returns:
        Rendered card grid as a string.
    """
    # Build modes list from entry attributes
    modes = []
    if entry.syntax.type:
        modes.append(str(entry.syntax.type))
    if entry.syntax.location:
        modes.append(str(entry.syntax.location))

    card = CardData(
        title=entry.language,
        purpose=f"Docstring syntax for {entry.language}",
        ui_description=f"Delimiters: {repr(entry.syntax.start)} ... {repr(entry.syntax.end) if entry.syntax.end else 'EOL'}",
        modes=modes,
        details=f"Tags: {', '.join(entry.tags)}" if entry.tags else None,
    )

    grid = CardGrid(cards=[card], columns=1)
    return grid.render(console)


def render_entry_as_accordion(
    entry: DocstringEntry, console: Console | None = None
) -> str:
    """Render a docstring entry as an accordion with expandable sections.

    Args:
        entry: The DocstringEntry to render.
        console: Optional Rich Console instance.

    Returns:
        Rendered accordion as a string.
    """
    sections = []

    # Basic syntax section (always open)
    syntax_content = (
        f"Start: {repr(entry.syntax.start)}\n"
        f"End: {repr(entry.syntax.end) if entry.syntax.end else 'None (line-based)'}\n"
        f"Type: {entry.syntax.type}\n"
        f"Location: {entry.syntax.location}"
    )
    sections.append(
        AccordionSection(title="Syntax Details", content=syntax_content, open=True)
    )

    # Tags section
    if entry.tags:
        tags_content = ", ".join(entry.tags)
        sections.append(AccordionSection(title="Tags", content=tags_content, open=False))

    # Example section
    if entry.example_content:
        sections.append(
            AccordionSection(
                title="Example Code", content=entry.example_content, open=False
            )
        )

    # Conflict section
    if entry.conflict_ref:
        sections.append(
            AccordionSection(
                title="⚠️ Conflict Warning",
                content=f"This syntax conflicts with: {entry.conflict_ref}",
                open=True,
            )
        )

    # PLUSREP section
    if entry.plusrep:
        plusrep_content = (
            f"P: {entry.plusrep.p} | L: {entry.plusrep.l} | U: {entry.plusrep.u} | "
            f"S: {entry.plusrep.s} | R: {entry.plusrep.r} | E: {entry.plusrep.e} | "
            f"P: {entry.plusrep.p2}"
        )
        sections.append(
            AccordionSection(title="PLUSREP Grade", content=plusrep_content, open=False)
        )

    accordion = Accordion(sections=sections, title=f"{entry.language} Docstring Syntax")
    return accordion.render(console)


def render_content_with_gutter(
    content: str,
    start_line: int = 1,
    plain: bool = False,
    console: Console | None = None,
) -> str:
    """Render content with line number gutter.

    Args:
        content: The content to render with line numbers.
        start_line: Starting line number (default: 1).
        plain: If True, render without ANSI codes.
        console: Optional Rich Console instance.

    Returns:
        Rendered content with line numbers.
    """
    gutter = LineGutter(content=content, start_line=start_line)
    return gutter.render(console=console, plain=plain)


def render_entry_with_gutter(
    entry: DocstringEntry,
    start_line: int = 1,
    plain: bool = False,
    console: Console | None = None,
) -> str:
    """Render a docstring entry's example with line number gutter.

    Args:
        entry: The DocstringEntry to render.
        start_line: Starting line number (default: 1).
        plain: If True, render without ANSI codes.
        console: Optional Rich Console instance.

    Returns:
        Rendered entry with line-numbered example.
    """
    if console is None:
        console = Console()

    lines = []

    # Header info
    lines.append(f"Language: {entry.language}")
    lines.append(f"Delimiters: {repr(entry.syntax.start)} ... {repr(entry.syntax.end) if entry.syntax.end else 'EOL'}")
    lines.append("")

    # Example with gutter if available
    if entry.example_content:
        lines.append("Example:")
        gutter = LineGutter(content=entry.example_content, start_line=start_line)
        example_with_gutter = gutter.render(console=console, plain=plain)
        lines.append(example_with_gutter)
    else:
        lines.append("[No example available]")

    return "\n".join(lines)


def apply_visual_options(
    entry: DocstringEntry,
    options: VisualOptions,
    console: Console | None = None,
) -> str:
    """Apply visual options to render a docstring entry.

    Determines which visual mode to use based on options and renders
    the entry accordingly. Priority: card > accordion > gutter > default.

    Args:
        entry: The DocstringEntry to render.
        options: VisualOptions controlling rendering mode.
        console: Optional Rich Console instance.

    Returns:
        Rendered entry as a string.
    """
    if options.card:
        return render_entry_as_card(entry, console)
    elif options.accordion:
        return render_entry_as_accordion(entry, console)
    elif options.gutter:
        return render_entry_with_gutter(
            entry,
            start_line=options.start_line,
            plain=options.plain,
            console=console,
        )
    else:
        # Default rendering - return None to use standard rendering
        return None
