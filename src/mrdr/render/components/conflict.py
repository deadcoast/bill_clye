"""Conflict Display component for MRDR.

This module implements the Conflict Display visual pattern for showing
syntax conflicts between programming languages that share identical
delimiter patterns.
"""

from dataclasses import dataclass, field

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


@dataclass
class SyntaxConflict:
    """Represents a syntax conflict between languages.

    Attributes:
        languages: List of languages sharing the same delimiter syntax.
        delimiter: The conflicting delimiter pattern (e.g., '\"\"\"').
        resolution: Guidance for resolving the conflict.
        attachment_rules: Dict mapping language to its attachment rule.
    """

    languages: list[str]
    delimiter: str
    resolution: str
    attachment_rules: dict[str, str] = field(default_factory=dict)


# Known syntax conflicts from the docstring database
KNOWN_CONFLICTS: list[SyntaxConflict] = [
    SyntaxConflict(
        languages=["Python", "Julia"],
        delimiter='"""',
        resolution="Check location: Python uses internal_first_line, Julia uses above_target.",
        attachment_rules={
            "Python": "internal_first_line",
            "Julia": "above_target",
        },
    ),
    SyntaxConflict(
        languages=["JavaScript", "D"],
        delimiter="/** or /++",
        resolution="D uses /++ +/ (nestable), JavaScript uses /** */ (non-nestable).",
        attachment_rules={
            "JavaScript": "above_target (/** */)",
            "D": "above_target (/++ +/)",
        },
    ),
]


@dataclass
class ConflictDisplay:
    """Component for displaying syntax conflicts.

    Renders conflict warnings and tables showing languages that share
    identical delimiter syntax with resolution guidance.

    Attributes:
        conflicts: List of SyntaxConflict instances to display.
    """

    conflicts: list[SyntaxConflict] = field(default_factory=lambda: KNOWN_CONFLICTS)

    def render_warning(
        self,
        language: str,
        conflict: SyntaxConflict,
        console: Console | None = None,
    ) -> str:
        """Render a conflict warning panel for a specific language.

        Args:
            language: The language being displayed.
            conflict: The SyntaxConflict to warn about.
            console: Optional Rich Console instance.

        Returns:
            Rendered warning panel as a string.
        """
        if console is None:
            console = Console()

        panel = self._render_warning_panel(language, conflict)

        with console.capture() as capture:
            console.print(panel)

        return capture.get()

    def _render_warning_panel(self, language: str, conflict: SyntaxConflict) -> Panel:
        """Render a conflict warning as a Rich Panel.

        Args:
            language: The language being displayed.
            conflict: The SyntaxConflict to warn about.

        Returns:
            Rich Panel with conflict warning.
        """
        text = Text()
        text.append("⚠️ Syntax Conflict\n\n", style="bold yellow")
        text.append("Delimiter: ", style="dim")
        text.append(f"{conflict.delimiter}\n", style="bold")
        text.append("Also used by: ", style="dim")
        others = [lang for lang in conflict.languages if lang != language]
        text.append(", ".join(others), style="cyan")

        # Add attachment rules if available
        if conflict.attachment_rules:
            text.append("\n\nAttachment Rules:\n", style="dim")
            for lang, rule in conflict.attachment_rules.items():
                style = "green" if lang == language else "cyan"
                text.append(f"  • {lang}: ", style=style)
                text.append(f"{rule}\n", style="")

        text.append("\nResolution: ", style="dim")
        text.append(conflict.resolution, style="italic")

        return Panel(text, title="Conflict Warning", border_style="yellow")

    def render_table(self, console: Console | None = None) -> str:
        """Render all conflicts in a table.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Rendered conflicts table as a string.
        """
        if console is None:
            console = Console()

        table = self._render_conflicts_table()

        with console.capture() as capture:
            console.print(table)

        return capture.get()

    def _render_conflicts_table(self) -> Table:
        """Render all conflicts as a Rich Table.

        Returns:
            Rich Table with all known syntax conflicts.
        """
        table = Table(title="Syntax Conflicts", border_style="yellow")
        table.add_column("Delimiter", style="bold")
        table.add_column("Languages", style="cyan")
        table.add_column("Resolution", style="italic")

        for conflict in self.conflicts:
            table.add_row(
                conflict.delimiter,
                ", ".join(conflict.languages),
                conflict.resolution,
            )

        return table

    def render_plain(self, console: Console | None = None) -> str:
        """Render conflicts as plain text without ANSI codes.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Plain text representation of conflicts.
        """
        lines = ["Syntax Conflicts", "=" * 40]

        for conflict in self.conflicts:
            lines.append(f"\nDelimiter: {conflict.delimiter}")
            lines.append(f"Languages: {', '.join(conflict.languages)}")
            if conflict.attachment_rules:
                lines.append("Attachment Rules:")
                for lang, rule in conflict.attachment_rules.items():
                    lines.append(f"  - {lang}: {rule}")
            lines.append(f"Resolution: {conflict.resolution}")

        return "\n".join(lines)

    def render_warning_plain(self, language: str, conflict: SyntaxConflict) -> str:
        """Render a conflict warning as plain text.

        Args:
            language: The language being displayed.
            conflict: The SyntaxConflict to warn about.

        Returns:
            Plain text warning.
        """
        others = [lang for lang in conflict.languages if lang != language]
        lines = [
            "[WARNING] Syntax Conflict",
            f"Delimiter: {conflict.delimiter}",
            f"Also used by: {', '.join(others)}",
        ]

        if conflict.attachment_rules:
            lines.append("Attachment Rules:")
            for lang, rule in conflict.attachment_rules.items():
                lines.append(f"  - {lang}: {rule}")

        lines.append(f"Resolution: {conflict.resolution}")

        return "\n".join(lines)

    def find_conflict_for_language(self, language: str) -> SyntaxConflict | None:
        """Find a conflict that includes the specified language.

        Args:
            language: The language to search for.

        Returns:
            SyntaxConflict if found, None otherwise.
        """
        for conflict in self.conflicts:
            if language in conflict.languages:
                return conflict
        return None

    def get_all_conflicts(self) -> list[SyntaxConflict]:
        """Get all known syntax conflicts.

        Returns:
            List of all SyntaxConflict instances.
        """
        return self.conflicts
