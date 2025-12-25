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
- HierarchyDisplay: Tree-based hierarchy visualization
- HierarchyNode: Data model for hierarchy tree nodes
- HierarchyLevel: Enum for hierarchy levels
- AlertComponent: Semantic alert message component
- AlertType: Enum for alert types (NOTE, TIP, IMPORTANT, WARNING, CAUTION)
- ALERT_CONFIG: Configuration dict for alert styling
- MermaidRenderer: Mermaid diagram to ASCII converter
- MermaidDiagramType: Enum for Mermaid diagram types
- ConflictDisplay: Syntax conflict display component
- SyntaxConflict: Data model for syntax conflicts
- KNOWN_CONFLICTS: List of known syntax conflicts
- AdvancedTableRenderer: Advanced table with filtering, sorting, pagination
- TableConfig: Configuration for advanced table rendering
"""

from mrdr.render.components.accordion import (
    Accordion,
    AccordionSection,
)
from mrdr.render.components.alert import (
    ALERT_CONFIG,
    AlertComponent,
    AlertType,
)
from mrdr.render.components.card_grid import (
    CardData,
    CardGrid,
)
from mrdr.render.components.conflict import (
    KNOWN_CONFLICTS,
    ConflictDisplay,
    SyntaxConflict,
)
from mrdr.render.components.golden_screen import (
    ContextStrip,
    GoldenScreen,
    HeaderBar,
    HintBar,
)
from mrdr.render.components.hierarchy import (
    HIERARCHY_STYLES,
    HierarchyDisplay,
    HierarchyLevel,
    HierarchyNode,
)
from mrdr.render.components.keybar import (
    Keybar,
)
from mrdr.render.components.line_gutter import (
    LineGutter,
)
from mrdr.render.components.mermaid import (
    MermaidDiagramType,
    MermaidRenderer,
)
from mrdr.render.components.plusrep import (
    PlusrepDisplay,
    calculate_rating,
    get_rating_label,
)
from mrdr.render.components.table_advanced import (
    AdvancedTableRenderer,
    TableConfig,
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
    # Hierarchy components
    "HierarchyDisplay",
    "HierarchyNode",
    "HierarchyLevel",
    "HIERARCHY_STYLES",
    # Alert components
    "AlertComponent",
    "AlertType",
    "ALERT_CONFIG",
    # Mermaid components
    "MermaidRenderer",
    "MermaidDiagramType",
    # Conflict components
    "ConflictDisplay",
    "SyntaxConflict",
    "KNOWN_CONFLICTS",
    # Advanced Table components
    "AdvancedTableRenderer",
    "TableConfig",
]
