"""Property tests for PLUSREP calculation.

Feature: mrdr-cli-foundation, Property 14: PLUSREP Calculation
Validates: Requirements 5.1, 5.3
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.components.plusrep import (
    PlusrepDisplay,
    calculate_rating,
    get_rating_label,
)
from tests.conftest import plusrep_tokens_strategy


@given(tokens=plusrep_tokens_strategy)
@settings(max_examples=100)
def test_plusrep_rating_calculation(tokens: str) -> None:
    """Property 14: PLUSREP Calculation.

    Feature: mrdr-cli-foundation, Property 14: PLUSREP Calculation
    For any PLUSREP token string of exactly 6 characters (each being `+` or `.`),
    the calculated rating SHALL equal `(count of '+') - 2`, ranging from -2 to +4.
    **Validates: Requirements 5.1, 5.3**
    """
    rating = calculate_rating(tokens)

    # Rating should equal (count of '+') - 2
    expected_rating = tokens.count("+") - 2
    assert rating == expected_rating

    # Rating should be in valid range
    assert -2 <= rating <= 4


@given(tokens=plusrep_tokens_strategy)
@settings(max_examples=100)
def test_plusrep_display_from_tokens(tokens: str) -> None:
    """Property 14: PLUSREP Calculation - display creation.

    Feature: mrdr-cli-foundation, Property 14: PLUSREP Calculation
    For any valid token string, PlusrepDisplay.from_tokens SHALL create
    a display with correctly calculated rating.
    **Validates: Requirements 5.1, 5.3**
    """
    display = PlusrepDisplay.from_tokens(tokens)

    assert display.grade is not None
    assert display.grade.tokens == tokens
    assert display.grade.rating == tokens.count("+") - 2


@given(tokens=plusrep_tokens_strategy)
@settings(max_examples=100)
def test_plusrep_render_contains_tokens(tokens: str) -> None:
    """Property 14: PLUSREP Calculation - render contains tokens.

    Feature: mrdr-cli-foundation, Property 14: PLUSREP Calculation
    For any valid token string, the rendered output SHALL contain
    all tokens from the input.
    **Validates: Requirements 5.1, 5.3**
    """
    display = PlusrepDisplay.from_tokens(tokens)
    rendered = display.render()

    # Plain text should contain all tokens
    plain = rendered.plain
    for char in tokens:
        assert char in plain


def test_plusrep_rating_boundaries() -> None:
    """PLUSREP rating SHALL have correct boundary values."""
    # All dots: rating = 0 - 2 = -2
    assert calculate_rating("......") == -2

    # All plus: rating = 6 - 2 = 4
    assert calculate_rating("++++++") == 4

    # Half and half: rating = 3 - 2 = 1
    assert calculate_rating("+++...") == 1


def test_plusrep_labels() -> None:
    """PLUSREP labels SHALL match rating values."""
    assert get_rating_label(4) == "MAXIMUM"
    assert get_rating_label(3) == "GREAT"
    assert get_rating_label(2) == "GOOD"
    assert get_rating_label(1) == "FAIR"
    assert get_rating_label(0) == "SLOPPY"
    assert get_rating_label(-1) == "POOR"
    assert get_rating_label(-2) == "RESET"


def test_plusrep_display_plain_no_ansi() -> None:
    """PLUSREP plain render SHALL contain no ANSI codes."""
    import re

    display = PlusrepDisplay.from_tokens("+++...")
    plain = display.render_plain()

    # No ANSI escape sequences
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
    assert len(ansi_pattern.findall(plain)) == 0


def test_plusrep_display_none_grade() -> None:
    """PLUSREP display with None grade SHALL render 'No grade'."""
    display = PlusrepDisplay(grade=None)

    rendered = display.render()
    assert "No grade" in rendered.plain

    plain = display.render_plain()
    assert "No grade" in plain


def test_plusrep_invalid_tokens_length() -> None:
    """PLUSREP calculation SHALL reject invalid token length."""
    import pytest

    with pytest.raises(ValueError, match="exactly 6 characters"):
        calculate_rating("+++++")  # 5 chars

    with pytest.raises(ValueError, match="exactly 6 characters"):
        calculate_rating("+++++++")  # 7 chars


def test_plusrep_invalid_tokens_chars() -> None:
    """PLUSREP calculation SHALL reject invalid characters."""
    import pytest

    with pytest.raises(ValueError, match="only contain"):
        calculate_rating("+++x..")  # invalid 'x'

    with pytest.raises(ValueError, match="only contain"):
        calculate_rating("+++  .")  # invalid spaces
