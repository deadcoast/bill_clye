"""Hierarchy Display component for MRDR.

This module implements the Hierarchy Display visual pattern from the Visual Pattern Library,
providing tree-based hierarchy visualization for data relationships.
"""

from dataclasses import dataclass, field
from enum import Enum

from rich.console import Console
from rich.text import Text
from rich.tree import Tree


class HierarchyLevel(str, Enum):
    """Hierarchy level enumeration.

    Defines the four levels of hierarchy depth:
    - GRANDPARENT: Top-level notation (e.g., NOTE, CLAIM, FORMAT)
    - PARENT: Mid-level commands (e.g., apd, objacc)
    - CHILD: Nested functions (e.g., sem, def, dstr)
    - GRANDCHILD: Deepest level (e.g., val, value)
    """

    GRANDPARENT = "grandparent"
    PARENT = "parent"
    CHILD = "child"
    GRANDCHILD = "grandchild"


HIERARCHY_STYLES = {
    HierarchyLevel.GRANDPARENT: "bold cyan",
    HierarchyLevel.PARENT: "bold green",
    HierarchyLevel.CHILD: "yellow",
    HierarchyLevel.GRANDCHILD: "dim",
}
"""Mapping of hierarchy levels to Rich style strings."""


@dataclass
class HierarchyNode:
    """A node in the hierarchy tree.

    Attributes:
        name: Display name of the node.
        alias: Short alias or abbreviation.
        level: Hierarchy level (grandparent, parent, child, grandchild).
        description: Optional description of the node.
        children: List of child nodes.
    """

    name: str
    alias: str
    level: HierarchyLevel
    description: str = ""
    children: list["HierarchyNode"] = field(default_factory=list)


@dataclass
class HierarchyDisplay:
    """Component for rendering data hierarchies.

    Renders hierarchy trees using Rich Tree with level-appropriate styling.
    Supports grandparent, parent, child, and grandchild levels with
    distinct visual styling for each level.

    Attributes:
        root: Root node of the hierarchy tree.
    """

    root: HierarchyNode

    def render(self, console: Console | None = None) -> str:
        """Render the hierarchy as a Rich Tree.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Rendered tree as a string.
        """
        if console is None:
            console = Console()

        tree = Tree(self._format_node(self.root))
        self._add_children(tree, self.root)

        with console.capture() as capture:
            console.print(tree)
        return capture.get()

    def render_tree(self) -> Tree:
        """Render the hierarchy as a Rich Tree object.

        Returns:
            Rich Tree object for direct console printing.
        """
        tree = Tree(self._format_node(self.root))
        self._add_children(tree, self.root)
        return tree

    def _format_node(self, node: HierarchyNode) -> Text:
        """Format a single node with appropriate styling.

        Args:
            node: HierarchyNode to format.

        Returns:
            Rich Text object with styled node content.
        """
        style = HIERARCHY_STYLES[node.level]
        text = Text()
        text.append(f"{node.name}", style=style)
        text.append(f" ({node.alias})", style="dim")
        if node.description:
            text.append(f" - {node.description}", style="italic")
        return text

    def _add_children(self, tree: Tree, node: HierarchyNode) -> None:
        """Recursively add children to the tree.

        Args:
            tree: Rich Tree or branch to add children to.
            node: Parent node whose children to add.
        """
        for child in node.children:
            branch = tree.add(self._format_node(child))
            self._add_children(branch, child)

    def find_node(self, term: str) -> HierarchyNode | None:
        """Find a node by name or alias.

        Args:
            term: Name or alias to search for (case-insensitive).

        Returns:
            HierarchyNode if found, None otherwise.
        """
        return self._find_node_recursive(self.root, term.lower())

    def _find_node_recursive(
        self, node: HierarchyNode, term: str
    ) -> HierarchyNode | None:
        """Recursively search for a node by name or alias.

        Args:
            node: Current node to check.
            term: Lowercase term to search for.

        Returns:
            HierarchyNode if found, None otherwise.
        """
        if node.name.lower() == term or node.alias.lower() == term:
            return node
        for child in node.children:
            result = self._find_node_recursive(child, term)
            if result:
                return result
        return None

    def get_ancestors(self, term: str) -> list[HierarchyNode]:
        """Get the ancestor path to a node.

        Args:
            term: Name or alias to search for.

        Returns:
            List of ancestor nodes from root to parent of target.
        """
        path: list[HierarchyNode] = []
        self._find_path(self.root, term.lower(), path)
        return path[:-1] if path else []  # Exclude the target node itself

    def _find_path(
        self, node: HierarchyNode, term: str, path: list[HierarchyNode]
    ) -> bool:
        """Recursively find path to a node.

        Args:
            node: Current node to check.
            term: Lowercase term to search for.
            path: Current path being built.

        Returns:
            True if node found in this subtree, False otherwise.
        """
        path.append(node)
        if node.name.lower() == term or node.alias.lower() == term:
            return True
        for child in node.children:
            if self._find_path(child, term, path):
                return True
        path.pop()
        return False
