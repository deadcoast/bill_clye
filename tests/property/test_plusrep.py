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
    """PLUSREP labels SHALL match rating values.
    
    Labels per schema:
    - MAXIMUM: +4 (6 plus)
    - GREAT: +1 to +3 (3-5 plus)
    - SLOPPY: -1 to 0 (1-2 plus)
    - REJECTED: -2 (0 plus)
    """
    assert get_rating_label(4) == "MAXIMUM"
    assert get_rating_label(3) == "GREAT"
    assert get_rating_label(2) == "GREAT"
    assert get_rating_label(1) == "GREAT"
    assert get_rating_label(0) == "SLOPPY"
    assert get_rating_label(-1) == "SLOPPY"
    assert get_rating_label(-2) == "REJECTED"


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


# =============================================================================
# Property 14: PLUSREP Consistency (Database Validation)
# Feature: mrdr-data-population, Property 14: PLUSREP Consistency
# Validates: Requirements 7.1, 7.2, 7.3, 7.4
# =============================================================================

import json
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.database.schema import (
    PlusrepGrade,
    PlusrepLabel,
    calculate_plusrep_rating,
    get_label_for_rating,
)


# Strategy for valid PLUSREP tokens
plusrep_tokens = st.text(alphabet=["+", "."], min_size=6, max_size=6)


@given(tokens=plusrep_tokens)
@settings(max_examples=100)
def test_property_14_plusrep_rating_formula(tokens: str) -> None:
    """Property 14: PLUSREP Consistency - Rating Formula.

    Feature: mrdr-data-population, Property 14: PLUSREP Consistency
    For any plusrep tokens, the rating SHALL equal (count of '+') - 2.
    **Validates: Requirements 7.2, 7.3**
    """
    expected_rating = tokens.count("+") - 2
    calculated_rating = calculate_plusrep_rating(tokens)

    assert calculated_rating == expected_rating
    assert -2 <= calculated_rating <= 4


@given(tokens=plusrep_tokens)
@settings(max_examples=100)
def test_property_14_plusrep_label_mapping(tokens: str) -> None:
    """Property 14: PLUSREP Consistency - Label Mapping.

    Feature: mrdr-data-population, Property 14: PLUSREP Consistency
    For any plusrep tokens, the label SHALL match the rating:
    MAXIMUM for +4, GREAT for +1 to +3, SLOPPY for -1 to 0, REJECTED for -2.
    **Validates: Requirements 7.4**
    """
    rating = calculate_plusrep_rating(tokens)
    label = get_label_for_rating(rating)

    # Verify label matches expected for rating
    if rating >= 4:
        assert label == PlusrepLabel.MAXIMUM
    elif rating >= 1:
        assert label == PlusrepLabel.GREAT
    elif rating >= -1:
        assert label == PlusrepLabel.SLOPPY
    else:
        assert label == PlusrepLabel.REJECTED


@given(tokens=plusrep_tokens)
@settings(max_examples=100)
def test_property_14_plusrep_grade_validation(tokens: str) -> None:
    """Property 14: PLUSREP Consistency - Grade Validation.

    Feature: mrdr-data-population, Property 14: PLUSREP Consistency
    For any valid tokens, creating a PlusrepGrade with correct rating and label
    SHALL succeed, while incorrect values SHALL raise ValueError.
    **Validates: Requirements 7.1, 7.2, 7.3, 7.4**
    """
    rating = calculate_plusrep_rating(tokens)
    label = get_label_for_rating(rating)

    # Valid grade should be created successfully
    grade = PlusrepGrade(tokens=tokens, rating=rating, label=label.value)
    assert grade.tokens == tokens
    assert grade.rating == rating
    assert grade.label == label.value


def test_property_14_database_plusrep_consistency() -> None:
    """Property 14: PLUSREP Consistency - Database Entries.

    Feature: mrdr-data-population, Property 14: PLUSREP Consistency
    For any plusrep grade in the database, the tokens SHALL be exactly 6 characters
    of `+` and `.`, the rating SHALL equal (count of '+') - 2, and the label SHALL
    match the rating.
    **Validates: Requirements 7.1, 7.2, 7.3, 7.4**
    """
    database_path = Path("database/docstrings/docstring_database.json")
    assert database_path.exists(), f"Database file not found: {database_path}"

    with open(database_path) as f:
        data = json.load(f)

    entries = data.get("entries", [])
    plusrep_entries = [e for e in entries if e.get("plusrep") is not None]

    # Ensure we have some entries with plusrep
    assert len(plusrep_entries) > 0, "No entries with plusrep found in database"

    for entry in plusrep_entries:
        plusrep = entry["plusrep"]
        language = entry.get("language", "unknown")

        # Validate tokens format (6 chars of + and .)
        tokens = plusrep["tokens"]
        assert len(tokens) == 6, f"{language}: tokens must be exactly 6 characters"
        assert all(
            c in ["+", "."] for c in tokens
        ), f"{language}: tokens must only contain '+' and '.'"

        # Validate rating formula
        expected_rating = tokens.count("+") - 2
        actual_rating = plusrep["rating"]
        assert (
            actual_rating == expected_rating
        ), f"{language}: rating {actual_rating} != expected {expected_rating}"

        # Validate label matches rating
        expected_label = get_label_for_rating(actual_rating)
        actual_label = plusrep["label"]
        assert (
            actual_label == expected_label.value
        ), f"{language}: label '{actual_label}' != expected '{expected_label.value}'"


def test_property_14_plusrep_invalid_rating_rejected() -> None:
    """Property 14: PLUSREP Consistency - Invalid Rating Rejected.

    Feature: mrdr-data-population, Property 14: PLUSREP Consistency
    Creating a PlusrepGrade with mismatched rating SHALL raise ValueError.
    **Validates: Requirements 7.2, 7.3**
    """
    import pytest

    tokens = "+++++."  # 5 plus = rating 3
    wrong_rating = 4  # Should be 3

    with pytest.raises(ValueError, match="does not match expected"):
        PlusrepGrade(tokens=tokens, rating=wrong_rating, label="MAXIMUM")


def test_property_14_plusrep_invalid_label_rejected() -> None:
    """Property 14: PLUSREP Consistency - Invalid Label Rejected.

    Feature: mrdr-data-population, Property 14: PLUSREP Consistency
    Creating a PlusrepGrade with mismatched label SHALL raise ValueError.
    **Validates: Requirements 7.4**
    """
    import pytest

    tokens = "+++++."  # 5 plus = rating 3 = GREAT
    rating = 3
    wrong_label = "MAXIMUM"  # Should be GREAT

    with pytest.raises(ValueError, match="does not match expected"):
        PlusrepGrade(tokens=tokens, rating=rating, label=wrong_label)
