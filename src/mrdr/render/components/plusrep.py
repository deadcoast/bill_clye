"""PLUSREP display component for MRDR.

This module implements the PLUSREP quality grading system display,
using `+` and `.` tokens for reputation weighting visualization.
"""

from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from mrdr.database.schema import PlusrepGrade


# Rating labels based on count of '+' tokens
RATING_LABELS = {
    4: "MAXIMUM",
    3: "GREAT",
    2: "GOOD",
    1: "FAIR",
    0: "SLOPPY",
    -1: "POOR",
    -2: "RESET",
}


def calculate_rating(tokens: str) -> int:
    """Calculate PLUSREP rating from token string.

    The rating is calculated as: (count of '+') - 2
    This gives a range from -2 (all dots) to +4 (all plus).

    Args:
        tokens: A 6-character string of '+' and '.' characters.

    Returns:
        Integer rating from -2 to +4.

    Raises:
        ValueError: If tokens is not exactly 6 characters or contains
            invalid characters.
    """
    if len(tokens) != 6:
        raise ValueError(f"PLUSREP tokens must be exactly 6 characters, got {len(tokens)}")

    invalid_chars = set(tokens) - {"+", "."}
    if invalid_chars:
        raise ValueError(f"PLUSREP tokens must only contain '+' and '.', found: {invalid_chars}")

    plus_count = tokens.count("+")
    return plus_count - 2


def get_rating_label(rating: int) -> str:
    """Get the label for a PLUSREP rating.

    Args:
        rating: Integer rating from -2 to +4.

    Returns:
        String label for the rating.
    """
    return RATING_LABELS.get(rating, "UNKNOWN")


@dataclass
class PlusrepDisplay:
    """PLUSREP quality grade display component.

    Renders PLUSREP tokens with color coding:
    - '+' tokens in green (positive)
    - '.' tokens in red (negative/neutral)

    Attributes:
        grade: PlusrepGrade object or None.
    """

    grade: PlusrepGrade | None = None

    @classmethod
    def from_tokens(cls, tokens: str) -> "PlusrepDisplay":
        """Create a PlusrepDisplay from a token string.

        Args:
            tokens: A 6-character string of '+' and '.' characters.

        Returns:
            PlusrepDisplay instance with calculated grade.
        """
        rating = calculate_rating(tokens)
        label = get_rating_label(rating)
        grade = PlusrepGrade(tokens=tokens, rating=rating, label=label)
        return cls(grade=grade)

    def render(self) -> Text:
        """Render the PLUSREP grade as Rich Text.

        Returns:
            Rich Text object with color-coded tokens and label.
        """
        if self.grade is None:
            return Text("No grade", style="dim")

        text = Text()
        text.append("[", style="dim")

        # Render each token with appropriate color
        for char in self.grade.tokens:
            if char == "+":
                text.append(char, style="bold green")
            else:  # '.'
                text.append(char, style="bold red")

        text.append("]", style="dim")
        text.append(" ", style="")
        text.append(self.grade.label, style=self._get_label_style())
        text.append(f" ({self.grade.rating:+d})", style="dim")

        return text

    def render_plain(self) -> str:
        """Render the PLUSREP grade as plain text.

        Returns:
            Plain text string without ANSI codes.
        """
        if self.grade is None:
            return "No grade"

        return f"[{self.grade.tokens}] {self.grade.label} ({self.grade.rating:+d})"

    def render_panel(self, console: Console | None = None) -> str:
        """Render the PLUSREP grade in a Rich Panel.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Rendered panel as a string.
        """
        if console is None:
            console = Console()

        if self.grade is None:
            panel = Panel("No grade available", title="PLUSREP", border_style="dim")
        else:
            panel = Panel(
                self.render(),
                title="PLUSREP Grade",
                border_style=self._get_border_style(),
            )

        with console.capture() as capture:
            console.print(panel)

        return capture.get()

    def _get_label_style(self) -> str:
        """Get the Rich style for the rating label.

        Returns:
            Style string based on rating value.
        """
        if self.grade is None:
            return "dim"

        if self.grade.rating >= 3:
            return "bold green"
        elif self.grade.rating >= 1:
            return "bold cyan"
        elif self.grade.rating >= 0:
            return "bold yellow"
        else:
            return "bold red"

    def _get_border_style(self) -> str:
        """Get the Rich border style for the panel.

        Returns:
            Border style string based on rating value.
        """
        if self.grade is None:
            return "dim"

        if self.grade.rating >= 3:
            return "green"
        elif self.grade.rating >= 1:
            return "cyan"
        elif self.grade.rating >= 0:
            return "yellow"
        else:
            return "red"
