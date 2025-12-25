"""Property tests for UDL (User Defined Language) system.

Feature: mrdr-visual-integration
Properties: 7, 8, 9
Validates: Requirements 3.3, 3.4, 3.6, 3.7
"""

from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError
import pytest

from mrdr.database.udl import (
    DOLPHIN_OPERATOR,
    WALRUS_OPERATOR,
    UDLDefinition,
    UDLOperator,
    UDLValidator,
)
from mrdr.database.udl.validator import UDLValidationError


# Strategy for valid two-character operator delimiters
two_char_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("P", "S")),
    min_size=2,
    max_size=2,
)

# Strategy for valid single-character delimiters
single_char_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("P", "S")),
    min_size=1,
    max_size=1,
)

# Strategy for operator names
operator_name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L",)),
    min_size=1,
    max_size=20,
)


@st.composite
def valid_operator_strategy(draw: st.DrawFn) -> dict[str, str]:
    """Generate valid UDL operator data."""
    return {
        "name": draw(operator_name_strategy),
        "open": draw(two_char_strategy),
        "close": draw(two_char_strategy),
    }


@st.composite
def valid_definition_strategy(draw: st.DrawFn) -> dict[str, str | list]:
    """Generate valid UDL definition data."""
    operators = []
    if draw(st.booleans()):
        num_operators = draw(st.integers(min_value=0, max_value=3))
        for _ in range(num_operators):
            operators.append(draw(valid_operator_strategy()))
    
    return {
        "title": draw(st.text(min_size=1, max_size=50)),
        "descr": draw(st.text(min_size=1, max_size=200)),
        "lang": draw(st.text(min_size=1, max_size=20)),
        "delimiter_open": draw(single_char_strategy),
        "delimiter_close": draw(single_char_strategy),
        "operators": operators,
    }


@given(
    open_delim=two_char_strategy,
    close_delim=two_char_strategy,
    name=operator_name_strategy,
)
@settings(max_examples=100)
def test_udl_operator_pattern_support(
    open_delim: str,
    close_delim: str,
    name: str,
) -> None:
    """Property 7: UDL Operator Pattern Support.

    Feature: mrdr-visual-integration, Property 7: UDL Operator Pattern Support
    For any UDL definition using dolphin (`<:`, `:>`) or walrus (`:=`, `=:`)
    operators, the UDL_System SHALL correctly parse and render the operator patterns.
    **Validates: Requirements 3.3, 3.4**
    """
    # Create operator with valid two-character delimiters
    operator = UDLOperator(name=name, open=open_delim, close=close_delim)
    
    # Verify operator was created correctly
    assert operator.name == name
    assert operator.open == open_delim
    assert operator.close == close_delim
    assert len(operator.open) == 2
    assert len(operator.close) == 2


def test_builtin_dolphin_operator() -> None:
    """Test that DOLPHIN_OPERATOR is correctly defined.

    **Validates: Requirements 3.3**
    """
    assert DOLPHIN_OPERATOR.name == "dolphin"
    assert DOLPHIN_OPERATOR.open == "<:"
    assert DOLPHIN_OPERATOR.close == ":>"
    assert len(DOLPHIN_OPERATOR.open) == 2
    assert len(DOLPHIN_OPERATOR.close) == 2


def test_builtin_walrus_operator() -> None:
    """Test that WALRUS_OPERATOR is correctly defined.

    **Validates: Requirements 3.4**
    """
    assert WALRUS_OPERATOR.name == "walrus"
    assert WALRUS_OPERATOR.open == ":="
    assert WALRUS_OPERATOR.close == "=:"
    assert len(WALRUS_OPERATOR.open) == 2
    assert len(WALRUS_OPERATOR.close) == 2


def test_definition_with_builtin_operators() -> None:
    """Test UDL definition with dolphin and walrus operators.

    **Validates: Requirements 3.3, 3.4**
    """
    definition = UDLDefinition(
        title="Test UDL",
        descr="A test UDL definition",
        lang="UDL",
        delimiter_open="<",
        delimiter_close=">",
        operators=[DOLPHIN_OPERATOR, WALRUS_OPERATOR],
    )
    
    assert len(definition.operators) == 2
    assert definition.operators[0].name == "dolphin"
    assert definition.operators[1].name == "walrus"


# Strategies for invalid delimiters
invalid_single_char_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("P", "S", "L")),
    min_size=0,
    max_size=10,
).filter(lambda x: len(x) != 1)

invalid_two_char_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("P", "S", "L")),
    min_size=0,
    max_size=10,
).filter(lambda x: len(x) != 2)


