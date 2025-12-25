"""Render components for MRDR.

This module provides reusable UI components:
- GoldenScreen: Standard output layout template
- HeaderBar: Command and database context header
- HintBar: Keybind hints footer
- ContextStrip: Counts, filter, sort, page info
- PlusrepDisplay: PLUSREP quality grade display
- CardGrid: Table-based card layout for command documentation
- CardData: Data model for card grid entries
- Accordion: Collapsible sections for expandable content
- AccordionSection: Data model for accordion sections
- LineGutter: Line number gutter for code display
- Keybar: Keycap-styled keybind display
"""

from mrdr.render.components.accordion import (
    Accordion,
    AccordionSection,
)
from mrdr.render.components.card_grid import (
    CardData,
    CardGrid,
)
from mrdr.render.components.golden_screen import (
    ContextStrip,
    GoldenScreen,
    HeaderBar,
    HintBar,
)
from mrdr.render.components.keybar import (
    Keybar,
)
from mrdr.render.components.line_gutter import (
    LineGutter,
)
from mrdr.render.components.plusrep import (
    PlusrepDisplay,
    calculate_rating,
    get_rating_label,
)

__all__ = [
    # Golden Screen components
    "GoldenScreen",
    "HeaderBar",
    "HintBar",
    "ContextStrip",
    # PLUSREP components
    "PlusrepDisplay",
    "calculate_rating",
    "get_rating_label",
    # Card Grid components
    "CardGrid",
    "CardData",
    # Accordion components
    "Accordion",
    "AccordionSection",
    # Line Gutter component
    "LineGutter",
    # Keybar component
    "Keybar",
]
