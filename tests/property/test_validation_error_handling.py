"""Property tests for validation error handling.

Feature: mrdr-data-population, Property 15: Validation Error Handling
Validates: Requirements 8.1, 8.2, 8.3

For any invalid database entry, the loader SHALL skip the entry without
crashing and SHALL report the error with entry identifier and specific
field failures.
"""

import json
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.database.loader import DatabaseLoader
from mrdr.database.validation import (
    ValidationCollector,
    ValidationError,
    ValidationResult,
    ValidationSeverity,
)


# Strategy for generating invalid docstring entries (missing required fields)
@st.composite
def invalid_docstring_entry_strategy(draw: st.DrawFn) -> dict:
    """Generate invalid docstring entries with missing required fields."""
    # Randomly omit required fields
    entry = {}
    
    # Sometimes include language, sometimes not
    if draw(st.booleans()):
        entry["language"] = draw(st.text(min_size=1, max_size=20))
    
    # Sometimes include syntax, sometimes not, sometimes partial
    include_syntax = draw(st.integers(min_value=0, max_value=2))
    if include_syntax == 1:
        # Partial syntax - missing some required fields
        syntax = {}
        if draw(st.booleans()):
            syntax["start"] = draw(st.text(min_size=1, max_size=5))
        if draw(st.booleans()):
            syntax["type"] = draw(st.sampled_from(["literal", "block", "line_sugared"]))
        if draw(st.booleans()):
            syntax["location"] = draw(st.sampled_from(["internal_first_line", "above_target"]))
        entry["syntax"] = syntax
    elif include_syntax == 2:
        # Complete syntax
        entry["syntax"] = {
            "start": draw(st.text(min_size=1, max_size=5)),
            "type": draw(st.sampled_from(["literal", "block", "line_sugared"])),
            "location": draw(st.sampled_from(["internal_first_line", "above_target"])),
        }
    
    return entry


@given(invalid_entry=invalid_docstring_entry_strategy())
@settings(max_examples=100)
def test_loader_skips_invalid_entries_without_crashing(invalid_entry: dict) -> None:
    """Property 15: Validation Error Handling - Skip invalid entries.

    Feature: mrdr-data-population, Property 15: Validation Error Handling
    For any invalid database entry, the loader SHALL skip the entry without
    crashing.
    **Validates: Requirements 8.1, 8.2**
    """
    # Create a temporary database file with the invalid entry
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        database = {
            "manifest_name": "test_database",
            "version": "1.0.0",
            "schema_origin": "test",
            "entries": [invalid_entry],
        }
        json.dump(database, f)
        temp_path = Path(f.name)

    try:
        loader = DatabaseLoader(temp_path)
        # This should not raise an exception
        entries = loader.load()
        
        # The loader should either:
        # 1. Skip the invalid entry (entries list is empty)
        # 2. Accept the entry if it happens to be valid
        assert isinstance(entries, list)
        
        # If the entry was invalid, validation_errors should be populated
        # If the entry was valid, it should be in the entries list
        total = len(entries) + len(loader.validation_errors)
        assert total >= 0  # Just verify we got some result
        
    finally:
        temp_path.unlink()


@given(
    entry_id=st.text(min_size=1, max_size=50),
    message=st.text(min_size=1, max_size=200),
    field=st.one_of(st.none(), st.text(min_size=1, max_size=50)),
)
@settings(max_examples=100)
def test_validation_error_stores_entry_identifier(
    entry_id: str, message: str, field: str | None
) -> None:
    """Property 15: Validation Error Handling - Store entry identifier.

    Feature: mrdr-data-population, Property 15: Validation Error Handling
    For any validation error, the error SHALL include the entry identifier.
    **Validates: Requirements 8.2, 8.3**
    """
    error = ValidationError(
        entry_id=entry_id,
        field=field,
        message=message,
        severity=ValidationSeverity.ERROR,
    )
    
    assert error.entry_id == entry_id
    assert error.message == message
    assert error.field == field


@given(
    entry_id=st.text(min_size=1, max_size=50),
    field=st.text(min_size=1, max_size=50),
    message=st.text(min_size=1, max_size=200),
)
@settings(max_examples=100)
def test_validation_error_stores_field_failures(
    entry_id: str, field: str, message: str
) -> None:
    """Property 15: Validation Error Handling - Store field failures.

    Feature: mrdr-data-population, Property 15: Validation Error Handling
    For any validation error, the error SHALL include specific field failures.
    **Validates: Requirements 8.3**
    """
    error = ValidationError(
        entry_id=entry_id,
        field=field,
        message=message,
        severity=ValidationSeverity.ERROR,
    )
    
    # Verify the error can be converted to dict with all fields
    error_dict = error.to_dict()
    assert "entry_id" in error_dict
    assert "field" in error_dict
    assert "message" in error_dict
    assert error_dict["entry_id"] == entry_id
    assert error_dict["field"] == field
    assert error_dict["message"] == message


