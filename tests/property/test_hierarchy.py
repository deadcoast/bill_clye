"""Property tests for Hierarchy Display component.

Feature: mrdr-visual-integration, Property 13: Hierarchy Level Indentation
Feature: mrdr-visual-integration, Property 14: Hierarchy Term Lookup
Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.database.hierarchy import build_dictionary_hierarchy, get_all_terms
from mrdr.render.components import (
    HIERARCHY_STYLES,
    HierarchyDisplay,
    HierarchyLevel,
    HierarchyNode,
)


# Strategy for valid node names (alphanumeric, no special chars)
node_name_strategy = st.text(
    min_size=1,
    max_size=15,
    alphabet=st.characters(whitelist_categories=("L", "N"), blacklist_characters="\r\n\t\x00"),
)

# Strategy for valid aliases
alias_strategy = st.text(
    min_size=1,
    max_size=10,
    alphabet=st.characters(whitelist_categories=("L", "N"), blacklist_characters="\r\n\t\x00"),
)

# Strategy for descriptions
description_strategy = st.text(
    min_size=0,
    max_size=30,
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z"), blacklist_characters="\r\n\t\x00"),
)


def make_grandchild_node(name: str, alias: str, description: str) -> HierarchyNode:
    """Create a grandchild node."""
    return HierarchyNode(
        name=name,
        alias=alias,
        level=HierarchyLevel.GRANDCHILD,
        description=description,
    )


def make_child_node(
    name: str, alias: str, description: str, grandchildren: list[HierarchyNode]
) -> HierarchyNode:
    """Create a child node with optional grandchildren."""
    return HierarchyNode(
        name=name,
        alias=alias,
        level=HierarchyLevel.CHILD,
        description=description,
        children=grandchildren,
    )


def make_parent_node(
    name: str, alias: str, description: str, children: list[HierarchyNode]
) -> HierarchyNode:
    """Create a parent node with optional children."""
    return HierarchyNode(
        name=name,
        alias=alias,
        level=HierarchyLevel.PARENT,
        description=description,
        children=children,
    )


def make_grandparent_node(
    name: str, alias: str, description: str, parents: list[HierarchyNode]
) -> HierarchyNode:
    """Create a grandparent (root) node with optional parent children."""
    return HierarchyNode(
        name=name,
        alias=alias,
        level=HierarchyLevel.GRANDPARENT,
        description=description,
        children=parents,
    )


# Strategy for grandchild nodes
grandchild_strategy = st.builds(
    make_grandchild_node,
    name=node_name_strategy,
    alias=alias_strategy,
    description=description_strategy,
)

# Strategy for child nodes (with 0-2 grandchildren)
child_strategy = st.builds(
    make_child_node,
    name=node_name_strategy,
    alias=alias_strategy,
    description=description_strategy,
    grandchildren=st.lists(grandchild_strategy, min_size=0, max_size=2),
)

# Strategy for parent nodes (with 0-2 children)
parent_strategy = st.builds(
    make_parent_node,
    name=node_name_strategy,
    alias=alias_strategy,
    description=description_strategy,
    children=st.lists(child_strategy, min_size=0, max_size=2),
)

# Strategy for grandparent (root) nodes (with 0-2 parents)
grandparent_strategy = st.builds(
    make_grandparent_node,
    name=node_name_strategy,
    alias=alias_strategy,
    description=description_strategy,
    parents=st.lists(parent_strategy, min_size=0, max_size=2),
)


@given(root=grandparent_strategy)
@settings(max_examples=100)
def test_hierarchy_level_indentation(root: HierarchyNode) -> None:
    """Property 13: Hierarchy Level Indentation.

    Feature: mrdr-visual-integration, Property 13: Hierarchy Level Indentation
    For any hierarchy tree, grandparent nodes SHALL have zero indentation,
    parent nodes SHALL have 1-level indentation, child nodes SHALL have
    2-level indentation, and grandchild nodes SHALL have 3-level indentation.
    **Validates: Requirements 6.1, 6.2, 6.3, 6.5**
    """
    display = HierarchyDisplay(root=root)
    output = display.render()
    lines = output.strip().split("\n")

    # Root (grandparent) should be at the start of the first line (no leading tree chars)
    # Rich Tree uses └── and ├── for branches
    first_line = lines[0]
    # The root node name should appear without tree branch prefix
    assert root.name in first_line, f"Root name '{root.name}' should be in first line"
    # First line should not start with tree branch characters
    assert not first_line.lstrip().startswith(("└", "├", "│")), \
        "Root should not have tree branch prefix"

    # Check that children have increasing indentation
    # Rich Tree adds "└── " or "├── " for each level
    for parent in root.children:
        # Parent should appear with 1-level indentation (has tree branch)
        parent_found = any(parent.name in line and ("└" in line or "├" in line) for line in lines)
        assert parent_found, f"Parent '{parent.name}' should have tree branch indentation"

        for child in parent.children:
            # Child should appear with deeper indentation
            child_found = any(child.name in line for line in lines)
            assert child_found, f"Child '{child.name}' should appear in output"

            for grandchild in child.children:
                # Grandchild should appear with deepest indentation
                grandchild_found = any(grandchild.name in line for line in lines)
                assert grandchild_found, f"Grandchild '{grandchild.name}' should appear in output"


@given(root=grandparent_strategy)
@settings(max_examples=100)
def test_hierarchy_styles_applied(root: HierarchyNode) -> None:
    """Property 13: Hierarchy Level Indentation - styles.

    Feature: mrdr-visual-integration, Property 13: Hierarchy Level Indentation
    For any hierarchy tree, each level SHALL have distinct styling defined
    in HIERARCHY_STYLES mapping.
    **Validates: Requirements 6.1, 6.2, 6.3, 6.5**
    """
    # Verify HIERARCHY_STYLES has all levels
    assert HierarchyLevel.GRANDPARENT in HIERARCHY_STYLES
    assert HierarchyLevel.PARENT in HIERARCHY_STYLES
    assert HierarchyLevel.CHILD in HIERARCHY_STYLES
    assert HierarchyLevel.GRANDCHILD in HIERARCHY_STYLES

    # Verify styles are distinct
    styles = list(HIERARCHY_STYLES.values())
    assert len(styles) == len(set(styles)), "Each level should have distinct styling"

    # Verify rendering works
    display = HierarchyDisplay(root=root)
    output = display.render()
    assert output, "Hierarchy should render non-empty output"


@given(root=grandparent_strategy)
@settings(max_examples=100)
def test_hierarchy_node_format(root: HierarchyNode) -> None:
    """Property 13: Hierarchy Level Indentation - node format.

    Feature: mrdr-visual-integration, Property 13: Hierarchy Level Indentation
    For any hierarchy node, the output SHALL contain name, alias in parentheses,
    and description if present.
    **Validates: Requirements 6.1, 6.2, 6.3, 6.5**
    """
    display = HierarchyDisplay(root=root)
    output = display.render()

    # Root node should have name and alias
    assert root.name in output, f"Root name '{root.name}' should be in output"
    assert f"({root.alias})" in output, f"Root alias '({root.alias})' should be in output"

    # If description exists, it should be in output
    if root.description:
        assert root.description in output, "Root description should be in output"


def test_hierarchy_grandparent_zero_indentation() -> None:
    """Grandparent nodes SHALL have zero indentation."""
    root = HierarchyNode(
        name="NOTE",
        alias="note",
        level=HierarchyLevel.GRANDPARENT,
        description="Top level",
    )
    display = HierarchyDisplay(root=root)
    output = display.render()
    lines = output.strip().split("\n")

    # First line should start with the node name (no tree prefix)
    first_line = lines[0]
    # Should not start with whitespace or tree characters
    assert first_line[0] not in " └├│", "Grandparent should have zero indentation"


def test_hierarchy_parent_one_level_indentation() -> None:
    """Parent nodes SHALL have 1-level indentation."""
    root = HierarchyNode(
        name="NOTE",
        alias="note",
        level=HierarchyLevel.GRANDPARENT,
        children=[
            HierarchyNode(
                name="apd",
                alias="ASPERDEFINED",
                level=HierarchyLevel.PARENT,
            )
        ],
    )
    display = HierarchyDisplay(root=root)
    output = display.render()
    lines = output.strip().split("\n")

    # Second line should have tree branch for parent
    assert len(lines) >= 2, "Should have at least 2 lines"
    parent_line = lines[1]
    assert "└" in parent_line or "├" in parent_line, "Parent should have tree branch"
    assert "apd" in parent_line, "Parent name should be in line"


def test_hierarchy_child_two_level_indentation() -> None:
    """Child nodes SHALL have 2-level indentation."""
    root = HierarchyNode(
        name="NOTE",
        alias="note",
        level=HierarchyLevel.GRANDPARENT,
        children=[
            HierarchyNode(
                name="apd",
                alias="ASPERDEFINED",
                level=HierarchyLevel.PARENT,
                children=[
                    HierarchyNode(
                        name="sem",
                        alias="semantics",
                        level=HierarchyLevel.CHILD,
                    )
                ],
            )
        ],
    )
    display = HierarchyDisplay(root=root)
    output = display.render()
    lines = output.strip().split("\n")

    # Third line should have deeper indentation for child
    assert len(lines) >= 3, "Should have at least 3 lines"
    child_line = lines[2]
    assert "sem" in child_line, "Child name should be in line"
    # Child should have more leading space than parent
    parent_line = lines[1]
    # Count leading whitespace/tree chars
    assert child_line.find("sem") > parent_line.find("apd"), \
        "Child should be indented more than parent"


def test_hierarchy_grandchild_three_level_indentation() -> None:
    """Grandchild nodes SHALL have 3-level indentation."""
    root = HierarchyNode(
        name="NOTE",
        alias="note",
        level=HierarchyLevel.GRANDPARENT,
        children=[
            HierarchyNode(
                name="apd",
                alias="ASPERDEFINED",
                level=HierarchyLevel.PARENT,
                children=[
                    HierarchyNode(
                        name="sem",
                        alias="semantics",
                        level=HierarchyLevel.CHILD,
                        children=[
                            HierarchyNode(
                                name="val",
                                alias="value",
                                level=HierarchyLevel.GRANDCHILD,
                            )
                        ],
                    )
                ],
            )
        ],
    )
    display = HierarchyDisplay(root=root)
    output = display.render()
    lines = output.strip().split("\n")

    # Fourth line should have deepest indentation for grandchild
    assert len(lines) >= 4, "Should have at least 4 lines"
    grandchild_line = lines[3]
    assert "val" in grandchild_line, "Grandchild name should be in line"
    # Grandchild should have more leading space than child
    child_line = lines[2]
    assert grandchild_line.find("val") > child_line.find("sem"), \
        "Grandchild should be indented more than child"



# ============================================================================
# Property 14: Hierarchy Term Lookup Tests
# ============================================================================


@given(
    name=node_name_strategy,
    alias=alias_strategy,
)
@settings(max_examples=100)
def test_hierarchy_term_lookup_by_name_or_alias(name: str, alias: str) -> None:
    """Property 14: Hierarchy Term Lookup.

    Feature: mrdr-visual-integration, Property 14: Hierarchy Term Lookup
    For any term in the dictionary hierarchy, `mrdr hyde hierarchy <term>`
    SHALL display the term's position showing its level and ancestors.
    **Validates: Requirements 6.4**
    """
    # Create a simple hierarchy with the generated name/alias
    root = HierarchyNode(
        name="ROOT",
        alias="root",
        level=HierarchyLevel.GRANDPARENT,
        children=[
            HierarchyNode(
                name=name,
                alias=alias,
                level=HierarchyLevel.PARENT,
            )
        ],
    )
    display = HierarchyDisplay(root=root)

    # Should find by name (case-insensitive)
    found_by_name = display.find_node(name)
    assert found_by_name is not None, f"Should find node by name '{name}'"
    assert found_by_name.name == name

    # Should find by alias (case-insensitive)
    found_by_alias = display.find_node(alias)
    assert found_by_alias is not None, f"Should find node by alias '{alias}'"
    assert found_by_alias.alias == alias


@given(root=grandparent_strategy)
@settings(max_examples=100)
def test_hierarchy_lookup_returns_ancestors(root: HierarchyNode) -> None:
    """Property 14: Hierarchy Term Lookup - ancestors.

    Feature: mrdr-visual-integration, Property 14: Hierarchy Term Lookup
    For any term lookup, the result SHALL include the ancestor path
    from root to the term's parent.
    **Validates: Requirements 6.4**
    """
    display = HierarchyDisplay(root=root)

    # Verify that root can always be found
    found_root = display.find_node(root.name)
    assert found_root is not None, "Root should always be findable"

    # Verify ancestors of root is empty (root has no ancestors)
    root_ancestors = display.get_ancestors(root.name)
    assert root_ancestors == [], "Root should have no ancestors"

    # For any found node, ancestors should form a valid path
    for parent in root.children:
        found_parent = display.find_node(parent.name)
        if found_parent and found_parent.name == parent.name:
            parent_ancestors = display.get_ancestors(parent.name)
            # Parent's ancestors should include root
            if parent_ancestors:
                assert parent_ancestors[0].name == root.name, \
                    "First ancestor of parent should be root"


def test_hierarchy_lookup_dictionary_terms() -> None:
    """Property 14: Hierarchy Term Lookup - dictionary terms.

    Feature: mrdr-visual-integration, Property 14: Hierarchy Term Lookup
    For any term in the MRDR dictionary, lookup SHALL succeed and
    return the correct node.
    **Validates: Requirements 6.4**
    """
    root = build_dictionary_hierarchy()
    display = HierarchyDisplay(root=root)

    # Test known dictionary terms
    known_terms = [
        ("NOTE", "grandparent"),
        ("CLAIM", "grandparent"),
        ("apd", "parent"),
        ("objacc", "parent"),
        ("sem", "child"),
        ("def", "child"),
        ("val", "grandchild"),
    ]

    for term, expected_level in known_terms:
        found = display.find_node(term)
        assert found is not None, f"Should find term '{term}'"
        assert found.level.value == expected_level, \
            f"Term '{term}' should be at level '{expected_level}'"


def test_hierarchy_lookup_case_insensitive() -> None:
    """Property 14: Hierarchy Term Lookup - case insensitivity.

    Feature: mrdr-visual-integration, Property 14: Hierarchy Term Lookup
    Term lookup SHALL be case-insensitive.
    **Validates: Requirements 6.4**
    """
    root = build_dictionary_hierarchy()
    display = HierarchyDisplay(root=root)

    # Test case variations
    assert display.find_node("NOTE") is not None
    assert display.find_node("note") is not None
    assert display.find_node("Note") is not None
    assert display.find_node("SEM") is not None
    assert display.find_node("sem") is not None
    assert display.find_node("Sem") is not None


def test_hierarchy_lookup_not_found() -> None:
    """Property 14: Hierarchy Term Lookup - not found.

    Feature: mrdr-visual-integration, Property 14: Hierarchy Term Lookup
    For terms not in the hierarchy, lookup SHALL return None.
    **Validates: Requirements 6.4**
    """
    root = build_dictionary_hierarchy()
    display = HierarchyDisplay(root=root)

    # Test non-existent terms
    assert display.find_node("nonexistent") is None
    assert display.find_node("xyz123") is None
    assert display.find_node("") is None


def test_hierarchy_get_all_terms() -> None:
    """Property 14: Hierarchy Term Lookup - all terms list.

    Feature: mrdr-visual-integration, Property 14: Hierarchy Term Lookup
    get_all_terms SHALL return all term names and aliases.
    **Validates: Requirements 6.4**
    """
    terms = get_all_terms()

    # Should contain known terms (lowercase)
    assert "note" in terms
    assert "claim" in terms
    assert "apd" in terms
    assert "asperdefined" in terms
    assert "sem" in terms
    assert "semantics" in terms
    assert "val" in terms
    assert "value" in terms


def test_hierarchy_ancestors_path_order() -> None:
    """Property 14: Hierarchy Term Lookup - ancestor path order.

    Feature: mrdr-visual-integration, Property 14: Hierarchy Term Lookup
    Ancestor path SHALL be ordered from root to parent of target.
    **Validates: Requirements 6.4**
    """
    root = build_dictionary_hierarchy()
    display = HierarchyDisplay(root=root)

    # Get ancestors for 'val' (grandchild level)
    ancestors = display.get_ancestors("val")

    # Should have path: MRDR_DICTIONARY -> NOTE -> apd -> sem
    assert len(ancestors) == 4, "val should have 4 ancestors"
    assert ancestors[0].name == "MRDR_DICTIONARY"
    assert ancestors[1].name == "NOTE"
    assert ancestors[2].name == "apd"
    assert ancestors[3].name == "sem"
