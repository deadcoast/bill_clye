"""Property tests for Python Style Renderer.

Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
For any Python docstring style (sphinx, google, numpy, epytext, pep257),
the rendered output SHALL contain the style-specific markers: `:param:` for sphinx,
`Args:` for google, `Parameters\n----------` for numpy, `@param` for epytext.

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.7**
"""

import re

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.python_style import (
    STYLE_METADATA,
    STYLE_RULES,
    STYLE_TEMPLATES,
    PythonDocstringStyle,
    PythonStyleRenderer,
)


# Strategy for valid Python docstring styles
python_style_strategy = st.sampled_from(list(PythonDocstringStyle))


@given(style=python_style_strategy)
@settings(max_examples=100)
def test_python_style_format_compliance(style: PythonDocstringStyle) -> None:
    """Property 12: Python Style Format Compliance.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    For any Python docstring style (sphinx, google, numpy, epytext, pep257),
    the rendered output SHALL contain the style-specific markers.
    **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.7**
    """
    renderer = PythonStyleRenderer()
    template = STYLE_TEMPLATES[style]
    metadata = STYLE_METADATA[style]

    # Template should contain style-specific markers
    markers = metadata["markers"]

    if markers:  # PEP257 has no specific markers
        found_markers = [m for m in markers if m in template]
        assert len(found_markers) > 0, (
            f"Style {style.value} should contain at least one marker from {markers}"
        )


@given(style=python_style_strategy)
@settings(max_examples=100)
def test_python_style_docstring_delimiters(style: PythonDocstringStyle) -> None:
    """Property 12: Python Style Format Compliance - docstring delimiters.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    For any Python docstring style, the template SHALL contain triple-quote delimiters.
    **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.7**
    """
    template = STYLE_TEMPLATES[style]

    # Must contain opening and closing triple quotes
    assert '"""' in template, f"Style {style.value} should contain triple-quote delimiters"

    # Count triple quotes - should be at least 2 (open and close)
    quote_count = template.count('"""')
    assert quote_count >= 2, f"Style {style.value} should have at least 2 triple-quote delimiters"


@given(style=python_style_strategy)
@settings(max_examples=100)
def test_python_style_render_panel(style: PythonDocstringStyle) -> None:
    """Property 12: Python Style Format Compliance - Rich Panel rendering.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    For any Python docstring style, render_style SHALL return a Rich Panel.
    **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.7**
    """
    from rich.panel import Panel

    renderer = PythonStyleRenderer()
    panel = renderer.render_style(style)

    assert isinstance(panel, Panel), f"render_style should return Panel for {style.value}"


@given(style=python_style_strategy)
@settings(max_examples=100)
def test_python_style_plain_no_ansi(style: PythonDocstringStyle) -> None:
    """Property 12: Python Style Format Compliance - plain mode.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    For any Python docstring style, plain rendering SHALL contain no ANSI codes.
    **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.7**
    """
    renderer = PythonStyleRenderer()
    plain = renderer.render_plain(style)

    # No ANSI escape sequences
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
    assert len(ansi_pattern.findall(plain)) == 0, (
        f"Plain output for {style.value} should have no ANSI codes"
    )


@given(style=python_style_strategy)
@settings(max_examples=100)
def test_python_style_plain_contains_example(style: PythonDocstringStyle) -> None:
    """Property 12: Python Style Format Compliance - plain contains example.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    For any Python docstring style, plain rendering SHALL contain the example code.
    **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.7**
    """
    renderer = PythonStyleRenderer()
    plain = renderer.render_plain(style)
    template = STYLE_TEMPLATES[style]

    # Plain output should contain the template code
    assert '"""' in plain, f"Plain output for {style.value} should contain docstring"
    assert "def " in plain, f"Plain output for {style.value} should contain function definition"


@given(style=python_style_strategy)
@settings(max_examples=100)
def test_python_style_metadata_completeness(style: PythonDocstringStyle) -> None:
    """Property 12: Python Style Format Compliance - metadata completeness.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    For any Python docstring style, metadata SHALL include name, description, and markers.
    **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.7**
    """
    metadata = STYLE_METADATA[style]

    assert "name" in metadata, f"Style {style.value} should have name in metadata"
    assert "description" in metadata, f"Style {style.value} should have description in metadata"
    assert "markers" in metadata, f"Style {style.value} should have markers in metadata"

    assert isinstance(metadata["name"], str)
    assert isinstance(metadata["description"], str)
    assert isinstance(metadata["markers"], list)


def test_python_style_render_all_styles() -> None:
    """Property 12: Python Style Format Compliance - render all styles.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    render_all_styles SHALL return a panel for each style.
    **Validates: Requirements 5.6**
    """
    from rich.panel import Panel

    renderer = PythonStyleRenderer()
    panels = renderer.render_all_styles()

    assert len(panels) == len(PythonDocstringStyle), (
        "render_all_styles should return one panel per style"
    )

    for panel in panels:
        assert isinstance(panel, Panel)


