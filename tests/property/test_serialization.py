"""Property tests for serialization round-trip.

Feature: mrdr-cli-foundation
Properties: 6, 13
Validates: Requirements 2.6, 2.7, 4.6
"""

import json

import yaml
from hypothesis import given, settings

from mrdr.database.schema import DocstringEntry
from tests.conftest import docstring_entry_strategy


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_json_export_roundtrip(data: dict) -> None:
    """Property 6: Export Round-Trip (JSON).

    Feature: mrdr-cli-foundation, Property 6: Export Round-Trip
    For any valid DocstringEntry, exporting to JSON and parsing the result
    SHALL produce an equivalent entry.
    **Validates: Requirements 2.6, 2.7**
    """
    # Create entry from generated data
    entry = DocstringEntry(**data)

    # Export to JSON
    json_str = entry.model_dump_json()

    # Parse back
    parsed_data = json.loads(json_str)
    restored_entry = DocstringEntry(**parsed_data)

    # Verify equivalence
    assert entry.language == restored_entry.language
    assert entry.syntax.start == restored_entry.syntax.start
    assert entry.syntax.end == restored_entry.syntax.end
    assert entry.syntax.type == restored_entry.syntax.type
    assert entry.syntax.location == restored_entry.syntax.location
    assert entry.tags == restored_entry.tags
    assert entry.example_content == restored_entry.example_content
    assert entry.conflict_ref == restored_entry.conflict_ref
    assert entry.parsing_rule == restored_entry.parsing_rule
    assert entry.metadata == restored_entry.metadata

    if entry.plusrep:
        assert restored_entry.plusrep is not None
        assert entry.plusrep.tokens == restored_entry.plusrep.tokens
        assert entry.plusrep.rating == restored_entry.plusrep.rating
        assert entry.plusrep.label == restored_entry.plusrep.label


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_yaml_export_roundtrip(data: dict) -> None:
    """Property 6: Export Round-Trip (YAML).

    Feature: mrdr-cli-foundation, Property 6: Export Round-Trip
    For any valid DocstringEntry, exporting to YAML and parsing the result
    SHALL produce an equivalent entry.
    **Validates: Requirements 2.6, 2.7**
    """
    # Create entry from generated data
    entry = DocstringEntry(**data)

    # Export to YAML via dict
    yaml_str = yaml.dump(entry.model_dump(), default_flow_style=False)

    # Parse back
    parsed_data = yaml.safe_load(yaml_str)
    restored_entry = DocstringEntry(**parsed_data)

    # Verify equivalence
    assert entry.language == restored_entry.language
    assert entry.syntax.start == restored_entry.syntax.start
    assert entry.syntax.end == restored_entry.syntax.end
    assert entry.syntax.type == restored_entry.syntax.type
    assert entry.syntax.location == restored_entry.syntax.location
    assert entry.tags == restored_entry.tags


@given(data=docstring_entry_strategy())
@settings(max_examples=100)
def test_serialization_roundtrip_preserves_fields(data: dict) -> None:
    """Property 13: Serialization Round-Trip.

    Feature: mrdr-cli-foundation, Property 13: Serialization Round-Trip
    For any valid DocstringEntry, serializing to JSON and deserializing
    SHALL produce an entry with identical field values.
    **Validates: Requirements 4.6**
    """
    # Create entry from generated data
    entry = DocstringEntry(**data)

    # Serialize to dict and back
    serialized = entry.model_dump()
    restored = DocstringEntry(**serialized)

    # Full equality check
    assert entry.model_dump() == restored.model_dump()


def test_real_database_entries_roundtrip() -> None:
    """Test round-trip with actual database entries."""
    from mrdr.database import QueryEngine

    qe = QueryEngine()
    for entry in qe.loader.get_entries():
        # JSON round-trip
        json_str = entry.model_dump_json()
        parsed = json.loads(json_str)
        restored = DocstringEntry(**parsed)
        assert entry.model_dump() == restored.model_dump()

        # YAML round-trip
        yaml_str = yaml.dump(entry.model_dump())
        parsed_yaml = yaml.safe_load(yaml_str)
        restored_yaml = DocstringEntry(**parsed_yaml)
        assert entry.model_dump() == restored_yaml.model_dump()
