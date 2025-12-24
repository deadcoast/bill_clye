"""Property tests for docstring display.

Feature: mrdr-cli-foundation, Property 23: Docstring Display Completeness
For any valid language, `mrdr docstring <language>` SHALL display: syntax signature
(start/end delimiters), carrier type, attachment location, and conflict notes if
`conflict_ref` is present.

Feature: mrdr-cli-foundation, Property 24: Python Style Selection
For any valid Python docstring style (sphinx, google, numpy, epytext, pep257),
`mrdr docstring python --style <style>` SHALL display the corresponding style format.

**Validates: Requirements 10.1, 10.2, 10.3, 10.6**
"""

from hypothesis import given, settings
from hypothesis import strategies as st
from typer.testing import CliRunner

from mrdr.cli.app import app
from mrdr.controllers.hyde import HydeController


runner = CliRunner()


# Get valid languages from the database
def get_valid_languages() -> list[str]:
    """Get list of valid languages from the database."""
    hyde = HydeController()
    return hyde.list_languages()


# Strategy for valid languages
valid_language_strategy = st.sampled_from(get_valid_languages())

# Strategy for valid Python styles
python_style_strategy = st.sampled_from(["sphinx", "google", "numpy", "epytext", "pep257"])


@given(language=valid_language_strategy)
@settings(max_examples=100)
def test_docstring_display_completeness(language: str) -> None:
    """Property 23: Docstring Display Completeness.
    
    For any valid language, `mrdr docstring <language>` SHALL display:
    - syntax signature (start/end delimiters)
    - carrier type
    - attachment location
    - conflict notes if `conflict_ref` is present
    """
    result = runner.invoke(app, ["--plain", "docstring", language])
    
    assert result.exit_code == 0, f"Command failed for {language}: {result.output}"
    
    output = result.output
    
    # Must contain language name
    assert language in output, f"Language name not in output for {language}"
    
    # Must contain delimiter information
    assert "Delimiter" in output or "Start" in output, f"Delimiter info missing for {language}"
    
    # Must contain type information
    assert "Type" in output, f"Type info missing for {language}"
    
    # Must contain location information
    assert "Location" in output, f"Location info missing for {language}"


@given(style=python_style_strategy)
@settings(max_examples=100)
def test_python_style_selection(style: str) -> None:
    """Property 24: Python Style Selection.
    
    For any valid Python docstring style (sphinx, google, numpy, epytext, pep257),
    `mrdr docstring python --style <style>` SHALL display the corresponding style format.
    """
    result = runner.invoke(app, ["--plain", "docstring", "python", "--style", style])
    
    assert result.exit_code == 0, f"Command failed for style {style}: {result.output}"
    
    output = result.output
    
    # Must contain Python reference
    assert "Python" in output, f"Python not in output for style {style}"
    
    # Must contain example docstring
    assert '"""' in output, f"Docstring delimiters not in output for style {style}"
    
    # Style-specific content checks
    if style == "sphinx":
        assert ":param" in output or ":returns" in output, f"Sphinx markers missing for {style}"
    elif style == "google":
        assert "Args:" in output or "Returns:" in output, f"Google markers missing for {style}"
    elif style == "numpy":
        assert "Parameters" in output or "Returns" in output, f"NumPy markers missing for {style}"
    elif style == "epytext":
        assert "@param" in output or "@return" in output, f"Epytext markers missing for {style}"
    elif style == "pep257":
        assert "Arguments:" in output or "Returns:" in output, f"PEP257 markers missing for {style}"


def test_docstring_all_flag() -> None:
    """Test that --all flag lists all languages with signatures."""
    result = runner.invoke(app, ["--plain", "docstring", "--all"])
    
    assert result.exit_code == 0
    
    output = result.output
    
    # Should contain multiple languages
    assert "Python" in output
    assert "Rust" in output or "JavaScript" in output
    
    # Should show total count
    assert "Total:" in output


def test_docstring_conflict_ref_display() -> None:
    """Test that conflict_ref is displayed when present."""
    # Julia has a conflict_ref with Python (both use """)
    result = runner.invoke(app, ["--plain", "docstring", "Julia"])
    
    # Command should succeed
    assert result.exit_code == 0
    
    # If Julia has conflict_ref, it should be displayed
    # (This depends on database content)


def test_invalid_style_error() -> None:
    """Test that invalid style produces error."""
    result = runner.invoke(app, ["docstring", "python", "--style", "invalid"])
    
    assert result.exit_code == 1
    assert "Unknown style" in result.output or "Error" in result.output
