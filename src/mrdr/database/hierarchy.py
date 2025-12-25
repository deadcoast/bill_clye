"""Hierarchy data loader for MRDR.

This module provides the dictionary hierarchy data structure based on
docs/dictionary.md, supporting term lookup and tree display.
"""

from mrdr.render.components import HierarchyLevel, HierarchyNode


def build_dictionary_hierarchy() -> HierarchyNode:
    """Build the complete dictionary hierarchy tree.

    Returns the root node containing the full MRDR dictionary hierarchy
    as defined in docs/dictionary.md.

    Returns:
        HierarchyNode: Root of the dictionary hierarchy tree.
    """
    # Grandchild level nodes
    val_node = HierarchyNode(
        name="val",
        alias="value",
        level=HierarchyLevel.GRANDCHILD,
        description="The value of Parent or Child function",
    )

    # Child level nodes (functions)
    child_nodes = [
        HierarchyNode(
            name="sem",
            alias="semantics",
            level=HierarchyLevel.CHILD,
            description="arguing out of good faith",
            children=[val_node],
        ),
        HierarchyNode(
            name="def",
            alias="definition",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="dstr",
            alias="docstring",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="rsch",
            alias="research",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="stat",
            alias="statistic",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="eg",
            alias="example",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="vldt",
            alias="validated",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="expr",
            alias="experimental",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="optml",
            alias="optimal",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="unstbl",
            alias="unstable",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="vislap",
            alias="visually_appealing",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
        HierarchyNode(
            name="crtv",
            alias="creative",
            level=HierarchyLevel.CHILD,
            description="APD",
        ),
    ]

    # Parent level nodes (commands)
    parent_nodes = [
        HierarchyNode(
            name="apd",
            alias="ASPERDEFINED",
            level=HierarchyLevel.PARENT,
            description="Reference is in context to traditional definition",
            children=child_nodes,
        ),
        HierarchyNode(
            name="objacc",
            alias="OBJECTIVEACCEPTANCE",
            level=HierarchyLevel.PARENT,
            description="A statement or claim that is obvious in nature",
        ),
    ]

    # Grandparent level nodes (top-level functions)
    grandparent_nodes = [
        HierarchyNode(
            name="NOTE",
            alias="note",
            level=HierarchyLevel.GRANDPARENT,
            description="Additional notes provided in the authors voice",
            children=parent_nodes,
        ),
        HierarchyNode(
            name="CLAIM",
            alias="claim",
            level=HierarchyLevel.GRANDPARENT,
            description="Top level Claims",
        ),
        HierarchyNode(
            name="LANG_USE",
            alias="lang_use",
            level=HierarchyLevel.GRANDPARENT,
            description="Identifies additional utilization of a term in a different language",
        ),
        HierarchyNode(
            name="FORMAT",
            alias="format",
            level=HierarchyLevel.GRANDPARENT,
            description="Identifies the format of the documentation",
        ),
        HierarchyNode(
            name="PURPOSE",
            alias="purpose",
            level=HierarchyLevel.GRANDPARENT,
            description="Identifies the purpose of the documentation",
        ),
        HierarchyNode(
            name="RESTRICTIONS",
            alias="restrictions",
            level=HierarchyLevel.GRANDPARENT,
            description="Identifies the restrictions of the documentation",
        ),
        HierarchyNode(
            name="STYLING",
            alias="styling",
            level=HierarchyLevel.GRANDPARENT,
            description="Identifies the styling of the documentation",
        ),
        HierarchyNode(
            name="USER",
            alias="user",
            level=HierarchyLevel.GRANDPARENT,
            description="Identifies the user of the documentation",
        ),
        HierarchyNode(
            name="NOTES",
            alias="notes",
            level=HierarchyLevel.GRANDPARENT,
            description="Identifies any additional important notes about the corresponding data",
        ),
    ]

    # Root node representing the entire dictionary
    root = HierarchyNode(
        name="MRDR_DICTIONARY",
        alias="dictionary",
        level=HierarchyLevel.GRANDPARENT,
        description="Visual CLI Database Ecosystem dictionary hierarchy",
        children=grandparent_nodes,
    )

    return root


def get_all_terms() -> list[str]:
    """Get all term names and aliases from the hierarchy.

    Returns:
        List of all term names and aliases (lowercase).
    """
    root = build_dictionary_hierarchy()
    terms: list[str] = []
    _collect_terms(root, terms)
    return terms


def _collect_terms(node: HierarchyNode, terms: list[str]) -> None:
    """Recursively collect all term names and aliases.

    Args:
        node: Current node to process.
        terms: List to append terms to.
    """
    terms.append(node.name.lower())
    terms.append(node.alias.lower())
    for child in node.children:
        _collect_terms(child, terms)