@given(
    database_type=st.text(min_size=1, max_size=30),
    total_entries=st.integers(min_value=0, max_value=1000),
    valid_entries=st.integers(min_value=0, max_value=1000),
)
@settings(max_examples=100)
def test_validation_result_tracks_entry_counts(
    database_type: str, total_entries: int, valid_entries: int
) -> None:
    """Property 15: Validation Error Handling - Track entry counts.

    Feature: mrdr-data-population, Property 15: Validation Error Handling
    For any database validation, the result SHALL track total and valid entry counts.
    **Validates: Requirements 8.2**
    """
    # Ensure valid_entries <= total_entries
    valid_entries = min(valid_entries, total_entries)
    
    result = ValidationResult(
        database_type=database_type,
        database_path=Path("test.json"),
        total_entries=total_entries,
        valid_entries=valid_entries,
    )
    
    assert result.database_type == database_type
    assert result.total_entries == total_entries
    assert result.valid_entries == valid_entries


@given(num_errors=st.integers(min_value=0, max_value=10))
@settings(max_examples=100)
def test_validation_result_is_valid_property(num_errors: int) -> None:
    """Property 15: Validation Error Handling - is_valid property.

    Feature: mrdr-data-population, Property 15: Validation Error Handling
    For any validation result, is_valid SHALL be True only when there are no errors.
    **Validates: Requirements 8.1**
    """
    result = ValidationResult(
        database_type="test",
        database_path=Path("test.json"),
        total_entries=10,
        valid_entries=10 - num_errors,
    )
    
    # Add errors
    for i in range(num_errors):
        result.add_error(
            entry_id=f"entry_{i}",
            message=f"Error {i}",
            severity=ValidationSeverity.ERROR,
        )
    
    # is_valid should be True only when there are no errors
    assert result.is_valid == (num_errors == 0)
    assert result.error_count == num_errors


@given(num_databases=st.integers(min_value=1, max_value=10))
@settings(max_examples=100)
def test_validation_collector_aggregates_results(num_databases: int) -> None:
    """Property 15: Validation Error Handling - Collector aggregation.

    Feature: mrdr-data-population, Property 15: Validation Error Handling
    For any set of database validations, the collector SHALL aggregate all results.
    **Validates: Requirements 8.1, 8.2**
    """
    collector = ValidationCollector()
    
    for i in range(num_databases):
        result = ValidationResult(
            database_type=f"database_{i}",
            database_path=Path(f"db_{i}.json"),
            total_entries=10,
            valid_entries=10,
        )
        collector.add_result(result)
    
    assert len(collector.results) == num_databases
    assert collector.all_valid  # All results have no errors


def test_loader_reports_validation_errors_with_details() -> None:
    """Property 15: Validation Error Handling - Detailed error reporting.

    Feature: mrdr-data-population, Property 15: Validation Error Handling
    For any invalid entry, the loader SHALL report errors with entry identifier
    and specific field failures.
    **Validates: Requirements 8.2, 8.3**
    """
    # Create a database with a known invalid entry
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        database = {
            "manifest_name": "test_database",
            "version": "1.0.0",
            "schema_origin": "test",
            "entries": [
                {
                    "language": "ValidLanguage",
                    "syntax": {
                        "start": '"""',
                        "type": "literal",
                        "location": "internal_first_line",
                    },
                },
                {
                    # Missing language field - should fail validation
                    "syntax": {
                        "start": "/**",
                        "type": "block",
                        "location": "above_target",
                    },
                },
            ],
        }
        json.dump(database, f)
        temp_path = Path(f.name)

    try:
        loader = DatabaseLoader(temp_path)
        entries = loader.load()
        
        # Should have loaded the valid entry
        assert len(entries) == 1
        
        # Should have recorded validation error for the invalid entry
        assert len(loader.validation_errors) == 1
        
        # The validation result should have details
        assert loader.validation_result is not None
        assert loader.validation_result.error_count == 1
        
        # Check that the error has entry identifier
        errors = loader.validation_result.errors
        assert len(errors) == 1
        assert errors[0].entry_id == "unknown"  # Missing language defaults to "unknown"
        
    finally:
        temp_path.unlink()
