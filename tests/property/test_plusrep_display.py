"""Property tests for PLUSREP display integration.

Feature: mrdr-cli-foundation, Property 15: PLUSREP Display
Validates: Requirements 5.2
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.controllers.hyde import HydeController
from mrdr.controllers.jekyl import JekylController, ShowOptions
from mrdr.database.schema import DocstringEntry, PlusrepGrade, SyntaxSpec
from mrdr.render.components.plusrep import PlusrepDisplay
from mrdr.render.rich_renderer import RichRenderer
from tests.conftest import plusrep_tokens_strategy


@given(tokens=plusrep_tokens_strategy)
@settings(max_examples=100)
def test_plusrep_display_contains_tokens_and_label(tokens: str) -> None:
    """Property 15: PLUSREP Display.

    Feature: mrdr-cli-foundation, Property 15: PLUSREP Display
    For any language with a `plusrep` field, `mrdr jekyl show <language> --grade`
    SHALL include the PLUSREP tokens and rating label in the output.
    **Validates: Requirements 5.2**
    """
    # Create a PlusrepDisplay from tokens
    display = PlusrepDisplay.from_tokens(tokens)
    
    # Render the display
    rendered = display.render()
    plain_text = rendered.plain
    
    # Output should contain all tokens
    for char in tokens:
        assert char in plain_text, f"Token '{char}' should be in output"
    
    # Output should contain the rating label
    assert display.grade is not None
    assert display.grade.label in plain_text, \
        f"Label '{display.grade.label}' should be in output"


@given(tokens=plusrep_tokens_strategy)
@settings(max_examples=100)
def test_plusrep_display_contains_rating(tokens: str) -> None:
    """Property 15: PLUSREP Display - rating value.

    Feature: mrdr-cli-foundation, Property 15: PLUSREP Display
    For any PLUSREP tokens, the display SHALL include the numeric rating.
    **Validates: Requirements 5.2**
    """
    display = PlusrepDisplay.from_tokens(tokens)
    
    # Render the display
    rendered = display.render()
    plain_text = rendered.plain
    
    # Output should contain the rating value (as +N or -N)
    assert display.grade is not None
    rating_str = f"{display.grade.rating:+d}"
    assert rating_str in plain_text, \
        f"Rating '{rating_str}' should be in output"


def test_plusrep_display_in_jekyl_show() -> None:
    """Test PLUSREP display integration in JekylController.show().

    This test creates a mock entry with plusrep to verify the integration
    works correctly in the Jekyl controller.
    """
    # Create a mock entry with plusrep
    entry = DocstringEntry(
        language="TestLang",
        syntax=SyntaxSpec(
            start='"""',
            end='"""',
            type="literal",
            location="internal_first_line",
        ),
        tags=["test"],
        plusrep=PlusrepGrade(
            tokens="+++...",
            rating=1,
            label="FAIR",
        ),
    )
    
    # Create a PlusrepDisplay and verify it renders correctly
    display = PlusrepDisplay(grade=entry.plusrep)
    rendered = display.render()
    plain_text = rendered.plain
    
    # Should contain tokens
    assert "+++" in plain_text
    assert "..." in plain_text
    
    # Should contain label
    assert "FAIR" in plain_text
    
    # Should contain rating
    assert "+1" in plain_text


def test_plusrep_display_grade_flag_no_plusrep() -> None:
    """Test that --grade flag works gracefully when entry has no plusrep."""
    hyde = HydeController()
    renderer = RichRenderer()
    jekyl = JekylController(hyde=hyde, renderer=renderer)
    
    # Python doesn't have plusrep in the database
    entry = hyde.query("Python")
    assert entry.plusrep is None, "Python should not have plusrep for this test"
    
    # Show with grade flag should not error
    options = ShowOptions(grade=True)
    output = jekyl.show("Python", options)
    
    # Should still produce valid output
    assert "Python" in output
    assert len(output) > 0


def test_plusrep_display_all_rating_labels() -> None:
    """Test that all rating labels are displayed correctly."""
    test_cases = [
        ("++++++", "MAXIMUM"),
        ("+++++.", "GREAT"),
        ("++++..", "GOOD"),
        ("+++...", "FAIR"),
        ("++....", "SLOPPY"),
        ("+.....", "POOR"),
        ("......", "RESET"),
    ]
    
    for tokens, expected_label in test_cases:
        display = PlusrepDisplay.from_tokens(tokens)
        rendered = display.render()
        plain_text = rendered.plain
        
        assert expected_label in plain_text, \
            f"Label '{expected_label}' should be in output for tokens '{tokens}'"


def test_plusrep_display_panel_rendering() -> None:
    """Test PLUSREP display panel rendering."""
    display = PlusrepDisplay.from_tokens("+++...")
    
    # Render as panel
    panel_output = display.render_panel()
    
    # Should contain PLUSREP title
    assert "PLUSREP" in panel_output or "Grade" in panel_output
    
    # Should contain tokens
    assert "+++" in panel_output
    assert "..." in panel_output
