"""Property tests for UDL Database Population.

Feature: mrdr-data-population
Properties: 11, 12
Validates: Requirements 5.3, 5.4, 5.5
"""

import json
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st
import pytest


# Path to the UDL database
UDL_DATABASE_PATH = Path("database/languages/udl/udl_database.json")


def load_udl_database() -> dict:
    """Load the UDL database from JSON file."""
    with open(UDL_DATABASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestUDLDatabasePopulation:
    """Tests for UDL database population."""

    @pytest.fixture(scope="class")
    def udl_database(self) -> dict:
        """Load UDL database once for all tests in class."""
        return load_udl_database()

    @pytest.fixture(scope="class")
    def templates(self, udl_database: dict) -> list[dict]:
        """Get templates from database."""
        return udl_database.get("templates", [])

    def test_database_file_exists(self) -> None:
        """Test that UDL database file exists.

        **Validates: Requirements 5.1**
        """
        assert UDL_DATABASE_PATH.exists(), f"UDL database not found at {UDL_DATABASE_PATH}"

    def test_database_has_manifest(self, udl_database: dict) -> None:
        """Test that UDL database has manifest.

        **Validates: Requirements 5.1**
        """
        assert "manifest" in udl_database
        manifest = udl_database["manifest"]
        assert "manifest_name" in manifest
        assert "version" in manifest

    def test_database_has_templates(self, udl_database: dict) -> None:
        """Test that UDL database has templates array.

        **Validates: Requirements 5.1**
        """
        assert "templates" in udl_database
        assert isinstance(udl_database["templates"], list)
        assert len(udl_database["templates"]) >= 1

    def test_pindx_template_exists(self, templates: list[dict]) -> None:
        """Test that Pointy-Numerical-Index template exists.

        **Validates: Requirements 5.2**
        """
        pindx_templates = [t for t in templates if t.get("name") == "pindx"]
        assert len(pindx_templates) == 1, "pindx template should exist"
        
        pindx = pindx_templates[0]
        assert pindx["delimiter_open"] == "<"
        assert pindx["delimiter_close"] == ">"
        assert pindx["bracket_open"] == "("
        assert pindx["bracket_close"] == ")"


class TestProperty11UDLOperatorDefinitions:
    """Property 11: UDL Operator Definitions.

    Feature: mrdr-data-population, Property 11: UDL Operator Definitions
    For any valid UDL database, the database SHALL contain dolphin operator
    with open=`<:` close=`:>` and walrus operator with open=`:=` close=`=:`.
    **Validates: Requirements 5.3, 5.4**
    """

    @pytest.fixture(scope="class")
    def udl_database(self) -> dict:
        """Load UDL database once for all tests in class."""
        return load_udl_database()

    @pytest.fixture(scope="class")
    def all_operators(self, udl_database: dict) -> list[dict]:
        """Collect all operators from all templates."""
        operators = []
        for template in udl_database.get("templates", []):
            operators.extend(template.get("operators", []))
        return operators

    def test_dolphin_operator_exists(self, all_operators: list[dict]) -> None:
        """Test that dolphin operator exists with correct delimiters.

        Feature: mrdr-data-population, Property 11: UDL Operator Definitions
        **Validates: Requirements 5.3**
        """
        dolphin_ops = [op for op in all_operators if op.get("name") == "dolphin"]
        assert len(dolphin_ops) >= 1, "dolphin operator should exist"
        
        # At least one dolphin operator should have correct delimiters
        correct_dolphin = [
            op for op in dolphin_ops 
            if op.get("open") == "<:" and op.get("close") == ":>"
        ]
        assert len(correct_dolphin) >= 1, "dolphin operator should have open=<: close=:>"

    def test_walrus_operator_exists(self, all_operators: list[dict]) -> None:
        """Test that walrus operator exists with correct delimiters.

        Feature: mrdr-data-population, Property 11: UDL Operator Definitions
        **Validates: Requirements 5.4**
        """
        walrus_ops = [op for op in all_operators if op.get("name") == "walrus"]
        assert len(walrus_ops) >= 1, "walrus operator should exist"
        
        # At least one walrus operator should have correct delimiters
        correct_walrus = [
            op for op in walrus_ops 
            if op.get("open") == ":=" and op.get("close") == "=:"
        ]
        assert len(correct_walrus) >= 1, "walrus operator should have open=:= close==:"

    def test_dolphin_template_variant_exists(self, udl_database: dict) -> None:
        """Test that dolphin template variant exists.

        **Validates: Requirements 5.3**
        """
        templates = udl_database.get("templates", [])
        dolphin_templates = [t for t in templates if t.get("name") == "dolphin"]
        assert len(dolphin_templates) >= 1, "dolphin template variant should exist"
        
        dolphin = dolphin_templates[0]
        assert "examples" in dolphin
        assert len(dolphin["examples"]) >= 1

    def test_walrus_template_variant_exists(self, udl_database: dict) -> None:
        """Test that walrus template variant exists.

        **Validates: Requirements 5.4**
        """
        templates = udl_database.get("templates", [])
        walrus_templates = [t for t in templates if t.get("name") == "walrus"]
        assert len(walrus_templates) >= 1, "walrus template variant should exist"
        
        walrus = walrus_templates[0]
        assert "examples" in walrus
        assert len(walrus["examples"]) >= 1


class TestProperty12UDLEntrySchemaValidity:
    """Property 12: UDL Entry Schema Validity.

    Feature: mrdr-data-population, Property 12: UDL Entry Schema Validity
    For any entry in the UDL database, the entry SHALL contain non-null values
    for: name, title, description, language, delimiter_open, delimiter_close.
    **Validates: Requirements 5.5**
    """

    @pytest.fixture(scope="class")
    def udl_database(self) -> dict:
        """Load UDL database once for all tests in class."""
        return load_udl_database()

    @pytest.fixture(scope="class")
    def templates(self, udl_database: dict) -> list[dict]:
        """Get templates from database."""
        return udl_database.get("templates", [])

    def test_all_entries_have_required_fields(self, templates: list[dict]) -> None:
        """Test that all UDL entries have required fields.

        Feature: mrdr-data-population, Property 12: UDL Entry Schema Validity
        **Validates: Requirements 5.5**
        """
        required_fields = [
            "name",
            "title", 
            "description",
            "language",
            "delimiter_open",
            "delimiter_close",
        ]
        
        for template in templates:
            for field in required_fields:
                assert field in template, f"Template missing required field: {field}"
                assert template[field] is not None, f"Template field {field} is null"
                assert template[field] != "", f"Template field {field} is empty"

    def test_all_entries_have_valid_name(self, templates: list[dict]) -> None:
        """Test that all UDL entries have valid name.

        **Validates: Requirements 5.5**
        """
        for template in templates:
            name = template.get("name")
            assert name is not None
            assert isinstance(name, str)
            assert len(name) >= 1

    def test_all_entries_have_valid_delimiters(self, templates: list[dict]) -> None:
        """Test that all UDL entries have valid delimiters.

        **Validates: Requirements 5.5**
        """
        for template in templates:
            delimiter_open = template.get("delimiter_open")
            delimiter_close = template.get("delimiter_close")
            
            assert delimiter_open is not None
            assert delimiter_close is not None
            assert isinstance(delimiter_open, str)
            assert isinstance(delimiter_close, str)
            assert len(delimiter_open) == 1, f"delimiter_open should be 1 char: {delimiter_open}"
            assert len(delimiter_close) == 1, f"delimiter_close should be 1 char: {delimiter_close}"

    def test_all_operators_have_valid_schema(self, templates: list[dict]) -> None:
        """Test that all operators have valid schema.

        **Validates: Requirements 5.5**
        """
        for template in templates:
            operators = template.get("operators", [])
            for operator in operators:
                assert "name" in operator
                assert "open" in operator
                assert "close" in operator
                assert operator["name"] is not None
                assert operator["open"] is not None
                assert operator["close"] is not None
                assert len(operator["open"]) == 2, f"operator open should be 2 chars: {operator['open']}"
                assert len(operator["close"]) == 2, f"operator close should be 2 chars: {operator['close']}"


# Property-based tests using Hypothesis

# Strategy for selecting a template from the database
@st.composite
def template_from_database(draw: st.DrawFn) -> dict:
    """Strategy to select a random template from the UDL database."""
    db = load_udl_database()
    templates = db.get("templates", [])
    if not templates:
        pytest.skip("No templates in database")
    return draw(st.sampled_from(templates))


@given(template=template_from_database())
@settings(max_examples=100)
def test_property_12_schema_validity_hypothesis(template: dict) -> None:
    """Property 12: UDL Entry Schema Validity (Hypothesis).

    Feature: mrdr-data-population, Property 12: UDL Entry Schema Validity
    For any entry in the UDL database, the entry SHALL contain non-null values
    for: name, title, description, language, delimiter_open, delimiter_close.
    **Validates: Requirements 5.5**
    """
    required_fields = [
        "name",
        "title",
        "description", 
        "language",
        "delimiter_open",
        "delimiter_close",
    ]
    
    for field in required_fields:
        assert field in template, f"Missing required field: {field}"
        assert template[field] is not None, f"Field {field} is null"
        assert template[field] != "", f"Field {field} is empty"


@given(template=template_from_database())
@settings(max_examples=100)
def test_property_12_delimiter_length_hypothesis(template: dict) -> None:
    """Property 12: UDL Delimiter Length Validation (Hypothesis).

    Feature: mrdr-data-population, Property 12: UDL Entry Schema Validity
    For any entry in the UDL database, delimiter_open and delimiter_close
    SHALL be exactly 1 character.
    **Validates: Requirements 5.5**
    """
    assert len(template["delimiter_open"]) == 1
    assert len(template["delimiter_close"]) == 1


@given(template=template_from_database())
@settings(max_examples=100)
def test_property_12_operator_length_hypothesis(template: dict) -> None:
    """Property 12: UDL Operator Length Validation (Hypothesis).

    Feature: mrdr-data-population, Property 12: UDL Entry Schema Validity
    For any operator in a UDL entry, open and close SHALL be exactly 2 characters.
    **Validates: Requirements 5.5**
    """
    for operator in template.get("operators", []):
        assert len(operator["open"]) == 2, f"Operator open should be 2 chars: {operator['open']}"
        assert len(operator["close"]) == 2, f"Operator close should be 2 chars: {operator['close']}"