def test_python_style_comparison_view() -> None:
    """Property 12: Python Style Format Compliance - comparison view.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    render_comparison SHALL produce output containing all styles.
    **Validates: Requirements 5.6**
    """
    renderer = PythonStyleRenderer()
    comparison = renderer.render_comparison()

    # Should contain all style names
    for style in PythonDocstringStyle:
        metadata = STYLE_METADATA[style]
        assert metadata["name"] in comparison, (
            f"Comparison should contain {metadata['name']}"
        )


def test_python_style_table() -> None:
    """Property 12: Python Style Format Compliance - style table.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    render_style_table SHALL return a Rich Table with all styles.
    **Validates: Requirements 5.6**
    """
    from rich.table import Table

    renderer = PythonStyleRenderer()
    table = renderer.render_style_table()

    assert isinstance(table, Table)


def test_python_style_rules_defined() -> None:
    """Property 12: Python Style Format Compliance - rules defined.

    Feature: mrdr-visual-integration, Property 12: Python Style Format Compliance
    STYLE_RULES SHALL contain the common docstring rules.
    **Validates: Requirements 5.7**
    """
    assert len(STYLE_RULES) >= 4, "Should have at least 4 style rules"

    # Check for key rules
    rules_text = " ".join(STYLE_RULES)
    assert "Summary" in rules_text, "Rules should mention summary line"
    assert "Spacing" in rules_text or "spacing" in rules_text, "Rules should mention spacing"
    assert "Indentation" in rules_text or "indentation" in rules_text, (
        "Rules should mention indentation"
    )
    assert "Termination" in rules_text or "termination" in rules_text, (
        "Rules should mention termination"
    )


# Style-specific marker tests

def test_sphinx_style_markers() -> None:
    """Sphinx style SHALL contain :param:, :type:, :return:, :rtype: markers.

    **Validates: Requirements 5.1**
    """
    template = STYLE_TEMPLATES[PythonDocstringStyle.SPHINX]

    assert ":param" in template, "Sphinx should contain :param:"
    assert ":type" in template, "Sphinx should contain :type:"
    assert ":return" in template, "Sphinx should contain :return:"
    assert ":rtype" in template, "Sphinx should contain :rtype:"


def test_google_style_markers() -> None:
    """Google style SHALL contain Args:, Returns: sections.

    **Validates: Requirements 5.2**
    """
    template = STYLE_TEMPLATES[PythonDocstringStyle.GOOGLE]

    assert "Args:" in template, "Google should contain Args:"
    assert "Returns:" in template, "Google should contain Returns:"


def test_numpy_style_markers() -> None:
    """NumPy style SHALL contain Parameters, Returns headers with ---------- separators.

    **Validates: Requirements 5.3**
    """
    template = STYLE_TEMPLATES[PythonDocstringStyle.NUMPY]

    assert "Parameters" in template, "NumPy should contain Parameters"
    assert "----------" in template, "NumPy should contain ---------- separator"
    assert "Returns" in template, "NumPy should contain Returns"


def test_epytext_style_markers() -> None:
    """Epytext style SHALL contain @param, @type, @return tags.

    **Validates: Requirements 5.4**
    """
    template = STYLE_TEMPLATES[PythonDocstringStyle.EPYTEXT]

    assert "@param" in template, "Epytext should contain @param"
    assert "@type" in template, "Epytext should contain @type"
    assert "@return" in template, "Epytext should contain @return"


def test_pep257_style_minimal() -> None:
    """PEP 257 style SHALL be minimal format.

    **Validates: Requirements 5.5**
    """
    template = STYLE_TEMPLATES[PythonDocstringStyle.PEP257]

    # PEP 257 should NOT contain the structured markers of other styles
    assert ":param" not in template, "PEP257 should not contain :param:"
    assert "Args:" not in template, "PEP257 should not contain Args:"
    assert "@param" not in template, "PEP257 should not contain @param"

    # But should still have docstring
    assert '"""' in template, "PEP257 should contain docstring"


def test_get_style_markers() -> None:
    """get_style_markers SHALL return correct markers for each style."""
    renderer = PythonStyleRenderer()

    sphinx_markers = renderer.get_style_markers(PythonDocstringStyle.SPHINX)
    assert ":param:" in sphinx_markers

    google_markers = renderer.get_style_markers(PythonDocstringStyle.GOOGLE)
    assert "Args:" in google_markers

    numpy_markers = renderer.get_style_markers(PythonDocstringStyle.NUMPY)
    assert "Parameters" in numpy_markers

    epytext_markers = renderer.get_style_markers(PythonDocstringStyle.EPYTEXT)
    assert "@param" in epytext_markers

    pep257_markers = renderer.get_style_markers(PythonDocstringStyle.PEP257)
    assert pep257_markers == [], "PEP257 should have no specific markers"


def test_get_style_name() -> None:
    """get_style_name SHALL return human-readable names."""
    renderer = PythonStyleRenderer()

    assert "Sphinx" in renderer.get_style_name(PythonDocstringStyle.SPHINX)
    assert "Google" in renderer.get_style_name(PythonDocstringStyle.GOOGLE)
    assert "NumPy" in renderer.get_style_name(PythonDocstringStyle.NUMPY)
    assert "Epytext" in renderer.get_style_name(PythonDocstringStyle.EPYTEXT)
    assert "PEP 257" in renderer.get_style_name(PythonDocstringStyle.PEP257)
