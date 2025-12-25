"""Card Grid layout component for MRDR.

This module implements the Card Grid visual pattern from the Visual Pattern Library,
providing table-based card layouts for command documentation display.
"""

from dataclasses import dataclass, field

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


@dataclass
class CardData:
    """Data for a single card in the grid.

    Attributes:
        title: Card title (command name).
        purpose: Brief purpose description.
        ui_description: UI/UX description.
        modes: List of supported modes.
        details: Optional additional details.
    """

    title: str
    purpose: str
    ui_description: str
    modes: list[str] = field(default_factory=list)
    details: str | None = None


@dataclass
class CardGrid:
    """Table-based card grid layout component.

    Renders cards in a grid layout using Rich tables and panels.
    Each card displays command name, purpose, UI description, and modes.

    Attributes:
        cards: List of CardData objects to display.
        columns: Number of columns in the grid (default: 2).
    """

    cards: list[CardData]
    columns: int = 2

    def render(self, console: Console | None = None) -> str:
        """Render cards in a grid layout using Rich tables.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Rendered grid as a string.
        """
        if console is None:
            console = Console()

        table = Table(show_header=False, box=None, padding=(0, 2))
        for _ in range(self.columns):
            table.add_column(width=40)

        # Group cards into rows
        for i in range(0, len(self.cards), self.columns):
            row_cards = self.cards[i : i + self.columns]
            panels = [self._render_card(card) for card in row_cards]
            # Pad with empty strings if row is incomplete
            while len(panels) < self.columns:
                panels.append("")
            table.add_row(*panels)

        with console.capture() as capture:
            console.print(table)
        return capture.get()

    def _render_card(self, card: CardData) -> Panel:
        """Render a single card as a Rich Panel.

        Args:
            card: CardData object to render.

        Returns:
            Rich Panel containing the card content.
        """
        content = f"[bold]{card.purpose}[/bold]\n"
        content += f"[dim]{card.ui_description}[/dim]\n"
        if card.modes:
            content += f"[cyan]Modes:[/cyan] {' · '.join(card.modes)}"
        if card.details:
            content += f"\n[italic]{card.details}[/italic]"
        return Panel(content, title=f"⌘ {card.title}", border_style="cyan")
