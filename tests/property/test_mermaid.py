"""Property tests for Mermaid Renderer component.

Feature: mrdr-visual-integration
Properties 15, 16, 17: Mermaid Flowchart, Sequence, and Fallback Rendering
Validates: Requirements 7.1, 7.2, 7.3, 7.4
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.components import MermaidDiagramType, MermaidRenderer


# Strategy for valid node identifiers (alphanumeric, starting with letter)
node_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L",)),
    min_size=1,
    max_size=5,
).map(lambda s: s.capitalize())

# Strategy for node labels (printable text without special chars)
node_label_strategy = st.text(
    min_size=1,
    max_size=15,
    alphabet=st.characters(
        whitelist_categories=("L", "N", "S"),
        blacklist_characters='[]"\'`\n\r\t\\',
    ),
).filter(lambda s: s.strip() == s and len(s.strip()) > 0)

# Strategy for flowchart directions
direction_strategy = st.sampled_from(["TB", "LR", "BT", "RL"])


def build_flowchart(
    direction: str, nodes: list[tuple[str, str]], connections: list[tuple[int, int]]
) -> str:
    """Build a Mermaid flowchart source string.

    Args:
        direction: Flowchart direction (TB, LR, BT, RL).
        nodes: List of (node_id, label) tuples.
        connections: List of (from_index, to_index) tuples.

    Returns:
        Mermaid flowchart source string.
    """
    lines = [f"flowchart {direction}"]
    for node_id, label in nodes:
        lines.append(f'    {node_id}["{label}"]')
    for from_idx, to_idx in connections:
        if 0 <= from_idx < len(nodes) and 0 <= to_idx < len(nodes):
            lines.append(f"    {nodes[from_idx][0]} --> {nodes[to_idx][0]}")
    return "\n".join(lines)


@given(
    direction=direction_strategy,
    node_labels=st.lists(node_label_strategy, min_size=1, max_size=4, unique=True),
)
@settings(max_examples=100)
def test_mermaid_flowchart_rendering(direction: str, node_labels: list[str]) -> None:
    """Property 15: Mermaid Flowchart Rendering.

    Feature: mrdr-visual-integration, Property 15: Mermaid Flowchart Rendering
    For any valid Mermaid flowchart source with LR or TB direction, the
    Mermaid_Renderer SHALL produce ASCII output containing box characters
    and arrow indicators.
    **Validates: Requirements 7.1, 7.2**
    """
    # Build nodes with unique IDs
    nodes = [(f"N{i}", label) for i, label in enumerate(node_labels)]

    # Build connections (linear chain)
    connections = [(i, i + 1) for i in range(len(nodes) - 1)]

    source = build_flowchart(direction, nodes, connections)
    renderer = MermaidRenderer()
    output = renderer.render(source)

    # Output should contain box characters
    assert "┌" in output, "Output should contain top-left box corner"
    assert "┐" in output, "Output should contain top-right box corner"
    assert "└" in output, "Output should contain bottom-left box corner"
    assert "┘" in output, "Output should contain bottom-right box corner"
    assert "─" in output, "Output should contain horizontal box line"
    assert "│" in output, "Output should contain vertical box line"

    # Output should contain all node labels
    for _, label in nodes:
        assert label in output, f"Output should contain node label '{label}'"

    # For multi-node flowcharts, output should contain arrow indicators
    if len(nodes) > 1:
        if direction in ("LR", "RL"):
            # Horizontal arrows
            assert "►" in output, "Horizontal flowchart should contain arrow indicator"
        else:
            # Vertical arrows
            assert "▼" in output, "Vertical flowchart should contain arrow indicator"


@given(direction=direction_strategy)
@settings(max_examples=50)
def test_mermaid_flowchart_type_detection(direction: str) -> None:
    """Property 15: Mermaid Flowchart Rendering - type detection.

    Feature: mrdr-visual-integration, Property 15: Mermaid Flowchart Rendering
    For any flowchart source, the renderer SHALL correctly detect the
    diagram type as FLOWCHART.
    **Validates: Requirements 7.1, 7.2**
    """
    source = f"""flowchart {direction}
    A["Start"]
    B["End"]
    A --> B
"""
    renderer = MermaidRenderer()
    diagram_type = renderer._detect_type(source)

    assert diagram_type == MermaidDiagramType.FLOWCHART, (
        f"Flowchart source should be detected as FLOWCHART, got {diagram_type}"
    )


def test_mermaid_flowchart_graph_keyword() -> None:
    """Flowchart with 'graph' keyword should also be detected.

    **Validates: Requirements 7.1**
    """
    source = """graph TB
    A["Start"]
    B["End"]
    A --> B
