"""Property tests for compare functionality.

Feature: mrdr-cli-foundation, Property 10: Compare Shows Both Languages
Validates: Requirements 3.4
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.controllers.hyde import HydeController
from mrdr.controllers.jekyl import JekylController
from mrdr.render.rich_renderer import RichRenderer


def get_valid_languages() -> list[str]:
    """Get list of valid languages from the database."""
    hyde = HydeController()
    return hyde.list_languages()


# Strategy for valid language pairs (different languages)
@st.composite
def valid_language_pair(draw: st.DrawFn) -> tuple[str, str]:
    """Generate a pair of different valid languages."""
    languages = get_valid_languages()
    if len(languages) < 2:
        # Fallback if database has fewer than 2 languages
        return ("Python", "JavaScript")
    
    lang1 = draw(st.sampled_from(languages))
    # Filter out lang1 to ensure different languages
    remaining = [l for l in languages if l != lang1]
    lang2 = draw(st.sampled_from(remaining))
    return (lang1, lang2)


@given(lang_pair=valid_language_pair())
@settings(max_examples=100)
def test_compare_shows_both_languages(lang_pair: tuple[str, str]) -> None:
    """Property 10: Compare Shows Both Languages.

    Feature: mrdr-cli-foundation, Property 10: Compare Shows Both Languages
    For any two valid languages, `mrdr jekyl compare <lang1> <lang2>` SHALL
    produce output containing information from both languages.
    **Validates: Requirements 3.4**
    """
    lang1, lang2 = lang_pair
    
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    output = jekyl.compare(lang1, lang2)
    
    # Output should contain both language names
    assert lang1 in output, f"Output should contain {lang1}"
    assert lang2 in output, f"Output should contain {lang2}"


@given(lang_pair=valid_language_pair())
@settings(max_examples=100)
def test_compare_contains_syntax_info(lang_pair: tuple[str, str]) -> None:
    """Property 10: Compare Shows Both Languages - syntax info.

    Feature: mrdr-cli-foundation, Property 10: Compare Shows Both Languages
    For any two valid languages, the comparison output SHALL contain
    syntax information (start delimiter, type, location) for both.
    **Validates: Requirements 3.4**
    """
    lang1, lang2 = lang_pair
    
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    # Get entries to verify syntax info
    entry1 = hyde.query(lang1)
    entry2 = hyde.query(lang2)
    
    output = jekyl.compare(lang1, lang2)
    
    # Output should contain syntax start delimiters (as repr strings)
    assert repr(entry1.syntax.start) in output or entry1.syntax.start in output
    assert repr(entry2.syntax.start) in output or entry2.syntax.start in output


def test_compare_same_language_shows_identical_values() -> None:
    """Compare with same language should show identical values in both columns."""
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    # This tests edge case - comparing a language with itself
    output = jekyl.compare("Python", "Python")
    
    # Should still work and contain Python twice
    assert output.count("Python") >= 2


def test_compare_output_is_table_format() -> None:
    """Compare output SHALL be in table format with columns for each language."""
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    output = jekyl.compare("Python", "JavaScript")
    
    # Should contain comparison-related text
    assert "Comparison" in output or "compare" in output.lower()
    # Should contain field labels
    assert "Start" in output
    assert "Type" in output
    assert "Location" in output
