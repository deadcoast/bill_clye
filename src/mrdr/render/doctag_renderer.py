"""Doctag Renderer for MRDR.

This module implements the Doctag Rendering System from the Visual Integration spec,
providing semantic coloring and formatting for doctag syntax elements.

Feature: mrdr-visual-integration
Requirements: 4.1, 4.2, 4.3, 4.4, 4.6
"""

from dataclasses import dataclass
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class DoctagType(str, Enum):
    """Doctag category types.

    Each type corresponds to a category of doctags as defined in docs/doctags.md:
    - DDL: Document Delimiters (DDL01-DDL10)
    - GRM: Grammar definitions (GRM01-GRM10)
    - IDC: Inter-Document Commands (IDC01-IDC10)
    - FMT: Formatting rules (FMT01-FMT10)
    - DOC: Document spec markers (DOC01-DOC05)
    """

    DELIMITER = "DDL"
    GRAMMAR = "GRM"
    INTER_DOC = "IDC"
    FORMATTING = "FMT"
    DOC_SPEC = "DOC"


# Semantic color mapping for each doctag type
DOCTAG_COLORS: dict[DoctagType, str] = {
    DoctagType.DELIMITER: "yellow",
    DoctagType.GRAMMAR: "cyan",
    DoctagType.INTER_DOC: "blue underline",
    DoctagType.FORMATTING: "magenta",
    DoctagType.DOC_SPEC: "green",
}


@dataclass
class DoctagEntry:
    """A single doctag entry with all metadata.

    Attributes:
        id: Tag identifier (e.g., "DDL01", "GRM05").
        short_name: Short identifier (e.g., "ADDTACH", "DASHLIST").
        full_name: Full identifier name (e.g., "add, or attach an item").
        description: Tag description text.
        example: Optional usage example.
    """

    id: str
    short_name: str
    full_name: str
    description: str
    example: str | None = None


@dataclass
class DoctagRenderer:
    """Renderer for doctag syntax with semantic coloring.

    Applies SCREAMINGSNAKE case styling to identifiers and semantic
    coloring based on tag type (DDL, GRM, IDC, FMT, DOC).
    """

    def render_tag(self, tag_id: str, tag_name: str, description: str) -> Text:
        """Render a single doctag with appropriate styling.

        Args:
            tag_id: Tag identifier (e.g., "DDL01").
            tag_name: Tag short name (e.g., "ADDTACH").
            description: Tag description text.

        Returns:
            Rich Text object with semantic styling applied.
        """
        text = Text()
        tag_type = self._get_tag_type(tag_id)
        color = DOCTAG_COLORS.get(tag_type, "white")

        # Tag ID with type-specific color
        text.append(f"{tag_id}: ", style=f"bold {color}")

        # Short name in SCREAMINGSNAKE case
        screaming_name = tag_name.upper()
        text.append(f"`{screaming_name}`", style="bold")

        # Full name in dim style
        text.append(f" - {description}", style="")

        return text

    def render_tag_full(
        self,
        entry: DoctagEntry,
        console: Console | None = None,
    ) -> str:
        """Render a complete doctag entry with all details.

        Args:
            entry: DoctagEntry with full metadata.
            console: Optional Rich Console instance.

        Returns:
            Rendered doctag entry as a string.
        """
        if console is None:
            console = Console()

        tag_type = self._get_tag_type(entry.id)
        color = DOCTAG_COLORS.get(tag_type, "white")

        content = Text()

        # Short name in SCREAMINGSNAKE
        content.append("Short: ", style="dim")
        content.append(f"{entry.short_name.upper()}\n", style="bold")

        # Full name
        content.append("Full: ", style="dim")
        content.append(f"{entry.full_name.upper()}\n", style="bold")

        # Description
        content.append("Description: ", style="dim")
        content.append(f"{entry.description}\n", style="")

        # Example if present
        if entry.example:
            content.append("Example: ", style="dim")
            content.append(f"{entry.example}", style="italic cyan")

        panel = Panel(
            content,
            title=f"[bold {color}]{entry.id}[/bold {color}]",
            border_style=color,
        )

        with console.capture() as capture:
            console.print(panel)

        return capture.get()

    def render_idc_link(self, tag_id: str, tag_name: str, target: str) -> Text:
        """Render an IDC (Inter-Document Command) as a clickable-style link.

        Args:
            tag_id: Tag identifier (e.g., "IDC02").
            tag_name: Tag short name (e.g., "DOCLINK").
            target: Link target reference.

        Returns:
            Rich Text object with link-style formatting.
        """
        text = Text()
        color = DOCTAG_COLORS[DoctagType.INTER_DOC]

        text.append(f"{tag_id}: ", style=f"bold {color}")
        text.append(f"`{tag_name.upper()}`", style="bold")
        text.append(" → ", style="dim")
        text.append(target, style=color)

        return text

    def _get_tag_type(self, tag_id: str) -> DoctagType:
        """Determine tag type from ID prefix.

        Args:
            tag_id: Tag identifier (e.g., "DDL01", "GRM05").

        Returns:
            DoctagType enum value based on prefix.
        """
        if len(tag_id) < 3:
            return DoctagType.DOC_SPEC

        prefix = tag_id[:3].upper()

        try:
            return DoctagType(prefix)
        except ValueError:
            return DoctagType.DOC_SPEC

    def render_plain(self, tag_id: str, tag_name: str, description: str) -> str:
        """Render a doctag as plain text without ANSI codes.

        Args:
            tag_id: Tag identifier (e.g., "DDL01").
            tag_name: Tag short name (e.g., "ADDTACH").
            description: Tag description text.

        Returns:
            Plain text representation of the doctag.
        """
        screaming_name = tag_name.upper()
        return f"{tag_id}: `{screaming_name}` - {description}"

    def render_entry_plain(self, entry: DoctagEntry) -> str:
        """Render a complete doctag entry as plain text.

        Args:
            entry: DoctagEntry with full metadata.

        Returns:
            Plain text representation of the doctag entry.
        """
        lines = [
            f"Tag: {entry.id}",
            f"Short: {entry.short_name.upper()}",
            f"Full: {entry.full_name.upper()}",
            f"Description: {entry.description}",
        ]
        if entry.example:
            lines.append(f"Example: {entry.example}")

        return "\n".join(lines)
