"""Property tests for Advanced Table Renderer component.

Feature: mrdr-visual-integration
Tests Properties 21-26 for table rendering capabilities.
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from mrdr.render.components import AdvancedTableRenderer, TableConfig


# Strategy for simple field names (alphanumeric, no special chars)
field_name = st.text(
    min_size=1,
    max_size=10,
    alphabet=st.characters(whitelist_categories=("L",), whitelist_characters="_"),
)

# Strategy for simple field values
field_value = st.text(
    min_size=1,
    max_size=20,
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters=" "),
)


# Strategy for table row data
def row_strategy(columns: list[str]) -> st.SearchStrategy[dict[str, str]]:
    """Generate a row with the given column names."""
    return st.fixed_dictionaries({col: field_value for col in columns})


@given(
    filter_value=st.sampled_from(["alpha", "beta", "gamma"]),
    num_matching=st.integers(min_value=0, max_value=5),
    num_non_matching=st.integers(min_value=0, max_value=5),
)
@settings(max_examples=100)
def test_table_row_filtering(
    filter_value: str, num_matching: int, num_non_matching: int
) -> None:
    """Property 23: Table Row Filtering.

    Feature: mrdr-visual-integration, Property 23: Table Row Filtering
    For any --filter field=value option, the rendered table SHALL contain
    only rows where the specified field matches the value.
    **Validates: Requirements 10.3**
    """
    assume(num_matching + num_non_matching > 0)

    # Create test data with known matching and non-matching rows
    data = []
    for i in range(num_matching):
        data.append({"language": f"lang_{i}", "type": filter_value})
    for i in range(num_non_matching):
        # Use a different value that won't match
        other_value = "other" if filter_value != "other" else "different"
        data.append({"language": f"other_{i}", "type": other_value})

    config = TableConfig(filter_field="type", filter_value=filter_value)
    renderer = AdvancedTableRenderer(data=data, config=config)

    filtered = renderer._apply_filter()

    # All filtered rows should match the filter value
    assert len(filtered) == num_matching
    for row in filtered:
        assert row["type"].lower() == filter_value.lower()


@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "name": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
                "value": st.text(min_size=1, max_size=10, alphabet="0123456789"),
            }
        ),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=100)
def test_table_filter_no_match(data: list[dict[str, str]]) -> None:
    """Property 23: Table Row Filtering - no matches case.

    Feature: mrdr-visual-integration, Property 23: Table Row Filtering
    When filter value matches no rows, result should be empty.
    **Validates: Requirements 10.3**
    """
    # Use a filter value that won't match any data
    config = TableConfig(filter_field="name", filter_value="NONEXISTENT_VALUE_XYZ")
    renderer = AdvancedTableRenderer(data=data, config=config)

    filtered = renderer._apply_filter()
    assert len(filtered) == 0


def test_table_filter_case_insensitive() -> None:
    """Property 23: Table Row Filtering - case insensitivity.

    Feature: mrdr-visual-integration, Property 23: Table Row Filtering
    Filter matching should be case-insensitive.
    **Validates: Requirements 10.3**
    """
    data = [
        {"language": "Python", "type": "LITERAL"},
        {"language": "Ruby", "type": "literal"},
        {"language": "JavaScript", "type": "block"},
    ]

    config = TableConfig(filter_field="type", filter_value="Literal")
    renderer = AdvancedTableRenderer(data=data, config=config)

    filtered = renderer._apply_filter()
    assert len(filtered) == 2
    assert all(row["type"].lower() == "literal" for row in filtered)



@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "name": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
                "value": st.integers(min_value=0, max_value=100),
            }
        ),
        min_size=2,
        max_size=10,
    ),
    sort_descending=st.booleans(),
)
@settings(max_examples=100)
def test_table_sorting(data: list[dict], sort_descending: bool) -> None:
    """Property 24: Table Sorting.

    Feature: mrdr-visual-integration, Property 24: Table Sorting
    For any --sort field option, the rendered table rows SHALL be ordered
    by the specified field in ascending order (or descending with toggle).
    **Validates: Requirements 10.4**
    """
    config = TableConfig(sort_field="name", sort_descending=sort_descending)
    renderer = AdvancedTableRenderer(data=data, config=config)

    sorted_data = renderer._apply_sort(data)

    # Extract sorted names
    names = [row["name"] for row in sorted_data]

    # Verify order
    expected = sorted(names, reverse=sort_descending)
    assert names == expected


@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "name": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
                "priority": st.integers(min_value=1, max_value=10),
            }
        ),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=100)
def test_table_sorting_preserves_data(data: list[dict]) -> None:
    """Property 24: Table Sorting - data preservation.

    Feature: mrdr-visual-integration, Property 24: Table Sorting
    Sorting should preserve all data, just reorder it.
    **Validates: Requirements 10.4**
    """
    config = TableConfig(sort_field="name")
    renderer = AdvancedTableRenderer(data=data, config=config)

    sorted_data = renderer._apply_sort(data)

    # Same number of rows
    assert len(sorted_data) == len(data)

    # Same data, just reordered
    original_set = {(row["name"], row["priority"]) for row in data}
    sorted_set = {(row["name"], row["priority"]) for row in sorted_data}
    assert original_set == sorted_set


def test_table_sorting_no_sort_field() -> None:
    """Property 24: Table Sorting - no sort field.

    Feature: mrdr-visual-integration, Property 24: Table Sorting
    When no sort field is specified, data order should be preserved.
    **Validates: Requirements 10.4**
    """
    data = [
        {"name": "zebra", "value": 1},
        {"name": "apple", "value": 2},
        {"name": "mango", "value": 3},
    ]

    config = TableConfig()  # No sort_field
    renderer = AdvancedTableRenderer(data=data, config=config)

    sorted_data = renderer._apply_sort(data)

    # Order should be preserved
    assert [row["name"] for row in sorted_data] == ["zebra", "apple", "mango"]
