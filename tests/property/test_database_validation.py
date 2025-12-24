"""Property tests for database schema validation.

Feature: mrdr-cli-foundation, Property 12: Database Validation
Validates: Requirements 4.1, 4.3, 4.4
"""

from hypothesis import given, settings
from pydantic import ValidationError

from mrdr.database.schema import DocstringEntry, SyntaxSpec
from tests.conftest import docstring_entry_strategy, syntax_spec_strategy


@given(data=syntax_spec_strategy())
@settings(max_examples=100)
def test_syntax_spec_validates_required_fields(data: dict) -> None:
    """Property 12: Database Validation - SyntaxSpec required fields.

    Feature: mrdr-cli-foundation, Property 12: Database Validation
    For any entry in the database, loading SHALL validate that required fields
    (syntax.start, syntax.type, syntax.location) are present.
    **Validates: Requirements 4.1, 4.3, 4.4**
    """
    spec = SyntaxSpec(**data)
    assert spec.start is not None
    assert spec.type is not None
    assert spec.location is not None


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_docstring_entry_validates_required_fields(data: dict) -> None:
    """Property 12: Database Validation - DocstringEntry required fields.

    Feature: mrdr-cli-foundation, Property 12: Database Validation
    For any entry in the database, loading SHALL validate that required fields
    (language, syntax.start, syntax.type, syntax.location) are present.
    **Validates: Requirements 4.1, 4.3, 4.4**
    """
    entry = DocstringEntry(**data)
    assert entry.language is not None
    assert entry.syntax.start is not None
    assert entry.syntax.type is not None
    assert entry.syntax.location is not None


def test_missing_language_fails_validation() -> None:
    """Invalid entries SHALL be skipped - missing language field."""
    try:
        DocstringEntry(
            syntax={
                "start": "/**",
                "end": "*/",
                "type": "block",
                "location": "above_target",
            }
        )
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass  # Expected


def test_missing_syntax_start_fails_validation() -> None:
    """Invalid entries SHALL be skipped - missing syntax.start field."""
    try:
        DocstringEntry(
            language="Test",
            syntax={
                "end": "*/",
                "type": "block",
                "location": "above_target",
            },
        )
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass  # Expected


def test_missing_syntax_type_fails_validation() -> None:
    """Invalid entries SHALL be skipped - missing syntax.type field."""
    try:
        DocstringEntry(
            language="Test",
            syntax={
                "start": "/**",
                "end": "*/",
                "location": "above_target",
            },
        )
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass  # Expected


def test_missing_syntax_location_fails_validation() -> None:
    """Invalid entries SHALL be skipped - missing syntax.location field."""
    try:
        DocstringEntry(
            language="Test",
            syntax={
                "start": "/**",
                "end": "*/",
                "type": "block",
            },
        )
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass  # Expected