"""
    renderer = MermaidRenderer()
    diagram_type = renderer._detect_type(source)

    assert diagram_type == MermaidDiagramType.FLOWCHART, (
        "Source starting with 'graph' should be detected as FLOWCHART"
    )


def test_mermaid_flowchart_vertical_layout() -> None:
    """Vertical flowchart (TB) should render with vertical arrows.

    **Validates: Requirements 7.1, 7.2**
    """
    source = """flowchart TB
    A["Start"]
    B["Process"]
    C["End"]
    A --> B
    B --> C
"""
    renderer = MermaidRenderer()
    output = renderer.render(source)

    # Should have vertical arrow
    assert "▼" in output, "Vertical flowchart should have down arrow"
    # Should have all labels
    assert "Start" in output
    assert "Process" in output
    assert "End" in output


def test_mermaid_flowchart_horizontal_layout() -> None:
    """Horizontal flowchart (LR) should render with horizontal arrows.

    **Validates: Requirements 7.1, 7.2**
    """
    source = """flowchart LR
    A["Input"]
    B["Process"]
    C["Output"]
    A --> B
    B --> C
"""
    renderer = MermaidRenderer()
    output = renderer.render(source)

    # Should have horizontal arrow
    assert "►" in output, "Horizontal flowchart should have right arrow"
    # Should have all labels
    assert "Input" in output
    assert "Process" in output
    assert "Output" in output


# Strategy for participant names (alphanumeric, starting with letter)
participant_strategy = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll"),  # Only uppercase and lowercase letters
        blacklist_characters="İıİı",  # Exclude Turkish dotted/dotless i variants
    ),
    min_size=2,
    max_size=10,
).map(lambda s: s.capitalize() if s else "Participant")

# Strategy for message text
message_strategy = st.text(
    min_size=1,
    max_size=20,
    alphabet=st.characters(
        whitelist_categories=("L", "N", "S"),
        blacklist_characters='\n\r\t\\:',
    ),
).filter(lambda s: s.strip() == s and len(s.strip()) > 0)


def build_sequence_diagram(
    participants: list[str], messages: list[tuple[int, int, str]]
) -> str:
    """Build a Mermaid sequence diagram source string.

    Args:
        participants: List of participant names.
        messages: List of (from_index, to_index, message) tuples.

    Returns:
        Mermaid sequence diagram source string.
    """
    lines = ["sequenceDiagram"]
    for p in participants:
        lines.append(f"    participant {p}")
    for from_idx, to_idx, msg in messages:
        if 0 <= from_idx < len(participants) and 0 <= to_idx < len(participants):
            lines.append(f"    {participants[from_idx]}->>{participants[to_idx]}: {msg}")
    return "\n".join(lines)


@given(
    participants=st.lists(participant_strategy, min_size=2, max_size=4, unique=True),
    message_texts=st.lists(message_strategy, min_size=1, max_size=3),
)
@settings(max_examples=100)
def test_mermaid_sequence_rendering(
    participants: list[str], message_texts: list[str]
) -> None:
    """Property 16: Mermaid Sequence Rendering.

    Feature: mrdr-visual-integration, Property 16: Mermaid Sequence Rendering
    For any valid Mermaid sequence diagram, the Mermaid_Renderer SHALL
    produce output containing participant names and message arrows.
    **Validates: Requirements 7.3**
    """
    # Build messages between participants
    messages = []
    for i, msg in enumerate(message_texts):
        from_idx = i % len(participants)
        to_idx = (i + 1) % len(participants)
        messages.append((from_idx, to_idx, msg))

    source = build_sequence_diagram(participants, messages)
    renderer = MermaidRenderer()
    output = renderer.render(source)

    # Output should contain participant names in brackets
    for p in participants:
        assert f"[{p}]" in output, f"Output should contain participant [{p}]"

    # Output should contain message arrows
    assert "►" in output, "Output should contain message arrow indicator"

    # Output should contain lifeline characters
    assert "│" in output, "Output should contain lifeline character"


@given(participants=st.lists(participant_strategy, min_size=2, max_size=3, unique=True))
@settings(max_examples=50)
def test_mermaid_sequence_type_detection(participants: list[str]) -> None:
    """Property 16: Mermaid Sequence Rendering - type detection.

    Feature: mrdr-visual-integration, Property 16: Mermaid Sequence Rendering
    For any sequence diagram source, the renderer SHALL correctly detect
    the diagram type as SEQUENCE.
    **Validates: Requirements 7.3**
    """
    source = f"""sequenceDiagram
    participant {participants[0]}
    participant {participants[1]}
    {participants[0]}->>{participants[1]}: Hello