@given(
    delimiter_open=single_char_strategy,
    delimiter_close=single_char_strategy,
)
@settings(max_examples=100)
def test_udl_delimiter_validation_valid(
    delimiter_open: str,
    delimiter_close: str,
) -> None:
    """Property 8: UDL Delimiter Validation (valid cases).

    Feature: mrdr-visual-integration, Property 8: UDL Delimiter Validation
    For any UDL definition, DELIMITER fields SHALL be exactly 1 character
    and OPERATOR fields SHALL be exactly 2 characters; invalid values SHALL be rejected.
    **Validates: Requirements 3.6**
    """
    # Valid single-character delimiters should be accepted
    definition = UDLDefinition(
        title="Test",
        descr="Test description",
        lang="UDL",
        delimiter_open=delimiter_open,
        delimiter_close=delimiter_close,
    )
    
    assert len(definition.delimiter_open) == 1
    assert len(definition.delimiter_close) == 1


@given(invalid_delimiter=invalid_single_char_strategy)
@settings(max_examples=100)
def test_udl_delimiter_validation_invalid_open(invalid_delimiter: str) -> None:
    """Property 8: UDL Delimiter Validation (invalid open delimiter).

    Feature: mrdr-visual-integration, Property 8: UDL Delimiter Validation
    For any UDL definition, DELIMITER fields SHALL be exactly 1 character;
    invalid values SHALL be rejected.
    **Validates: Requirements 3.6**
    """
    with pytest.raises(ValidationError):
        UDLDefinition(
            title="Test",
            descr="Test description",
            lang="UDL",
            delimiter_open=invalid_delimiter,
            delimiter_close=">",
        )


@given(invalid_delimiter=invalid_single_char_strategy)
@settings(max_examples=100)
def test_udl_delimiter_validation_invalid_close(invalid_delimiter: str) -> None:
    """Property 8: UDL Delimiter Validation (invalid close delimiter).

    Feature: mrdr-visual-integration, Property 8: UDL Delimiter Validation
    For any UDL definition, DELIMITER fields SHALL be exactly 1 character;
    invalid values SHALL be rejected.
    **Validates: Requirements 3.6**
    """
    with pytest.raises(ValidationError):
        UDLDefinition(
            title="Test",
            descr="Test description",
            lang="UDL",
            delimiter_open="<",
            delimiter_close=invalid_delimiter,
        )


@given(invalid_operator=invalid_two_char_strategy)
@settings(max_examples=100)
def test_udl_operator_validation_invalid(invalid_operator: str) -> None:
    """Property 8: UDL Delimiter Validation (invalid operator).

    Feature: mrdr-visual-integration, Property 8: UDL Delimiter Validation
    For any UDL definition, OPERATOR fields SHALL be exactly 2 characters;
    invalid values SHALL be rejected.
    **Validates: Requirements 3.6**
    """
    with pytest.raises(ValidationError):
        UDLOperator(
            name="test",
            open=invalid_operator,
            close=":>",
        )


def test_validator_delimiter_validation() -> None:
    """Test UDLValidator.validate_delimiter function.

    **Validates: Requirements 3.6**
    """
    # Valid single character
    assert UDLValidator.validate_delimiter("<") == "<"
    assert UDLValidator.validate_delimiter(">") == ">"
    
    # Invalid: empty string
    with pytest.raises(UDLValidationError) as exc_info:
        UDLValidator.validate_delimiter("")
    assert "exactly 1 character" in str(exc_info.value)
    
    # Invalid: multiple characters
    with pytest.raises(UDLValidationError) as exc_info:
        UDLValidator.validate_delimiter("<<")
    assert "exactly 1 character" in str(exc_info.value)


def test_validator_operator_delimiter_validation() -> None:
    """Test UDLValidator.validate_operator_delimiter function.

    **Validates: Requirements 3.6**
    """
    # Valid two characters
    assert UDLValidator.validate_operator_delimiter("<:") == "<:"
    assert UDLValidator.validate_operator_delimiter(":>") == ":>"
    
    # Invalid: single character
    with pytest.raises(UDLValidationError) as exc_info:
        UDLValidator.validate_operator_delimiter("<")
    assert "exactly 2 characters" in str(exc_info.value)
    
    # Invalid: three characters
    with pytest.raises(UDLValidationError) as exc_info:
        UDLValidator.validate_operator_delimiter("<:>")
    assert "exactly 2 characters" in str(exc_info.value)



import tempfile
from pathlib import Path
import json

from mrdr.database.udl import UDLLoader
from mrdr.database.udl.loader import UDLNotFoundError


