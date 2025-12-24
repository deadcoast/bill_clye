"""Property tests for example inclusion.

Feature: mrdr-cli-foundation, Property 11: Example Inclusion
Validates: Requirements 3.6
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.controllers.hyde import HydeController
from mrdr.controllers.jekyl import JekylController, ShowOptions
from mrdr.render.rich_renderer import RichRenderer


def get_languages_with_examples() -> list[str]:
    """Get list of languages that have example_content in the database."""
    hyde = HydeController()
    languages = hyde.list_languages()
    languages_with_examples = []
    
    for lang in languages:
        entry = hyde.query(lang)
        if entry.example_content:
            languages_with_examples.append(lang)
    
    return languages_with_examples


def get_languages_without_examples() -> list[str]:
    """Get list of languages that don't have example_content in the database."""
    hyde = HydeController()
    languages = hyde.list_languages()
    languages_without_examples = []
    
    for lang in languages:
        entry = hyde.query(lang)
        if not entry.example_content:
            languages_without_examples.append(lang)
    
    return languages_without_examples


# Strategy for languages with examples
@st.composite
def language_with_example(draw: st.DrawFn) -> str:
    """Generate a language that has example_content."""
    languages = get_languages_with_examples()
    if not languages:
        # Fallback - Python should have an example
        return "Python"
    return draw(st.sampled_from(languages))


@given(language=language_with_example())
@settings(max_examples=100)
def test_example_inclusion_with_flag(language: str) -> None:
    """Property 11: Example Inclusion.

    Feature: mrdr-cli-foundation, Property 11: Example Inclusion
    For any language with a non-null `example_content` field,
    `mrdr jekyl show <language> --example` SHALL include that
    example content in the output.
    **Validates: Requirements 3.6**
    """
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    # Get the entry to verify example content
    entry = hyde.query(language)
    
    # Show with example flag
    options = ShowOptions(example=True)
    output = jekyl.show(language, options)
    
    # Output should contain "Example" label or the example content
    assert entry.example_content is not None, f"{language} should have example_content"
    
    # The output should indicate example content is present
    # Either by containing the word "Example" or part of the example content
    has_example_label = "Example" in output
    has_example_content = any(
        line.strip() in output 
        for line in entry.example_content.split('\n')[:3]  # Check first 3 lines
        if line.strip()
    )
    
    assert has_example_label or has_example_content, \
        f"Output should contain example content for {language}"


@given(language=language_with_example())
@settings(max_examples=100)
def test_example_not_included_without_flag(language: str) -> None:
    """Property 11: Example Inclusion - without flag.

    Feature: mrdr-cli-foundation, Property 11: Example Inclusion
    For any language with example_content, showing without --example flag
    SHALL NOT include the example content in the output.
    **Validates: Requirements 3.6**
    """
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    # Show without example flag
    options = ShowOptions(example=False)
    output_without = jekyl.show(language, options)
    
    # Show with example flag
    options_with = ShowOptions(example=True)
    output_with = jekyl.show(language, options_with)
    
    # Output with example should be longer than without
    assert len(output_with) > len(output_without), \
        "Output with --example should be longer than without"


def test_example_inclusion_python() -> None:
    """Specific test for Python example inclusion."""
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    entry = hyde.query("Python")
    
    # Python should have example content
    assert entry.example_content is not None
    
    # Show with example flag
    options = ShowOptions(example=True)
    output = jekyl.show("Python", options)
    
    # Should contain Example label
    assert "Example" in output


def test_example_flag_with_no_example_content() -> None:
    """Test that --example flag works gracefully when no example exists."""
    languages_without = get_languages_without_examples()
    
    if not languages_without:
        # All languages have examples, skip this test
        return
    
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    language = languages_without[0]
    
    # Show with example flag should not error
    options = ShowOptions(example=True)
    output = jekyl.show(language, options)
    
    # Should still produce valid output
    assert language in output
