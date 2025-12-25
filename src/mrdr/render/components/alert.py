"""Alert component for MRDR.

This module implements the Alert visual pattern from the Visual Pattern Library,
providing semantic alert messages with distinct styling for NOTE, TIP, IMPORTANT,
WARNING, and CAUTION types.
"""

from dataclasses import dataclass
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class AlertType(str, Enum):
    """Alert type enumeration for semantic alert messages.

    Each type has distinct styling (icon, color, title) defined in ALERT_CONFIG.
    """

    NOTE = "note"
    TIP = "tip"
    IMPORTANT = "important"
    WARNING = "warning"
    CAUTION = "caution"


ALERT_CONFIG: dict[AlertType, dict[str, str]] = {
    AlertType.NOTE: {"icon": "ℹ️", "color": "cyan", "title": "Note"},
    AlertType.TIP: {"icon": "💡", "color": "green", "title": "Tip"},
    AlertType.IMPORTANT: {"icon": "❗", "color": "magenta", "title": "Important"},
    AlertType.WARNING: {"icon": "⚠️", "color": "yellow", "title": "Warning"},
    AlertType.CAUTION: {"icon": "🛑", "color": "red", "title": "Caution"},
}


@dataclass
class AlertComponent:
    """Semantic alert message component.

    Renders alert messages with type-specific styling including icons,
    colors, and titles. Supports both Rich Panel output and plain text.

    Attributes:
        alert_type: The type of alert (NOTE, TIP, IMPORTANT, WARNING, CAUTION).
        message: The alert message content.
    """

    alert_type: AlertType
    message: str

    def render(self, console: Console | None = None) -> str:
        """Render the alert as a Rich Panel.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Rendered alert as a string.
        """
        if console is None:
            console = Console()

        panel = self._render_panel()

        with console.capture() as capture:
            console.print(panel)

        return capture.get()

    def _render_panel(self) -> Panel:
        """Render the alert as a Rich Panel object.

        Returns:
            Rich Panel with icon, color, and styled title.
        """
        config = ALERT_CONFIG[self.alert_type]
        title = Text()
        title.append(f"{config['icon']} ", style="")
        title.append(config["title"], style=f"bold {config['color']}")

        return Panel(
            self.message,
            title=title,
            border_style=config["color"],
        )

    def render_plain(self) -> str:
        """Render the alert as plain text without ANSI codes.

        Returns:
            Plain text representation of the alert.
        """
        config = ALERT_CONFIG[self.alert_type]
        return f"[{config['title'].upper()}] {self.message}"

    def get_config(self) -> dict[str, str]:
        """Get the configuration for this alert type.

        Returns:
            Dictionary with icon, color, and title for the alert type.
        """
        return ALERT_CONFIG[self.alert_type]
