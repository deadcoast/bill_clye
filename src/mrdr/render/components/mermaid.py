"""Mermaid diagram renderer for MRDR.

This module converts Mermaid diagram source code to ASCII art representation
for terminal display. Supports flowchart and sequence diagram types with
graceful fallback for unsupported or invalid diagrams.
"""

from dataclasses import dataclass
from enum import Enum
import re


class MermaidDiagramType(str, Enum):
    """Mermaid diagram type enumeration."""

    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    UNKNOWN = "unknown"


@dataclass
class MermaidRenderer:
    """Converts Mermaid diagrams to ASCII art representation.

    Supports flowchart diagrams (LR/TB directions) and sequence diagrams.
    Falls back to displaying raw source for unsupported diagram types.
    """

    def render(self, mermaid_source: str) -> str:
        """Convert Mermaid source to ASCII representation.

        Args:
            mermaid_source: Raw Mermaid diagram source code.

        Returns:
            ASCII art representation of the diagram, or raw source
            wrapped in code fence if rendering fails.
        """
        try:
            diagram_type = self._detect_type(mermaid_source)
            if diagram_type == MermaidDiagramType.FLOWCHART:
                return self._render_flowchart(mermaid_source)
            elif diagram_type == MermaidDiagramType.SEQUENCE:
                return self._render_sequence(mermaid_source)
            else:
                return self._render_fallback(mermaid_source)
        except Exception:
            return self._render_fallback(mermaid_source)

    def _detect_type(self, source: str) -> MermaidDiagramType:
        """Detect the Mermaid diagram type from source.

        Args:
            source: Raw Mermaid diagram source code.

        Returns:
            MermaidDiagramType enum value.
        """
        stripped = source.strip().lower()
        if stripped.startswith(("flowchart", "graph")):
            return MermaidDiagramType.FLOWCHART
        elif stripped.startswith("sequencediagram"):
            return MermaidDiagramType.SEQUENCE
        return MermaidDiagramType.UNKNOWN

    def _render_flowchart(self, source: str) -> str:
        """Render flowchart as ASCII boxes and arrows.

        Args:
            source: Mermaid flowchart source code.

        Returns:
            ASCII art representation with boxes and arrows.
        """
        # Extract nodes with labels: A["Label"] or A[Label]
        nodes = re.findall(r'(\w+)\s*\[\s*"?([^"\]]+)"?\s*\]', source)
        # Extract connections: A --> B or A --> B
        connections = re.findall(r'(\w+)\s*-->\s*(\w+)', source)

        if not nodes:
            return self._render_fallback(source)

        result = []
        node_map = {n[0]: n[1] for n in nodes}

        # Detect direction (LR = left-right, TB = top-bottom)
        direction = "TB"  # default
        dir_match = re.search(r'(?:flowchart|graph)\s+(LR|TB|RL|BT)', source, re.IGNORECASE)
        if dir_match:
            direction = dir_match.group(1).upper()

        if direction in ("LR", "RL"):
            # Horizontal layout
            result = self._render_flowchart_horizontal(nodes, connections, node_map)
        else:
            # Vertical layout (TB/BT)
            result = self._render_flowchart_vertical(nodes, connections, node_map)

        return "\n".join(result)

    def _render_flowchart_vertical(
        self,
        nodes: list[tuple[str, str]],
        connections: list[tuple[str, str]],
        node_map: dict[str, str],
    ) -> list[str]:
        """Render flowchart in vertical (top-bottom) layout.

        Args:
            nodes: List of (node_id, label) tuples.
            connections: List of (from_id, to_id) tuples.
            node_map: Mapping of node_id to label.

        Returns:
            List of lines forming the ASCII diagram.
        """
        result = []
        rendered_nodes = set()

        # Build connection order
        ordered_nodes = []
        for node_id, label in nodes:
            if node_id not in rendered_nodes:
                ordered_nodes.append((node_id, label))
                rendered_nodes.add(node_id)

        for i, (node_id, label) in enumerate(ordered_nodes):
            box_width = len(label) + 4
            result.append("┌" + "─" * box_width + "┐")
            result.append(f"│  {label}  │")
            result.append("└" + "─" * box_width + "┘")

            # Add arrow if not last node and there's a connection
            if i < len(ordered_nodes) - 1:
                # Check if there's a connection from this node
                has_connection = any(
                    conn[0] == node_id for conn in connections
                )
                if has_connection:
                    center = (box_width + 2) // 2
                    result.append(" " * center + "│")
                    result.append(" " * center + "▼")

        return result

    def _render_flowchart_horizontal(
        self,
        nodes: list[tuple[str, str]],
        connections: list[tuple[str, str]],
        node_map: dict[str, str],
    ) -> list[str]:
        """Render flowchart in horizontal (left-right) layout.

        Args:
            nodes: List of (node_id, label) tuples.
            connections: List of (from_id, to_id) tuples.
            node_map: Mapping of node_id to label.

        Returns:
            List of lines forming the ASCII diagram.
        """
        if not nodes:
            return []

        # Build boxes for each node
        boxes = []
        for node_id, label in nodes:
            box_width = len(label) + 4
            box = [
                "┌" + "─" * box_width + "┐",
                f"│  {label}  │",
                "└" + "─" * box_width + "┘",
            ]
            boxes.append(box)

        # Combine boxes horizontally with arrows
        lines = ["", "", ""]  # 3 lines for boxes
        for i, box in enumerate(boxes):
            lines[0] += box[0]
            lines[1] += box[1]
            lines[2] += box[2]
            # Add arrow between boxes
            if i < len(boxes) - 1:
                lines[0] += "     "
                lines[1] += " ──► "
                lines[2] += "     "

        return lines

    def _render_sequence(self, source: str) -> str:
        """Render sequence diagram as ASCII.

        Args:
            source: Mermaid sequence diagram source code.

        Returns:
            ASCII art representation with participants and messages.
        """
        # Extract participants
        participants = re.findall(r'participant\s+(\w+)', source, re.IGNORECASE)

        # If no explicit participants, extract from messages
        if not participants:
            messages = re.findall(r'(\w+)\s*->>?\s*(\w+)', source)
            seen = set()
            for sender, receiver in messages:
                if sender not in seen:
                    participants.append(sender)
                    seen.add(sender)
                if receiver not in seen:
                    participants.append(receiver)
                    seen.add(receiver)

        # Extract messages: A->>B: message or A->B: message
        messages = re.findall(r'(\w+)\s*->>?\s*(\w+)\s*:\s*(.+)', source)

        if not participants:
            return self._render_fallback(source)

        result = []

        # Header with participants
        header_parts = []
        for p in participants:
            header_parts.append(f"[{p}]")
        result.append("  ".join(header_parts))

        # Lifelines
        lifeline_parts = []
        for p in participants:
            lifeline_parts.append(" " * (len(p) // 2) + "│" + " " * (len(p) - len(p) // 2))
        result.append("  ".join(lifeline_parts))

        # Messages
        for sender, receiver, msg in messages:
            if sender in participants and receiver in participants:
                result.append(f"  {sender} ──► {receiver}: {msg.strip()}")

        return "\n".join(result)

    def _render_fallback(self, source: str) -> str:
        """Fallback: display raw Mermaid source in code fence.

        Args:
            source: Raw Mermaid diagram source code.

        Returns:
            Source wrapped in mermaid code fence markers.
        """
        return f"```mermaid\n{source.strip()}\n```"

    def get_diagram_type(self, source: str) -> str:
        """Get the diagram type as a string.

        Args:
            source: Raw Mermaid diagram source code.

        Returns:
            Diagram type name as string.
        """
        return self._detect_type(source).value