@st.composite
def udl_entry_data_strategy(draw: st.DrawFn) -> dict:
    """Generate valid UDL entry data for JSON files."""
    name = draw(st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=20,
    ))
    
    return {
        "name": name,
        "definition": {
            "title": draw(st.text(min_size=1, max_size=50)),
            "descr": draw(st.text(min_size=1, max_size=100)),
            "lang": "UDL",
            "delimiter_open": draw(single_char_strategy),
            "delimiter_close": draw(single_char_strategy),
            "bracket_open": "(",
            "bracket_close": ")",
            "operators": [],
        },
        "examples": [],
        "created_at": "2024-01-01T00:00:00",
    }


@given(entries=st.lists(udl_entry_data_strategy(), min_size=0, max_size=5, unique_by=lambda x: x["name"].lower()))
@settings(max_examples=100)
def test_udl_list_completeness(entries: list[dict]) -> None:
    """Property 9: UDL List Completeness.

    Feature: mrdr-visual-integration, Property 9: UDL List Completeness
    For any set of registered UDL definitions, `mrdr hyde udl list` SHALL return
    a list containing all UDL names with no duplicates or omissions.
    **Validates: Requirements 3.7**
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        udl_path = Path(tmpdir)
        
        # Write UDL entries as JSON files
        expected_names = set()
        for entry_data in entries:
            name = entry_data["name"]
            expected_names.add(name.lower())
            
            file_path = udl_path / f"{name.lower()}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(entry_data, f)
        
        # Load and list UDLs
        loader = UDLLoader(udl_path=udl_path)
        listed_names = loader.list_udls()
        
        # Verify completeness: all expected names are present
        assert set(listed_names) == expected_names
        
        # Verify no duplicates
        assert len(listed_names) == len(set(listed_names))


def test_udl_loader_empty_directory() -> None:
    """Test UDL loader with empty directory.

    **Validates: Requirements 3.7**
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        loader = UDLLoader(udl_path=tmpdir)
        
        # Should return empty list
        assert loader.list_udls() == []


def test_udl_loader_nonexistent_directory() -> None:
    """Test UDL loader with nonexistent directory.

    **Validates: Requirements 3.7**
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        nonexistent = Path(tmpdir) / "nonexistent"
        loader = UDLLoader(udl_path=nonexistent)
        
        # Should return empty list without error
        assert loader.list_udls() == []


def test_udl_loader_get_udl() -> None:
    """Test UDL loader get_udl method.

    **Validates: Requirements 3.5**
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        udl_path = Path(tmpdir)
        
        # Create a test UDL file
        entry_data = {
            "name": "test-udl",
            "definition": {
                "title": "Test UDL",
                "descr": "A test UDL",
                "lang": "UDL",
                "delimiter_open": "<",
                "delimiter_close": ">",
                "bracket_open": "(",
                "bracket_close": ")",
                "operators": [
                    {"name": "dolphin", "open": "<:", "close": ":>"},
                ],
            },
            "examples": ["example1"],
            "created_at": "2024-01-01T00:00:00",
        }
        
        with open(udl_path / "test-udl.json", "w", encoding="utf-8") as f:
            json.dump(entry_data, f)
        
        loader = UDLLoader(udl_path=udl_path)
        
        # Get UDL definition
        definition = loader.get_udl("test-udl")
        
        assert definition.title == "Test UDL"
        assert definition.description == "A test UDL"
        assert definition.delimiter_open == "<"
        assert definition.delimiter_close == ">"
        assert len(definition.operators) == 1
        assert definition.operators[0].name == "dolphin"


def test_udl_loader_get_udl_not_found() -> None:
    """Test UDL loader raises error for nonexistent UDL.

    **Validates: Requirements 3.5**
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        loader = UDLLoader(udl_path=tmpdir)
        
        with pytest.raises(UDLNotFoundError) as exc_info:
            loader.get_udl("nonexistent")
        
        assert "nonexistent" in str(exc_info.value)


def test_udl_loader_save_and_load() -> None:
    """Test UDL loader save and load round-trip.

    **Validates: Requirements 3.5, 3.7**
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        udl_path = Path(tmpdir)
        loader = UDLLoader(udl_path=udl_path)
        
        # Create and save a UDL
        entry = loader.create_udl(
            name="my-udl",
            title="My UDL",
            description="My custom UDL",
            delimiter_open="[",
            delimiter_close="]",
        )
        loader.save_udl(entry)
        
        # Create new loader to verify persistence
        new_loader = UDLLoader(udl_path=udl_path)
        
        # Verify UDL is listed
        assert "my-udl" in new_loader.list_udls()
        
        # Verify UDL can be retrieved
        definition = new_loader.get_udl("my-udl")
        assert definition.title == "My UDL"
        assert definition.description == "My custom UDL"
        assert definition.delimiter_open == "["
        assert definition.delimiter_close == "]"