"""
    renderer = MermaidRenderer()
    diagram_type = renderer._detect_type(source)

    assert diagram_type == MermaidDiagramType.SEQUENCE, (
        f"Sequence diagram source should be detected as SEQUENCE, got {diagram_type}"
    )


def test_mermaid_sequence_implicit_participants() -> None:
    """Sequence diagram without explicit participants should still render.

    **Validates: Requirements 7.3**
    """
    source = """sequenceDiagram
    Client->>Server: Request
    Server->>Client: Response
"""
    renderer = MermaidRenderer()
    output = renderer.render(source)

    # Should detect participants from messages
    assert "[Client]" in output, "Should detect Client participant"
    assert "[Server]" in output, "Should detect Server participant"
    # Should contain messages
    assert "Request" in output
    assert "Response" in output


def test_mermaid_sequence_message_arrows() -> None:
    """Sequence diagram should render message arrows correctly.

    **Validates: Requirements 7.3**
    """
    source = """sequenceDiagram
    participant Alice
    participant Bob
    Alice->>Bob: Hello
    Bob->>Alice: Hi
"""
    renderer = MermaidRenderer()
    output = renderer.render(source)

    # Should have arrow indicators
    assert "►" in output, "Should have arrow indicator"
    # Should have both messages
    assert "Hello" in output
    assert "Hi" in output


# Strategy for arbitrary text (for fallback testing)
arbitrary_text_strategy = st.text(
    min_size=1,
    max_size=100,
    alphabet=st.characters(
        whitelist_categories=("L", "N", "P", "S"),
        blacklist_characters="\x00",
    ),
)


@given(source=arbitrary_text_strategy)
@settings(max_examples=100)
def test_mermaid_fallback_rendering(source: str) -> None:
    """Property 17: Mermaid Fallback.

    Feature: mrdr-visual-integration, Property 17: Mermaid Fallback
    For any invalid or unsupported Mermaid source, the Mermaid_Renderer
    SHALL return the raw source wrapped in mermaid code fence markers.
    **Validates: Requirements 7.4**
    """
    # Ensure source doesn't start with valid diagram keywords
    if source.strip().lower().startswith(("flowchart", "graph", "sequencediagram")):
        source = "invalid_" + source

    renderer = MermaidRenderer()
    output = renderer.render(source)

    # Output should be wrapped in mermaid code fence
    assert output.startswith("```mermaid\n"), "Fallback should start with ```mermaid"
    assert output.endswith("\n```"), "Fallback should end with ```"

    # Output should contain the original source (stripped)
    assert source.strip() in output, "Fallback should contain original source"


@given(source=arbitrary_text_strategy)
@settings(max_examples=50)
def test_mermaid_unknown_type_detection(source: str) -> None:
    """Property 17: Mermaid Fallback - unknown type detection.

    Feature: mrdr-visual-integration, Property 17: Mermaid Fallback
    For any source that doesn't match known diagram types, the renderer
    SHALL detect it as UNKNOWN type.
    **Validates: Requirements 7.4**
    """
    # Ensure source doesn't start with valid diagram keywords
    if source.strip().lower().startswith(("flowchart", "graph", "sequencediagram")):
        source = "unknown_" + source

    renderer = MermaidRenderer()
    diagram_type = renderer._detect_type(source)

    assert diagram_type == MermaidDiagramType.UNKNOWN, (
        f"Unknown source should be detected as UNKNOWN, got {diagram_type}"
    )


def test_mermaid_fallback_pie_chart() -> None:
    """Unsupported pie chart should fall back to raw source.

    **Validates: Requirements 7.4**
    """
    source = """pie title Pets
    "Dogs" : 386
    "Cats" : 85
"""
    renderer = MermaidRenderer()
    output = renderer.render(source)

    assert "```mermaid" in output, "Should wrap in mermaid fence"
    assert "pie title Pets" in output, "Should contain original source"
    assert "```" in output, "Should have closing fence"


def test_mermaid_fallback_class_diagram() -> None:
    """Unsupported class diagram should fall back to raw source.

    **Validates: Requirements 7.4**
    """
    source = """classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
"""
    renderer = MermaidRenderer()
    output = renderer.render(source)

    assert "```mermaid" in output, "Should wrap in mermaid fence"
    assert "classDiagram" in output, "Should contain original source"


def test_mermaid_fallback_exception_handling() -> None:
    """Renderer should gracefully handle exceptions and fall back.

    **Validates: Requirements 7.4**
    """
    # This tests that even if internal parsing fails, we get fallback
    source = """flowchart TB
    A["Unclosed bracket
"""
    renderer = MermaidRenderer()
    output = renderer.render(source)

    # Should either render partially or fall back gracefully
    # The key is no exception should propagate
    assert isinstance(output, str), "Should return a string"
    assert len(output) > 0, "Should return non-empty output"
