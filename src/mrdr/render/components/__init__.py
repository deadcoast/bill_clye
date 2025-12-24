"""Render components for MRDR.

This module provides reusable UI components:
- GoldenScreen: Standard output layout template
- HeaderBar: Command and database context header
- HintBar: Keybind hints footer
- ContextStrip: Counts, filter, sort, page info
- PlusrepDisplay: PLUSREP quality grade display
"""

from mrdr.render.components.golden_screen import (
    ContextStrip,
    GoldenScreen,
    HeaderBar,
    HintBar,
)
from mrdr.render.components.plusrep import (
    PlusrepDisplay,
    calculate_rating,
    get_rating_label,
)

__all__ = [
    "GoldenScreen",
    "HeaderBar",
    "HintBar",
    "ContextStrip",
    "PlusrepDisplay",
    "calculate_rating",
    "get_rating_label",
]
