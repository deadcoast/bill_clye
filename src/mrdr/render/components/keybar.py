"""Keybar component for MRDR.

This module implements the Keybar visual pattern from the Visual Pattern Library,
providing keycap-styled keybind display using kbd-style formatting.
"""

from dataclasses import dataclass, field

from rich.console import Console
from rich.text import Text


@dataclass
class Keybar:
    """Keycap-styled keybind display component.

    Extends the HintBar concept with kbd-style formatting for
    keyboard shortcuts, providing a more visual representation
    of keybinds.

    Attributes:
        hints: List of (key, action) tuples for keybind hints.
        separator: Separator between hints (default: " · ").
    """

    hints: list[tuple[str, str]] = field(
        default_factory=lambda: [
            ("/", "search"),
            ("↵", "details"),
            ("f", "filter"),
            ("q", "quit"),
        ]
    )
    separator: str = " · "

    def render(self, console: Console | None = None) -> str:
        """Render the keybar with kbd-style formatting.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Rendered keybar as a string.
        """
        if console is None:
            console = Console()

        text = self._render_text()

        with console.capture() as capture:
            console.print(text)

        return capture.get()

    def _render_text(self) -> Text:
        """Render the keybar as Rich Text with kbd styling.

        Returns:
            Rich Text object with kbd-styled keybinds.
        """
        text = Text()
        for i, (key, action) in enumerate(self.hints):
            if i > 0:
                text.append(self.separator, style="dim")
            # kbd-style: bordered key with distinct styling
            text.append("⌨ ", style="dim")
            text.append(f"[{key}]", style="bold cyan reverse")
            text.append(f" {action}", style="dim")
        return text

    def render_plain(self) -> str:
        """Render the keybar as plain text without ANSI codes.

        Returns:
            Plain text representation of keybar.
        """
        parts = []
        for key, action in self.hints:
            parts.append(f"[{key}] {action}")
        return self.separator.join(parts)

    def render_kbd_html(self) -> str:
        """Render the keybar as HTML with <kbd> tags.

        Useful for documentation or web output.

        Returns:
            HTML string with kbd-styled keybinds.
        """
        parts = []
        for key, action in self.hints:
            parts.append(f"<kbd>{key}</kbd> {action}")
        return self.separator.join(parts)

    def has_kbd_markers(self) -> bool:
        """Check if rendered output contains kbd-style markers.

        Returns:
            True if output contains kbd-style formatting.
        """
        text = self._render_text()
        plain = text.plain
        # Check for bracket markers around keys
        return any(f"[{key}]" in plain for key, _ in self.hints)
